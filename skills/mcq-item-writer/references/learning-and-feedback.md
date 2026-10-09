# Items that teach: learning effects, distractors, and feedback

Sources: Butler (2018), *J Applied Research in Memory and Cognition* 7:323–331 [Butler p. N]; Xu, Kauer & Tupy (2016), *Scholarship of Teaching and Learning in Psychology* 2:147–158 [Xu p. N]. Findings are summarised in our own words. See the papers for the primary studies.

The NBME guide treats items as **measurement**. In e-learning and formative use, items are also **learning activities**. Answering them changes what learners remember. This file covers what that means for writing and delivering items.

## Contents
- Taking the test is itself learning
- The risk: learning the distractors
- Distractor policy by purpose
- Feedback is required, for every option
- Writing good feedback
- When to release feedback
- Difficulty: the target, not just the limits
- Answering procedures that don't help
- Other ways to improve learning from tests

---

## Taking the test is itself learning

Retrieving an answer strengthens memory and can deepen understanding. This is the **testing effect**. Classroom studies from middle school to university show that multiple-choice quizzing improves later exam performance and transfer [Butler p. 324; Xu p. 148]. Quizzing can also strengthen related material that wasn't directly tested, and can bring back knowledge the learner had lost access to [Butler p. 324].

So for an item used for learning, the question is not only "does it measure the objective?" but also **"does answering it make the learner think the way the objective requires?"** [Butler pp. 325–326]. Design the thinking each item demands as carefully as any other learning activity.

## The risk: learning the distractors

Multiple-choice items show learners wrong information. Learners can later recall a distractor as true. This is the **negative suggestion effect**, and the risk is greatest when the learner **chose** that distractor [Butler p. 327]. Familiarity alone can make a false statement feel true [Xu pp. 150–151].

What makes it worse [Butler pp. 327–328]:
- **More options** mean more wrong information shown, and more chances to pick it.
- **Low success rates.** When learners mostly fail, they learn more errors than facts.
- **No feedback.**

What reduces it:
- **Feedback.** This is the biggest single factor (below).
- Moderate-to-high success rates (see Difficulty below).
- **Collaborative testing**, where learners answer in pairs or groups, reduced false learning and improved retention weeks later [Xu p. 151].

## Distractor policy by purpose

Every item records a `purpose`: `assessment`, `learning`, or `both`.

| | `assessment` | `learning` / `both` |
|---|---|---|
| Plausible misconceptions | ✓ | ✓, **and the feedback must name and correct the misconception** |
| True statements that don't answer the question asked [Butler p. 327] | ✓ | ✓ **preferred**: learners see only accurate information |
| Correct answers to *other* items in the set | ⚠ can cue answers across items [Butler pp. 327–328] | ⚠ can help learning when rejected, but can create wrong associations when chosen. Use sparingly |
| Invented false "facts" | acceptable if plausible | **avoid**: learners may remember them as true |
| "None of the above" as the key | avoid (ID-NOTA) | **never**: the learner never sees the correct answer [Butler p. 326] |
| "All of the above" | avoid (X-AOTA) | avoid. It may help learning when it is the key, but it still gives answers away [Butler pp. 326–327] |

## Feedback is required, for every option

**Every item this skill writes includes feedback for every option, the key as well as each distractor.** This applies whatever the purpose:
- For learning, feedback is the main defence against learning false information. It strengthens the testing effect and reduces the negative effects [Butler p. 329].
- Feedback on the **key** matters too. It helps learners who got it right without confidence keep that answer [Butler p. 329].
- For summative use, feedback may be held back or never shown, but writing it is still the best check that the key is defensible and each distractor is truly less correct. If you can't explain why a distractor is wrong, it may not be wrong.

Required fields per option:

```json
{
  "label": "B",
  "text": "Disconnect the laptop from the network",
  "correct": true,
  "feedback": "Correct. Isolating the affected machine first stops the malware from spreading to other shared drives. Cleanup and restoration come after it is contained.",
  "misconception": null
}
```

For a distractor, `misconception` names the error the option represents (e.g. "restoring from backup before the threat is contained"). The feedback addresses that error. In ordered MC (see `ordered-mc.md`), the option's level indicates what to say.

## Writing good feedback

- **Explain, don't just mark.** Explanatory feedback beats right/wrong verification [Xu p. 151]. Say *why* the answer is right or wrong, using the evidence in the scenario.
- **Comment on the response, not the learner.** Keep it supportive and non-judgemental [Xu p. 151]: "This option treats the symptom rather than the cause...", not "You didn't read carefully."
- **Name the misconception** a wrong option represents, and give the correct reasoning in its place.
- **Point back to the scenario.** "The 20-minute timeline and the README files indicate..." This models how an expert reads the evidence.
- **Teaching content belongs here.** Explanations, caveats, and links to resources go in feedback, never in the option text (TW-KEY-STANDS-OUT) [NBME p. 23].
- **Keep it short.** Two to four sentences per option. Add a link or reference to the source material if the learner needs more.
- **Don't reveal other items' answers** when the item is part of a set.

## When to release feedback

The evidence is mixed, and the right choice depends on context:
- In experiments, a **short delay** (end of the test rather than after each item) can beat immediate feedback, because it spaces the learning [Butler p. 329; Xu p. 151].
- Reviews of classroom studies find **immediate** feedback generally better in real quiz settings, with delay helping more as items get **harder** [Xu p. 151].
- Delayed feedback only works if learners actually look at it. Engagement falls with delay, so **require or reward** reviewing it [Butler p. 329].

Default release settings this skill recommends:

| Context | Release feedback |
|---|---|
| Short knowledge check or practice quiz | immediately after each item, where the platform allows it. Some platforms (e.g. Canvas) only show per-answer feedback after submission; there, use end of attempt |
| Scenario or application items, practice test | at the end of the attempt, with review required (e.g. a short reflection or a gated next step) |
| Graded online quiz | after the quiz **closes for everyone**, to protect item security [Xu p. 152] |
| High-stakes summative | per policy; usually score report only, with feedback reserved for remediation |

## Difficulty: the target, not just the limits

NBME flags items outside p = .30–.95 [NBME p. 26]. A **target** is more useful when writing.

- Discrimination tends to peak when item difficulty is **somewhat easier than halfway between chance and 100%** (Lord, 1952, via [Butler p. 328]).
- The halfway point is (1/k + 1) / 2, where k is the number of options. For **3 options**, Butler gives **p ≈ .77** [Butler p. 328]. For the **4-option** default the halfway point is .625, so aim around **.70–.75**. That range is our approximation of Lord's rule, not a published figure. In both cases the target works out to roughly 70–77% of attempts correct.
- The same target suits learning. Learners benefit when they succeed most of the time, but items that are too easy let them succeed without thinking [Butler pp. 328–329].
- **Productive difficulty** comes from the thinking the objective requires: options that are conceptually close, or distractors built from real misconceptions. **Unproductive difficulty** comes from tricks, ambiguity, and technical flaws (see `technical-flaws.md`) [Butler pp. 328–329].
- When learning is the goal and items are challenging, **support the learner and give feedback** [Butler p. 329].

## Answering procedures that don't help

- **Answer-until-correct** (keep trying until right, sometimes with partial credit) taught no more than a **single attempt followed by immediate feedback**. It also lowers reliability, because learners use different strategies [Butler p. 325]. Recommended e-learning pattern: **one attempt, then explanatory feedback**, rather than "Try again".
- **Complex formats** (combinations, "A and B but not C", multiple-response) produce more varied thinking across learners. Fewer of them engage in the reasoning the writer intended [Butler pp. 324–325]. See `formats.md`.

## Other ways to improve learning from tests

From [Xu pp. 151–152]:
- **Self-correction.** Learners submit answers, take the questions away, and resubmit corrections. Full credit if correct both times, partial credit if corrected, none if wrong both times. Students who could self-correct a midterm did better on the final.
- **Resubmission after feedback** on low-stakes online quizzes.
- **Collaborative testing** (see above).
- **Ask learners for feedback on the items.** Their comments surface ambiguity you missed.
