# Five rules for writing one-best-answer items

Sources: NBME Item-Writing Guide, Ch 5 [NBME pp. 33–35], with distractor and feedback guidance from Butler (2018) and Xu, Kauer & Tupy (2016). Restated and generalised for any subject. Each rule is followed by a description of how to apply it.

## Contents
- Rule 1: Test an important concept
- Rule 2: Test application, not isolated recall
- Rule 3: Write a focused, closed, clear lead-in
- Rule 4: Make options homogeneous and plausible
- Rule 5: Review for technical flaws
- Recommended writing sequence
- Final review questions

---

## Rule 1: Aim every item at an important concept (the "testing point")

Before writing anything, decide what the item is meant to show the learner can do. The topic normally comes from a **blueprint**: a grid of content areas against tasks, with a target number of items in each cell [NBME p. 33].

Example blueprint for an introductory project-management course:

| Content ↓ / Task → | Identify cause | Choose next action | Interpret data | Predict outcome |
|---|---|---|---|---|
| Scope management | 2 | 3 | 1 | 1 |
| Scheduling | 1 | 2 | 3 | 2 |
| Risk management | 2 | 3 | 1 | 2 |
| Stakeholder communication | 1 | 3 | 0 | 1 |

**How to apply:**
- Write the testing point as one sentence before drafting, e.g. "The learner can recognise scope creep from a change-request log and choose the correct control response."
- If no blueprint exists, build one from the learning objectives first (see SKILL.md, Blueprint mode).
- Spend items where the objectives place weight. Testing time per topic should reflect the topic's importance [NBME p. 10].

## Rule 2: Test the use of knowledge, not memory of an isolated fact

Without a scenario, an item almost always tests recall [NBME p. 33]. "Which of the following is used to reduce X?" tests memory of a list. Putting the same knowledge inside a realistic scenario makes the learner recognise the situation and decide what to do.

**How to apply:**
- Start from a realistic situation the learner might face, then ask them to make a decision about it.
- Use typical, representative cases. Real cases you remember are a good starting point, but they often contain unusual details that confuse learners. Simplify them toward the typical [NBME p. 33].
- **Match the scenario's complexity to the learner's level** [NBME pp. 33–34]:
  - *Novice*: classic, textbook presentation; key features clear; few distractions.
  - *Advanced*: atypical features, incidental details, and context the learner must judge relevant or irrelevant.
- When a cause has several possible origins, make the background details consistent with the cause you intend. A new employee and a 20-year veteran making the same error usually have different backstories.

See `cognitive-level.md` for when a recall item is acceptable.

## Rule 3: Write a closed, focused, unambiguous lead-in that can be answered from the stem alone

**How to apply:**
- Write the lead-in as a single complete question ending in "?" [NBME p. 34]: "Which of the following is the most appropriate next step?"
- Avoid open lead-ins that the options have to complete: "The best response is:" or "The cause of the outage is". Open lead-ins invite grammatical cues and fail the cover-the-options test.
- Use superlatives that create one best answer: *most likely*, *most appropriate*, *best*, *greatest risk*, *first priority*.
- Choose a lead-in template from `lead-in-bank.md` that matches the testing point.

## Rule 4: Make every option the same kind of thing, and believable

**Homogeneity** [NBME p. 34]: the lead-in determines what kind of thing each option is and what grammatical form it takes. If the lead-in asks for a *cause*, every option is a cause, and none of them are effects, tools, or people. Uniform options let the learner weigh them all with the same frame of mind.

**Plausibility** [NBME p. 34]: every distractor must attract learners who don't know the answer. If a distractor is obviously wrong in context, learners can eliminate it without the knowledge being tested.

**How to apply:**
1. Write the key first.
2. Generate distractors to fill the bank's option count (default 4 options, so **three** distractors; see `item-anatomy.md`) that are **the same kind of thing** as the key and that a partly informed learner might choose:
   - common misconceptions and typical errors at this learner level. Real learner errors from past tests or class work are the best source [Xu p. 150]
   - true statements that don't answer the question asked [Butler p. 327]
   - answers that would be right in a slightly different scenario
   - steps that are correct but out of sequence (right action, wrong time)
   - near neighbours in the same category

   When `purpose` is `learning` or `both`, prefer true-but-not-the-answer distractors and misconceptions the feedback will correct. Avoid inventing false "facts" learners might remember (see `learning-and-feedback.md`).
3. Sometimes the assignment supplies the key. If the blueprint cell is "identify the cause: phishing", phishing is the key, and the distractors are other plausible causes of the same symptoms [NBME pp. 34–35].
4. Write **feedback for every option**, the key included:
   - for each distractor: the misconception it represents, why a learner might choose it, and why it is less correct than the key
   - for the key: why it is best, using the scenario's evidence

   If you can't explain why someone would choose a distractor, replace it.
5. If the user chose **ordered MC** for this objective, build the options from the confirmed progression instead (see `ordered-mc.md`).
6. **Text shared by every option isn't tested.** Move it into the stem (NBME's fix for long options [NBME p. 25]). But if that shared step is part of what you want to test (e.g. "thank the student" in a correct response), make it *differ* across options so choosing it requires knowing it. For example, some options open by thanking the student and some don't, with the key's other elements also correct.

## Rule 5: Review every item for technical flaws

**How to apply** [NBME p. 35]:
- Put most of the text before the lead-in. Very little should follow it.
- Present the scenario in a logical order: who and where → presenting situation → background → observations or data → actions so far (see `scenarios.md`). A consistent template makes items easier to write and to read.
- Run the full flaw audit in `technical-flaws.md`, including the automated linter.
- Have a colleague or subject-matter expert review the item for content accuracy, clarity, and fit for the learner population.

---

## Recommended writing sequence

1. Testing point (Rule 1)
2. Scenario that sets up a decision (Rule 2)
3. Closed lead-in (Rule 3)
4. Key, then distractors, then feedback for every option (Rule 4)
5. Flaw audit, cover-the-options test, peer review (Rule 5)

## Final review questions

Ask these for every item [NBME p. 35]:

1. With the options removed, could a knowledgeable learner answer correctly?
2. Is there anything in the wording that could confuse a learner who knows the material?
3. Is there any clue that would help a test-savvy learner guess correctly without knowing the material?
4. Has someone other than the author checked the content, clarity, and fit for the learners?
