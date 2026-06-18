# MVP_ACCEPTANCE.md

## Purpose

Defines when the MVP is considered complete.

A feature is not finished because code exists.

A feature is finished when acceptance criteria pass.

---

# MVP Definition

The user can:

1. Connect GitHub
2. Write learning notes
3. View timeline
4. Generate daily context
5. Generate drafts
6. Review drafts
7. Browse history

with less than 2 minutes of effort per day.

---

# Feature: GitHub Integration

Requirements

Receive push events.

Store commits.

Update timeline.

---

Pass Criteria

✓ Commit appears within 10 seconds

✓ Commit stored in database

✓ Evidence record created

✓ Timeline updated

---

Fail Criteria

✗ Commit missing

✗ Duplicate commit stored

✗ Webhook crashes

---

# Feature: Learning Notes

Requirements

User can add notes.

---

Pass Criteria

✓ Save note

✓ Edit note

✓ Delete note

✓ Note appears in timeline

---

Fail Criteria

✗ Data loss

✗ Timeline not updated

---

# Feature: Timeline

Requirements

Unified activity view.

---

Pass Criteria

✓ Commits displayed

✓ Notes displayed

✓ Sorted chronologically

✓ No duplicate events

---

Fail Criteria

✗ Incorrect order

✗ Missing events

---

# Feature: Daily Context

Requirements

Build context from evidence.

---

Pass Criteria

✓ Uses commits

✓ Uses notes

✓ Context generated successfully

---

Fail Criteria

✗ Missing evidence

✗ Empty context

---

# Feature: AI Generation

Requirements

Generate:

Summary

LinkedIn

X

---

Pass Criteria

✓ Summary created

✓ LinkedIn created

✓ X created

✓ Stored in database

---

Fail Criteria

✗ Hallucinated content

✗ Missing output

✗ Generation crash

---

# Feature: Draft Review

Requirements

View drafts.

---

Pass Criteria

✓ Copy works

✓ Edit works

✓ Regenerate works

✓ Approve works

---

Fail Criteria

✗ Draft cannot be edited

✗ Draft cannot be copied

---

# Feature: Archive

Requirements

Historical access.

---

Pass Criteria

✓ Search works

✓ Open previous day

✓ View drafts

✓ View timeline

---

Fail Criteria

✗ Missing history

✗ Broken search

---

# Performance Targets

Timeline Load

< 2 seconds

---

Draft Generation

< 30 seconds

---

Webhook Processing

< 5 seconds

---

Search

< 2 seconds

---

# Final MVP Checklist

✓ GitHub Connected

✓ Notes Working

✓ Timeline Working

✓ Context Generation Working

✓ AI Working

✓ Drafts Working

✓ Archive Working

If all are true:

MVP Complete.
