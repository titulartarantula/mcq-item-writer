# Assembling and administering a test

Sources: Xu, Kauer & Tupy (2016) [Xu p. N]; Butler (2018) [Butler p. N]; NBME Item-Writing Guide [NBME p. N]. Findings are summarised in our own words.

**When this applies:** whenever the skill produces more than a handful of items for use together (a quiz, test, or item bank), it adds an **administration note** to the output covering the relevant sections below. Keep it short and specific to the user's context (LMS, stakes, in-person or online).

## Contents
- Fairness and communicating expectations
- Question order
- Option order and shuffling
- Integrity: in person and online
- Scoring and guessing
- Item banks, rotation, and exposure
- After the test
- Administration note template

---

## Fairness and communicating expectations

[Xu p. 150]
- **Clear items**, **broad coverage**, and **alignment with the syllabus** make a test feel fair. Learners who see a test as fair study the material rather than the test.
- Learners tend to assume MCQs test memorised facts, and they study shallowly when they expect MCQs [Xu pp. 149–150]. **Tell learners in advance what kind of thinking the items require.** For example: "Most questions give you a workplace scenario and ask you to choose the best next action."
- Share sample items written to the same standard.
- Cover the blueprint (see `blueprint.md`). Don't test only a small part of what was taught.

## Question order

[Xu p. 153]
- **Easy-to-hard ordering** doesn't change actual scores, but learners *feel* they did better. Hard-first ordering lowers their confidence without lowering their scores.
- **Order that follows the course sequence** (questions in the order topics were taught) produced higher scores than random or grouped-by-chapter order. Following the learning sequence seems to help recall.
- **Sequential sets** (see `item-sets.md`) must stay together, in order, with backward navigation locked.

Recommendation:
- **Formative or practice:** follow the course sequence. Optionally open with an easier item to build confidence.
- **Summative, in person:** course sequence, or multiple forms with different orders (see Integrity).
- **Summative, online:** randomise question order **within sections**, keep sets intact, and shuffle options as described below.

## Option order and shuffling

The sources pull in different directions:
- **Logical order** within an item (numeric, chronological, alphabetical for short terms) reduces reading effort and avoids illogical sequences [NBME p. 18].
- **Randomise answer positions**, because writers put keys in the middle and guessers favour middle positions [Xu pp. 153–154].

**This skill's rule:** each item has a `shuffle` flag.

| Options are... | `shuffle` | Why |
|---|---|---|
| Numbers, ranges, dates, ordered scales, steps in sequence | `false`. Author them in logical order | Shuffling would create an illogical order and ID-NUMERIC problems |
| Ordered-MC levels | either. Level is stored as a tag, not a position | |
| Anything else | `true` | Removes key-position bias; supports integrity |

When `shuffle` is `false`, the linter checks that key positions are balanced across the set (X-KEY-POSITION). Exporters set the LMS's per-question shuffle setting from this flag.

## Integrity: in person and online

[Xu pp. 154–155]

**In person**
- **Alternate forms** with **both questions and options** rearranged. Rearranging questions alone did not significantly reduce copying.
- Alternating or assigned seating. A seating record also allows copying to be investigated afterwards.

**Online**
- Draw each learner's questions from a **larger bank**, and randomise question and option order.
- **Hold back feedback and answer keys until the quiz has closed for everyone** [Xu p. 152].
- Set time limits and access windows.
- Lockdown browsers where policy allows. One study found no difference in scores between lockdown-browser online exams and in-person exams.

**For all settings**
- A clear **academic integrity policy**. **Honor codes** and signed integrity agreements reduce cheating, and longer, formal codes with consequences work better.
- **Change items between terms** as resources allow. Rotating part of a large bank is more realistic than rewriting everything.

For bank planning: an online summative quiz drawing *n* items per learner should have a bank of **several times n** items per blueprint cell. The exact multiple is a local decision.

## Scoring and guessing

- **Number-right scoring** is the default.
- **Formula scoring** (subtracting a fraction of wrong answers to correct for guessing) discourages guessing [Xu p. 150]. It adds complexity and penalises learners who are more reluctant to take risks. Use it only if the context requires it, and tell learners in advance.
- **Partial credit** is available for ordered MC (see `ordered-mc.md`) and self-correction (see `learning-and-feedback.md`).
- **Confidence-weighted testing** (learners rate their confidence and scoring combines confidence with correctness) is promising for both measurement and learning [Butler p. 325; Xu pp. 149–150]. But personality affects how confident people say they are, at least until they've practised, and most LMSs need workarounds. This skill documents it but doesn't generate it.
- **Discrete-option MC** (options shown one at a time, each judged correct or not) [Xu p. 150] needs platform support. Documented only.

## Item banks, rotation, and exposure

- Record per item: when it was first used, how many times it has been used, and which forms or courses used it.
- Watch for **drift**: a sharp rise in p across administrations can mean the item has been shared among learners [NBME pp. 27–28] (see `item-analysis.md`).
- Retire or revise items that are exposed. Revised items count as new items.

## After the test

- **Run an item analysis before releasing final scores** [NBME p. 26; Xu p. 150]. See `item-analysis.md`. A large audit of classroom tests found flawed items were common, mostly distractors almost nobody chose and items with weak discrimination (DiBattista & Kurzawa, 2011, via [Xu p. 150]).
- **Ask learners to comment on items** [Xu p. 152]. Their comments surface ambiguity.
- **Release feedback** according to the plan in `learning-and-feedback.md`.
- **Common wrong answers become future distractors.** Learners' real errors make the best distractors [Xu p. 150].

## Administration note template

Include this with any quiz, test, or bank the skill produces. Fill in only what applies.

```markdown
### Administration notes
- **Tell learners:** [what kind of thinking the items require; sample item]
- **Order:** [course sequence / randomised within sections]; sets [list] stay in order with back-navigation locked
- **Option shuffling:** on for all items except [IDs with shuffle=false: numeric/ordered]
- **Feedback release:** [immediate / end of attempt / after quiz closes]
- **Integrity:** [bank size per cell, alternate forms, time limits, integrity statement]
- **Scoring:** [number-right / partial credit for ordered items IDs]
- **After delivery:** run item analysis before finalising grades; collect learner comments on items
```
