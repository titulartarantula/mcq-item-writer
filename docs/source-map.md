# Source coverage map

How each section of the NBME Item-Writing Guide (6th ed., Oct 2024 printing) and the two supporting reviews map onto this skill. Use it to check coverage and to find the right reference file. Page numbers are the guide's printed page numbers.

| Guide section | Pages | Covered in | Notes |
|---|---|---|---|
| **Ch 1** Introduction: assessment, content sampling, psychometric performance | 9–10 | `blueprint.md`, `cognitive-level.md` | |
| Purposes of testing; what material to test | 10 | `blueprint.md` | |
| **Ch 2** One-best-answer vs true-false families | 11 | `item-anatomy.md`, `formats.md` | |
| Stem / vignette / lead-in / options; single-continuum distractors | 12 | `item-anatomy.md` | |
| Cover-the-options rule | 13 | `item-anatomy.md`, `writing-rules.md` (Rule 3) | |
| Homogeneous options | 13 | `item-anatomy.md`, `writing-rules.md` (Rule 4) | |
| General rules for one-best-answer items; recommendation | 14 | `item-anatomy.md` | |
| True-false family: rules and challenges | 15–16 | `formats.md` | |
| **Ch 3** Irrelevant-difficulty flaws (7) | 17–21 | `technical-flaws.md` (ID-*) | |
| Testwise-cue flaws (6) | 21–24 | `technical-flaws.md` (TW-*) | |
| Summary table of flaws and solutions | 25 | `technical-flaws.md` summary | Teaching statements added under ID-COMPLEX-STEM |
| **Ch 4** Difficulty, discrimination, option analysis, group comparisons | 26–28 | `item-analysis.md` | |
| Five example analyses | 28–29 | `item-analysis.md` diagnostic patterns | Original numbers illustrate the same patterns |
| **Ch 5** Rules 1–5 | 33–35 | `writing-rules.md` | |
| **Ch 6** Choosing topics to test | 36 | `blueprint.md`, `cognitive-level.md` | |
| Recall vs application; Figures 1–2 | 36–38 | `cognitive-level.md` | |
| Guidelines for vignette content; vignette template | 39 | `scenarios.md` | Generalised to any domain |
| Shape of a good item | 40 | `item-anatomy.md` (Item shape) | |
| Patient chart / table format | 41–42 | `scenarios.md` (Data-table format) | |
| F-type sequential sets | 42–43 | `item-sets.md` | |
| Lead-in guidelines; with/without vignette data | 44–45 | `lead-in-bank.md`, `cognitive-level.md` | |
| Verbosity, window dressing, red herrings; real patients; unreliable history | 45 | `scenarios.md` | |
| Patient characteristics guidelines, flowchart, examples A–F | 46–50 | `people-in-scenarios.md` | Generalised to all people in scenarios |
| Structuring items to fit task competencies | 51–55 | `lead-in-bank.md` | Reorganised by cognitive task |
| **Ch 7** Media: rationale, types, selection | 56–59 | `media.md` | |
| Content areas suited to media | 60–61 | `media.md` | |
| Acquiring and creating media; metadata; sources | 62–63 | `media.md` | |
| Video tips | 64 | `media.md` | |
| Media accessibility | 65–66 | `media.md` | WCAG note added beyond the guide |
| **App A** Quick reference guide to item writing | 69 | `SKILL.md` (Write workflow) | Phase 3 |
| **App B** Sample lead-ins by task competency | 70–84 | `lead-in-bank.md` | Generalised; clinical-only lead-ins omitted |
| **App C** Retired formats (B, C, D, H, I, K, R) | 85–90 | `formats.md`, `item-sets.md` (R-type) | |
| **App D** Resources and further reading | 91–92 | `ATTRIBUTION.md` | Only sources this skill cites |

## Butler (2018): *Multiple-choice testing in education*

| Section | Pages | Covered in |
|---|---|---|
| Testing as learning; testing effect | 323–324 | `learning-and-feedback.md` |
| BP1 Avoid complex item types and answering procedures (incl. answer-until-correct, confidence-weighted) | 324–325 | `formats.md`, `learning-and-feedback.md`, `administration.md` |
| BP2 Items engaging specific cognitive processes; item shells; Bloom | 325–326 | `cognitive-level.md` (cognitive process tag), `lead-in-bank.md` |
| BP3 Avoid NOTA/AOTA (assessment and learning effects) | 326–327 | `technical-flaws.md` (ID-NOTA, X-AOTA), `learning-and-feedback.md` |
| BP4 Three plausible options; negative suggestion effect; distractors as other items' keys | 327–328 | `item-anatomy.md`, `learning-and-feedback.md`, X-OPTION-COUNT |
| BP5 Challenging but not too difficult; target p ≈ .77 (3 options) | 328–329 | `learning-and-feedback.md`, `item-analysis.md` |
| Bonus: feedback, including timing and motivation | 329 | `learning-and-feedback.md` |

## Xu, Kauer & Tupy (2016): *Multiple-choice questions: Tips for optimizing assessment*

| Section | Pages | Covered in |
|---|---|---|
| Effectiveness; shallower assessment; deeper thinking | 148–149 | `cognitive-level.md` |
| Ordered MC; confidence testing; discrete-option MC; "You are the teacher"; formula scoring | 149–150 | `ordered-mc.md`, `formats.md`, `administration.md` |
| Low-quality items (DiBattista & Kurzawa thresholds) | 150 | `item-analysis.md`, `administration.md` |
| Fairness | 150 | `administration.md`, `blueprint.md` |
| False knowledge; collaborative testing | 150–151 | `learning-and-feedback.md` |
| Feedback content, timing, techniques (self-correction, online, deferral, student feedback) | 151–152 | `learning-and-feedback.md`, `administration.md` |
| Efficiency; number of options | 152–153 | `item-anatomy.md`, `blueprint.md` |
| Negatives, NOTA, composites, AOTA, parallel options | 153 | `technical-flaws.md`, `formats.md` |
| Question order; answer-position randomisation | 153–154 | `administration.md`, X-KEY-POSITION |
| Cheating prevention and countermeasures | 154–155 | `administration.md` |

## Deliberately omitted (health-sciences specific)

- Clinical-only lead-ins (e.g., vaccines, pharmacotherapy, brain death, autopsy consent, involuntary admission). Their *cognitive patterns* are kept in `lead-in-bank.md`.
- USMLE-specific context.
- Clinical media specifics (radiographs, heart sounds, avatars). Generalised in `media.md`.

## Additions beyond the NBME guide

Labelled "Beyond the guide" or cited to Butler or Xu where they appear:
- `X-AOTA`, `X-KEY-POSITION`, `X-OPTION-COUNT`, `X-FEEDBACK-MISSING` checks
- configurable option count (default 4; 3 offered as a research-backed alternative) (`item-anatomy.md`)
- required per-option feedback and a purpose-based distractor policy (`learning-and-feedback.md`)
- ordered MC, offered to the user (`ordered-mc.md`)
- test administration guidance (`administration.md`)
- target difficulty and discrimination/nonfunctional thresholds (`item-analysis.md`); the drift threshold is a convention
- timing heuristic (`blueprint.md`)
- WCAG 2.2 AA note (`media.md`)
