# Technical item flaws

Source: NBME Item-Writing Guide, Ch 3 [NBME pp. 17–25]. Restated and generalised for any subject. All examples are original.

Technical flaws come in two kinds [NBME p. 17]:

1. **Irrelevant difficulty (ID).** The item is hard for reasons unrelated to the testing point, so it confuses everyone. This adds construct-irrelevant variance to scores.
2. **Testwise cues (TW).** The item helps savvy test-takers guess correctly from test-taking skill alone.

A learner's chance of answering correctly should depend only on what they know about the topic. Flaws should neither lower that chance through bad wording nor raise it through test-taking tricks.

Each flaw has a stable **code**. The linter (`scripts/lint_items.py`) and review reports use these codes. The **Detect** line describes what to look for, and marks which checks can be automated.

## Contents
- Irrelevant-difficulty flaws: ID-LONG-OPTIONS, ID-NUMERIC, ID-VAGUE, ID-NOTA, ID-NONPARALLEL, ID-COMPLEX-STEM, ID-NEGATIVE
- Testwise flaws: TW-GRAMMAR, TW-EXHAUSTIVE, TW-ABSOLUTE, TW-KEY-STANDS-OUT, TW-CLANG, TW-CONVERGENCE
- Additional checks beyond the guide: X-AOTA, X-KEY-POSITION
- Summary table

---

## Irrelevant-difficulty flaws

### ID-LONG-OPTIONS: Long or complex options  [NBME p. 17]
Long options increase reading load, so the item starts measuring reading speed instead of knowledge. The flaw is about the **options**. A long scenario is fine when the testing point is interpreting and synthesising information.

*Flawed:*
> Under the organisation's data-retention policy, which of the following must happen before customer records are deleted?
> A. Legal review, a documented retention-period check, manager sign-off, and a backup verified within 30 days
> B. Confirmation that the retention period has passed, approval from the data owner, and a check for any legal hold
> C. A formal request from the customer, review by compliance, and written confirmation sent to the customer within 14 days

*Fix:* move the shared content into the stem, make the options parallel, and shorten them. Usually this means turning the item into a scenario with a focused lead-in, such as "Which of the following must be confirmed first?", followed by short, single-concept options.

**Detect:** option word count above about 15 words, or a mean option length that is large compared with the stem *(automatable)*.

### ID-NUMERIC: Numeric data presented inconsistently  [NBME p. 18]
Sort numeric options from lowest to highest and express them all the same way: either every option is a point value or every option is a range. Mixed formats confuse learners. Overlapping ranges create more than one defensible answer, and when one option contains another, test-savvy learners can eliminate options.

*Flawed:*
> ...what proportion of the survey respondents are likely to be repeat customers?
> A. Under 10%  B. 10–25%  C. More than 40%  D. 55%  E. 70%

C contains D and E, and ranges are mixed with point values.

*Fix:* use non-overlapping ranges *or* single values, in ascending order. If the exact value is debatable, ask for a minimum or maximum ("Which of the following is the lowest value that...?").

**Detect:** options parse as numbers or ranges; check sort order, mixed formats, and overlap *(automatable)*.

### ID-VAGUE: Vague frequency terms  [NBME p. 18]
Words like *often*, *usually*, *frequently*, *rarely*, *sometimes*, and *commonly* mean different things to different readers, including experts. Different readings lead to more than one correct answer, or to options that can't be ranked. The same applies to imprecise phrases like *is associated with*, *is useful for*, and *is important* [NBME p. 14].

*Flawed:*
> Remote-work policies:
> A. usually reduce office costs
> B. often lower team cohesion
> C. frequently improve retention

*Fix:* turn the item into a scenario with a closed lead-in that asks for a specific consequence, cause, or action.

**Detect:** match a word list against stem and options *(automatable)*.

### ID-NOTA: "None of the above"  [NBME p. 19]
When options call for judgment, "None of the above" forces the learner to compare each listed option against every option that *wasn't* listed. A knowledgeable learner may think of something better than the intended key and choose "None of the above" for that reason. In effect, the learner is judging each option as true or false against an unlisted universe, rather than ranking the listed options.

*Fix:* replace it with a specific option that commits to a decision, e.g. "No change to the current process is needed", "No further action is required at this time", or "Continue monitoring".

**Detect:** match "none of the above", "none of these", and "none of the options" *(automatable)*.

### ID-NONPARALLEL: Nonparallel options  [NBME p. 19]
Options with different grammatical structures (one a noun phrase, one a full sentence, one a calculation, one a conclusion) take longer to read, and the learner has to change mental frame for each one.

*Fix:* rewrite the lead-in so it asks for one kind of answer (for example, "Which of the following is the main limitation of these results?"), then edit every option to answer it in the same form.

**Detect:** options start with different parts of speech, mix fragments with full sentences, or vary in sentence count *(partly automatable; confirm by judgment)*.

### ID-COMPLEX-STEM: Tricky or needlessly complicated stems  [NBME p. 20]
Stems that require extra processing unrelated to the testing point, such as ranking Roman-numeral lists or decoding combinations, add difficulty that has nothing to do with the content.

*Flawed:*
> Rank the following backup strategies from fastest to slowest recovery time:
> I. Full nightly backup  II. Incremental hourly  III. Continuous replication  IV. Weekly full + daily differential
> A. III, II, I, IV  B. III, I, II, IV  C. II, III, I, IV  D. I, III, II, IV

*Fix:* ask about a single element ("Which of the following strategies provides the fastest recovery after the failure described?") and put the elements themselves in the options.

Also avoid **teaching statements** in the stem: explanations included to instruct rather than to inform the decision [NBME p. 25].

**Detect:** Roman-numeral lists, "rank/arrange/order the following", or options that are combinations of other elements *(automatable)*.

### ID-NEGATIVE: Negatively phrased lead-ins  [NBME pp. 21, 40]
"All of the following EXCEPT", "Which is NOT", and "LEAST likely" ask the learner to find the *least* correct option. When most items on a test are phrased positively, learners miss the negative word even if it is bold or capitalised.

*Fix:* rewrite with a positive structure. If the true statements could build a scenario, use them as scenario details and ask a positive question.

**Detect:** EXCEPT, NOT, LEAST, FALSE, or "incorrect" in the lead-in *(automatable)*.

---

## Testwise flaws

### TW-GRAMMAR: Grammatical cues  [NBME p. 21]
Some options don't follow grammatically from the stem: a/an mismatches, singular/plural disagreement, or tense mismatches. These options can be eliminated on grammar alone. The cause is usually that the writer polished the key and neglected the distractors.

*Flawed:*
> ...The most likely cause of the error is an:
> A. incorrect cell reference*  B. circular formula  C. hidden row  D. locked worksheet

*Fix:* use closed lead-ins (a full question ending in "?"). Make all options singular or all plural. Read every option directly after the stem to confirm it fits.

**Detect:** stem ends in "a"/"an"/"the"/":" with no "?"; a/an versus option initial sound; singular/plural mismatch *(automatable)*.

### TW-EXHAUSTIVE: Grouped or collectively exhaustive options  [NBME p. 22]
If a subset of options covers every possible outcome (increase / decrease / no change), the key must be in that subset, and the other options can be ignored. This often happens when the writer pads the option set to reach five.

*Flawed:*
> Raising the price of the product by 10% will most likely cause unit sales to:
> A. decrease  B. increase  C. require a new marketing plan  D. remain unchanged  E. shift to online channels

A, B, and D are exhaustive. C and E don't answer the question asked.

*Fix:* replace at least one option in the exhaustive subset, and avoid creating an obvious opposite pair while revising. Ideally, move to a richer outcome dimension, such as specific magnitudes or specific downstream effects.

**Detect:** option sets containing increase/decrease/no-change, more/less/same, or similar triads; a true/false pair of opposites *(partly automatable)*.

### TW-ABSOLUTE: Absolute terms  [NBME p. 22]
Test-savvy learners eliminate options with *always*, *never*, *all*, *none*, *only*, or *completely*, because absolute claims are rarely true. Hedged options (*can*, *may*, *possibly*) look safer. The flaw usually appears when the verb sits in the options instead of the lead-in.

*Fix:* remove the absolutes, put the verb in the lead-in, and use short, homogeneous options.

**Detect:** match absolute and hedge word lists in options *(automatable)*.

### TW-KEY-STANDS-OUT: Correct option stands out  [NBME p. 23]
The key is longer, more detailed, more qualified, or the only compound option. Writers who are also teachers tend to pack the key with caveats and explanation.

*Fix:* make all options similar in length and detail. Move teaching content to the **rationale/feedback** field, not the option text.

**Detect:** key length is 1.5 times the mean distractor length or more; key is the only option with a comma, "and", or parentheses *(automatable)*.

### TW-CLANG: Word repetition ("clang clue")  [NBME p. 23]
A distinctive word or word root from the stem reappears in the key. The repetition can be **etymological** too: a stem that mentions "heat" paired with a key starting with "thermo-".

*Flawed:*
> An employee says the new software feels "cluttered" and that they cannot find the features they need. Which of the following usability problems best describes this complaint?
> A. Inconsistent terminology  B. Poor error recovery  C. Slow response time  D. Visual clutter*  E. Weak affordances

*Fix:* change the repeated word in the stem or in the option, or use it in every option.

**Detect:** content words or stems shared between stem and key but absent from the distractors *(automatable)*.

### TW-CONVERGENCE: Convergence  [NBME p. 24]
The key shares the most elements with the other options, so counting repeated terms points to it. This happens when the writer starts from the key and builds distractors as permutations of it. The flaw can also be conceptual: if three of five options come from the same category, savvy learners eliminate the two outliers.

*Flawed:*
> Data is most secure in transit when sent:
> A. unencrypted, over a public network
> B. encrypted, over a private network*
> C. encrypted, over a public network
> D. hashed, over a private network
> E. hashed, over a public network

"Encrypted" and "private" each appear more often than their alternatives, and B is the only option that has both.

*Fix:* balance how often each term or category appears across options, or rebuild the option set along one dimension.

**Detect:** tally shared tokens or categories across options and flag a key that holds the most frequent value in every component *(automatable)*.

---

## Additional checks beyond the guide

These checks are not in the NBME guide. They come from the wider item-writing literature (Haladyna, Downing & Rodriguez, 2002) and are standard practice.

### X-AOTA: "All of the above"
If a learner can identify two options as correct, "All of the above" must be the key. If they can identify one option as wrong, it can't be. Either way, partial knowledge earns the point. Replace it with a single best option.

**Detect:** match "all of the above" or "all of these" *(automatable)*.

### X-KEY-POSITION: Unbalanced key positions across a set
Writers tend to place keys in the middle positions (B, C). Across a set of items, keys should be spread roughly evenly over positions. Within an item, options should be in a logical order: alphabetical for single words or short phrases, numeric for numbers, chronological for steps.

**Detect:** key-position distribution across the item set; option order checks *(automatable)*.

---

## Summary table

| Code | Flaw | Fix | Auto |
|---|---|---|---|
| ID-LONG-OPTIONS | Long or complex options | Move shared text to the stem; make parallel; shorten | ✓ |
| ID-NUMERIC | Inconsistent numeric options | One format, ascending, no overlap; ask for minimum/maximum | ✓ |
| ID-VAGUE | Vague frequency or association terms | Remove; ask a closed, specific question | ✓ |
| ID-NOTA | "None of the above" | Replace with a specific "no action / no change" option | ✓ |
| ID-NONPARALLEL | Nonparallel options | Refocus lead-in; give options the same form | ~ |
| ID-COMPLEX-STEM | Tricky or complex stem; teaching statements | Ask about a single element; keep only needed content | ✓ |
| ID-NEGATIVE | EXCEPT / NOT / LEAST lead-in | Rewrite positively | ✓ |
| TW-GRAMMAR | Grammatical cue | Closed lead-in; consistent number and article | ✓ |
| TW-EXHAUSTIVE | Collectively exhaustive subset | Replace an option in the subset; avoid opposite pairs | ~ |
| TW-ABSOLUTE | Always / never / only | Remove; put the verb in the lead-in | ✓ |
| TW-KEY-STANDS-OUT | Key longer or more detailed | Equalise; move teaching text to the rationale | ✓ |
| TW-CLANG | Stem word repeated in key | Change the word, or use it in all options | ✓ |
| TW-CONVERGENCE | Key shares the most elements | Balance terms and categories | ✓ |
| X-AOTA | "All of the above" | Replace with a single best option | ✓ |
| X-KEY-POSITION | Key position bias / illogical order | Spread keys; order options logically | ✓ |

✓ = mostly automatable · ~ = linter flags candidates, judgment confirms
