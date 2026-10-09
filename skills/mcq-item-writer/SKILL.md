---
name: mcq-item-writer
description: Write, review, and analyse one-best-answer multiple-choice questions (MCQs) using evidence-based item-writing rules (NBME Item-Writing Guide, plus research on learning from tests). Produces scenario-based items with 4 options by default (configurable), explanatory feedback on every option, a flaw audit, and LMS-ready exports (Moodle XML, GIFT, QTI, CSV, H5P). Use this skill whenever the user wants quiz, test, or exam questions; knowledge checks or assessments for an e-learning module, course, or training programme; a question bank; distractors or answer feedback; a critique or improvement of existing multiple-choice questions; item analysis of quiz results (difficulty, discrimination, distractor performance); or an exam blueprint, even if they never say "MCQ" or "item".
---

# MCQ item writer

Write multiple-choice items that measure what they claim to measure and teach while they do it. The rules come from the NBME Item-Writing Guide (Billings et al.), generalised to any subject, plus research on learning from tests (Butler, 2018; Xu, Kauer & Tupy, 2016). Every rule has a reason, given in the reference files. Use the reasons to make judgment calls the rules don't cover.

## Defaults that make this skill different

These are deliberate choices. Explain them to the user if they ask, but don't drop them silently.

- **One-best-answer format.** The learner picks the single best option, and distractors only need to be *less* correct. This tests judgment rather than trivia, and avoids the guess-the-writer's-intent problems of true/false and "select all" formats.
- **Scenario first.** Items put the learner in a realistic situation and ask for a decision. Without a scenario, an item almost always tests recall.
- **4 options by default** (key + 3 distractors), and the user can choose another number. Three is a well-supported alternative: research shows three plausible options measure as well as four, take less time, and expose learners to less wrong information. Whatever the count, never pad with a weak option to reach it. A filler option cues the answer and wastes the learner's time.
- **Feedback on every option, the key included.** Learners can come away believing a distractor they chose. Explanatory feedback is the main protection, and writing it is also the best check that the key is right.
- **No "none of the above", "all of the above", EXCEPT/NOT lead-ins, or combination formats** ("A and B only"). Each one either rewards test-taking tricks or adds difficulty unrelated to the content.

## Modes

Work out which mode the request needs, then read the listed references **before** starting. They are short and they contain the actual rules. The SKILL.md only gives the workflow.

| Mode | Use when the user... | Read first |
|---|---|---|
| **Write** | wants new items from objectives or content | `writing-rules.md`, `technical-flaws.md`, `learning-and-feedback.md`, `scenarios.md`; from `lead-in-bank.md` only the sections for the tasks you're testing |
| **Review** | gives existing items to check or improve | `technical-flaws.md`, `item-anatomy.md`, `formats.md`, `learning-and-feedback.md`; `lead-in-bank.md` sections when rewriting lead-ins |
| **Analyze** | has learner response data or item statistics | `item-analysis.md` |
| **Blueprint** | needs a test plan, or wants many items across many objectives | `blueprint.md`, `cognitive-level.md` |

Read these as the task requires:
- `cognitive-level.md` (recall vs application, Bloom tags)
- `item-sets.md` (case-based or sequential sets)
- `people-in-scenarios.md` (any scenario with people in it, which is most of them)
- `ordered-mc.md` (diagnostic items)
- `media.md` (images, video, audio)
- `administration.md` (whenever you deliver a quiz or test, not just loose items)
- `item-anatomy.md` (item structure basics)

All paths in this file are relative to this skill's own directory (the folder containing this SKILL.md), not the user's project. References are in `references/`. The output format is `assets/item.schema.json`, and `assets/example-bank.json` is a complete worked example. Read it before writing your first bank in a session.

---

## Intake

Collect a brief before writing. Calling projects (e-learning builds, course modules) often supply most of it up front. **Ask only for what's missing and actually blocks you.** Otherwise use the default and say which defaults you used.

| Field | Default if not given | Why it matters |
|---|---|---|
| Learning objectives | derive from the source content and show them to the user | Every item tests one objective |
| Source content | none: write from general knowledge **and flag every factual claim for expert review** | Items must be correct. Grounding is what makes them trustworthy |
| Learner level | ask; this one usually matters | Sets how typical or complex scenarios should be |
| `purpose`: assessment / learning / both | infer it: ungraded practice or a knowledge check → `learning`; graded quiz or test → `both`; certification or placement → `assessment`. If unclear, `both` | Distractor policy and feedback release |
| `assessment_type`: formative / summative | graded at any weight → `summative`; ungraded → `formative` | Recall/application mix |
| Stakes | `low` | Rigour of review; integrity advice |
| Number of items | 1–2 per objective | |
| Options per item | 4 (key + 3 distractors) | User's choice. Mention 3 as an option when `purpose` is `learning` or testing time is tight (see `item-anatomy.md`). Stored as `bank.defaults.options_per_item` |
| Platform / export format | JSON + Markdown review sheet | Which exporter to run. For Canvas use `--format canvas` (see Platform notes) |

**Offer ordered (diagnostic) MC** when `purpose` is `learning` or `both` **and** at least one objective covers a concept learners typically misunderstand in recognisable stages (e.g. correlation vs causation, sampling bias, supply and demand, threat models). Ask once per batch, naming the objectives that qualify, using the prompt in `ordered-mc.md`. Never switch to ordered MC without the user agreeing. If they accept, confirm the levels of understanding (the progression) with them before writing those items.

If the user asks for a discouraged format ("select all that apply", true/false, "A and B only", "let them try again until correct"), follow the handling table in `formats.md`: explain the problem in a sentence, offer the better alternative, and comply with warnings if they insist (except combination formats, which you convert).

---

## Talking to the user

The files carry the detail. The chat reply is for a busy teacher or designer deciding what to do next. Write it for them:

- **Plain language.** No flaw codes (ID-*, TW-*, X-*), schema field names, or page citations in the chat reply unless the user asks. Codes and citations belong in the review sheet and the JSON, where reviewers look things up.
- **Most important first.** For reviews and analyses, group findings as **Must fix** (wrong or doubtful key, two defensible answers, a question that can't be answered from its stem), **Should fix** (answer clues, confusing wording, weak distractors), and **Optional** (polish). One line per problem: which question, what's wrong, what to do.
- **Point to the files** rather than pasting long item text. Show at most one revised item inline as an example if it helps.
- **End with decisions only the user can make** (e.g. "Is Q4 meant to test equal sample sizes or normality?"), and the defaults you assumed.
- Aim for a reply that fits on one screen. If it doesn't, move detail into the review sheet.

---

## Write mode

For each item, in this order. The order matters: the stem and its answer come **before** the options, which is what makes the cover-the-options check real rather than a formality.

1. **Testing point.** One sentence: what a correct answer shows the learner can do. Choose the task category (`lead-in-bank.md`) and the Bloom level (`cognitive-level.md`). For summative items, prefer application. A recall item needs a recorded reason.

2. **Scenario.** A realistic situation that calls for the decision, with elements in template order (`scenarios.md`): who → where → situation → time frame → background → observations → data → actions so far. Pitch it at the learner's level. Include everything needed to reach the key and to make the distractors tempting. No red herrings. Apply `people-in-scenarios.md` to anyone in it.

3. **Lead-in.** One closed question ending in "?", adapted from `lead-in-bank.md`. No EXCEPT/NOT/LEAST.

4. **Answer from the stem alone.** Before writing any options, write the answer an expert would give from the stem alone (`audit.cover_the_options.stem_only_answer`). If you can't, or several answers are equally defensible, fix the scenario or lead-in now. This is the most important quality check.

5. **Key.** Make the stem-only answer the key, worded concisely.

6. **Distractors to fill the bank's option count** (three, for the default of 4), of the same kind as the key (all causes, all actions...), and plausible to a learner who doesn't know the material:
   - Sources: real misconceptions at this level, answers that would be right in a slightly different situation, right action at the wrong time, near neighbours, true statements that don't answer this question.
   - If `purpose` is `learning` or `both`, prefer true-but-not-the-answer distractors and misconceptions the feedback will correct. Don't invent false "facts" learners might remember.
   - If you genuinely can't find enough plausible distractors, write fewer options and set `option_count_reason`. Don't pad. The third distractor is usually the hardest, and the place where filler creeps in.
   - How close the distractors are to the key is the main control on difficulty. Aim for roughly 70–75% of the intended learners answering correctly (`learning-and-feedback.md`): close enough that the item requires the knowledge, not so close that experts would disagree.

7. **Feedback for every option.** Two to four sentences each, written to the learner, commenting on the answer and not the person:
   - **Key:** why it's best, citing the scenario's evidence.
   - **Distractor:** name the misconception (also record it in `misconception`), say why it's tempting, and say why it's less correct here.

   Explanations and teaching points go in the feedback, never in the option text, because a key padded with explanation stands out. Options should be comparable in length, not identical: a word or two of difference is fine, and meaning and readability come first.

8. **Options in order.** If they have a natural order (numbers, dates, scales, steps), arrange them that way and set `shuffle: false`. Otherwise set `shuffle: true`.

9. **Audit.** Once the batch is drafted, save the bank file and run the linter on it (below). Then do the judgment checks it can't do, item by item:
   - homogeneity
   - plausibility
   - one clearly best answer that experts would agree on
   - no clue that lets a test-savvy learner guess the answer

   Fix what you find. Record anything left unresolved in `audit.lint` / `audit.warnings`.

10. **Grounding.** Link the key and feedback to the source (`references`). Any claim not supported by supplied source material goes in `sme_review.claims_to_verify`, with `sme_review.required: true`. Never invent citations, statistics, guideline thresholds, or legal and regulatory specifics. Flag them instead.

**Sets.** For case-based or unfolding scenarios, follow `item-sets.md`:
- Keep the opening scenario and updates in the `sets` record.
- Set `navigation: "locked"` for sequential sets.
- Write each update so it implies the previous answer without giving away the next one.

**Batches.** Across a batch:
- vary scenarios, settings, people, and roles
- spread key positions across items with `shuffle: false`
- vary task types to match the blueprint
- avoid items that give away each other's answers

### The linter

```bash
python <skill-dir>/scripts/lint_items.py <bank.json>          # schema + automatable flaw checks
python <skill-dir>/scripts/lint_items.py <bank.json> --write  # also record findings in each item's audit.lint
```

It checks the schema and the automatable flaw codes in `technical-flaws.md`:
- ID-*: e.g. NOTA, vague terms, negative lead-ins, numeric option order and overlap
- TW-*: e.g. a/an grammar cues, absolute terms, key length, clang words, convergence
- X-*: option count against the bank setting, missing or thin feedback, key-position balance

Treat findings as prompts for judgment, not verdicts. A flagged repeated word may be harmless. If Python or the script isn't available, validate the bank against the schema as best you can, apply the "Detect" checks in `technical-flaws.md` by hand, and tell the user the automated checks didn't run.

---

## Review mode

Use this when the user supplies existing items in any format (pasted text, a document, an LMS export).

1. Convert each item to the schema as faithfully as possible, keeping the original wording in `notes`. Originals often won't validate (no feedback, open lead-ins). That's expected: for missing feedback write `(none in original): no feedback was written for this option.` so the linter reports it once per item. Save it as `<name>-original.items.json`, lint it, and treat the findings as your diagnosis. Put each item's diagnosis (flaw codes, source pages, what you changed) in the revised item's `notes`, so it appears in the review sheet. The revised bank is a separate file that must validate.
2. **Cover-the-options check first:** read each stem, answer it, *then* look at the options. Note mismatches.
3. Run the linter, then do the judgment checks from Write mode step 9.
4. Write the revised items as a validated bank (feedback on every option) and generate the review sheet. In the sheet, record each item's flaws with their code and source page from `technical-flaws.md` (e.g. `[NBME p. 23]`) and what changed.
5. **Check your own revisions** with the linter and the judgment checks. A revision must not add new problems: a key that's now the longest option, an open lead-in left in place, a distractor that could be argued correct, or a different testing point.
6. In the chat reply, follow "Talking to the user": Must fix / Should fix / Optional, plain language. Must fix covers, in this order:
   1. wrong or doubtful keys
   2. more than one defensible answer
   3. questions that can't be answered from the stem

   Don't bury a miskey under wording notes.
7. If many items share one flaw (e.g. all recall, or all keys in position C), say so once at batch level.

Respect the author's intent and content. Revise the item's form, but don't change *what* it tests unless the testing point itself is the problem, and then ask.

---

## Analyze mode

Use this when the user has response data from a delivered quiz.

```bash
python <skill-dir>/scripts/analyze_responses.py <responses.csv> --bank <bank.json> [--groups 27] [--format text|markdown|json] [--write]
```

The script computes:
- p (difficulty)
- corrected point-biserial (discrimination)
- High/Low option tables
- the flags in `item-analysis.md`: possible miskey, possible two answers, negative or low discrimination, too easy or too hard, nonfunctional or reverse distractors, drift

Run `--help` for the input formats it accepts (per-learner response matrix, or LMS item-analysis exports). If the user only has summary statistics, or the script isn't available, compute or interpret the statistics directly using `item-analysis.md`, and say which method you used.

Report flags as **prompts for expert review, never automatic verdicts**. For each flagged item:
- explain the pattern in plain language
- give the most likely cause
- recommend an action: rekey, accept both answers, revise distractor, rewrite, drop from scoring, or keep

**Regrades.** When an item looks miskeyed or has two defensible answers, show what each fix would do to last term's scores before anyone decides:

```bash
python <skill-dir>/scripts/analyze_responses.py <responses.csv> --key <keys> --rekey "Q4=D,Q11=B|D"
```

This reports, per item, how many learners would **gain and lose** a point, plus the mean and reliability before and after. Accepting both answers (`B|D`) never takes points away. Rekeying moves points between learners. Both directions matter to the instructor.

**Reshaping LMS exports.** The script reads one row per learner with a column per question (or one row per response). LMS exports such as Canvas's Student Analysis report usually have extra columns and question text in the headers. Reshape them first: keep a learner id plus one column per question, holding the chosen option letter. Tell the user what you dropped.

**Keep the data for next time.** If there's no bank, offer to save a minimal one (ids, keys, stats via `--write`) so next term's run can check for drift.

Warn about unstable statistics with fewer than about 30 learners. Point out that changing distractors creates a new item whose statistics start over. With `--write`, the statistics are stored in each item's `stats`, so the next run can check for drift.

---

## Blueprint mode

Use this when the user needs a test plan, or asks for many items across many objectives (blueprint first, then write against it).

Follow `blueprint.md`:
1. Weight the objectives by importance.
2. Choose task categories and Bloom levels.
3. Allocate items to a content × task grid.
4. Set the recall/application mix from `assessment_type`.
5. Mark cells where the user accepted ordered MC.
6. Run the fairness check.

Show the grid to the user for approval before writing items against it. It's much cheaper to adjust the plan than 40 items.

---

## Output

**Files.** Save to the user's chosen location, or to the current project if none is given:
- `<name>.items.json`: the bank, valid against `assets/item.schema.json`. This is the format other projects and the exporters read, so keep it complete.
- `<name>.review.md`: a human-readable review sheet for subject-matter experts and reviewers. Generate it with `export.py --format markdown` so it always matches the JSON. The template below shows what it contains.
- Exports, if requested:

```bash
python <skill-dir>/scripts/export.py <bank.json> --format moodle-xml|gift|qti21|qti12|csv|h5p|markdown [--out <path>] [--only-status approved]
```

The exporters carry feedback, shuffle flags, partial credit for ordered MC where the format supports it, and set order. Each run prints the format's limitations; pass them on to the user (e.g. H5P has no partial credit). Exports refuse a bank that doesn't validate, and warn when items are still drafts. `--only-status approved` exports only reviewed items. If the exporter isn't available, hand-write only the simple text formats (GIFT, CSV), and say the file hasn't been machine-checked. Don't hand-write QTI or H5P packages.

**Review sheet template:**

```markdown
# <Bank title>
Purpose: <purpose> · Type: <formative/summative> · Learners: <level> · Items: <n>

## <ITEM-ID> · <objective id> · <task> / <Bloom> · <format>
**Testing point:** ...

<scenario>
<data table, if any>

**<lead-in>**

| | Option | Feedback |
|---|---|---|
| A | ... | ... |
| **B ✓** | ... | ... |
| C | ... | ... |
| D | ... | ... |

Audit: cover-the-options ✓ · lint: <none | codes> · SME check: <claims or "none">
```

**Chat summary.** Follow "Talking to the user". Include:
- what you produced and where
- the defaults you assumed
- items needing expert verification, with the specific claims
- unresolved warnings
- the distribution of people and roles across the batch, if scenarios include people

**Administration note.** Whenever the output is a quiz, test, or bank (not just one or two loose items), include the administration note from `administration.md` in the review sheet and in the bank's `administration` field. Cover: what to tell learners, question order, shuffling, feedback release, attempts (one attempt plus feedback, not "try until correct"), integrity measures suited to the stakes and platform, and running item analysis afterwards. In the chat reply, give only the two or three settings the user must actually change.

---

## Platform notes

**Canvas** (Classic Quizzes and New Quizzes):
- Export with `--format canvas`. This builds a QTI 1.2 package and prints the import steps for both quiz engines. Pass the steps on to the user.
- Per-answer feedback shows **after the learner submits**, depending on the quiz's result-view settings. So for Canvas, release feedback at the end of the attempt. This overrides the "immediate" default in `learning-and-feedback.md`. Point the user to the setting, noting that labels vary by Canvas version: in Classic Quizzes, the options to let students see their quiz responses (and, if wanted, the correct answers); in New Quizzes, the **Restrict student result view** settings.
- Canvas ignores per-item shuffle. Spread key positions across A–D yourself (the linter checks this). Tell the user to turn on "Shuffle answers" unless the quiz has numeric or ordered options.
- Recommend **1 attempt** for knowledge checks. Canvas practice quizzes often default to unlimited attempts with answers shown, which becomes try-until-correct.
- Canvas multiple-choice questions can't give partial credit, so ordered-MC partial credit is lost. Mention it if ordered MC was used.

**Moodle**: use `moodle-xml` (keeps per-item shuffle and partial credit), or `gift` for quick text editing. **Brightspace / D2L**: `qti21`, or `qti12` if that fails. **H5P**: experimental (see the exporter's notes).

Untested imports: say so. The exporters produce schema-valid files, but each LMS has quirks. Suggest a test import into a sandbox course before the real one.

---

## Calling this skill from another project

Other projects (e-learning module builders, course generators) can invoke this skill with a brief and consume the JSON. A minimal brief:

```yaml
objectives: ["LO1: ...", "LO2: ..."]
source: path/to/module-content.md
learner_level: "new customer-service hires"
purpose: both            # assessment | learning | both
assessment_type: formative
items_per_objective: 2
options_per_item: 4       # default; 3 is a good choice for learning-focused checks
export: [canvas]           # or gift, moodle-xml, qti21, h5p, csv
out_dir: build/assessment/
```

With a complete brief, don't stop to ask questions. Use defaults, record assumptions in the chat summary, and still **offer** ordered MC in the summary rather than applying it. Items stay at `status: "draft"` until a human reviews them. The skill writes drafts, and people approve them.
