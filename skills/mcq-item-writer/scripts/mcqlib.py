"""Shared helpers for the mcq-item-writer scripts.

Standard library only. If the optional `jsonschema` package is installed,
full schema validation is used; otherwise a basic structural check runs.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

SKILL_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = SKILL_DIR / "assets" / "item.schema.json"
DEFAULT_OPTIONS_PER_ITEM = 4
GENERATOR = "mcq-item-writer 0.1.0"


class BankError(Exception):
    """Raised when a bank file cannot be read or parsed."""


# --------------------------------------------------------------------------- I/O

def utf8_output() -> None:
    """Make console output UTF-8 so non-ASCII text (dashes, accents) prints correctly on Windows."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def load_bank(path: str | Path) -> dict:
    p = Path(path)
    if not p.is_file():
        raise BankError(f"File not found: {p}")
    try:
        with p.open(encoding="utf-8-sig") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        raise BankError(f"{p} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or "items" not in data:
        raise BankError(f"{p} does not look like an item bank (no 'items' array).")
    return data


def save_bank(bank: dict, path: str | Path) -> None:
    p = Path(path)
    with p.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(bank, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# --------------------------------------------------------------------- validation

def validate_schema(bank: dict) -> tuple[list[tuple[str, str]], bool]:
    """Return ([(json_path, message)], used_full_schema)."""
    try:
        import jsonschema  # type: ignore
        from jsonschema import Draft202012Validator, FormatChecker  # type: ignore
    except ImportError:
        return _basic_validate(bank), False

    with SCHEMA_PATH.open(encoding="utf-8") as fh:
        schema = json.load(fh)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for err in sorted(validator.iter_errors(bank), key=lambda e: list(e.absolute_path)):
        errors.append((_json_path(err.absolute_path), _short(err.message)))
    return errors, True


def _json_path(parts: Iterable[Any]) -> str:
    out = "$"
    for part in parts:
        out += f"[{part}]" if isinstance(part, int) else f".{part}"
    return out


def _short(msg: str, limit: int = 200) -> str:
    return msg if len(msg) <= limit else msg[: limit - 3] + "..."


def _basic_validate(bank: dict) -> list[tuple[str, str]]:
    """Minimal structural checks used when jsonschema is unavailable."""
    errs: list[tuple[str, str]] = []
    for key in ("schema_version", "bank", "items"):
        if key not in bank:
            errs.append(("$", f"'{key}' is a required property"))
    items = bank.get("items", [])
    if not isinstance(items, list):
        return errs + [("$.items", "must be an array")]
    required = ["id", "status", "format", "objective", "testing_point", "task",
                "cognitive_process", "cognitive_level", "purpose", "assessment_type",
                "stem", "options", "shuffle", "audit"]
    for i, item in enumerate(items):
        base = f"$.items[{i}]"
        for key in required:
            if key not in item:
                errs.append((base, f"'{key}' is a required property"))
        lead = (item.get("stem") or {}).get("lead_in", "")
        if lead and not lead.rstrip().endswith("?"):
            errs.append((f"{base}.stem.lead_in", "must end with '?'"))
        opts = item.get("options") or []
        for j, opt in enumerate(opts):
            for key in ("label", "text", "correct", "feedback"):
                if key not in opt:
                    errs.append((f"{base}.options[{j}]", f"'{key}' is a required property"))
        if item.get("format") in ("one-best-answer", "ordered-mc"):
            keys = sum(1 for o in opts if o.get("correct") is True)
            if keys != 1:
                errs.append((f"{base}.options", f"one-best-answer items need exactly 1 key (found {keys})"))
    return errs


# ------------------------------------------------------------------- bank helpers

def options_per_item(bank: dict) -> int:
    return int(bank.get("bank", {}).get("defaults", {}).get("options_per_item", DEFAULT_OPTIONS_PER_ITEM))


def sets_by_id(bank: dict) -> dict[str, dict]:
    return {s["id"]: s for s in bank.get("sets", []) if "id" in s}


def key_option(item: dict) -> dict | None:
    for opt in item.get("options", []):
        if opt.get("correct") is True:
            return opt
    return None


def delivery_order(bank: dict) -> list[dict]:
    """Items in delivery order: bank order, but set members kept together in set order."""
    items = bank.get("items", [])
    by_id = {it.get("id"): it for it in items}
    sets = sets_by_id(bank)
    out: list[dict] = []
    placed: set[str] = set()
    for it in items:
        iid = it.get("id")
        if iid in placed:
            continue
        sid = it.get("set_id")
        if sid and sid in sets:
            for member in sets[sid].get("item_ids", []):
                if member in by_id and member not in placed:
                    out.append(by_id[member])
                    placed.add(member)
        if iid not in placed:
            out.append(it)
            placed.add(iid)
    return out


def item_context(bank: dict, item: dict) -> list[str]:
    """Text blocks a learner sees before this item's lead-in (set context + own scenario)."""
    blocks: list[str] = []
    sid = item.get("set_id")
    s = sets_by_id(bank).get(sid) if sid else None
    if s:
        if s.get("opening_scenario"):
            blocks.append(s["opening_scenario"])
        if s.get("stimulus"):
            blocks.append(s["stimulus"])
        if s.get("type") == "sequential":
            members = s.get("item_ids", [])
            if item.get("id") in members:
                idx = members.index(item["id"])
                earlier = set(members[:idx])
                for upd in s.get("updates", []):
                    if upd.get("after_item") in earlier:
                        blocks.append(upd["text"])
    stem = item.get("stem", {})
    if stem.get("scenario"):
        blocks.append(stem["scenario"])
    return blocks


# ------------------------------------------------------------------ text helpers

STOPWORDS = set("""
a about above after again against all also am an and any are as at be because been before being
below between both but by can could did do does doing down during each few for from further had has
have having he her here hers herself him himself his how i if in into is it its itself just least
let me more most my myself no nor not now of off on once only or other ought our ours ourselves out
over own same she should so some such than that the their theirs them themselves then there these
they this those through to too under until up very was we were what when where which while who whom
why will with would you your yours yourself yourselves following best likely appropriate which most
item option options patient person learner one two three first next
""".split())

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")


def words(text: str) -> list[str]:
    return WORD_RE.findall(text or "")


def word_count(text: str) -> int:
    return len(words(text))


def content_words(text: str) -> list[str]:
    out = []
    for w in words(text):
        w = re.sub(r"'s$|'$", "", w.lower())
        if len(w) >= 4 and w not in STOPWORDS:
            out.append(w)
    return out


_SUFFIXES = ("ations", "ation", "ments", "ment", "ities", "ity", "ings", "ing", "ions", "ion",
             "ness", "ers", "er", "ed", "es", "ly", "s")


def stem_word(w: str) -> str:
    w = w.lower().strip("'-")
    for suf in _SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


# ---------------------------------------------------------------- HTML helpers

def esc(text: str) -> str:
    return html.escape(text or "", quote=True)


_INLINE_RE = re.compile(r"\*\*(.+?)\*\*|__(.+?)__|(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])|`(.+?)`")


def inline_runs(text: str) -> list[tuple[str, str]]:
    """Split text into (style, text) runs for **bold**, *italic*/_italic_ and `code`. style is '', 'strong', 'em' or 'code'."""
    runs: list[tuple[str, str]] = []
    pos = 0
    for mt in _INLINE_RE.finditer(text or ""):
        if mt.start() > pos:
            runs.append(("", text[pos:mt.start()]))
        if mt.group(1) is not None or mt.group(2) is not None:
            runs.append(("strong", mt.group(1) or mt.group(2)))
        elif mt.group(3) is not None:
            runs.append(("em", mt.group(3)))
        else:
            runs.append(("code", mt.group(4)))
        pos = mt.end()
    if pos < len(text or ""):
        runs.append(("", text[pos:]))
    return runs


def inline_html(text: str) -> str:
    """Escape text and render inline Markdown emphasis as HTML."""
    return "".join(esc(t) if not tag else f"<{tag}>{esc(t)}</{tag}>" for tag, t in inline_runs(text))


def strip_inline(text: str) -> str:
    """Plain text with inline Markdown markers removed (for formats without rich text)."""
    return "".join(t for _, t in inline_runs(text))


def is_md_table(text: str) -> bool:
    lines = [l.strip() for l in (text or "").strip().splitlines() if l.strip()]
    return len(lines) >= 2 and all(l.startswith("|") for l in lines) and re.match(r"^\|[\s:|-]+\|$", lines[1]) is not None


def md_table_to_html(text: str) -> str:
    """Convert a simple Markdown pipe table to HTML. Non-table text becomes <pre>."""
    if not is_md_table(text):
        return f"<pre>{esc(text)}</pre>"
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]

    def cells(line: str) -> list[str]:
        return [c.strip() for c in line.strip("|").split("|")]

    head = cells(lines[0])
    rows = [cells(l) for l in lines[2:]]
    out = ['<table border="1" cellpadding="4">', "<thead><tr>"]
    out += [f"<th>{inline_html(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for r in rows:
        out.append("<tr>" + "".join(f"<td>{inline_html(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def paragraphs_html(text: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text or "") if p.strip()]
    return "".join(f"<p>{inline_html(p).replace(chr(10), '<br>')}</p>" for p in paras)


def question_html(bank: dict, item: dict) -> str:
    """Full question text (set context, scenario, data table, media note, lead-in) as HTML."""
    parts = [paragraphs_html(b) for b in item_context(bank, item)]
    stem = item.get("stem", {})
    if stem.get("data_table"):
        parts.append(md_table_to_html(stem["data_table"]))
    media = item.get("media")
    if media:
        parts.append(f"<p><em>[{esc(media.get('type', 'media')).capitalize()}: {esc(media.get('alt_text', ''))}]</em></p>")
    parts.append(f"<p><strong>{esc(stem.get('lead_in', ''))}</strong></p>")
    return "".join(parts)


def question_text_plain(bank: dict, item: dict) -> str:
    parts = list(item_context(bank, item))
    stem = item.get("stem", {})
    if stem.get("data_table"):
        parts.append(stem["data_table"])
    if item.get("media"):
        m = item["media"]
        parts.append(f"[{m.get('type', 'media').capitalize()}: {m.get('alt_text', '')}]")
    parts.append(stem.get("lead_in", ""))
    return "\n\n".join(p for p in parts if p)
