# mcq-item-writer

A Claude skill for writing, reviewing, and analysing **one-best-answer multiple-choice questions** in any subject. It is built on the evidence-based principles in the NBME Item-Writing Guide (Billings et al., *Constructing Written Test Questions for the Health Sciences*), generalised beyond health care for e-learning, course assessment, and training programmes. Research on learning from tests adds to it (Butler, 2018; Xu, Kauer & Tupy, 2016), so items work for **learning** as well as measurement.

> **Status: v0.1.0.** First release, see the [release notes](https://github.com/titulartarantula/mcq-item-writer/releases/tag/v0.1.0). Canvas import has not yet been confirmed in a live Canvas course, so please [open an issue](https://github.com/titulartarantula/mcq-item-writer/issues) if an import goes wrong.

## Install

In Claude Code:

```
/plugin marketplace add titulartarantula/mcq-item-writer
/plugin install mcq-item-writer@mcq-item-writer
```

Then ask in plain language, for example:

- "Write 6 knowledge-check questions for this module, for Canvas."
- "Review these quiz questions before I give them to students."
- "Here are last term's quiz results. Which questions should I fix?"

## What it does

| Mode | Input | Output |
|---|---|---|
| **Write** | learning objectives, source content, learner level, stakes, purpose (assessment / learning / both) | scenario-based items with key, feedback on every option, a flaw audit, and administration notes |
| **Review** | existing items | problems explained in plain language (Must fix / Should fix / Optional), with suggested revisions |
| **Analyze** | learner response data | difficulty, discrimination, reliability, and option analysis, with flags for miskeys, items with two answers, and distractors nobody picks; shows the score impact of rekeying |
| **Blueprint** | objectives and weights | content × task grid that drives item writing |

Defaults:

- 4 options per item. You can change this; 3 is a research-backed alternative.
- Explanatory feedback on every option, the correct one included.
- Ordered (diagnostic) multiple choice is offered, never applied without asking.
- Safer distractors when the purpose is learning.
- Options are kept comparable in length, but are never forced to match.

Export formats: JSON (canonical), Markdown review sheet, Moodle XML, Moodle GIFT, QTI 2.1 and QTI 1.2 packages (both validate against the official IMS schemas), Canvas (QTI 1.2 with import notes), CSV, and H5P (experimental).

## Calling it from another project

Other projects (e-learning builds, course modules) can hand the skill a short brief: objectives, source material, audience, purpose, `options_per_item`, and the export formats wanted. See "Calling this skill from another project" in [`SKILL.md`](skills/mcq-item-writer/SKILL.md) for the brief format.

## Scripts

Python 3.9+, standard library only. Install `jsonschema` for full schema validation; without it a basic structural check runs.

```bash
python skills/mcq-item-writer/scripts/lint_items.py bank.items.json          # flaw audit
python skills/mcq-item-writer/scripts/export.py bank.items.json --format canvas
python skills/mcq-item-writer/scripts/analyze_responses.py responses.csv --bank bank.items.json
```

Each script has `--help`. Tests: `python -m unittest discover -s tests -v`.

## Repository layout

```
.claude-plugin/            plugin + marketplace manifests
skills/mcq-item-writer/
  SKILL.md                 workflow: intake, Write / Review / Analyze / Blueprint modes
  references/              15 reference files on item-writing principles, loaded on demand
  scripts/                 lint_items.py, export.py, analyze_responses.py (+ mcqlib.py)
  assets/                  item.schema.json + example-bank.json
docs/source-map.md         source section → reference file coverage
tests/                     unit tests (seeded flaws, simulated response data, export checks)
evals/                     skill-level evals: prompts, expectations, and input files
```

## Roadmap

- [x] Phase 1: repo, licensing, plugin manifests
- [x] Phase 2: reference files distilled from the guide (page-cited, original examples)
- [x] Phase 2b: supporting research added (Butler 2018; Xu et al. 2016): learning and feedback, ordered MC, administration
- [x] Phase 3: item JSON schema, worked example bank, and `SKILL.md` workflow
- [x] Phase 4: `lint_items.py`, `export.py`, `analyze_responses.py`, unit tests (63), CI on Python 3.9 and 3.13
- [x] Phase 5: evals on writing, reviewing, and analysis tasks (100% of expectations met with the skill vs 78% without)
- [x] Phase 6: v0.1.0 release
- [ ] Confirm Canvas import (Classic and New Quizzes) in a live course

## Source and licensing

This project restates the NBME guide's principles, and the findings of the supporting reviews, in its own words, with page citations. It does **not** reproduce any source's text, sample items, figures, or tables, and all examples are original. Read the original free at <https://www.nbme.org/educators/item-writing-guide>. Not affiliated with or endorsed by NBME. See [ATTRIBUTION.md](ATTRIBUTION.md).

- Code: MIT ([LICENSE](LICENSE))
- Documentation and reference content: CC BY-NC 4.0 ([LICENSE-DOCS](LICENSE-DOCS))
