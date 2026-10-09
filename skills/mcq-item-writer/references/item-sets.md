# Item sets and shared-stimulus formats

Source: NBME Item-Writing Guide, Ch 2, Ch 6, Appendix C [NBME pp. 11, 42–43, 85, 90]. Generalised for any subject. Examples are original.

## Contents
- Set types
- Sequential (unfolding) sets
- Rules for sequential sets
- Example sequential set
- Shared-stimulus sets (navigable)
- Extended matching (use with care)
- E-learning notes

## Set types

| Type | Guide name | Structure | Can the learner go back? |
|---|---|---|---|
| **Single item** | A-type | one stem, one lead-in, 4+ options | n/a |
| **Sequential set** | F-type | 2–3 items on a scenario that unfolds over time | **No.** Later items reveal earlier answers |
| **Shared-stimulus set** | G-type | 2–3 items on the same content or stimulus | Yes |

[NBME pp. 11, 85]

## Sequential (unfolding) sets

A scenario develops over time. Each item adds new information and asks for a decision at that point [NBME p. 42]. This mirrors real work: assess, act, see what happens, act again.

Because later items reveal what happened next, and so imply the answers to earlier items, **learners must not be able to go back** to change earlier answers. In an LMS, this means sequential navigation with no backtracking for the set. Record this as `navigation: "locked"` in the set metadata.

## Rules for sequential sets

[NBME p. 42]

1. **Make the opening scenario rich enough** to support every item in the set.
2. **Move time forward and add new information** with each item. If a learner may have gone down a wrong path, bring them back to a common starting point ("The analyst isolated the laptop from the network...").
3. **Imply the previous answer without turning the next item into recall.** The new information should reveal what was done, but the next item must still require new reasoning, not just repeat a fact the update gave away.

Also:
- Each item in the set must pass the flaw audit on its own.
- Avoid **dependency chains** where getting item 1 wrong guarantees getting item 2 wrong. The reset in rule 2 prevents this.
- Two or three items per set is typical. Longer sets give too much weight to one scenario in the blueprint.

## Example sequential set

**Opening scenario**
> A help-desk analyst at a 200-person accounting firm receives a call at 09:40 from an employee who cannot open files on a shared drive. File names now end in ".lck", and a README text file has appeared in each folder. The employee says they clicked a link in an email that appeared to come from the payroll provider at about 09:15. The employee's laptop is still switched on at their desk.

**Item 1**
> Which of the following is the most appropriate immediate action?
> A. Delete the README files from the shared drive
> B. Disconnect the employee's laptop from the network*
> C. Restore the shared drive from last night's backup
> D. Run a full antivirus scan on the laptop
> E. Send a firm-wide email warning about the phishing message

**Update**
> The laptop is disconnected. Twenty minutes later, two more employees on a different floor report the same file extensions on a different shared drive. Neither of them received the payroll email.

**Item 2**
> Which of the following is the most likely explanation for these new reports?
> A. A second phishing email reached other employees
> B. The backup system corrupted the file names
> C. The malware spread before the laptop was isolated*
> D. The shared drives developed a hardware fault
> E. The two employees opened the README files

Item 2 implies that Item 1's answer (isolate the laptop) was carried out, but it doesn't repeat that fact as a clue. It asks for a new inference. The options are clauses of similar length, so the key doesn't stand out.

## Shared-stimulus sets (navigable)

Several items draw on one stimulus: a dataset, a document excerpt, a diagram, or a case. Learners may move freely between them [NBME p. 11]. Rules:
- Each item must test a **different** testing point.
- No item may reveal the answer to another.
- Each item should be answerable from the stimulus plus its own lead-in.

## Extended matching (use with care)

Extended matching uses one long option list (often 8–26 options) shared by several items with a common theme. The guide's R-type is an example [NBME p. 90]. It has been retired from NBME exams but can still be useful in course assessments. Known risks:
- **Nonfunctional distractors.** Many options in the long list are implausible for any given item. After writing the items, check that **each item has at least three plausible distractors** in the shared list [NBME p. 90].
- **Reading load** grows with the length of the list.
- Every item in the set must have a clear theme and a closed lead-in ("For each situation described, select the most likely cause"). Older matching formats without lead-ins often left the actual question unclear [NBME p. 86].

## E-learning notes

- Sequential sets map onto branching scenarios in authoring tools. Use the update text as the feedback or next screen, but **lock backward navigation**.
- Shared-stimulus sets map onto "case study" or "question group" features in an LMS.
- When importing, keep the set's order and its navigation setting. Many LMS randomisation features would break a sequential set.
