# Anatomy of a one-best-answer item

Source: NBME Item-Writing Guide, Ch 2 and Ch 6 [NBME pp. 11–16, 40]. Restated and generalised for any subject.

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
  OPTION SET
   A. distractor
   B. key  ← the single best answer
   C. distractor
   D. distractor
   E. distractor
```

- **Stem**: everything before the options. Usually a scenario followed by a lead-in [NBME p. 12].
- **Scenario / vignette**: a short case or situation that gives the question context. Required if you want to test application rather than recall (see `cognitive-level.md` and `scenarios.md`).
- **Lead-in**: the actual question. It should be one complete, closed question that ends in a question mark (see `lead-in-bank.md`).
- **Options**: the key plus the distractors. They should be short and uniform.
- **Key**: the single best answer.
- **Distractors**: plausible options that are less correct than the key.

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
> B. Increase in loan-loss provisions
> C. Increase in retained earnings
> D. Decrease in regulatory capital requirements
> E. Increase in cash reserves

Every option is now a balance-sheet effect, and the options can be ranked from least to most likely.

## Distractors do not need to be wholly wrong

In a one-best-answer item, the distractors can be partly correct. They only need to be **less correct than the key** along the same dimension [NBME pp. 12, 14]. This is a major advantage over true-false formats, where every statement must be absolutely true or absolutely false.

The test: content experts would all agree on which option is best, even if they think some distractors are defensible.

## How many options

One-best-answer items have one key and **three to seven distractors** [NBME p. 12]. Most published items have four or five options in total. What matters is whether each distractor is plausible, not how many there are. Never add an implausible option just to reach five. Filler options cue savvy learners and waste reading time [NBME p. 22] (see `technical-flaws.md`, TW-EXHAUSTIVE).

> Beyond the guide: research summarised by Haladyna, Downing & Rodriguez (2002) suggests that three well-functioning options often perform as well as four or five. If you cannot write a third or fourth plausible distractor, use fewer options rather than adding filler.

## Checklist

- [ ] One-best-answer format (or a documented reason for using a true-false format)
- [ ] Stem contains a scenario plus a single closed lead-in ending in "?"
- [ ] Passes the cover-the-options test
- [ ] All options are the same kind of thing and can be ranked along one dimension
- [ ] Options are short; no new information appears only in the options
- [ ] Exactly one option is clearly best, and experts would agree
- [ ] Every distractor is plausible to a learner who doesn't know the material
