# PRD: DevLog AI

## Version

V1

## Product Type

Personal Developer Activity Aggregator and Content Generator

---

# 1. Vision

Developers learn, build projects, solve problems, push code, and make contributions every day.

Most of this work remains invisible because documenting and posting about it requires additional effort.

DevLog AI automatically captures evidence of learning from GitHub activity and user notes, constructs a daily learning log, and generates platform-specific content drafts.

The user should spend less than 2 minutes per day documenting their progress.

---

# 2. Problem Statement

Current workflow:

Learn Something
→ Build Something
→ Commit Code
→ Push to GitHub
→ Forget What Was Done
→ Skip Posting

Problems:

1. Learning is not documented.
2. GitHub activity is scattered across commits.
3. Social posts require manual rewriting.
4. Weekly and monthly progress is difficult to track.
5. Valuable work becomes invisible.

---

# 3. Goals

Primary Goals:

* Automatically collect development activity.
* Build daily learning logs.
* Generate social media drafts.
* Create a historical record of growth.

Secondary Goals:

* Build a personal knowledge timeline.
* Generate portfolio content.
* Generate resume bullet points.
* Generate weekly and monthly reports.

---

# 4. Non Goals (V1)

Not included:

* Auto posting to LinkedIn.
* Auto posting to X.
* Team collaboration.
* Multiple users.
* Public profiles.
* Scheduling social posts.
* Analytics.

User remains in control.

All content must be reviewed before publishing.

---

# 5. User Persona

Primary User:

Student Developer

Characteristics:

* Learning daily
* Building projects
* Using GitHub
* Wants online presence
* Doesn't want to spend time writing posts

Example:

Shubh learns DSA, builds projects, pushes commits, and wants consistent LinkedIn and X updates.

---

# 6. Core Workflow

Throughout Day:

User learns concepts.

User pushes code.

GitHub sends webhook events.

System stores activity.

User optionally writes manual notes.

At end of day:

System combines:

* Manual notes
* Commits
* Repository activity
* Contributions

AI generates:

* Daily summary
* LinkedIn draft
* X draft
* Learning report

User reviews.

User copies and publishes.

---

# 7. Functional Requirements

## Module 1: User Authentication

V1:

Single user system.

Authentication:

* Local login
  or
* Secret access URL

No OAuth required initially.

---

## Module 2: GitHub Integration

### GitHub Webhook Listener

Events:

* Push Event

When push occurs:

Receive:

* Repository name
* Commit message
* Commit author
* Timestamp
* Branch
* Changed files

Store event.

---

### Commit Processing

Extract:

Repository:
AI-Ingest

Commit:
Added webhook parser

Files:
webhook.py
database.py

Timestamp:
2026-06-18 20:45

Store as activity record.

---

## Module 3: Learning Notes

User opens dashboard.

Form:

What did you learn today?

Fields:

Concepts Learned

Challenges Faced

Key Insight

Resources Used

Additional Notes

Example:

Concept:
Binary Search

Challenge:
Off-by-one errors

Insight:
Think in intervals instead of indexes

Store in database.

---

## Module 4: Activity Timeline

System builds chronological timeline.

Example:

09:00
Learned Binary Search

14:00
Commit:
Added binary search implementation

18:00
Commit:
Added test cases

20:00
Learned STL vectors

Timeline becomes source of truth.

---

## Module 5: Daily Log Builder

Nightly Process

Time:
11:00 PM

System collects:

Manual Notes

*

GitHub Activity

*

Contribution Data

Creates:

Raw Daily Context

Example:

Today user:

* Learned Binary Search
* Implemented Binary Search
* Solved 5 problems
* Added test coverage

Store compiled log.

---

## Module 6: AI Content Generation

Input:

Raw Daily Context

Output:

1. Daily Summary

2. LinkedIn Post

3. X Post

4. Key Learnings

5. Tomorrow Focus

---

### LinkedIn Generator

Style:

* Professional
* Reflective
* Learning focused

Structure:

Hook

Learning

Challenge

Takeaway

Hashtags

---

### X Generator

Style:

Short

Direct

Technical

Maximum:
280 characters

---

## Module 7: Review Dashboard

Page:

Generated Content

Sections:

Daily Summary

LinkedIn Draft

X Draft

Buttons:

Edit

Regenerate

Approve

Copy

---

## Module 8: Daily Archive

Store every day.

Example:

June 18

Summary

LinkedIn Draft

X Draft

Commits

Notes

Searchable later.

---

# 8. Database Design

Users

id
name

Projects

id
repo_name

Commits

id
repo
message
timestamp
files_changed

LearningNotes

id
date
concepts
challenges
insights

DailyLogs

id
date
compiled_context

GeneratedContent

id
date
linkedin
x_post
summary

---

# 9. AI Prompt Strategy

Step 1

Create factual summary.

No creativity.

Only facts.

Step 2

Generate platform content.

This prevents hallucination.

Pipeline:

Activities
→ Summary
→ Platform Posts

Not

Activities
→ LinkedIn Directly

---

# 10. Scheduler

Runs nightly.

Default:

11:00 PM

Tasks:

Fetch GitHub Activity

Compile Context

Generate Drafts

Save Outputs

Mark Day Complete

---

# 11. Dashboard Pages

1. Home

Today's Activity

2. Learning Notes

Manual Input

3. Activity Feed

All Commits

4. Generated Content

Drafts

5. Archive

Historical Records

6. Settings

GitHub Configuration

AI Configuration

---

# 12. Future Features

V2

* Auto GitHub contribution tracking
* Weekly reports
* Monthly reports
* Streak tracking

V3

* LinkedIn publishing
* X publishing

V4

* Resume bullet generation
* Portfolio generation

V5

* AI learning graph

* Skill progression tracking

* Detect:
  "Learning DSA"
  "Learning ML"
  "Learning Web Dev"

Automatically build skill maps.

---

# 13. Success Metrics

Daily Log Completion Rate

Target:
80%

Days with Generated Posts

Target:
90%

Manual Writing Time Saved

Target:
70%

Daily User Effort

Target:
Less than 2 minutes

---

# 14. MVP Definition

User pushes code.

GitHub webhook captures activity.

User writes learning notes.

System creates daily log.

AI generates:

* Summary
* LinkedIn Draft
* X Draft

User reviews and copies.

MVP complete.
