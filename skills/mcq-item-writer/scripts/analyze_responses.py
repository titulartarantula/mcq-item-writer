#!/usr/bin/env python3
"""Item analysis for delivered multiple-choice items (classical test theory).

Computes per item: difficulty (p), corrected point-biserial discrimination, option
proportions for the whole group and for High/Low groups, and review flags from
references/item-analysis.md. Also reports test-level KR-20 reliability.

Flags are prompts for expert review, never automatic verdicts.

INPUT FORMATS (CSV with a header row; auto-detected):
  wide   one row per learner: a learner-id column (optional) plus one column per item id,
         each cell the chosen option label (A, B, C...). Blank or '-' = omitted.
         Cells may also hold the option text if --bank is given (matched exactly).
  long   one row per response, with columns named like learner/student/user, item/question,
         and response/answer/choice.
  scored wide format where every cell is 1/0 (correct/incorrect). Gives p and discrimination
         only; option analysis needs the chosen options.
LMS item-analysis exports are not read directly; export the per-learner responses
(e.g. Moodle 'Responses' report, Canvas 'Student Analysis') and reshape to wide or long.

KEYS come from --bank (the item bank JSON) or --key "ITEM1=B,ITEM2=D" / --key keys.csv (item,key).

Usage:
  python analyze_responses.py responses.csv --bank bank.json
  python analyze_responses.py responses.csv --key "Q1=B,Q2=A" --format markdown
  python analyze_responses.py responses.csv --bank bank.json --write --date 2026-11-02
  python analyze_responses.py responses.csv --bank bank.json --previous last_term.items.json   # drift
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

import mcqlib as m

LEARNER_COLS = {"learner", "learner_id", "student", "student_id", "user", "user_id", "username", "id", "name", "email", "candidate"}
ITEM_COLS = {"item", "item_id", "question", "question_id", "q"}
RESP_COLS = {"response", "answer", "choice", "selected", "option", "selection"}
OMIT = {"", "-", "—", "na", "n/a", "null", "none", "omit", "omitted", "blank"}

FLAG_TEXT = {
    "POSSIBLE_MISKEY": "Strong learners preferred a distractor and discrimination is negative; the key may be wrong.",
    "POSSIBLE_TWO_ANSWERS": "A distractor attracted 30% or more of the High group; it may be defensible.",
    "NEGATIVE_DISCRIMINATION": "Weaker learners did better on this item than stronger learners.",
    "LOW_DISCRIMINATION": "Discrimination below .20; the item adds little to ranking learners.",
    "TOO_EASY": "p above .95; tells you little about this group.",
    "TOO_HARD": "p below .30; check the key, clarity, and whether the topic was taught.",
    "NONFUNCTIONAL_DISTRACTOR": "Distractor chosen by under 5% of learners; replace it.",
    "REVERSE_DISTRACTOR": "Distractor chosen more by the High group than the Low group (by 5 points or more).",
    "DRIFT": "p changed by more than .15 since the previous administration (exposure, outdated content, or teaching change).",
}


# --------------------------------------------------------------------------- input

def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        rows = list(csv.reader(fh, dialect))
    if not rows:
        raise ValueError(f"{path} is empty")
    return [h.strip() for h in rows[0]], [r for r in rows[1:] if any(c.strip() for c in r)]


def parse_keys(arg: str | None) -> dict[str, str]:
    if not arg:
        return {}
    p = Path(arg)
    if p.is_file():
        head, rows = read_csv(p)
        return {r[0].strip(): r[1].strip().upper() for r in rows if len(r) >= 2}
    out = {}
    for part in arg.split(","):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip().upper()
    return out


def load_responses(path: Path, item_ids_hint: set[str]) -> tuple[list[str], list[str], dict[str, dict[str, str]]]:
    """Return (learner_ids, item_ids, responses[learner][item] = raw value)."""
    head, rows = read_csv(path)
    low = [h.lower() for h in head]
    li = next((i for i, h in enumerate(low) if h in LEARNER_COLS), None)
    ii = next((i for i, h in enumerate(low) if h in ITEM_COLS), None)
    ri = next((i for i, h in enumerate(low) if h in RESP_COLS), None)

    resp: dict[str, dict[str, str]] = {}
    items: list[str] = []
    learners: list[str] = []
    if ii is not None and ri is not None and len(head) <= 5:           # long format
        for n, r in enumerate(rows):
            lid = r[li].strip() if li is not None and li < len(r) else f"L{n}"
            iid = r[ii].strip()
            if lid not in resp:
                resp[lid] = {}
                learners.append(lid)
            if iid not in items:
                items.append(iid)
            resp[lid][iid] = r[ri].strip() if ri < len(r) else ""
        return learners, items, resp

    if li is None and head and head[0] not in item_ids_hint and not re.fullmatch(r"[A-Za-z]*\d+", head[0] or ""):
        li = 0                                                         # unnamed first column = learner id
    item_cols = [(i, h) for i, h in enumerate(head) if i != li and h]
    items = [h for _, h in item_cols]
    for n, r in enumerate(rows):
        lid = r[li].strip() if li is not None and li < len(r) else f"L{n + 1}"
        learners.append(lid)
        resp[lid] = {h: (r[i].strip() if i < len(r) else "") for i, h in item_cols}
    return learners, items, resp


# ---------------------------------------------------------------------- statistics

def pearson(x: list[float], y: list[float]) -> float | None:
    n = len(x)
    if n < 3:
        return None
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(sxx * syy)


def analyse(learners, items, resp, keys, bank, group_pct, previous):
    by_id = {it["id"]: it for it in (bank or {}).get("items", [])}
    scored_mode = all(v.strip() in {"0", "1", ""} for lr in resp.values() for v in lr.values())

    def normalise(iid: str, raw: str) -> str | None:
        v = (raw or "").strip()
        if v.lower() in OMIT:
            return None
        if scored_mode:
            return v
        if re.fullmatch(r"[A-Ha-h]", v):
            return v.upper()
        it = by_id.get(iid)
        if it:
            for o in it["options"]:
                if o["text"].strip().lower() == v.lower():
                    return o["label"]
        return v.upper()

    choice = {l: {i: normalise(i, resp[l].get(i, "")) for i in items} for l in learners}

    def correct(l, i) -> int:
        c = choice[l][i]
        if scored_mode:
            return 1 if c == "1" else 0
        return 1 if c is not None and c == keys.get(i) else 0

    missing_keys = [] if scored_mode else [i for i in items if i not in keys]
    items_scored = [i for i in items if scored_mode or i in keys]
    X = {l: {i: correct(l, i) for i in items_scored} for l in learners}
    totals = {l: sum(X[l].values()) for l in learners}
    N, k = len(learners), len(items_scored)

    g = max(1, round(N * group_pct / 100))

    results = []
    pq_sum = 0.0
    for i in items_scored:
        xs = [X[l][i] for l in learners]
        p = sum(xs) / N if N else 0.0
        pq_sum += p * (1 - p)
        rest = [totals[l] - X[l][i] for l in learners]
        # High/Low groups are formed from the score on the OTHER items. On short quizzes the item's
        # own answer is a large share of the total, which would push its key into the High group.
        order = sorted(learners, key=lambda l: totals[l] - X[l][i], reverse=True)
        high, low = order[:g], order[-g:]
        disc = pearson([float(v) for v in xs], [float(v) for v in rest])
        res = {"item": i, "n": N, "p": round(p, 3), "discrimination": None if disc is None else round(disc, 3),
               "key": keys.get(i), "flags": [], "notes": []}
        it = by_id.get(i)
        if it:
            res["target"] = it.get("difficulty_target")
        if not scored_mode:
            labels = sorted({choice[l][i] for l in learners if choice[l][i]} |
                            ({o["label"] for o in it["options"]} if it else set()))
            prop = lambda grp, lab: sum(1 for l in grp if choice[l][i] == lab) / len(grp) if grp else 0.0
            res["options"] = {lab: {"total": round(prop(learners, lab), 3), "high": round(prop(high, lab), 3),
                                    "low": round(prop(low, lab), 3)} for lab in labels}
            res["omitted"] = round(sum(1 for l in learners if choice[l][i] is None) / N, 3) if N else 0
        _flag(res, previous.get(i))
        if it and it.get("format") == "ordered-mc" and not scored_mode:
            lev = {o["label"]: o.get("level") for o in it["options"]}
            dist = {}
            for lab, v in res["options"].items():
                if lev.get(lab) is not None:
                    dist[f"level {lev[lab]}"] = v["total"]
            res["level_distribution"] = dict(sorted(dist.items()))
        results.append(res)

    mean = sum(totals.values()) / N if N else 0
    var = sum((t - mean) ** 2 for t in totals.values()) / N if N else 0
    kr20 = (k / (k - 1)) * (1 - pq_sum / var) if k > 1 and var > 0 else None
    summary = {"learners": N, "items": k, "mean_score": round(mean, 2), "sd": round(math.sqrt(var), 2),
               "kr20": None if kr20 is None else round(kr20, 3), "group_percent": group_pct, "group_size": g,
               "scored_only": scored_mode, "items_without_key": missing_keys}
    return summary, results


def _flag(res: dict, prev_p: float | None) -> None:
    p, d, key = res["p"], res["discrimination"], res.get("key")
    flags = res["flags"]
    if d is not None:
        if d < 0:
            flags.append("NEGATIVE_DISCRIMINATION")
        elif d < 0.20:
            flags.append("LOW_DISCRIMINATION")
    if p > 0.95:
        flags.append("TOO_EASY")
    if p < 0.30:
        flags.append("TOO_HARD")
    opts = res.get("options")
    if opts and key:
        k_high = opts.get(key, {}).get("high", 0)
        dis = {lab: v for lab, v in opts.items() if lab != key}
        if d is not None and d < 0 and any(v["high"] > k_high for v in dis.values()):
            flags.append("POSSIBLE_MISKEY")
            best = max(dis.items(), key=lambda kv: kv[1]["high"])[0]
            res["notes"].append(f"High group preferred {best} over the key {key}.")
        two = [lab for lab, v in dis.items() if v["high"] >= 0.30]
        if two:
            flags.append("POSSIBLE_TWO_ANSWERS")
            res["notes"].append(f"High group chose {', '.join(two)} 30%+ of the time.")
        nf = [lab for lab, v in dis.items() if v["total"] < 0.05]
        if nf:
            flags.append("NONFUNCTIONAL_DISTRACTOR")
            res["notes"].append(f"Nonfunctional: {', '.join(nf)}.")
        rev = [lab for lab, v in dis.items() if v["high"] - v["low"] >= 0.05]
        if rev:
            flags.append("REVERSE_DISTRACTOR")
            res["notes"].append(f"Chosen more by High than Low: {', '.join(rev)}.")
    if prev_p is not None and abs(p - prev_p) > 0.15:
        flags.append("DRIFT")
        res["notes"].append(f"p was {prev_p:.2f}, now {p:.2f}.")


# --------------------------------------------------------------------------- output

def fmt_num(v, nd=2):
    return "-" if v is None else f"{v:.{nd}f}"


def report_text(summary, results, markdown=False) -> str:
    L = []
    s = summary
    hdr = "# Item analysis" if markdown else "ITEM ANALYSIS"
    L += [hdr, ""]
    L.append(f"Learners: {s['learners']} | Items: {s['items']} | Mean: {s['mean_score']} | SD: {s['sd']} | "
             f"KR-20: {fmt_num(s['kr20'])} | High/Low groups: top/bottom {s['group_percent']}% (n={s['group_size']})")
    if s["learners"] < 30:
        L.append(f"CAUTION: only {s['learners']} learners; statistics are unstable. Lean on content review.")
    if s["items_without_key"]:
        L.append(f"Not scored (no key): {', '.join(s['items_without_key'])}")
    if s["scored_only"]:
        L.append("Input was scored 0/1, so option analysis is not available.")
    L.append("")
    if markdown:
        L += ["| Item | p | target | disc | flags |", "|---|---|---|---|---|"]
    for r in results:
        flags = ", ".join(r["flags"]) or "-"
        if markdown:
            L.append(f"| {r['item']} | {fmt_num(r['p'])} | {fmt_num(r.get('target'))} | {fmt_num(r['discrimination'])} | {flags} |")
        else:
            L.append(f"{r['item']:<18} p={fmt_num(r['p'])}  target={fmt_num(r.get('target'))}  disc={fmt_num(r['discrimination'])}  {flags}")
    flagged = [r for r in results if r["flags"]]
    if flagged:
        L += ["", "## Flagged items" if markdown else "FLAGGED ITEMS (review with a subject-matter expert)"]
        for r in flagged:
            L += ["", f"### {r['item']}" if markdown else f"{r['item']}  (key {r.get('key')})"]
            if markdown:
                L.append(f"Key: {r.get('key')}")
            if "options" in r:
                labs = list(r["options"])
                L.append("        " + "  ".join(f"{(l + ('*' if l == r.get('key') else '')):>5}" for l in labs))
                for grp in ("high", "low", "total"):
                    L.append(f"  {grp:<6}" + "  ".join(f"{round(r['options'][l][grp] * 100):>5}" for l in labs))
            for fl in r["flags"]:
                L.append(f"  - {fl}: {FLAG_TEXT[fl]}")
            for note in r["notes"]:
                L.append(f"    {note}")
            if r.get("level_distribution"):
                L.append(f"  Ordered-MC levels: " + ", ".join(f"{k} {round(v * 100)}%" for k, v in r["level_distribution"].items()))
    ordered = [r for r in results if r.get("level_distribution") and not r["flags"]]
    for r in ordered:
        L.append(f"{r['item']} ordered-MC levels: " + ", ".join(f"{k} {round(v * 100)}%" for k, v in r["level_distribution"].items()))
    L += ["", "Flags are prompts for review, not verdicts. Changing an item's options makes it a new item; its statistics start over."]
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------------------- main

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("responses", help="CSV of learner responses (wide, long, or scored 0/1)")
    ap.add_argument("--bank", help="Item bank JSON (supplies keys, option text, targets, ordered-MC levels)")
    ap.add_argument("--key", help="Keys as 'ID=B,ID2=C' or a CSV file with item,key columns")
    ap.add_argument("--groups", type=float, default=27, help="High/Low group size as a percentage (default 27)")
    ap.add_argument("--previous", help="An earlier bank JSON whose items have stats.p, for drift checks")
    ap.add_argument("--format", choices=["text", "markdown", "json"], default="text")
    ap.add_argument("--write", action="store_true", help="Store stats in the bank's items (needs --bank)")
    ap.add_argument("--date", default=date.today().isoformat(), help="Administration date stored with --write")
    args = ap.parse_args(argv)
    m.utf8_output()

    bank = None
    try:
        if args.bank:
            bank = m.load_bank(args.bank)
    except m.BankError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    keys = {}
    if bank:
        keys = {it["id"]: m.key_option(it)["label"] for it in bank["items"] if m.key_option(it)}
    keys.update(parse_keys(args.key))

    try:
        learners, items, resp = load_responses(Path(args.responses), set(keys))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if not learners:
        print("error: no learner rows found", file=sys.stderr)
        return 2

    previous: dict[str, float] = {}
    src = m.load_bank(args.previous) if args.previous else bank
    for it in (src or {}).get("items", []):
        st = it.get("stats") or {}
        if st.get("p") is not None and (args.previous or st.get("administered") != args.date):
            previous[it["id"]] = st["p"]

    summary, results = analyse(learners, items, resp, keys, bank, args.groups, previous)

    if args.format == "json":
        print(json.dumps({"summary": summary, "items": results}, indent=2))
    else:
        print(report_text(summary, results, markdown=args.format == "markdown"), end="")

    if args.write:
        if not bank:
            print("error: --write needs --bank", file=sys.stderr)
            return 2
        by = {r["item"]: r for r in results}
        for it in bank["items"]:
            r = by.get(it["id"])
            if not r:
                continue
            st = {"n": r["n"], "p": r["p"], "flags": r["flags"], "administered": args.date}
            if r["discrimination"] is not None:
                st["discrimination"] = r["discrimination"]
            if "options" in r:
                st["option_proportions"] = {k: v["total"] for k, v in r["options"].items()}
            it["stats"] = st
        m.save_bank(bank, args.bank)
        print(f"Stats written to {args.bank}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
