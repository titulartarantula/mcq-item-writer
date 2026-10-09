# mcq-item-writer

A Claude skill for writing, reviewing, and analysing **one-best-answer multiple-choice questions** in any subject. It is built on the evidence-based principles in the NBME Item-Writing Guide (Billings et al., *Constructing Written Test Questions for the Health Sciences*), generalised beyond health care for e-learning, course assessment, and training programmes. Research on learning from tests adds to it (Butler, 2018; Xu, Kauer & Tupy, 2016), so items work for **learning** as well as measurement.

Defaults: 3 options per item, explanatory feedback on every option, and optional diagnostic (ordered) items.

> **Status: in development (v0.1.0-dev).** The reference content is complete. The workflow (`SKILL.md`), linter, exporters, and evals are in progress. See the roadmap below.

## What it will do

| Mode | Input | Output |
|---|---|---|
| **Write** | learning objectives, source content, learner level, stakes, purpose (assessment / learning / both) | scenario-based items with key, per-option feedback, a flaw audit, and administration notes |
| **Review** | existing items | flaws identified by code, with page-cited explanations and suggested revisions |
| **Analyze** | learner response data | difficulty, discrimination, and option analysis, with flags for miskeys, items with two answers, and weak distractors |
| **Blueprint** | objectives and weights | content × task grid that drives item writing |

Planned export formats: JSON (canonical), Markdown review sheet, Moodle GIFT and Moodle XML, QTI 1.2 and 2.1, CSV, H5P.

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
  SKILL.md                 workflow (in progress)
  references/              item-writing principles, loaded on demand
  scripts/                 linter, exporters, response analysis (in progress)
  assets/                  item JSON schema (in progress)
docs/source-map.md         guide section → reference file coverage
evals/                     test items and generation tasks (in progress)
```

## Roadmap

- [x] Phase 1: repo, licensing, plugin manifests
- [x] Phase 2: reference files distilled from the guide (12 files, page-cited, original examples)
- [x] Phase 2b: supporting research added (Butler 2018; Xu et al. 2016): learning and feedback, ordered MC, administration
- [ ] Phase 3: item JSON schema and `SKILL.md` workflow
- [ ] Phase 4: `lint_items.py`, exporters, `analyze_responses.py`
- [ ] Phase 5: evals across several unrelated domains
- [ ] Phase 6: v0.1.0 release

## Source and licensing

This project restates the NBME guide's principles, and the findings of the supporting reviews, in its own words, with page citations. It does **not** reproduce any source's text, sample items, figures, or tables, and all examples are original. Read the original free at <https://www.nbme.org/educators/item-writing-guide>. Not affiliated with or endorsed by NBME. See [ATTRIBUTION.md](ATTRIBUTION.md).

- Code: MIT ([LICENSE](LICENSE))
- Documentation and reference content: CC BY-NC 4.0 ([LICENSE-DOCS](LICENSE-DOCS))
