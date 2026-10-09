"""Tests for lint_items.py: each flaw code fires on a seeded flaw, and the clean example passes.

Run from the repo root:  python -m unittest discover -s tests -v
"""

import contextlib
import copy
import io
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "mcq-item-writer"
sys.path.insert(0, str(SKILL / "scripts"))

import lint_items  # noqa: E402

EXAMPLE = json.loads((SKILL / "assets" / "example-bank.json").read_text(encoding="utf-8"))
FB = "This feedback explains clearly why the option is or is not the best answer here."


def base_item(**over):
    """A clean, standalone 4-option item."""
    item = {
        "id": "T-1", "status": "draft", "format": "one-best-answer",
        "objective": {"text": "Choose the first action when a server overheats."},
        "testing_point": "Prioritises safe shutdown.",
        "task": "choose-action", "cognitive_process": "apply", "cognitive_level": "application",
        "purpose": "assessment", "assessment_type": "summative",
        "stem": {"scenario": "A technician in a small data room hears a cooling fan grinding. The rack temperature display reads 41 °C and rising.",
                 "lead_in": "Which of the following is the most appropriate first action?"},
        "options": [
            {"label": "A", "text": "Shut down the affected rack safely", "correct": True, "feedback": FB + " (A)", "misconception": None},
            {"label": "B", "text": "Replace the fan while the rack runs", "correct": False, "feedback": FB + " (B)", "misconception": "x"},
            {"label": "C", "text": "Log a ticket for the next maintenance window", "correct": False, "feedback": FB + " (C)", "misconception": "x"},
            {"label": "D", "text": "Open the room door to improve airflow", "correct": False, "feedback": FB + " (D)", "misconception": "x"},
        ],
        "shuffle": True,
        "audit": {"cover_the_options": {"passed": True, "stem_only_answer": "Shut it down."}, "lint": [], "warnings": []},
    }
    item.update(over)
    return item


def bank_with(*items, **defaults):
    d = {"purpose": "assessment", "assessment_type": "summative", "learner_level": "new technicians"}
    d.update(defaults)
    return {"schema_version": "0.1.0", "bank": {"title": "t", "defaults": d}, "items": list(items)}


def codes(bank, item_id="T-1"):
    findings, _ = lint_items.lint_bank(bank)
    return {(f.code, f.severity) for f in findings if f.item == item_id}


def code_set(bank, item_id="T-1"):
    return {c for c, _ in codes(bank, item_id)}


class CleanExamples(unittest.TestCase):
    def test_example_bank_is_clean(self):
        findings, _ = lint_items.lint_bank(copy.deepcopy(EXAMPLE))
        problems = [f for f in findings if f.severity in ("error", "warning")]
        self.assertEqual(problems, [], "\n".join(f"{f.item} {f.code} {f.message}" for f in problems))

    def test_base_item_is_clean(self):
        bad = {c for c, s in codes(bank_with(base_item())) if s in ("error", "warning")}
        self.assertEqual(bad, set())


class FlawCodes(unittest.TestCase):
    def mutate(self, fn, **defaults):
        it = base_item()
        fn(it)
        return code_set(bank_with(it, **defaults))

    def test_long_options(self):
        self.assertIn("ID-LONG-OPTIONS", self.mutate(lambda it: it["options"][1].update(
            text="Replace the fan while the rack keeps running so that services are not interrupted for the users at all")))

    def test_numeric_order_and_overlap(self):
        def f(it):
            it["shuffle"] = False
            for o, t in zip(it["options"], ["Less than 20%", "20% to 30%", "Greater than 50%", "75%"]):
                o["text"] = t
        self.assertIn("ID-NUMERIC", self.mutate(f))

    def test_numeric_shuffle_flag(self):
        def f(it):
            for o, t in zip(it["options"], ["10", "20", "30", "40"]):
                o["text"] = t
        self.assertIn("X-KEY-POSITION", self.mutate(f))

    def test_vague_terms(self):
        self.assertIn("ID-VAGUE", self.mutate(lambda it: it["options"][2].update(text="Usually log a ticket for later")))

    def test_nota(self):
        self.assertIn("ID-NOTA", self.mutate(lambda it: it["options"][3].update(text="None of the above")))

    def test_aota(self):
        self.assertIn("X-AOTA", self.mutate(lambda it: it["options"][3].update(text="All of the above")))

    def test_nonparallel(self):
        self.assertIn("ID-NONPARALLEL", self.mutate(lambda it: it["options"][1].update(
            text="Replace it. Then restart the rack.")))

    def test_combination_option(self):
        self.assertIn("ID-COMPLEX-STEM", self.mutate(lambda it: it["options"][3].update(text="A and C only")))

    def test_rank_stem(self):
        self.assertIn("ID-COMPLEX-STEM", self.mutate(lambda it: it["stem"].update(
            lead_in="Which of the following orders these steps correctly, if you rank the following steps?")))

    def test_negative_strong(self):
        self.assertIn(("ID-NEGATIVE", "error"), codes(bank_with(base_item(stem={
            "scenario": "x", "lead_in": "Each of the following is appropriate EXCEPT which?"}))))

    def test_negative_soft_is_warning(self):
        self.assertIn(("ID-NEGATIVE", "warning"), codes(bank_with(base_item(stem={
            "scenario": "x", "lead_in": "Which of the following is least likely to help?"}))))

    def test_positive_question_about_negative_event_not_flagged(self):
        c = code_set(bank_with(base_item(stem={"scenario": "The nightly job failed.",
                                               "lead_in": "Which of the following best explains why the backup did not run?"})))
        self.assertNotIn("ID-NEGATIVE", c)

    def test_grammar_article(self):
        def f(it):
            it["stem"]["lead_in"] = "The most likely cause of the fault is an?"
        self.assertIn("TW-GRAMMAR", self.mutate(f))

    def test_absolute(self):
        self.assertIn("TW-ABSOLUTE", self.mutate(lambda it: it["options"][1].update(text="Never touch a running rack")))

    def test_key_stands_out(self):
        self.assertIn("TW-KEY-STANDS-OUT", self.mutate(lambda it: it["options"][0].update(
            text="Shut down the affected rack safely and in the documented order, then notify the facilities team")))

    def test_clang(self):
        def f(it):
            it["stem"]["scenario"] = "A technician hears a fan grinding. Users say the room feels unusually humid."
            it["options"][0]["text"] = "Check the humidity controls"
        self.assertIn("TW-CLANG", self.mutate(f))

    def test_convergence(self):
        # Key (A) holds the most common value on both dimensions: cationic (2x) and inside (3x).
        texts = ["cationic, acting inside", "anionic, acting inside",
                 "cationic, acting outside", "neutral, acting inside"]
        def f(it):
            for o, t in zip(it["options"], texts):
                o["text"] = t
        self.assertIn("TW-CONVERGENCE", self.mutate(f))

    def test_exhaustive(self):
        texts = ["Increase", "Decrease", "No change", "Requires a new cooling vendor contract"]
        def f(it):
            it["options"].append({"label": "E", "text": "Depends on budget approval", "correct": False, "feedback": FB, "misconception": "x"})
            for o, t in zip(it["options"], texts):
                o["text"] = t
            it["option_count_reason"] = "test"
        self.assertIn("TW-EXHAUSTIVE", self.mutate(f))

    def test_option_count(self):
        self.assertIn("X-OPTION-COUNT", self.mutate(lambda it: it["options"].pop()))

    def test_option_count_respects_bank_setting(self):
        it = base_item()
        it["options"].pop()
        self.assertNotIn("X-OPTION-COUNT", code_set(bank_with(it, options_per_item=3)))

    def test_option_count_reason_accepted(self):
        def f(it):
            it["options"].pop()
            it["option_count_reason"] = "only two plausible distractors"
        self.assertNotIn("X-OPTION-COUNT", self.mutate(f))

    def test_thin_feedback(self):
        self.assertIn("X-FEEDBACK-MISSING", self.mutate(lambda it: it["options"][1].update(feedback="Incorrect.")))

    def test_duplicate_feedback(self):
        def f(it):
            for o in it["options"]:
                o["feedback"] = FB
        self.assertIn("X-FEEDBACK-MISSING", self.mutate(f))

    def test_placeholder_feedback(self):
        self.assertIn("X-FEEDBACK-MISSING", self.mutate(lambda it: it["options"][2].update(
            feedback="(none in original) This option was converted from the draft without any feedback.")))

    def test_cover_the_options_failed(self):
        self.assertIn("X-COVER-THE-OPTIONS", self.mutate(lambda it: it["audit"]["cover_the_options"].update(passed=False)))

    def test_schema_two_keys(self):
        self.assertIn("SCHEMA-INVALID", self.mutate(lambda it: it["options"][1].update(correct=True)))

    def test_nota_key_in_learning_item(self):
        it = base_item(purpose="learning")
        it["options"][0]["text"] = "None of the above"
        findings, _ = lint_items.lint_bank(bank_with(it))
        msgs = [x.message for x in findings if x.code == "ID-NOTA"]
        self.assertTrue(any("learning item" in mm for mm in msgs), msgs)


class BankLevel(unittest.TestCase):
    def test_key_position_bias(self):
        items = []
        for i in range(5):
            it = base_item(id=f"T-{i}", shuffle=False)
            items.append(it)
        findings, _ = lint_items.lint_bank(bank_with(*items))
        self.assertTrue(any(f.code == "X-KEY-POSITION" and f.item == "BANK" for f in findings))

    def test_key_position_bias_even_when_shuffled(self):
        items = [base_item(id=f"T-{i}", shuffle=True) for i in range(6)]
        findings, _ = lint_items.lint_bank(bank_with(*items))
        self.assertTrue(any(f.code == "X-KEY-POSITION" and f.item == "BANK" for f in findings))

    def test_key_positions_balanced_no_warning(self):
        items = []
        for i, k in enumerate("ABCDABCD"):
            it = base_item(id=f"T-{i}")
            for o in it["options"]:
                o["correct"] = o["label"] == k
            items.append(it)
        findings, _ = lint_items.lint_bank(bank_with(*items))
        self.assertFalse(any(f.code == "X-KEY-POSITION" for f in findings))

    def test_duplicate_ids(self):
        findings, _ = lint_items.lint_bank(bank_with(base_item(), base_item()))
        self.assertTrue(any(f.code == "SCHEMA-DUPLICATE-ID" for f in findings))

    def test_ordered_levels(self):
        it = copy.deepcopy([x for x in EXAMPLE["items"] if x["format"] == "ordered-mc"][0])
        it["options"][2]["level"] = 1
        it["options"][0]["level"] = 3
        findings, _ = lint_items.lint_bank(bank_with(it))
        self.assertTrue(any(f.code == "SCHEMA-ORDERED-LEVELS" for f in findings))

    def test_write_back_and_resolved(self):
        import tempfile
        it = base_item()
        it["options"][1]["text"] = "Never touch a running rack"
        bank = bank_with(it)
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "b.json"
            p.write_text(json.dumps(bank), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                lint_items.main([str(p), "--write", "--format", "json"])
            saved = json.loads(p.read_text(encoding="utf-8"))
            entries = saved["items"][0]["audit"]["lint"]
            self.assertTrue(any(e["code"] == "TW-ABSOLUTE" for e in entries))
            for e in entries:
                e["resolved"] = True
                e["resolution"] = "accepted by reviewer"
            p.write_text(json.dumps(saved), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                rc = lint_items.main([str(p), "--strict", "--format", "json"])
            self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
