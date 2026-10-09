# Item analysis: interpreting response data

Sources: NBME Item-Writing Guide, Ch 4 [NBME pp. 26–29]; Butler (2018); Xu, Kauer & Tupy (2016). The worked patterns below are original illustrations of the guide's interpretive rules. Thresholds marked "beyond the guide" come from the cited research or common convention, not from NBME.

## Contents
- The four standard analyses
- Difficulty (p-value)
- Discrimination (item–total correlation)
- Option (distractor) analysis
- Group comparisons
- Diagnostic patterns
- Decision rules for this skill
- Cautions

## The four standard analyses

Run these **before final scores are released** [NBME p. 26]:
1. Item difficulty
2. Item discrimination
3. Option analysis
4. Comparison across groups of learners

## Difficulty (p-value)

**p** = the proportion of learners who answered correctly (0–1 or 0–100%). Choose one scale and use it consistently [NBME p. 26]. A higher p means an easier item.

- The real value of p comes from **comparing it with what the writer expected**. Was the item about as hard as intended?
- Items with **p > .95** (very easy) or **p < .30** (very hard) tell you little about the group as a whole, and may mean the content doesn't match the learners' level [NBME p. 26].
- Clusters of extreme p-values in one topic can mean the topic was fully mastered, or not taught at all.
- A good test covers a **range** of difficulties as well as a range of topics.
- **Target difficulty** *(beyond the guide)*: discrimination tends to peak when difficulty is somewhat easier than halfway between chance and 100%, which is **p ≈ .77 for 3-option items** (Lord, 1952, via [Butler p. 328]). The general rule is to aim a little above (1/k + 1) / 2, where k is the number of options. For 4-option items that suggests about .70–.75 (our approximation). A target suits learning items too, because learners benefit most when they usually succeed (see `learning-and-feedback.md`). Report each item's p alongside the target.

## Discrimination (item–total correlation)

Discrimination is the correlation between getting the item right and the total test score, using the **point-biserial** or **biserial** correlation, from −1 to +1 [NBME pp. 26–27]. The total score can include or exclude the item. Excluding it (the "corrected" item–total) avoids inflating the value on short tests.

| Value | Meaning |
|---|---|
| Large positive | Learners who got the item right also did well overall. **Desirable.** |
| Near zero | The item adds little information for ranking learners |
| Negative | Weaker learners got it right more often than stronger ones. **Problem.** |

Causes of near-zero or negative discrimination [NBME p. 27]:
- the item measures something different from the rest of the test
- a flaw that weaker learners exploit, or that forces everyone to guess
- **a miskey.** A miskeyed item usually shows a very low p **and** negative discrimination

> Beyond the guide: an audit of 1,198 classroom items treated item–total correlations below **.20** as unsatisfactory, and these were among the most common problems (DiBattista & Kurzawa, 2011, via [Xu p. 150]). Treat .20 as a prompt for review, not an automatic rejection.

## Option (distractor) analysis

Always look at how every option performed [NBME p. 27]:
- **Option chosen by almost nobody** → implausible, or ruled out by a structural flaw. Rewrite it.
  > Beyond the guide: a distractor chosen by **under 5%** of learners is treated as nonfunctional. This was the single most common flaw in the classroom audit above (DiBattista & Kurzawa, 2011, via [Xu p. 150]). With 3- or 4-option items, every nonfunctional distractor removes a large share of the item's choices, so replace it promptly.
- **A distractor chosen somewhat more often than expected** → there may be two defensible answers.
- **A distractor chosen more often than the key** → probably miskeyed.
- **Distractor more popular among weaker learners than stronger ones** → working as intended.
- **Distractor more popular among stronger learners** → it may be defensible. Review the content.
- Watch for **whole tests** where many distractors are rarely chosen. That points to weak distractor writing overall.

## Group comparisons

**Within-item, by performance group** [NBME p. 27]:
- **High/Low split**: the top and bottom 50%, or more informatively the top and bottom **27%** (Kelley, 1939), usually rounded to 25%.
- With large numbers of learners, use quartiles or quintiles.
- Difficulty and discrimination are usually computed on the whole group. **Option analysis is most informative when broken down by High/Low.**

**Across groups** [NBME pp. 27–28]:
- Compare cohorts, sections, or years on the same items, ideally within performance bands.
- A **sharp change over time** in an item's p or discrimination can mean the item has been **exposed** (shared among learners), its content is **out of date**, or the topic is **no longer taught**.

## Diagnostic patterns

Original illustrations of the five patterns the guide describes [NBME pp. 28–29]. Values are percentages choosing each option (* = key). The High and Low groups are the top and bottom 25%.

**1. Miskey**
```
        A    B*   C    D    E
High    2    1   92    3    2
Low    18    8   49   17    8
p = .03   disc = −.20
```
Almost nobody, and almost no strong learner, chose the key. C behaves like a correct answer. → **Have a subject-matter expert verify. The key is almost certainly C.** Rekeying should give a good p and positive discrimination.

**2. Healthy item with weak distractors**
```
        A    B    C*   D    E
High    0    1   88    6    5
Low     1    0   57   27   15
p = .73   disc = +.31
```
Good difficulty and discrimination. A and B are almost never chosen. → **Keep the item. Consider rewriting A and B for future use**, and note that changing them may shift difficulty and discrimination unpredictably.

**3. Hard item, possibly two answers**
```
        A    B    C*   D    E
High   42    2   51    3    2
Low    21   16   22   23   18
p = .35   disc = +.29
```
Strong learners are split between A and C. → **A subject-matter expert must confirm that A is clearly wrong.** If the item was meant to be easier, look for structural flaws. If it was meant to be hard and A is definitely wrong, score it as is.

**4. Hard item, healthy guessing pattern**
```
        A    B    C*   D    E
High   17   11   52   16    4
Low    25   23   22   24    6
p = .35   disc = +.29
```
Same key statistics as pattern 3, but weaker learners spread across the distractors, and each distractor attracts more weak than strong learners. → **Probably fine.** Review A, B, and D for clarity only if the item wasn't meant to be hard.

**5. Two correct answers**
```
        A    B    C    D*   E
High    8   55    4   31    2
Low    22   33   12   30    3
p = .31   disc = −.04
```
Both groups prefer B over the key, and B pulls in strong learners even more than weak ones. The key doesn't separate the groups at all. → **Don't score until a subject-matter expert reviews it.** Something in the stem or options makes B defensible even to strong learners.

## Decision rules for this skill

`scripts/analyze_responses.py` (Analyze mode) applies these flags. A flag means "review this item", not "reject it automatically".

| Flag | Condition |
|---|---|
| `POSSIBLE_MISKEY` | a distractor chosen by more of the High group than the key, **and** discrimination < 0 |
| `POSSIBLE_TWO_ANSWERS` | a distractor chosen by ≥ 30% of the High group *(threshold beyond the guide)* |
| `NEGATIVE_DISCRIMINATION` | discrimination < 0 |
| `LOW_DISCRIMINATION` | 0 ≤ discrimination < .20 *(DiBattista & Kurzawa, 2011)* |
| `TOO_EASY` | p > .95 |
| `TOO_HARD` | p < .30 |
| `NONFUNCTIONAL_DISTRACTOR` | distractor chosen by < 5% of all learners *(DiBattista & Kurzawa, 2011)* |
| `REVERSE_DISTRACTOR` | distractor chosen by more High than Low learners |
| `DRIFT` | change in p of more than .15 against an earlier administration *(beyond the guide)* |

## Cautions

- Small groups (fewer than about 30 learners) give unstable statistics. Report them with a caution and lean on content review instead.
- Revising distractors changes item statistics in ways that are hard to predict [NBME p. 28]. Treat a revised item as a new item.
- Statistics point to problems. **A subject-matter expert decides** whether to rekey, revise, drop, or keep.
- Use the results to improve the bank. The wrong answers learners actually choose often make good future distractors [Xu p. 150], and learners' comments on items surface ambiguity the statistics miss [Xu p. 152].
