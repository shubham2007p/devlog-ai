# PROMPT_EVALUATION.md

## Purpose

Measure AI output quality.

Prevent hallucinations.

Ensure consistent content generation.

---

# Evaluation Categories

1. Factual Accuracy
2. Evidence Coverage
3. Tone
4. Readability
5. Consistency

---

# Evaluation Checklist

## Factual Accuracy

Question

Can every statement be traced to evidence?

---

Pass

100%

---

Fail

Any invented claim.

---

# Evidence Coverage

Question

Did the output include all major activities?

---

Pass

All major concepts represented.

---

Fail

Important learning omitted.

---

# Learning Validation

Question

Did AI claim learning that never occurred?

---

Pass

No invented learning.

---

Fail

Any unsupported learning.

---

# Achievement Validation

Question

Did AI invent achievements?

---

Pass

No invented achievements.

---

Fail Examples

"Mastered"

"Deep expertise"

"Completed project"

when unsupported.

---

# Tone Evaluation

LinkedIn

Professional

Reflective

Honest

---

X

Short

Technical

Direct

---

Summary

Objective

Journal Style

---

# Readability

Question

Can user understand within 30 seconds?

---

Pass

Clear.

---

Fail

Overly verbose.

---

# Hallucination Score

0

No hallucinations

Excellent

---

1

Minor wording issue

Acceptable

---

2

Unsupported assumption

Needs review

---

3

Fabricated learning

Failure

---

4

Fabricated achievement

Failure

---

# Regression Testing

Monthly evaluation.

Use same evidence.

Generate output.

Compare:

Facts

Tone

Coverage

Consistency

---

# Prompt Change Rules

Before releasing:

Test 10 historical logs.

---

Required Metrics

Accuracy

95%+

---

Hallucination Rate

0%

---

Coverage

90%+

---

# Success Criteria

Output is accepted if:

✓ Evidence-backed

✓ Accurate

✓ Readable

✓ No hallucinations

✓ User recognizes the day

Otherwise regenerate.
