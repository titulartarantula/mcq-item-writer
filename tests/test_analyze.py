"""Tests for analyze_responses.py using simulated learners with planted item problems."""

import contextlib
import csv
import io
import json
import math
import random
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "mcq-item-writer" / "scripts"))

import analyze_responses as ar  # noqa: E402

FB = "This feedback explains clearly why the option is or is not the best answer here."
N_LEARNERS = 300


def logistic(x):
    return 1 / (1 + math.exp(-x))


def bank_item(iid, key="A"):
    return {
        "id": iid, "status": "draft", "format": "one-best-answer",
        "objective": {"text": "x"}, "testing_point": "x", "task": "explain",
        "cognitive_process": "apply", "cognitive_level": "application",
        "purpose": "assessment", "assessment_type": "summative", "difficulty_target": 0.72,
        "stem": {"scenario": "x", "lead_in": "Which?"},
        "options": [{"label": L, "text": f"Option {L} for {iid}", "correct": L == key, "feedback": FB} for L in "ABCD"],
        "shuffle": True, "audit": {"cover_the_options": {"passed": True}},
    }


def simulate(seed=7):
    """Return (bank, rows). Items: GOOD, MISKEY (bank says B, truth is C), TWO (A and B both attract strong
    learners), DEADD (option D never chosen), EASY (almost everyone right), and five filler items."""
    rng = random.Random(seed)
    ids = ["GOOD", "MISKEY", "TWO", "DEADD", "EASY"] + [f"F{i}" for i in range(5)]
    bank = {"schema_version": "0.1.0",
            "bank": {"title": "sim", "defaults": {"purpose": "assessment", "assessment_type": "summative", "learner_level": "x"}},
            "items": [bank_item(i, key="B" if i == "MISKEY" else "A") for i in ids]}

    def pick(weights):
        r, acc = rng.random() * sum(weights.values()), 0.0
        for k, w in weights.items():
            acc += w
            if r <= acc:
                return k
        return k

    rows = []
    for n in range(N_LEARNERS):
        th = rng.gauss(0, 1)
        row = {"learner": f"L{n}"}
        pc = logistic(1.6 * th + 0.6)
        row["GOOD"] = pick({"A": pc, "B": (1 - pc) / 3, "C": (1 - pc) / 3, "D": (1 - pc) / 3})
        pt = logistic(1.6 * th + 0.4)                       # truth is C
        row["MISKEY"] = pick({"C": pt, "A": (1 - pt) / 3, "B": (1 - pt) / 3, "D": (1 - pt) / 3})
        ps = logistic(1.6 * th + 0.6)                       # strong learners split A/B
        row["TWO"] = pick({"A": ps * 0.5, "B": ps * 0.5, "C": (1 - ps) / 2, "D": (1 - ps) / 2})
        pd = logistic(1.6 * th + 0.6)
        row["DEADD"] = pick({"A": pd, "B": (1 - pd) / 2, "C": (1 - pd) / 2})
        row["EASY"] = "A" if rng.random() < 0.985 else "B"
        for i in range(5):
            pf = logistic(1.4 * th + rng.uniform(-0.5, 1.0))
            row[f"F{i}"] = pick({"A": pf, "B": (1 - pf) / 3, "C": (1 - pf) / 3, "D": (1 - pf) / 3})
        rows.append(row)
    return bank, rows


def write_wide(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


class Analyze(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.tmp.name)
        cls.bank, cls.rows = simulate()
        (cls.dir / "bank.json").write_text(json.dumps(cls.bank), encoding="utf-8")
        write_wide(cls.rows, cls.dir / "wide.csv")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ar.main([str(cls.dir / "wide.csv"), "--bank", str(cls.dir / "bank.json"), "--format", "json"])
        cls.result = json.loads(out.getvalue())
        cls.by = {r["item"]: r for r in cls.result["items"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_summary(self):
        s = self.result["summary"]
        self.assertEqual(s["learners"], N_LEARNERS)
        self.assertEqual(s["items"], 10)
        self.assertIsNotNone(s["kr20"])
        self.assertTrue(0 < s["kr20"] < 1)

    def test_good_item_unflagged(self):
        g = self.by["GOOD"]
        self.assertGreater(g["discrimination"], 0.2)
        self.assertEqual(g["flags"], [])

    def test_miskey(self):
        self.assertIn("POSSIBLE_MISKEY", self.by["MISKEY"]["flags"])
        self.assertIn("NEGATIVE_DISCRIMINATION", self.by["MISKEY"]["flags"])

    def test_two_answers(self):
        self.assertIn("POSSIBLE_TWO_ANSWERS", self.by["TWO"]["flags"])

    def test_nonfunctional(self):
        self.assertIn("NONFUNCTIONAL_DISTRACTOR", self.by["DEADD"]["flags"])
        self.assertTrue(any("D" in n for n in self.by["DEADD"]["notes"]))

    def test_too_easy(self):
        self.assertIn("TOO_EASY", self.by["EASY"]["flags"])

    def test_long_format_matches_wide(self):
        p = self.dir / "long.csv"
        with open(p, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["learner", "item", "response"])
            for r in self.rows:
                for k, v in r.items():
                    if k != "learner":
                        w.writerow([r["learner"], k, v])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ar.main([str(p), "--bank", str(self.dir / "bank.json"), "--format", "json"])
        long_by = {r["item"]: r for r in json.loads(out.getvalue())["items"]}
        for iid in ("GOOD", "MISKEY"):
            self.assertEqual(long_by[iid]["p"], self.by[iid]["p"])
            self.assertEqual(long_by[iid]["discrimination"], self.by[iid]["discrimination"])

    def test_scored_format(self):
        p = self.dir / "scored.csv"
        keys = {it["id"]: next(o["label"] for o in it["options"] if o["correct"]) for it in self.bank["items"]}
        scored = [{k: (v if k == "learner" else ("1" if v == keys[k] else "0")) for k, v in r.items()} for r in self.rows]
        write_wide(scored, p)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ar.main([str(p), "--format", "json"])
        res = json.loads(out.getvalue())
        self.assertTrue(res["summary"]["scored_only"])
        by = {r["item"]: r for r in res["items"]}
        self.assertEqual(by["GOOD"]["p"], self.by["GOOD"]["p"])
        self.assertNotIn("options", by["GOOD"])

    def test_key_argument_without_bank(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ar.main([str(self.dir / "wide.csv"), "--key", "GOOD=A,MISKEY=C", "--format", "json"])
        res = json.loads(out.getvalue())
        by = {r["item"]: r for r in res["items"]}
        self.assertGreater(by["MISKEY"]["discrimination"], 0.2)   # with the true key, the item is healthy
        self.assertIn("TWO", res["summary"]["items_without_key"])

    def test_write_and_drift(self):
        bank_path = self.dir / "bank_w.json"
        bank_path.write_text(json.dumps(self.bank), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            ar.main([str(self.dir / "wide.csv"), "--bank", str(bank_path), "--write", "--date", "2026-01-01"])
        saved = json.loads(bank_path.read_text(encoding="utf-8"))
        st = {it["id"]: it.get("stats") for it in saved["items"]}
        self.assertEqual(st["GOOD"]["administered"], "2026-01-01")
        # Second administration where GOOD becomes much harder -> DRIFT
        rows2 = [dict(r, GOOD=("A" if i % 3 == 0 else "B")) for i, r in enumerate(self.rows)]
        write_wide(rows2, self.dir / "wide2.csv")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ar.main([str(self.dir / "wide2.csv"), "--bank", str(bank_path), "--format", "json", "--date", "2026-06-01"])
        by = {r["item"]: r for r in json.loads(out.getvalue())["items"]}
        self.assertIn("DRIFT", by["GOOD"]["flags"])

    def test_small_n_caution(self):
        write_wide(self.rows[:20], self.dir / "small.csv")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ar.main([str(self.dir / "small.csv"), "--bank", str(self.dir / "bank.json")])
        self.assertIn("CAUTION", out.getvalue())


if __name__ == "__main__":
    unittest.main()
