# Item formats: what to use and what to avoid

Sources: NBME Item-Writing Guide, Ch 2 and Appendix C [NBME pp. 11–16, 85–90]; Butler (2018); Xu, Kauer & Tupy (2016). Generalised. Examples are original.

## Contents
- Default: one-best-answer
- When a true-false format is requested
- Rules if you must write true-false items
- Retired formats and their problems
- Variants and alternative formats
- Handling format requests in this skill

## Default: one-best-answer

Use one-best-answer items (single items, or sets as described in `item-sets.md`) unless there is a specific reason not to [NBME pp. 14, 85]. Reasons:
- Learners don't have to guess what the writer meant by "true".
- Distractors only need to be *less correct*, not entirely false, so the format can test judgment and application.
- One scenario can support several lead-ins (diagnose, act, predict), which makes efficient item sets.
- Using one format consistently means writers focus on content rather than format, test-takers get one familiar format, and review is simpler [NBME p. 85].
- Complex formats **don't measure higher-order thinking any better**. They make guessing easier, lower reliability, are hard to write, and are often thrown out at review. They also lead learners to answer in different ways, so fewer of them do the reasoning the writer intended, which undermines both measurement and learning [Butler pp. 324–325].

## When a true-false format is requested

True-false formats include "select all that apply", multiple true-false, and "A, B, both, or neither". In these, learners must decide **how true** an option has to be before marking it true. That judgment often has more to do with guessing the writer's intent than with subject knowledge [NBME p. 15]. Reviewers rewrite or discard true-false items much more often than one-best-answer items. Many problems only appear at review, and reviewers sometimes change the key [NBME p. 16]. To avoid ambiguity, writers also tend to fall back on isolated facts, which pushes the item toward recall.

**Recommendation:** convert the request into one-best-answer items if you can. A "select all the risk factors present" item can usually become "Which of the following factors in this situation most increased the risk of X?"

## Rules if you must write true-false items

[NBME pp. 15–16]
- Wording of the stem and every option must leave no room for interpretation. Avoid "is associated with", "may", "could", "usually", and "often".
- The lead-in must be closed and focused.
- **Every option must be absolutely true or absolutely false.** No shades of grey. Content experts must agree on every option without asking for more context.
- Options must be homogeneous (all the same kind of thing) and of similar length.
- Number the options (1, 2, 3...) rather than lettering them, by convention.

*Acceptable (original):*
> Which of the following are prime numbers?
> 1. 21  2. 23  3. 27  4. 29

Every option is unambiguously true or false and all options are the same type.

*Flawed (original):*
> True statements about remote work include:
> 1. It is a form of flexible working
> 2. It usually improves productivity
> 3. Remote employees are less engaged
> 4. Adoption is about 30%

Options 2–4 depend on context (which workers? measured how? where? when?), so experts would disagree.

## Retired formats and their problems

NBME no longer uses these formats [NBME pp. 85–90]. Some still appear in course exams. If a user asks for one, explain the risk and offer a one-best-answer alternative.

| Format | Structure | Main problems |
|---|---|---|
| **B-type** (simple matching) | short option list shared by several items; each option can be the answer to several items, or to none | often no lead-in, so the actual question is unclear |
| **C-type** (A / B / both / neither) | each item is matched to A, B, both, or neither | really multiple true-false; learners must guess how strongly something must apply to count as "both" |
| **D-type** (complex matching) | categories plus items, and the learner also picks the item that doesn't belong | confusing instructions; hard to write; discriminates poorly |
| **H-type** (quantitative comparison) | is A greater than B, B greater than A, or are they about equal? | unclear how big a difference counts as "greater" |
| **I-type** (covariation) | do the two quantities increase together, move in opposite directions, or vary independently? | only three options make guessing easy; tends toward minor details |
| **K-type** (complex true-false) | lettered combinations of numbered statements (e.g. "A = 1 and 3", "B = 2 and 4", "E = all") | absolute facts only, so no judgment; heavy load from the answer code; the combinations cue the answer and reduce discrimination |
| **R-type** (extended matching) | long shared option list (up to ~26) with a themed set of items | many nonfunctional distractors; high reading load. Usable only if each item has at least 3 plausible distractors in the list |
| **X-type** (simple true-false) | each option judged true or false | all the true-false family problems above |

## Variants and alternative formats

These came from the research literature, not NBME. Each one is **offered or documented**, never applied silently.

| Format | What it is | Delivery | This skill |
|---|---|---|---|
| **Ordered MC** | one-best-answer item whose options represent levels of understanding (Briggs et al., 2006, via [Xu p. 149]) | standard single-answer question; optional partial credit | **Offered** to the user when the purpose is `learning` or `both` and the concept has a progression. See `ordered-mc.md` |
| **Confidence-weighted MC** | learner rates their confidence; scoring combines confidence with correctness [Butler p. 325; Xu pp. 149–150] | needs a confidence rating per item and custom scoring; few LMSs support it natively | Documented only (see `administration.md`) |
| **Discrete-option MC** | options shown one at a time, each judged correct or not [Xu p. 150] | needs dedicated platform support | Documented only |
| **"You are the teacher"** | learner reads a short answer and chooses how many errors it contains [Xu p. 150] | standard single-answer question | Can be written on request as a one-best-answer item with numeric options (0, 1, 2, 3 or more) and `shuffle: false` |
| **Answer-until-correct** | learner keeps trying until right | LMS "multiple attempts" setting | **Advise against.** It taught no more than one attempt with feedback, and it lowers reliability [Butler p. 325] |

## Handling format requests in this skill

| Request | Response |
|---|---|
| "Multiple choice", "MCQ", "quiz questions" | One-best-answer items (default) |
| "Case-based", "scenario sets", "branching" | Sequential set (see `item-sets.md`); navigation locked |
| "Select all that apply", "multiple response" | Explain the risk; offer a one-best-answer conversion. If the user insists, follow the true-false rules above and set `format: "multiple-response"` with a warning in the review notes |
| "True/false" | Same as above |
| "Matching" | Offer extended matching only with a clear theme and lead-in, and check that each item has at least 3 plausible distractors |
| K-type, "1 and 3 only" combinations, "A and B but not C" | Decline the format, explain why [Butler pp. 324–325; Xu p. 153], and convert to one-best-answer |
| "Diagnostic" questions, "find out what they misunderstand" | Offer ordered MC (see `ordered-mc.md`) |
| "Let them try again until they get it" | Recommend one attempt plus explanatory feedback instead (see `learning-and-feedback.md`) |
