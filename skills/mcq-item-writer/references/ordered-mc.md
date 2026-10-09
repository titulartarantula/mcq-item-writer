# Ordered multiple-choice (diagnostic options)

Source: the format is from Briggs, Alonzo, Schwab & Wilson (2006), as summarised in [Xu p. 149]. The workflow and rules below were developed for this skill. All examples are original.

## Contents
- What it is
- When to offer it
- Workflow
- Example
- Feedback in ordered MC
- Scoring
- Export support
- Pitfalls

## What it is

A normal one-best-answer item in which **each option stands for a different level of understanding** of the same concept, from a common naive idea up to expert understanding. The learner sees an ordinary multiple-choice question. Behind the scenes, each option is tagged with its level.

What it adds over a standard item: a wrong answer tells you **how** the learner is thinking, not just that they are wrong. Across a class, the spread of levels shows where understanding stalls.

It is **not** a special item type for delivery. It imports as a standard single-answer question. Only the authoring, the metadata, and (optionally) the scoring are different.

## When to offer it

The skill **always asks the user**. It never switches to ordered MC on its own. Offer it when:
- the purpose is `learning` or `both` (diagnostic or formative), **and**
- the objective involves a concept where learners typically move through recognisable stages of misunderstanding. Examples: sampling and bias, causation versus correlation, force and motion, supply and demand, security threat models.

Prompt to show the user at intake (adapt as needed):

> For objective [X], I can write standard items or **ordered (diagnostic) items**. In ordered items, each wrong option represents a specific level of misunderstanding, so you can see *how* learners are thinking and the feedback can target that level. They import as normal multiple-choice questions, and in Moodle or QTI they can give partial credit. Would you like ordered items for this objective?

Don't offer it for: pure recall objectives, summative-only purposes where right/wrong scoring is required, or topics without a defensible progression.

## Workflow

1. **Define the progression** for the concept: one level per option. The default is 3 options, so 3 levels.
   - Level 1: a common naive conception
   - Level 2: partial understanding (some correct elements, one key gap)
   - Level 3: target understanding (the key)

   Base the levels on the source material, known misconceptions in the field, or the user's teaching experience. Show the progression to the user for confirmation before writing items.
2. **Write the scenario and lead-in** as usual. The lead-in must accept answers at every level ("Which of the following is the best evaluation...", "Which of the following best explains...").
3. **Write one option per level.** Each option must be what a learner at that level would actually choose. Keep the options parallel in form and similar in length.
4. **Write feedback for each level** (see below).
5. **Run the standard flaw audit.** Ordered options are especially prone to TW-KEY-STANDS-OUT and TW-CONVERGENCE (see Pitfalls).
6. **Record level tags and optional weights** in the item JSON.

## Example

Progression: *evaluating a survey estimate*
1. "A bigger sample means a more accurate estimate"
2. "Estimates vary by chance" (knows about sampling error, but not bias)
3. "How respondents were selected can bias the estimate in a predictable direction"

> A city council surveys residents about a proposed bike lane by posting a link on a local cycling club's social-media page. 2,400 people respond, and 81% support the lane. Which of the following is the best evaluation of the 81% figure?
>
> A. It is trustworthy because the sample is large *(level 1)*
> B. It may be off by a few points due to random sampling error *(level 2)*
> C. It likely overstates support because respondents selected themselves *(level 3, key)*

## Feedback in ordered MC

Each option's feedback **addresses the thinking at that level** and points to the next level up:

| Option | Feedback |
|---|---|
| A (level 1) | "A large sample reduces random error, but it can't fix *who* is in the sample. Here, everyone saw the link on a cycling club's page. Ask how respondents were chosen, not just how many there are." |
| B (level 2) | "Random sampling error is real, but it assumes respondents were picked at random. These respondents chose to respond after seeing a cycling club's post, so the error has a direction, not just a margin." |
| C (level 3) | "Correct. People who follow a cycling club and choose to answer are more likely to support bike lanes, so the 81% probably overstates support among all residents. A large sample doesn't remove this bias." |

## Scoring

Choose one with the user:
- **Right/wrong** (default). Score the key 1 and everything else 0. Use the level data for reporting only.
- **Partial credit.** Weight by level, e.g. 3 options → 100% / 50% / 0%. Use only for formative scoring, and tell learners in advance.

## Export support

| Format | Level tags | Partial credit |
|---|---|---|
| JSON (canonical) | ✓ `options[].level` | ✓ `options[].weight` |
| Moodle XML | in option feedback / tags | ✓ per-answer fraction |
| GIFT | in comments | ✓ `~%50%` syntax |
| QTI 2.1 | ✓ metadata | ✓ response mapping |
| QTI 1.2 | partial | ✓ varies by LMS |
| CSV | ✓ column | ✓ column |
| H5P | ✗ | ✗ (right/wrong only) |

## Pitfalls

- **The key stands out.** Higher-level ideas need more words. Trim every option to the same length and level of detail, and move any explanation into the feedback.
- **Convergence.** Options built as steps on one ladder can share words ("sampling", "error"). Vary the wording.
- **A low-level option nobody chooses.** If level 1 is a misconception that few learners at this stage actually hold, it becomes a nonfunctional distractor. Base the levels on real learner thinking.
- **An unconfirmed progression.** An invented progression gives misleading diagnostics. Get it confirmed by the user or a subject-matter expert.
