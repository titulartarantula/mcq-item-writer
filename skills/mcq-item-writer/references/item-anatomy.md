# Anatomy of a one-best-answer item

Sources: NBME Item-Writing Guide, Ch 2 and Ch 6 [NBME pp. 11–16, 40]; Butler (2018); Xu, Kauer & Tupy (2016). Restated and generalised for any subject.

## Contents
- The two families of multiple-choice items
- Parts of an item
- Item shape
- The cover-the-options test
- Homogeneous options on a single dimension
- Distractors do not need to be wholly wrong
- How many options
- Checklist

## The two families of multiple-choice items

Every multiple-choice format belongs to one of two families [NBME p. 11]:

| Family | The learner must... | Examples |
|---|---|---|
| **One-best-answer** | pick the single most accurate option | standard single items; sets of items sharing one scenario |
| **True-false** | mark every option that is true (anywhere from one to all) | multiple true-false, "select all that apply", complex combinations (e.g. "1 and 3 only") |

**Default to one-best-answer.** NBME now uses only this family on its exams [NBME p. 14]. One-best-answer items test judgment and application better. They are also easier to write well, because a wrong option only has to be *less* correct than the key, not entirely false. See `formats.md` for when a true-false format is unavoidable and how to limit the damage.

## Parts of an item

```
┌──────────────────────────── STEM ────────────────────────────┐
│ Scenario (vignette): the situation, data, and context.       │
│ Lead-in: one closed question about the scenario.             │
└──────────────────────────────────────────────────────────────┘
  OPTION SET (default 4)                    FEEDBACK (every option)
   A. distractor                     →  why it is less correct; the misconception
   B. key  ← the single best answer  →  why it is best, using the scenario's evidence
   C. distractor                     →  why it is less correct; the misconception
   D. distractor                     →  why it is less correct; the misconception
```

- **Stem**: everything before the options. Usually a scenario followed by a lead-in [NBME p. 12].
- **Scenario / vignette**: a short case or situation that gives the question context. Required if you want to test application rather than recall (see `cognitive-level.md` and `scenarios.md`).
- **Lead-in**: the actual question. It should be one complete, closed question that ends in a question mark (see `lead-in-bank.md`).
- **Options**: the key plus the distractors. They should be short and uniform.
- **Key**: the single best answer.
- **Distractors**: plausible options that are less correct than the key.
- **Feedback**: a short explanation for **every** option, the key included, of why it is or isn't the best answer. Required for every item this skill writes (see `learning-and-feedback.md`). Teaching content goes here, never in the option text.

## Item shape

A well-built item is **top-heavy**: a substantial stem followed by a column of short, uniform options [NBME p. 40]. All the information needed to answer belongs in the stem. The options should never add new facts.

The stem should:
- focus on an important concept, not a trivial fact
- be answerable without seeing the options
- contain every fact the learner needs; options add no new data
- avoid being tricky or needlessly complex
- avoid negative phrasing ("EXCEPT", "NOT", "LEAST") in the lead-in

If an item has a one-line stem and five long, sentence-length options, it is upside down. The content that should be in the stem has leaked into the options, and the item is probably testing recall of isolated statements.

## The cover-the-options test

If the lead-in is properly focused, a knowledgeable learner should be able to **cover the options, read the stem, and state the answer** [NBME p. 13]. This is the main quality check for a lead-in.

- **Passes:** "...Which of the following is the most likely cause of the network outage?" An expert can name the cause before looking at the options.
- **Fails:** "Which of the following is true about subnet masks?" Nobody can answer this without the options, because the question doesn't actually ask anything.

To use it as a check, read only the stem and write your own answer. If you can't, or if several different answers would be equally reasonable, focus the lead-in.

## Homogeneous options on a single dimension

Every option should answer the lead-in **in the same way**, and all of them should fall along **one dimension** so they can be ranked from least to most correct [NBME p. 13]. If the lead-in asks for a cause, every option is a cause. If it asks for an action, every option is an action.

**Heterogeneous (flawed). Original example:**

> Which of the following is true about the 2008 financial crisis?
> A. It was caused mainly by a single bank
> B. It rarely affected European markets
> C. It may be linked to subprime mortgage lending
> D. It mostly affected small businesses
> E. It was resolved within six months

The options cover cause, geography, affected sectors, and duration. They can't be ranked along any one axis, so the learner is really judging five separate true/false statements.

**Homogeneous (revised):**

> A regional bank holds a large portfolio of adjustable-rate mortgages issued to borrowers with low credit scores. Interest rates rise sharply over 18 months. Which of the following is the most likely immediate effect on the bank's balance sheet?
> A. Decrease in deposit liabilities
> B. Increase in loan-loss provisions*
> C. Increase in retained earnings
> D. Increase in cash reserves

Every option is now a balance-sheet effect, and the options can be ranked from least to most likely.

## Distractors do not need to be wholly wrong

In a one-best-answer item, the distractors can be partly correct. They only need to be **less correct than the key** along the same dimension [NBME pp. 12, 14]. This is a major advantage over true-false formats, where every statement must be absolutely true or absolutely false.

The test: content experts would all agree on which option is best, even if they think some distractors are defensible.

## How many options

**This skill's default: 4 options (the key plus 3 plausible distractors). The user can choose a different number.** The choice is stored as `bank.defaults.options_per_item`.

The sources differ on this:
- **NBME convention:** one key plus three to seven distractors, so most published items have four or five options [NBME p. 12]. Four options is also what most learners and LMS question banks expect.
- **Research favouring 3:** a meta-analysis of 80 years of studies (Rodriguez, 2005) concluded that **three options** give the best balance of psychometric quality and testing time. A classroom study found no loss of reliability or difficulty when items were cut from five options to three [Butler p. 327; Xu pp. 152–153].
- **Efficiency:** learners answer three-option items about 5 seconds faster, so a test can cover more content in the same time [Xu p. 153].
- **Learning:** fewer options mean less wrong information on screen and fewer chances to pick it up (the negative suggestion effect) [Butler p. 327]. See `learning-and-feedback.md`.
- **Guessing:** with 4 options, a blind guess succeeds 25% of the time, against 33% with 3.

Choosing a count. Use the user's choice if they give one. Otherwise use 4, and mention 3 as an option when it fits:

| Choose... | When |
|---|---|
| **4** (default) | most quizzes and tests; when three plausible distractors exist; when matching an existing bank or LMS convention |
| **3** | `purpose: learning` and limiting exposure to wrong information matters; time-limited tests that need more items; topics with only two genuinely plausible distractors |
| **5** | only on request, matching an existing exam's format, and only if four distractors are genuinely plausible |
| **Ordered MC** | one option per level in the confirmed progression (see `ordered-mc.md`) |

Rules:
- **Never pad.** A filler option is worse than one fewer option. It cues savvy learners and wastes reading time [NBME p. 22] (see `technical-flaws.md`, TW-EXHAUSTIVE). If you can't find enough plausible distractors for the bank's count, write fewer and record `option_count_reason`. Butler notes three options are fine when a third distractor would be weak, and even two beats a filler option [Butler p. 327]. Tell the user about any two-option item, because guessing becomes much easier.
- What matters is that **every distractor works**. After delivery, a distractor almost nobody chose is a candidate for replacement (see `item-analysis.md`).

## Checklist

- [ ] One-best-answer format (or a documented reason for using a true-false format)
- [ ] Stem contains a scenario plus a single closed lead-in ending in "?"
- [ ] Passes the cover-the-options test
- [ ] All options are the same kind of thing and can be ranked along one dimension
- [ ] Options are short; no new information appears only in the options
- [ ] Exactly one option is clearly best, and experts would agree
- [ ] Every distractor is plausible to a learner who doesn't know the material
- [ ] Option count matches the bank setting (default 4), or a reason is recorded; no filler
- [ ] Every option, the key included, has feedback explaining why it is or isn't best
