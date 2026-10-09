#!/usr/bin/env python3
"""Export an MCQ item bank to LMS and authoring-tool formats.

Formats:
  moodle-xml  Moodle XML question file (.xml): per-option feedback, shuffle flag, partial credit
  gift        Moodle GIFT text (.gift.txt): per-option feedback, partial credit (shuffle is a quiz setting)
  qti21       IMS QTI 2.1 content package (.zip): items + assessmentTest; locked sets as linear test parts
  qti12       IMS QTI 1.2 package (.zip), Canvas-style: per-option feedback; single correct answer
  csv         Spreadsheet (.csv, UTF-8 with BOM for Excel): one row per item, all metadata
  h5p         H5P Question Set (.h5p), EXPERIMENTAL: content only; target platform must already
              have H5P.QuestionSet 1.20+ and H5P.MultiChoice 1.16+ installed
  markdown    Review sheet (.review.md) for subject-matter experts

Usage:
  python export.py BANK.json --format moodle-xml [--out PATH] [--only-status approved]

Items are exported in delivery order (set members kept together). Set context (opening
scenario and the updates seen so far) is written into each set item's question text,
because most formats have no native "unfolding case" structure.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import uuid
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import mcqlib as m

SUFFIX = {"moodle-xml": ".moodle.xml", "gift": ".gift.txt", "qti21": ".qti21.zip", "qti12": ".qti12.zip",
          "csv": ".csv", "h5p": ".h5p", "markdown": ".review.md"}

LIMITATIONS = {
    "moodle-xml": [
        "Sequential sets: in the Moodle quiz, set navigation to 'Sequential' and keep these questions in order (don't shuffle questions).",
        "Media are written as text placeholders; upload the real files in Moodle and replace them.",
    ],
    "gift": [
        "Per-item shuffle flags are not carried; option shuffling is a quiz setting in Moodle. Turn it off for quizzes with numeric/ordered options.",
        "Data tables and set context are written as HTML ([html] format).",
    ],
    "qti21": [
        "Per-option feedback uses modalFeedback; LMS support varies, so check after import.",
        "Sequential sets are exported as linear test parts (no going back).",
    ],
    "qti12": [
        "Canvas multiple-choice questions score right/wrong only; ordered-MC partial credit is not carried.",
        "Per-item shuffle is ignored by Canvas; shuffling is a quiz setting.",
    ],
    "csv": [],
    "h5p": [
        "EXPERIMENTAL: the package contains content only. The target platform must already have H5P.QuestionSet and H5P.MultiChoice installed.",
        "No partial credit; retry is disabled (one attempt plus feedback). Data tables may be simplified by the H5P editor.",
        "If the bank contains a sequential set, backward navigation is disabled for the whole question set (H5P can't lock only part of it).",
    ],
    "markdown": [],
}

MOODLE_FRACTIONS = [100, 90, 83.33333, 80, 75, 70, 66.66667, 60, 50, 40, 33.33333, 30, 25, 20,
                    16.66667, 14.28571, 12.5, 11.11111, 10, 5, 0]


# ------------------------------------------------------------------ helpers

def ncname(s: str) -> str:
    """Make a valid XML NCName / identifier."""
    s = re.sub(r"[^A-Za-z0-9._-]", "_", s or "item")
    return s if re.match(r"[A-Za-z_]", s) else f"I_{s}"


def option_weight(item: dict, opt: dict) -> float:
    """Score for choosing this option (0..1). Partial credit only for ordered MC set to partial-credit."""
    if opt.get("correct"):
        return 1.0
    om = item.get("ordered_mc") or {}
    if item.get("format") == "ordered-mc" and om.get("scoring") == "partial-credit":
        return float(opt.get("weight") or 0.0)
    return 0.0


def moodle_fraction(w: float) -> str:
    target = w * 100
    best = min(MOODLE_FRACTIONS, key=lambda f: abs(f - target))
    return f"{best:g}"


def to_string(root: ET.Element) -> str:
    ET.indent(root) if hasattr(ET, "indent") else None
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n"


def sub(parent, tag, text=None, **attrs):
    el = ET.SubElement(parent, tag, {k.rstrip("_"): str(v) for k, v in attrs.items()})
    if text is not None:
        el.text = text
    return el


def question_elements(parent: ET.Element, bank: dict, item: dict) -> None:
    """Build the question body as XHTML elements (QTI 2.1 itemBody subset) without parsing any markup."""
    for block in m.item_context(bank, item):
        for para in [p.strip() for p in re.split(r"\n\s*\n", block) if p.strip()]:
            lines = para.splitlines()
            p = sub(parent, "p", lines[0])
            for line in lines[1:]:
                br = sub(p, "br")
                br.tail = line
    stem = item.get("stem", {})
    table = stem.get("data_table")
    if table:
        if m.is_md_table(table):
            rows = [r.strip() for r in table.strip().splitlines() if r.strip()]
            cells = lambda r: [c.strip() for c in r.strip("|").split("|")]
            tbl = sub(parent, "table")
            tr = sub(sub(tbl, "thead"), "tr")
            for c in cells(rows[0]):
                sub(tr, "th", c)
            tb = sub(tbl, "tbody")
            for r in rows[2:]:
                tr = sub(tb, "tr")
                for c in cells(r):
                    sub(tr, "td", c)
        else:
            sub(parent, "pre", table)
    if item.get("media"):
        md = item["media"]
        sub(sub(parent, "p"), "em", f"[{md.get('type', 'media').capitalize()}: {md.get('alt_text', '')}]")
    sub(sub(parent, "p"), "strong", stem.get("lead_in", ""))


# --------------------------------------------------------------- moodle xml

def export_moodle(bank: dict, items: list[dict]) -> str:
    quiz = ET.Element("quiz")
    cat = sub(quiz, "question", type="category")
    c = sub(cat, "category")
    sub(c, "text", f"$course$/top/{bank['bank'].get('title', 'Imported questions')}")
    for it in items:
        q = sub(quiz, "question", type="multichoice")
        name = sub(q, "name")
        sub(name, "text", it["id"])
        qt = sub(q, "questiontext", format="html")
        sub(qt, "text", m.question_html(bank, it))
        gf = sub(q, "generalfeedback", format="html")
        sub(gf, "text", "")
        sub(q, "defaultgrade", "1")
        sub(q, "penalty", "0")
        sub(q, "hidden", "0")
        sub(q, "idnumber", it["id"])
        sub(q, "single", "true")
        sub(q, "shuffleanswers", "true" if it.get("shuffle", True) else "false")
        sub(q, "answernumbering", "ABCD")
        sub(q, "showstandardinstruction", "0")
        for opt in it["options"]:
            a = sub(q, "answer", fraction=moodle_fraction(option_weight(it, opt)), format="html")
            sub(a, "text", m.esc(opt["text"]))
            fb = sub(a, "feedback", format="html")
            sub(fb, "text", m.esc(opt.get("feedback", "")))
        tags = list(it.get("tags", [])) + [f"objective:{it['objective'].get('id', '')}".rstrip(":"),
                                            f"bloom:{it.get('cognitive_process')}", f"task:{it.get('task')}"]
        tg = sub(q, "tags")
        for t in tags:
            if t and not t.endswith(":"):
                sub(sub(tg, "tag"), "text", t)
    return to_string(quiz)


# --------------------------------------------------------------------- gift

GIFT_SPECIAL = re.compile(r"([~=#{}:\\])")


def gift_escape(s: str) -> str:
    return GIFT_SPECIAL.sub(r"\\\1", s or "").replace("\n", " ")


def export_gift(bank: dict, items: list[dict]) -> str:
    out = [f"// {bank['bank'].get('title', '')}", f"// Generated by {m.GENERATOR}. Review before use.",
           f"$CATEGORY: $course$/top/{re.sub(r'[~=#{}:/]', ' -', bank['bank'].get('title', 'Imported questions'))}", ""]
    for it in items:
        q_html = m.question_html(bank, it)
        lines = [f"// {it['id']} | {it['objective'].get('id', '')} {it.get('task')} / {it.get('cognitive_process')}",
                 f"::{gift_escape(it['id'])}::[html]{gift_escape(q_html)} {{"]
        for opt in it["options"]:
            w = option_weight(it, opt)
            if opt.get("correct"):
                prefix = "="
            elif w > 0:
                prefix = f"~%{moodle_fraction(w)}%"
            else:
                prefix = "~"
            lines.append(f"\t{prefix}{gift_escape(opt['text'])}#{gift_escape(opt.get('feedback', ''))}")
        lines.append("}")
        out.append("\n".join(lines))
        out.append("")
    return "\n".join(out)


# -------------------------------------------------------------------- qti 2.1

QTI21_NS = "http://www.imsglobal.org/xsd/imsqti_v2p1"
QTI21_XSD = "http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1.xsd"
XSI = "http://www.w3.org/2001/XMLSchema-instance"


def qti21_item(bank: dict, it: dict) -> str:
    ident = ncname(it["id"])
    root = ET.Element("assessmentItem", {
        "xmlns": QTI21_NS, "xmlns:xsi": XSI, "xsi:schemaLocation": f"{QTI21_NS} {QTI21_XSD}",
        "identifier": ident, "title": it["id"], "adaptive": "false", "timeDependent": "false"})
    rd = sub(root, "responseDeclaration", identifier="RESPONSE", cardinality="single", baseType="identifier")
    cr = sub(rd, "correctResponse")
    sub(cr, "value", m.key_option(it)["label"])
    mp = sub(rd, "mapping", defaultValue="0")
    for opt in it["options"]:
        sub(mp, "mapEntry", mapKey=opt["label"], mappedValue=f"{option_weight(it, opt):g}")
    for oid, base, val in [("SCORE", "float", "0"), ("MAXSCORE", "float", "1")]:
        od = sub(root, "outcomeDeclaration", identifier=oid, cardinality="single", baseType=base)
        sub(sub(od, "defaultValue"), "value", val)
    sub(root, "outcomeDeclaration", identifier="FEEDBACK", cardinality="single", baseType="identifier")
    body = sub(root, "itemBody")
    question_elements(sub(body, "div"), bank, it)
    ci = sub(body, "choiceInteraction", responseIdentifier="RESPONSE",
             shuffle="true" if it.get("shuffle", True) else "false", maxChoices="1")
    for opt in it["options"]:
        sub(ci, "simpleChoice", opt["text"], identifier=opt["label"])
    rp = sub(root, "responseProcessing")
    rc = sub(rp, "responseCondition")
    ri = sub(rc, "responseIf")
    sub(sub(ri, "isNull"), "variable", identifier="RESPONSE")
    sub(sub(ri, "setOutcomeValue", identifier="SCORE"), "baseValue", "0", baseType="float")
    re_ = sub(rc, "responseElse")
    sub(sub(re_, "setOutcomeValue", identifier="SCORE"), "mapResponse", identifier="RESPONSE")
    sub(sub(rp, "setOutcomeValue", identifier="FEEDBACK"), "variable", identifier="RESPONSE")
    for opt in it["options"]:
        mf = sub(root, "modalFeedback", outcomeIdentifier="FEEDBACK", identifier=opt["label"], showHide="show")
        sub(mf, "p", opt.get("feedback", ""))
    return to_string(root)


def export_qti21(bank: dict, items: list[dict]) -> bytes:
    sets = m.sets_by_id(bank)
    # Group consecutive items into test parts: each locked (sequential) set is its own linear part.
    parts: list[tuple[str, list[dict]]] = []
    for it in items:
        s = sets.get(it.get("set_id")) if it.get("set_id") else None
        mode = "linear" if s and s.get("navigation") == "locked" else "nonlinear"
        key = f"{mode}:{it.get('set_id') if mode == 'linear' else ''}"
        if parts and parts[-1][0] == key:
            parts[-1][1].append(it)
        else:
            parts.append((key, [it]))

    test = ET.Element("assessmentTest", {"xmlns": QTI21_NS, "xmlns:xsi": XSI,
                                         "xsi:schemaLocation": f"{QTI21_NS} {QTI21_XSD}",
                                         "identifier": "TEST", "title": bank["bank"].get("title", "Assessment")})
    for n, (key, members) in enumerate(parts, 1):
        tp = sub(test, "testPart", identifier=f"P{n}", navigationMode=key.split(":")[0], submissionMode="individual")
        sec = sub(tp, "assessmentSection", identifier=f"S{n}", title=key.split(":", 1)[1] or f"Section {n}", visible="true")
        for it in members:
            sub(sec, "assessmentItemRef", identifier=ncname(it["id"]), href=f"items/{ncname(it['id'])}.xml")

    man = ET.Element("manifest", {"xmlns": "http://www.imsglobal.org/xsd/imscp_v1p1",
                                  "identifier": f"MANIFEST-{uuid.uuid4().hex[:12]}"})
    md = sub(man, "metadata")
    sub(md, "schema", "QTIv2.1 Package")
    sub(md, "schemaversion", "1.0.0")
    sub(man, "organizations")
    res = sub(man, "resources")
    tr = sub(res, "resource", identifier="RES-TEST", type="imsqti_test_xmlv2p1", href="assessment.xml")
    sub(tr, "file", href="assessment.xml")
    for it in items:
        rid = f"RES-{ncname(it['id'])}"
        sub(tr, "dependency", identifierref=rid)
        r = sub(res, "resource", identifier=rid, type="imsqti_item_xmlv2p1", href=f"items/{ncname(it['id'])}.xml")
        sub(r, "file", href=f"items/{ncname(it['id'])}.xml")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("imsmanifest.xml", to_string(man))
        z.writestr("assessment.xml", to_string(test))
        for it in items:
            z.writestr(f"items/{ncname(it['id'])}.xml", qti21_item(bank, it))
    return buf.getvalue()


# -------------------------------------------------------------------- qti 1.2

def export_qti12(bank: dict, items: list[dict]) -> bytes:
    title = bank["bank"].get("title", "Assessment")
    root = ET.Element("questestinterop", {"xmlns": "http://www.imsglobal.org/xsd/ims_qtiasiv1p2"})
    asmt = sub(root, "assessment", ident="A1", title=title)
    md = sub(asmt, "qtimetadata")
    f = sub(md, "qtimetadatafield")
    sub(f, "fieldlabel", "cc_maxattempts")
    sub(f, "fieldentry", "1")
    sec = sub(asmt, "section", ident="root_section")
    for it in items:
        iid = ncname(it["id"])
        item = sub(sec, "item", ident=iid, title=it["id"])
        imd = sub(sub(item, "itemmetadata"), "qtimetadata")
        for label, entry in [("question_type", "multiple_choice_question"), ("points_possible", "1.0"),
                             ("original_answer_ids", ",".join(f"{iid}_{o['label']}" for o in it["options"])),
                             ("assessment_question_identifierref", iid)]:
            fld = sub(imd, "qtimetadatafield")
            sub(fld, "fieldlabel", label)
            sub(fld, "fieldentry", entry)
        pres = sub(item, "presentation")
        sub(sub(pres, "material"), "mattext", m.question_html(bank, it), texttype="text/html")
        rl = sub(pres, "response_lid", ident="response1", rcardinality="Single")
        rc = sub(rl, "render_choice", shuffle="Yes" if it.get("shuffle", True) else "No")
        for o in it["options"]:
            lab = sub(rc, "response_label", ident=f"{iid}_{o['label']}")
            sub(sub(lab, "material"), "mattext", o["text"], texttype="text/plain")
        rp = sub(item, "resprocessing")
        sub(sub(rp, "outcomes"), "decvar", maxvalue="100", minvalue="0", varname="SCORE", vartype="Decimal")
        for o in it["options"]:
            cond = sub(rp, "respcondition", continue_="Yes")
            sub(sub(cond, "conditionvar"), "varequal", f"{iid}_{o['label']}", respident="response1")
            sub(cond, "displayfeedback", feedbacktype="Response", linkrefid=f"{iid}_{o['label']}_fb")
        key = m.key_option(it)
        cond = sub(rp, "respcondition", continue_="No")
        sub(sub(cond, "conditionvar"), "varequal", f"{iid}_{key['label']}", respident="response1")
        sub(cond, "setvar", "100", action="Set", varname="SCORE")
        for o in it["options"]:
            fb = sub(item, "itemfeedback", ident=f"{iid}_{o['label']}_fb")
            sub(sub(sub(fb, "flow_mat"), "material"), "mattext", o.get("feedback", ""), texttype="text/plain")

    man = ET.Element("manifest", {"xmlns": "http://www.imsglobal.org/xsd/imscp_v1p1",
                                  "identifier": f"MANIFEST-{uuid.uuid4().hex[:12]}"})
    sub(man, "organizations")
    res = sub(man, "resources")
    r = sub(res, "resource", identifier="RES-1", type="imsqti_xmlv1p2", href="assessment.xml")
    sub(r, "file", href="assessment.xml")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("imsmanifest.xml", to_string(man))
        z.writestr("assessment.xml", to_string(root))
    return buf.getvalue()


# ------------------------------------------------------------------------ csv

def export_csv(bank: dict, items: list[dict]) -> str:
    n_opt = max((len(it["options"]) for it in items), default=4)
    labels = [chr(ord("A") + i) for i in range(n_opt)]
    head = ["id", "status", "set_id", "set_position", "objective_id", "objective", "testing_point", "format",
            "task", "cognitive_process", "cognitive_level", "purpose", "assessment_type", "question_context",
            "data_table", "lead_in"]
    for L in labels:
        head += [f"option_{L}", f"feedback_{L}", f"misconception_{L}", f"level_{L}", f"weight_{L}"]
    head += ["key", "shuffle", "option_count_reason", "difficulty_target", "sme_required", "claims_to_verify", "tags"]
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(head)
    for it in items:
        stem = it.get("stem", {})
        row = [it["id"], it.get("status"), it.get("set_id", ""), it.get("set_position", ""),
               it["objective"].get("id", ""), it["objective"].get("text", ""), it.get("testing_point", ""),
               it.get("format"), it.get("task"), it.get("cognitive_process"), it.get("cognitive_level"),
               it.get("purpose"), it.get("assessment_type"), "\n\n".join(m.item_context(bank, it)),
               stem.get("data_table") or "", stem.get("lead_in", "")]
        opts = {o["label"]: o for o in it["options"]}
        for L in labels:
            o = opts.get(L, {})
            row += [o.get("text", ""), o.get("feedback", ""), o.get("misconception") or "", o.get("level", ""), o.get("weight", "")]
        sme = it.get("sme_review") or {}
        row += [m.key_option(it)["label"], it.get("shuffle"), it.get("option_count_reason", ""), it.get("difficulty_target", ""),
                sme.get("required", False), " | ".join(sme.get("claims_to_verify", [])), ", ".join(it.get("tags", []))]
        w.writerow(row)
    return "\ufeff" + buf.getvalue()


# ------------------------------------------------------------------------ h5p

def _h5p_html(text: str) -> str:
    return f"<div>{m.esc(text)}</div>\n"


def export_h5p(bank: dict, items: list[dict]) -> bytes:
    questions = []
    for it in items:
        answers = [{"text": _h5p_html(o["text"]), "correct": bool(o.get("correct")),
                    "tipsAndFeedback": {"tip": "", "chosenFeedback": _h5p_html(o.get("feedback", "")), "notChosenFeedback": ""}}
                   for o in it["options"]]
        params = {
            "question": m.question_html(bank, it),
            "answers": answers,
            "behaviour": {"enableRetry": False, "enableSolutionsButton": True, "enableCheckButton": True,
                          "type": "single", "singlePoint": False, "randomAnswers": bool(it.get("shuffle", True)),
                          "showSolutionsRequiresInput": True, "confirmCheckDialog": False, "confirmRetryDialog": False,
                          "autoCheck": False, "passPercentage": 100, "showScorePoints": True},
            "media": {"disableImageZooming": False},
            "overallFeedback": [{"from": 0, "to": 100}],
            "UI": {"checkAnswerButton": "Check", "submitAnswerButton": "Submit", "showSolutionButton": "Show solution",
                   "tryAgainButton": "Retry", "tipsLabel": "Show tip", "scoreBarLabel": "You got :num out of :total points",
                   "tipAvailable": "Tip available", "feedbackAvailable": "Feedback available", "readFeedback": "Read feedback",
                   "wrongAnswer": "Wrong answer", "correctAnswer": "Correct answer", "shouldCheck": "Should have been checked",
                   "shouldNotCheck": "Should not have been checked", "noInput": "Please answer before viewing the solution",
                   "a11yCheck": "Check the answers.", "a11yShowSolution": "Show the solution.", "a11yRetry": "Retry the task."},
        }
        questions.append({"library": "H5P.MultiChoice 1.16", "params": params, "subContentId": str(uuid.uuid4()),
                          "metadata": {"contentType": "Multiple Choice", "license": "U", "title": it["id"]}})
    sets = m.sets_by_id(bank)
    locked = any(sets.get(it.get("set_id"), {}).get("navigation") == "locked" for it in items)
    content = {
        "introPage": {"showIntroPage": False, "startButtonText": "Start", "introduction": ""},
        "progressType": "dots", "passPercentage": 50, "questions": questions,
        "disableBackwardsNavigation": locked, "randomQuestions": False,
        "endGame": {"showResultPage": True, "showSolutionButton": True, "showRetryButton": False,
                    "noResultMessage": "Finished", "message": "Your result:", "overallFeedback": [{"from": 0, "to": 100}],
                    "solutionButtonText": "Show solution", "retryButtonText": "Retry", "finishButtonText": "Finish",
                    "showAnimations": False, "skippable": False, "skipButtonText": "Skip video"},
        "override": {"checkButton": True},
        "texts": {"prevButton": "Previous question", "nextButton": "Next question", "finishButton": "Finish",
                  "textualProgress": "Question: @current of @total questions", "jumpToQuestion": "Question %d of %total",
                  "questionLabel": "Question", "readSpeakerProgress": "Question @current of @total",
                  "unansweredText": "Unanswered", "answeredText": "Answered", "currentQuestionText": "Current question"},
    }
    h5p_json = {"title": bank["bank"].get("title", "Quiz"), "language": bank["bank"].get("language", "en"),
                "mainLibrary": "H5P.QuestionSet", "embedTypes": ["div", "iframe"], "license": "U",
                "defaultLanguage": bank["bank"].get("language", "en"),
                "preloadedDependencies": [{"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
                                          {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16}]}
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("h5p.json", json.dumps(h5p_json, indent=2, ensure_ascii=False))
        z.writestr("content/content.json", json.dumps(content, indent=2, ensure_ascii=False))
    return buf.getvalue()


# ------------------------------------------------------------------- markdown

def export_markdown(bank: dict, items: list[dict]) -> str:
    b = bank["bank"]
    d = b.get("defaults", {})
    out = [f"# {b.get('title', 'Item bank')}",
           f"Purpose: {d.get('purpose')} · Type: {d.get('assessment_type')} · Learners: {d.get('learner_level')} · Items: {len(items)}", ""]
    sets = m.sets_by_id(bank)
    for it in items:
        stem = it.get("stem", {})
        s = sets.get(it.get("set_id")) if it.get("set_id") else None
        out.append(f"## {it['id']} · {it['objective'].get('id', '-')} · {it.get('task')} / {it.get('cognitive_process')} · {it.get('format')}")
        if s:
            out.append(f"*Set {s['id']} ({s.get('type')}, navigation {s.get('navigation')}), item {it.get('set_position', '?')}*")
        out.append(f"**Testing point:** {it.get('testing_point', '')}")
        out.append("")
        for blk in m.item_context(bank, it):
            out += [blk, ""]
        if stem.get("data_table"):
            out += [stem["data_table"], ""]
        if it.get("media"):
            out += [f"*[{it['media'].get('type')}: {it['media'].get('alt_text')}]*", ""]
        out += [f"**{stem.get('lead_in', '')}**", "", "| | Option | Feedback |", "|---|---|---|"]
        for o in it["options"]:
            lab = f"**{o['label']} ✓**" if o.get("correct") else o["label"]
            if o.get("level") is not None:
                lab += f" (L{o['level']})"
            cell = lambda t: (t or "").replace("|", "\\|").replace("\n", " ")
            out.append(f"| {lab} | {cell(o['text'])} | {cell(o.get('feedback'))} |")
        audit = it.get("audit", {})
        cto = "✓" if audit.get("cover_the_options", {}).get("passed") else "✗"
        lint = ", ".join(sorted({e["code"] for e in audit.get("lint", []) if not e.get("resolved")})) or "none"
        sme = it.get("sme_review") or {}
        claims = "; ".join(sme.get("claims_to_verify", [])) or "none"
        out += ["", f"Audit: cover-the-options {cto} · lint: {lint} · SME check: {claims}", ""]
    adm = bank.get("administration")
    if adm:
        out += ["## Administration notes", ""]
        for k, v in adm.items():
            v = "; ".join(v) if isinstance(v, list) else v
            out.append(f"- **{k.replace('_', ' ').capitalize()}:** {v}")
        out.append("")
    return "\n".join(out)


# ----------------------------------------------------------------------- main

EXPORTERS = {"moodle-xml": export_moodle, "gift": export_gift, "qti21": export_qti21, "qti12": export_qti12,
             "csv": export_csv, "h5p": export_h5p, "markdown": export_markdown}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bank", help="Path to the item bank JSON file")
    ap.add_argument("--format", required=True, choices=list(EXPORTERS))
    ap.add_argument("--out", help="Output file (default: next to the bank, with a format-specific suffix)")
    ap.add_argument("--only-status", nargs="+", metavar="STATUS",
                    help="Export only items with these statuses, e.g. --only-status approved reviewed")
    args = ap.parse_args(argv)
    m.utf8_output()

    try:
        bank = m.load_bank(args.bank)
    except m.BankError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    errs, _ = m.validate_schema(bank)
    if errs:
        print("error: the bank doesn't validate; run lint_items.py and fix these first:", file=sys.stderr)
        for path, msg in errs[:10]:
            print(f"  {path}: {msg}", file=sys.stderr)
        return 2

    items = m.delivery_order(bank)
    if args.only_status:
        items = [it for it in items if it.get("status") in args.only_status]
        if not items:
            print(f"error: no items with status {args.only_status}", file=sys.stderr)
            return 2
    drafts = sum(1 for it in items if it.get("status") == "draft")

    result = EXPORTERS[args.format](bank, items)
    bank_path = Path(args.bank)
    stem_name = bank_path.name[:-len(".items.json")] if bank_path.name.endswith(".items.json") else bank_path.stem
    out = Path(args.out) if args.out else bank_path.with_name(stem_name + SUFFIX[args.format])
    if isinstance(result, bytes):
        out.write_bytes(result)
    else:
        out.write_text(result, encoding="utf-8", newline="\n")

    print(f"Wrote {len(items)} item(s) to {out}")
    if drafts:
        print(f"note: {drafts} item(s) are still 'draft'; have them reviewed before learners see them "
              f"(use --only-status approved to export reviewed items only).")
    for line in LIMITATIONS[args.format]:
        print(f"note: {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
