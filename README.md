# mcq-item-writer

A Claude skill for writing, reviewing, and analysing **one-best-answer multiple-choice questions** in any subject. It is built on the evidence-based principles in the NBME Item-Writing Guide (Billings et al., *Constructing Written Test Questions for the Health Sciences*), generalised beyond health care for e-learning, course assessment, and training programmes. Research on learning from tests adds to it (Butler, 2018; Xu, Kauer & Tupy, 2016), so items work for **learning** as well as measurement.

Defaults: 4 options per item (configurable; 3 is a research-backed alternative), explanatory feedback on every option, and optional diagnostic (ordered) items.

> **Status: in development (v0.1.0-dev).** The reference content, item schema, `SKILL.md` workflow, and scripts are complete and tested. Real-world evals and LMS import testing come next. See the roadmap below.

## What it will do

| Mode | Input | Output |
|---|---|---|
| **Write** | learning objectives, source content, learner level, stakes, purpose (assessment / learning / both) | scenario-based items with key, per-option feedback, a flaw audit, and administration notes |
| **Review** | existing items | flaws identified by code, with page-cited explanations and suggested revisions |
| **Analyze** | learner response data | difficulty, discrimination, and option analysis, with flags for miskeys, items with two answers, and weak distractors |
| **Blueprint** | objectives and weights | content × task grid that drives item writing |

Export formats: JSON (canonical), Markdown review sheet, Moodle XML, Moodle GIFT, QTI 2.1 and QTI 1.2 packages (both validate against the official IMS schemas), CSV, and H5P (experimental).

## Scripts

Python 3.9+, standard library only. Install `jsonschema` for full schema validation; without it a basic structural check runs.

```bash
python skills/mcq-item-writer/scripts/lint_items.py bank.items.json          # flaw audit
python skills/mcq-item-writer/scripts/export.py bank.items.json --format qti21
python skills/mcq-item-writer/scripts/analyze_responses.py responses.csv --bank bank.items.json
```

Each script has `--help`. Tests: `python -m unittest discover -s tests -v`.

## Install (once published)

In Claude Code:

```
/plugin marketplace add titulartarantula/mcq-item-writer
/plugin install mcq-item-writer@mcq-item-writer
```

## Repository layout

```
.claude-plugin/            plugin + marketplace manifests
skills/mcq-item-writer/
  SKILL.md                 workflow: intake, Write / Review / Analyze / Blueprint modes
  references/              item-writing principles, loaded on demand
  scripts/                 lint_items.py, export.py, analyze_responses.py (+ mcqlib.py)
  assets/                  item.schema.json + example-bank.json
docs/source-map.md         guide section → reference file coverage
tests/                     unit tests (seeded flaws, simulated response data, export checks)
evals/                     skill-level evals (in progress)
```

## Roadmap

- [x] Phase 1: repo, licensing, plugin manifests
- [x] Phase 2: reference files distilled from the guide (12 files, page-cited, original examples)
- [x] Phase 2b: supporting research added (Butler 2018; Xu et al. 2016): learning and feedback, ordered MC, administration
- [x] Phase 3: item JSON schema, worked example bank, and `SKILL.md` workflow
- [x] Phase 4: `lint_items.py`, `export.py` (7 formats), `analyze_responses.py`, 52 unit tests, CI
- [ ] Phase 5: evals across several unrelated domains
- [ ] Phase 6: v0.1.0 release

## Source and licensing

This project restates the NBME guide's principles, and the findings of the supporting reviews, in its own words, with page citations. It does **not** reproduce any source's text, sample items, figures, or tables, and all examples are original. Read the original free at <https://www.nbme.org/educators/item-writing-guide>. Not affiliated with or endorsed by NBME. See [ATTRIBUTION.md](ATTRIBUTION.md).

- Code: MIT ([LICENSE](LICENSE))
- Documentation and reference content: CC BY-NC 4.0 ([LICENSE-DOCS](LICENSE-DOCS))
