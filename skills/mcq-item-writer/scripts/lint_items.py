#!/usr/bin/env python3
"""Lint an MCQ item bank: schema validation plus automatable item-writing flaw checks.

Flaw codes match references/technical-flaws.md. Findings are prompts for judgment,
not verdicts: a flagged repeated word may be harmless.

Usage:
  python lint_items.py BANK.json                 # report
  python lint_items.py BANK.json --write         # also store findings in each item's audit.lint
  python lint_items.py BANK.json --format json   # machine-readable output
  python lint_items.py BANK.json --strict        # exit 1 on warnings as well as errors

Exit codes: 0 = no errors (warnings allowed unless --strict); 1 = errors found; 2 = unreadable input.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass

import mcqlib as m

SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


@dataclass
class Finding:
    item: str          # item id, or "BANK"
    code: str
    severity: str      # error | warning | info
    message: str
    option: str | None = None


# ----------------------------------------------------------------- word lists

VAGUE_TERMS = ["often", "usually", "frequently", "rarely", "sometimes", "commonly", "generally",
               "occasionally", "seldom", "typically", "normally"]
VAGUE_PHRASES = ["is associated with", "are associated with", "is useful for", "is important",
                 "may be", "could be", "might be"]
ABSOLUTE_STRONG = ["always", "never", "invariably", "absolutely", "completely", "entirely", "totally"]
ABSOLUTE_WEAK = ["all", "none", "only", "every", "must"]
HEDGES = ["may", "might", "can", "could", "possibly", "sometimes", "perhaps"]
NEGATIVE_STRONG_RE = re.compile(r"\b(EXCEPT|NOT|LEAST|FALSE|INCORRECT|UNTRUE)\b")
NEGATIVE_SOFT_RE = re.compile(r"\b(except|least (likely|appropriate|accurate|useful)|not (true|correct|appropriate|indicated|likely)|incorrect|false|untrue)\b", re.I)
NOTA_RE = re.compile(r"\bnone of (the )?(above|these|the options|the following)\b", re.I)
AOTA_RE = re.compile(r"\ball of (the )?(above|these|the options|the following)\b", re.I)
ROMAN_LIST_RE = re.compile(r"(^|\n)\s*(I|II|III|IV|V|VI)[.):]\s", re.M)
RANK_RE = re.compile(r"\b(rank|arrange|order|sequence)\b[^.?]*\b(following|these|items|steps)\b", re.I)
COMBO_RE = re.compile(r"^\s*((both\s+)?[A-H1-9IVX]+\s*(,\s*[A-H1-9IVX]+\s*)*,?\s*(and|&)\s*[A-H1-9IVX]+(\s*(only|but not\s+[A-H1-9IVX]+))?|[1-9IVX]+(\s*,\s*[1-9IVX]+)+(\s*only)?|neither\s+[A-H]\s+nor\s+[A-H])\s*$", re.I)
ABBREV_RE = re.compile(r"\b(e\.g|i\.e|etc|vs|pp|p|Dr|Mr|Ms|Mrs|No|Fig|approx|cf)\.", re.I)
# Words that come from lead-in templates (references/lead-in-bank.md); a key echoing these is not a clang cue.
LEADIN_WORDS = {"strongly", "supported", "support", "data", "findings", "finding", "explanation", "explains", "likely",
                "appropriate", "situation", "action", "step", "cause", "result", "results", "conclusion", "conclusions",
                "evaluation", "interpretation", "describes", "best", "first", "next", "initial", "priority"}
TRIADS = [
    ({"increase", "increased", "increases", "rise", "rises", "higher", "more", "greater"},
     {"decrease", "decreased", "decreases", "fall", "falls", "lower", "less", "fewer", "smaller"},
     {"no change", "unchanged", "remain unchanged", "remains unchanged", "same", "stay the same", "stays the same", "not change"}),
]
THIN_FEEDBACK_RE = re.compile(r"^\s*(correct|incorrect|wrong|right|yes|no|true|false)[.!]?\s*$", re.I)
# Sentinel used when converting existing items that had no feedback (Review mode), plus common placeholders.
PLACEHOLDER_FEEDBACK_RE = re.compile(r"\(none in original\)|\bTODO\b|\bTBD\b|lorem ipsum|no feedback (was )?provided", re.I)

NUM_RE = r"[-+]?\d+(?:[.,]\d+)?"
RANGE_RE = re.compile(rf"^\s*(?:from\s+)?({NUM_RE})\s*%?\s*(?:-|–|—|to)\s*({NUM_RE})\s*%?\s*$", re.I)
POINT_RE = re.compile(rf"^\s*(?:about|approximately|~)?\s*({NUM_RE})\s*(%|[a-zA-Z/°µ]+(?:/[a-zA-Z]+)?)?\s*$")
BOUND_RE = re.compile(rf"^\s*(less than|fewer than|under|below|<|greater than|more than|over|above|>)\s*({NUM_RE})\s*%?\s*$", re.I)


def has_word(text: str, word: str) -> bool:
    return re.search(rf"\b{re.escape(word)}\b", text or "", re.I) is not None


# ------------------------------------------------------------------ item checks

def lint_item(item: dict, bank: dict) -> list[Finding]:
    f: list[Finding] = []
    iid = item.get("id", "?")
    opts = item.get("options") or []
    stem = item.get("stem") or {}
    lead = stem.get("lead_in", "") or ""
    context = " ".join(m.item_context(bank, item))
    stem_text = f"{context} {stem.get('data_table') or ''} {lead}"
    key = m.key_option(item)
    distractors = [o for o in opts if not o.get("correct")]
    purpose = item.get("purpose") or bank.get("bank", {}).get("defaults", {}).get("purpose")

    def add(code, sev, msg, option=None):
        f.append(Finding(iid, code, sev, msg, option))

    # --- option labels
    labels = [o.get("label") for o in opts]
    expected = [chr(ord("A") + i) for i in range(len(opts))]
    if labels != expected:
        add("SCHEMA-LABELS", "warning", f"Option labels should run {''.join(expected)} in order (found {''.join(str(l) for l in labels)}).")

    # --- ID-LONG-OPTIONS
    for o in opts:
        n = m.word_count(o.get("text", ""))
        if n > 15:
            add("ID-LONG-OPTIONS", "warning", f"Option has {n} words; move shared content into the stem and shorten options.", o.get("label"))

    # --- ID-NUMERIC
    f += _numeric_checks(item)

    # --- ID-VAGUE (lead-in and options; scenarios may legitimately use these words)
    for where, text, label in [("lead-in", lead, None)] + [("option", o.get("text", ""), o.get("label")) for o in opts]:
        hits = [w for w in VAGUE_TERMS if has_word(text, w)] + [p for p in VAGUE_PHRASES if p in text.lower()]
        if hits:
            add("ID-VAGUE", "warning", f"Vague term(s) in {where}: {', '.join(sorted(set(hits)))}.", label)

    # --- ID-NOTA / X-AOTA
    for o in opts:
        t = o.get("text", "")
        if NOTA_RE.search(t):
            if o.get("correct") and purpose in ("learning", "both"):
                add("ID-NOTA", "error", "'None of the above' is the key in a learning item; learners never see the correct answer.", o.get("label"))
            else:
                add("ID-NOTA", "error", "'None of the above': replace with a specific option such as 'No further action is needed'.", o.get("label"))
        if AOTA_RE.search(t):
            add("X-AOTA", "error", "'All of the above': rewards partial knowledge; replace with a single best option.", o.get("label"))

    # --- ID-NONPARALLEL (candidates)
    if len(opts) >= 3:
        counts = [m.word_count(o.get("text", "")) for o in opts]
        sentences = [len(re.findall(r"[.!?](\s|$)", ABBREV_RE.sub(lambda mm: mm.group(1), o.get("text", "").strip()))) for o in opts]
        if min(counts) > 0 and max(counts) / min(counts) >= 3:
            add("ID-NONPARALLEL", "warning", f"Option lengths vary widely ({min(counts)}–{max(counts)} words); check options share one grammatical form.")
        if len(set(s > 1 for s in sentences)) > 1:
            add("ID-NONPARALLEL", "warning", "Some options are multi-sentence and others are not; make options parallel.")

    # --- ID-COMPLEX-STEM
    if ROMAN_LIST_RE.search(stem_text) or RANK_RE.search(lead):
        add("ID-COMPLEX-STEM", "warning", "Stem asks learners to rank or decode a numbered list; ask about a single element instead.")
    for o in opts:
        if COMBO_RE.match(o.get("text", "")):
            add("ID-COMPLEX-STEM", "error", "Combination option (e.g. 'A and C', '1, 2 only'); convert to one-best-answer.", o.get("label"))

    # --- ID-NEGATIVE
    neg = NEGATIVE_STRONG_RE.search(lead)
    soft = NEGATIVE_SOFT_RE.search(lead)
    if neg:
        add("ID-NEGATIVE", "error", f"Negative lead-in ('{neg.group(0)}'); rewrite as a positive question.")
    elif soft:
        add("ID-NEGATIVE", "warning", f"Possible negative lead-in ('{soft.group(0)}'); check it asks for the best answer, not the least.")

    # --- TW-GRAMMAR
    if re.search(r"\b(a|an|the)\s*[:?]?\s*$", lead, re.I) or lead.rstrip().endswith(":"):
        add("TW-GRAMMAR", "error", "Open lead-in (ends with an article or colon); use a closed question ending in '?'.")
    article = re.search(r"\b(a|an)\s*$", lead.rstrip("?: "), re.I)
    if article:
        art = article.group(1).lower()
        for o in opts:
            first = (o.get("text", "") or " ")[0].lower()
            vowel = first in "aeiou"
            if (art == "an") != vowel:
                add("TW-GRAMMAR", "error", f"Option doesn't fit the article '{art}' at the end of the lead-in.", o.get("label"))

    # --- TW-ABSOLUTE
    for o in opts:
        t = o.get("text", "")
        strong = [w for w in ABSOLUTE_STRONG if has_word(t, w)]
        weak = [w for w in ABSOLUTE_WEAK if has_word(t, w)]
        if strong:
            add("TW-ABSOLUTE", "warning", f"Absolute term(s): {', '.join(strong)}. Test-savvy learners eliminate these.", o.get("label"))
        elif weak:
            add("TW-ABSOLUTE", "info", f"Possible absolute term(s): {', '.join(weak)}. Check they aren't acting as a cue.", o.get("label"))
    hedged = [o.get("label") for o in opts if any(has_word(o.get("text", ""), h) for h in HEDGES)]
    if hedged and len(hedged) < len(opts) and any(f_.code == "TW-ABSOLUTE" and f_.severity == "warning" for f_ in f):
        add("TW-ABSOLUTE", "warning", f"Mix of hedged ({', '.join(hedged)}) and absolute options; the hedged ones look safer.")

    # --- TW-KEY-STANDS-OUT
    if key and distractors:
        k_len = m.word_count(key.get("text", ""))
        d_lens = [m.word_count(d.get("text", "")) for d in distractors]
        mean_d = sum(d_lens) / len(d_lens)
        # Absolute margins avoid false alarms on short term lists ("Standard deviation" vs "Mean").
        if mean_d > 0 and k_len >= 1.5 * mean_d and k_len > max(d_lens) and k_len - mean_d >= 3:
            add("TW-KEY-STANDS-OUT", "warning", f"Key is the longest option ({k_len} words vs mean {mean_d:.1f}); equalise and move explanation into feedback.", key.get("label"))
        elif mean_d >= 6 and k_len <= 0.5 * mean_d and k_len < min(d_lens):
            add("TW-KEY-STANDS-OUT", "warning", f"Key is conspicuously the shortest option ({k_len} words vs mean {mean_d:.1f}); a reverse length cue.", key.get("label"))
        if "(" in key.get("text", "") and not any("(" in d.get("text", "") for d in distractors):
            add("TW-KEY-STANDS-OUT", "warning", "Key is the only option with a parenthetical qualifier.", key.get("label"))

    # --- TW-CLANG
    if key:
        f += _clang(item, key, distractors, stem_text)

    # --- TW-CONVERGENCE
    if key and len(opts) >= 4:
        f += _convergence(item, opts, key)

    # --- TW-EXHAUSTIVE
    f += _exhaustive(item, opts)

    # --- X-OPTION-COUNT
    target = m.options_per_item(bank)
    if len(opts) != target and not item.get("option_count_reason"):
        add("X-OPTION-COUNT", "warning", f"{len(opts)} options but the bank setting is {target}; record option_count_reason or adjust.")
    if len(opts) == 2:
        add("X-OPTION-COUNT", "info", "Two-option item: blind guessing succeeds 50% of the time. Tell the user.")

    # --- X-FEEDBACK-MISSING
    placeholders = [o.get("label") for o in opts if PLACEHOLDER_FEEDBACK_RE.search(o.get("feedback") or "")]
    if placeholders:
        # One finding per item: converted originals often have no feedback at all, and per-option noise hides the real problems.
        add("X-FEEDBACK-MISSING", "error", f"No real feedback on option(s) {', '.join(placeholders)} (placeholder from the original). Write feedback for each option.")
    for o in opts:
        fb = (o.get("feedback") or "").strip()
        if o.get("label") in placeholders:
            continue
        if not fb:
            add("X-FEEDBACK-MISSING", "error", "No feedback.", o.get("label"))
        elif THIN_FEEDBACK_RE.match(fb) or m.word_count(fb) < 8:
            add("X-FEEDBACK-MISSING", "error", "Feedback too thin; explain why this option is or isn't best.", o.get("label"))
        if not o.get("correct") and not o.get("misconception"):
            add("X-FEEDBACK-MISSING", "info", "Distractor has no 'misconception' recorded.", o.get("label"))
    fbs = [re.sub(r"\s+", " ", (o.get("feedback") or "").strip().lower()) for o in opts if o.get("label") not in placeholders]
    dupes = {fb for fb in fbs if fb and fbs.count(fb) > 1}
    if dupes:
        labels = [o.get("label") for o, fb in zip(opts, fbs) if fb in dupes]
        add("X-FEEDBACK-MISSING", "error", f"Options {', '.join(labels)} share identical feedback; each option needs its own explanation.")

    # --- numeric options should not shuffle
    if _all_numeric(opts) and item.get("shuffle") is True:
        add("X-KEY-POSITION", "warning", "Numeric options should keep logical order: set shuffle to false.")

    # --- ordered MC structure
    if item.get("format") == "ordered-mc":
        levels = [o.get("level") for o in opts]
        if None not in levels:
            if sorted(levels) != list(range(1, len(opts) + 1)):
                add("SCHEMA-ORDERED-LEVELS", "error", f"Levels should be 1..{len(opts)}, one per option (found {levels}).")
            elif key and key.get("level") != max(levels):
                add("SCHEMA-ORDERED-LEVELS", "error", "The key should be the highest level of understanding.", key.get("label"))
        om = item.get("ordered_mc") or {}
        if om and not om.get("confirmed_by_user"):
            add("SCHEMA-ORDERED-LEVELS", "warning", "Progression not yet confirmed by the user.")

    # --- cover-the-options / SME
    cto = (item.get("audit") or {}).get("cover_the_options") or {}
    if cto.get("passed") is False:
        add("X-COVER-THE-OPTIONS", "error", "Item failed the cover-the-options check; focus the lead-in or scenario.")
    elif not cto.get("stem_only_answer"):
        add("X-COVER-THE-OPTIONS", "info", "No stem_only_answer recorded for the cover-the-options check.")
    sme = item.get("sme_review") or {}
    if sme.get("required") and sme.get("outcome") not in ("approved",):
        claims = sme.get("claims_to_verify") or []
        add("X-SME-PENDING", "info", f"Needs expert verification ({len(claims)} claim(s)).")

    if item.get("cognitive_level") == "recall" and not (stem.get("scenario") or item.get("set_id")):
        add("X-RECALL", "info", "Recall item with no scenario; fine for formative checks, prefer application for summative.")

    return f


def _num_value(text: str):
    t = text.strip().rstrip(".")
    mr = RANGE_RE.match(t)
    if mr:
        return ("range", float(mr.group(1).replace(",", ".")), float(mr.group(2).replace(",", ".")))
    mb = BOUND_RE.match(t)
    if mb:
        v = float(mb.group(2).replace(",", "."))
        lower = mb.group(1).lower() in ("less than", "fewer than", "under", "below", "<")
        return ("bound", float("-inf") if lower else v, v if lower else float("inf"))
    mp = POINT_RE.match(t)
    if mp:
        v = float(mp.group(1).replace(",", "."))
        return ("point", v, v)
    return None


def _all_numeric(opts: list[dict]) -> bool:
    return len(opts) >= 2 and all(_num_value(o.get("text", "")) for o in opts)


def _numeric_checks(item: dict) -> list[Finding]:
    opts = item.get("options") or []
    if not _all_numeric(opts):
        return []
    iid = item.get("id", "?")
    vals = [_num_value(o.get("text", "")) for o in opts]
    out: list[Finding] = []
    kinds = {v[0] for v in vals}
    if "point" in kinds and kinds & {"range", "bound"}:
        out.append(Finding(iid, "ID-NUMERIC", "warning", "Numeric options mix single values with ranges; use one format."))
    lows = [v[1] for v in vals]
    if lows != sorted(lows):
        out.append(Finding(iid, "ID-NUMERIC", "warning", "Numeric options are not in ascending order."))
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            a, b = vals[i], vals[j]
            if a[0] == b[0] == "point":
                if a[1] == b[1]:
                    out.append(Finding(iid, "ID-NUMERIC", "error", f"Options {opts[i].get('label')} and {opts[j].get('label')} have the same value."))
                continue
            if a[1] <= b[2] and b[1] <= a[2]:  # intervals share at least one value (touching ends count)
                out.append(Finding(iid, "ID-NUMERIC", "warning",
                                   f"Options {opts[i].get('label')} and {opts[j].get('label')} overlap; more than one could be correct."))
    return out


def _clang(item: dict, key: dict, distractors: list[dict], stem_text: str) -> list[Finding]:
    # Only distinctive words count: a term mentioned once in the stem and echoed by the key.
    # Words the scenario repeats (actors, the main object) are context, not cues.
    stem_counts = Counter(m.stem_word(w) for w in m.content_words(stem_text))
    dis_stems = {m.stem_word(w) for d in distractors for w in m.content_words(d.get("text", ""))}
    hits = []
    for w in set(m.content_words(key.get("text", ""))):
        s = m.stem_word(w)
        if s in dis_stems or w in LEADIN_WORDS:
            continue
        if stem_counts.get(s) == 1:
            hits.append(w)
    if hits:
        return [Finding(item.get("id", "?"), "TW-CLANG", "warning",
                        f"Key repeats stem word(s) not used in any distractor: {', '.join(sorted(hits))}.", key.get("label"))]
    return []


def _convergence(item: dict, opts: list[dict], key: dict) -> list[Finding]:
    toks = [{m.stem_word(w) for w in m.content_words(o.get("text", ""))} for o in opts]
    scores = []
    for i, t in enumerate(toks):
        scores.append(sum(1 for w in t for j, other in enumerate(toks) if j != i and w in other))
    k_idx = opts.index(key)
    k_score = scores[k_idx]
    others = [s for i, s in enumerate(scores) if i != k_idx]
    if k_score >= 2 and all(k_score > s for s in others):
        return [Finding(item.get("id", "?"), "TW-CONVERGENCE", "warning",
                        f"Key shares the most terms with the other options (score {k_score} vs max {max(others)}); balance terms across options.",
                        key.get("label"))]
    return []


def _exhaustive(item: dict, opts: list[dict]) -> list[Finding]:
    texts = [o.get("text", "").lower() for o in opts]
    out = []
    for up, down, same in TRIADS:
        has_up = [i for i, t in enumerate(texts) if any(re.search(rf"\b{w}\b", t) for w in up)]
        has_down = [i for i, t in enumerate(texts) if any(re.search(rf"\b{w}\b", t) for w in down)]
        has_same = [i for i, t in enumerate(texts) if any(w in t for w in same)]
        short = [i for i, t in enumerate(texts) if m.word_count(t) <= 4]
        if has_up and has_down and has_same:
            subset = set(has_up[:1] + has_down[:1] + has_same[:1])
            if len(opts) > len(subset) and subset <= set(short):
                out.append(Finding(item.get("id", "?"), "TW-EXHAUSTIVE", "warning",
                                   "An increase / decrease / no-change subset covers every outcome, so other options can be ignored."))
    return out


# ------------------------------------------------------------------ bank checks

def lint_bank(bank: dict) -> tuple[list[Finding], bool]:
    findings: list[Finding] = []
    schema_errs, full = m.validate_schema(bank)
    for path, msg in schema_errs:
        iid = "BANK"
        mm = re.match(r"\$\.items\[(\d+)\]", path)
        if mm:
            idx = int(mm.group(1))
            items = bank.get("items", [])
            if idx < len(items):
                iid = items[idx].get("id", f"items[{idx}]")
        findings.append(Finding(iid, "SCHEMA-INVALID", "error", f"{path}: {msg}"))

    items = bank.get("items", [])
    ids = Counter(it.get("id") for it in items)
    for iid, n in ids.items():
        if n > 1:
            findings.append(Finding(str(iid), "SCHEMA-DUPLICATE-ID", "error", f"Item id used {n} times."))

    by_id = {it.get("id"): it for it in items}
    for s in bank.get("sets", []):
        for mid in s.get("item_ids", []):
            if mid not in by_id:
                findings.append(Finding("BANK", "SCHEMA-SET-REF", "error", f"Set {s.get('id')} lists unknown item {mid}."))
            elif by_id[mid].get("set_id") != s.get("id"):
                findings.append(Finding(mid, "SCHEMA-SET-REF", "warning", f"Item is in set {s.get('id')} but its set_id is {by_id[mid].get('set_id')!r}."))
        for upd in s.get("updates", []):
            if upd.get("after_item") not in s.get("item_ids", []):
                findings.append(Finding("BANK", "SCHEMA-SET-REF", "error", f"Set {s.get('id')} update refers to {upd.get('after_item')}, which is not in the set."))
    set_ids = {s.get("id") for s in bank.get("sets", [])}
    for it in items:
        if it.get("set_id") and it["set_id"] not in set_ids:
            findings.append(Finding(it.get("id", "?"), "SCHEMA-SET-REF", "error", f"set_id {it['set_id']} has no matching set."))

    for it in items:
        try:
            findings += lint_item(it, bank)
        except Exception as exc:  # keep linting other items
            findings.append(Finding(it.get("id", "?"), "SCHEMA-INVALID", "error", f"Could not lint item: {exc}"))

    # X-KEY-POSITION across all items. Many platforms (Canvas, Moodle via GIFT) ignore the per-item shuffle
    # flag and only shuffle if the quiz setting is on, so authored positions are often what learners see.
    keyed = [it for it in items if m.key_option(it)]
    if len(keyed) >= 4:
        pos = Counter(m.key_option(it).get("label") for it in keyed)
        top, n = pos.most_common(1)[0]
        n_opts = max(len(it.get("options", [])) for it in keyed)
        unused = [chr(ord("A") + i) for i in range(n_opts) if chr(ord("A") + i) not in pos]
        if n / len(keyed) > 0.5:
            findings.append(Finding("BANK", "X-KEY-POSITION", "warning",
                                    f"{n} of {len(keyed)} items have the key in position {top}; spread key positions "
                                    "(platforms such as Canvas ignore per-item shuffle unless the quiz setting is on)."))
        elif len(keyed) >= 2 * n_opts and unused:
            findings.append(Finding("BANK", "X-KEY-POSITION", "warning",
                                    f"No item has its key in position {', '.join(unused)}; spread key positions."))

    findings.sort(key=lambda x: (x.item == "BANK", x.item, SEVERITY_ORDER[x.severity], x.code))
    return findings, full


# ------------------------------------------------------------------------ output

def write_back(bank: dict, findings: list[Finding]) -> None:
    by_item: dict[str, list[Finding]] = {}
    for fd in findings:
        by_item.setdefault(fd.item, []).append(fd)
    for it in bank.get("items", []):
        audit = it.setdefault("audit", {"cover_the_options": {"passed": False}})
        kept = [e for e in audit.get("lint", []) if e.get("resolved")]
        kept_keys = {(e.get("code"), e.get("option")) for e in kept}
        new = []
        for fd in by_item.get(it.get("id"), []):
            if fd.code == "SCHEMA-INVALID" or (fd.code, fd.option) in kept_keys:
                continue
            entry = {"code": fd.code, "severity": fd.severity, "message": fd.message}
            if fd.option:
                entry["option"] = fd.option
            new.append(entry)
        audit["lint"] = kept + new


def print_text(findings: list[Finding], full_schema: bool, n_items: int) -> None:
    if not full_schema:
        print("note: 'jsonschema' not installed; basic structural checks only (pip install jsonschema for full validation).\n")
    current = None
    for fd in findings:
        if fd.item != current:
            current = fd.item
            print(f"\n{current}")
        opt = f" [{fd.option}]" if fd.option else ""
        print(f"  {fd.severity:<7} {fd.code:<22}{opt} {fd.message}")
    c = Counter(fd.severity for fd in findings)
    print(f"\n{n_items} item(s): {c.get('error', 0)} error(s), {c.get('warning', 0)} warning(s), {c.get('info', 0)} info.")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bank", help="Path to the item bank JSON file")
    ap.add_argument("--write", action="store_true", help="Store findings in each item's audit.lint (keeps entries marked resolved)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--strict", action="store_true", help="Exit 1 on warnings too")
    ap.add_argument("--quiet", action="store_true", help="Hide info-level findings in text output")
    args = ap.parse_args(argv)
    m.utf8_output()

    try:
        bank = m.load_bank(args.bank)
    except m.BankError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    findings, full = lint_bank(bank)
    # A reviewer can accept a finding by marking its audit.lint entry "resolved": true
    # (with a "resolution" note). Those are not reported again.
    resolved = {(it.get("id"), e.get("code"), e.get("option"))
                for it in bank.get("items", []) for e in (it.get("audit") or {}).get("lint", []) if e.get("resolved")}
    n_resolved = sum(1 for f in findings if (f.item, f.code, f.option) in resolved)
    findings = [f for f in findings if (f.item, f.code, f.option) not in resolved]
    shown = [f for f in findings if not (args.quiet and f.severity == "info")]
    if args.format == "json":
        print(json.dumps({"full_schema_validation": full, "findings": [asdict(f) for f in shown]}, indent=2, ensure_ascii=False))
    else:
        print_text(shown, full, len(bank.get("items", [])))
        if n_resolved:
            print(f"{n_resolved} finding(s) previously marked resolved were not repeated.")

    if args.write:
        write_back(bank, findings)
        m.save_bank(bank, args.bank)
        if args.format == "text":
            print(f"Findings written to audit.lint in {args.bank}")

    errors = any(f.severity == "error" for f in findings)
    warnings = any(f.severity == "warning" for f in findings)
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
