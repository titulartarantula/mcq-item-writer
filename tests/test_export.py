"""Tests for export.py: every format is produced, well-formed, and carries keys, feedback, and settings."""

import contextlib
import csv
import io
import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "mcq-item-writer"
sys.path.insert(0, str(SKILL / "scripts"))

import export  # noqa: E402

EXAMPLE = SKILL / "assets" / "example-bank.json"
BANK = json.loads(EXAMPLE.read_text(encoding="utf-8"))
N = len(BANK["items"])


def run(fmt, *extra):
    tmp = tempfile.mkdtemp()
    out = Path(tmp) / f"out.{fmt}"
    with contextlib.redirect_stdout(io.StringIO()):
        rc = export.main([str(EXAMPLE), "--format", fmt, "--out", str(out), *extra])
    return rc, out


class Exports(unittest.TestCase):
    def test_moodle_xml(self):
        rc, out = run("moodle-xml")
        self.assertEqual(rc, 0)
        root = ET.parse(out).getroot()
        qs = root.findall("question[@type='multichoice']")
        self.assertEqual(len(qs), N)
        for q in qs:
            fr = [a.get("fraction") for a in q.findall("answer")]
            self.assertIn("100", fr)
            for a in q.findall("answer"):
                self.assertTrue(a.find("feedback/text").text)
        ordered = [q for q in qs if q.find("name/text").text == "STATS-BIAS-01"][0]
        self.assertEqual([a.get("fraction") for a in ordered.findall("answer")], ["0", "50", "100"])

    def test_set_context_in_question_text(self):
        rc, out = run("moodle-xml")
        root = ET.parse(out).getroot()
        q2 = [q for q in root.findall("question[@type='multichoice']") if q.find("name/text").text == "IR-RANSOM-02"][0]
        text = q2.find("questiontext/text").text
        self.assertIn("accounting firm", text)          # opening scenario
        self.assertIn("The laptop is disconnected", text)  # update after item 1

    def test_gift(self):
        rc, out = run("gift")
        text = out.read_text(encoding="utf-8")
        self.assertEqual(text.count("::IR-RANSOM-01::"), 1)
        self.assertEqual(text.count("\n}"), N)
        self.assertIn("~%50%", text)                      # ordered-MC partial credit
        self.assertIn("09\\:40", text)                    # colon escaped

    def test_qti21(self):
        rc, out = run("qti21")
        z = zipfile.ZipFile(out)
        names = z.namelist()
        self.assertIn("imsmanifest.xml", names)
        self.assertIn("assessment.xml", names)
        items = [n for n in names if n.startswith("items/")]
        self.assertEqual(len(items), N)
        for n in names:
            ET.fromstring(z.read(n))                       # well-formed
        test = z.read("assessment.xml").decode()
        self.assertIn('navigationMode="linear"', test)    # locked sequential set

    def test_qti12(self):
        rc, out = run("qti12")
        z = zipfile.ZipFile(out)
        root = ET.fromstring(z.read("assessment.xml"))
        ns = {"q": "http://www.imsglobal.org/xsd/ims_qtiasiv1p2"}
        self.assertEqual(len(root.findall(".//q:item", ns)), N)
        self.assertGreaterEqual(len(root.findall(".//q:itemfeedback", ns)), N * 3)

    def test_csv(self):
        rc, out = run("csv")
        rows = list(csv.DictReader(io.StringIO(out.read_text(encoding="utf-8-sig"))))
        self.assertEqual(len(rows), N)
        r = [x for x in rows if x["id"] == "PM-SCHED-01"][0]
        self.assertEqual(r["key"], "D")
        self.assertTrue(r["feedback_A"])

    def test_h5p(self):
        rc, out = run("h5p")
        z = zipfile.ZipFile(out)
        h = json.loads(z.read("h5p.json"))
        c = json.loads(z.read("content/content.json"))
        self.assertEqual(h["mainLibrary"], "H5P.QuestionSet")
        self.assertEqual(len(c["questions"]), N)
        self.assertFalse(c["questions"][0]["params"]["behaviour"]["enableRetry"])

    def test_markdown(self):
        rc, out = run("markdown")
        text = out.read_text(encoding="utf-8")
        self.assertEqual(text.count("\n## "), N + 1)      # items + administration notes
        self.assertIn("✓", text)

    def test_only_status_filters(self):
        tmp = Path(tempfile.mkdtemp())
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = export.main([str(EXAMPLE), "--format", "csv", "--out", str(tmp / "x.csv"), "--only-status", "approved"])
        self.assertEqual(rc, 2)                            # example items are all drafts

    def test_invalid_bank_refused(self):
        bad = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        bad["items"][0]["options"][1]["correct"] = True
        tmp = Path(tempfile.mkdtemp())
        p = tmp / "bad.json"
        p.write_text(json.dumps(bad), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = export.main([str(p), "--format", "gift"])
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
