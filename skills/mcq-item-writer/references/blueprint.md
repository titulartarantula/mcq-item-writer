# Blueprinting: deciding what to test

Source: NBME Item-Writing Guide, Ch 1, Ch 5 Rule 1, Ch 6 [NBME pp. 9–10, 33, 36]. Generalised.

## Contents
- Why tests need a blueprint
- Purposes of testing
- What material to test
- Building a blueprint
- How many items
- Blueprint output format (for this skill)

## Why tests need a blueprint

A test is a sample. Scores are used to draw **inferences** about the learner's ability across a wider domain than the items themselves [NBME p. 9]. That only works if:
- **The sample represents the domain.** A "general IT support" exam made up only of networking items gives a biased estimate of general competence.
- **The sample is large enough.** Too few items give imprecise, unreliable scores.

Testing time is limited. Every item spent on one topic is time not spent on another, so the allocation has to reflect each topic's importance [NBME p. 9].

## Purposes of testing

[NBME p. 10]
- Show learners what is important. Learners study what they think the test values.
- Motivate study.
- Find gaps that need remediation or further learning.
- Assign grades or make progression decisions.
- Find where instruction could improve.

The purpose determines both the content and how much psychometric rigour is needed [NBME pp. 10, 36]:
- **Higher stakes** (grades, progression, certification, decisions based on the test alone): need high reliability **and** documented evidence that content matches the intended inferences (the blueprint *is* that evidence).
- **Lower stakes** (one input among many, formative feedback): need less evidence, but reliability and validity still matter.

## What material to test

[NBME p. 10]
- Align items with the course objectives or competency framework (curricular alignment).
- Weight important topics more heavily, decided **in advance**.
- Allocate testing time in proportion to that importance.
- Make the spread of items representative of the instructional goals.
- For competency or certification exams, test what a newly competent practitioner must be able to do. That may include things a particular course didn't teach [NBME p. 36].

## Building a blueprint

Use two dimensions [NBME p. 33]:
1. **Content**: topics, units, or objectives.
2. **Task**: the cognitive task (see the categories in `lead-in-bank.md`: explain, gather information, interpret, classify, predict, prevent, act, communicate...).

Steps:
1. List the objectives or topics. Give each a weight (percentage of the test) based on importance. Time spent in instruction is a reasonable starting proxy, but importance is what should drive it.
2. Choose the task categories relevant to the domain and level. Novice courses lean on explain/classify/interpret. Professional exams lean on act/prevent/prioritise.
3. Distribute the total item count across the grid. Not every cell needs items.
4. Set the cognitive-level mix (recall versus application) from the stakes (see `cognitive-level.md`).
5. Pass each cell to item writing as an assignment: content × task × number × level.

## How many items

- High-stakes written exams usually need **100 or more items** for reproducible scores [NBME p. 9].
- Classroom summative tests: as many as testing time allows. Longer tests are more reliable.
- Formative checks: short is fine. Each item gives feedback, but the total score is not reliable enough for decisions about individuals.

> Beyond the guide: a common planning figure is about 1 minute per short recall item and 1.5–2 minutes per scenario-based application item.

## Blueprint output format (for this skill)

```json
{
  "blueprint": {
    "title": "Intro Project Management: Unit 2 summative",
    "purpose": "summative",
    "stakes": "medium",
    "learner_level": "first-year undergraduate",
    "total_items": 40,
    "time_minutes": 70,
    "cognitive_mix": {"application": 0.8, "recall": 0.2},
    "content_weights": {"Scope management": 0.25, "Scheduling": 0.30, "Risk": 0.30, "Communication": 0.15},
    "cells": [
      {"content": "Scheduling", "task": "interpret-data", "n": 4, "objective_ids": ["PM2.3"]},
      {"content": "Risk", "task": "choose-action", "n": 5, "objective_ids": ["PM2.5", "PM2.6"]}
    ]
  }
}
```
