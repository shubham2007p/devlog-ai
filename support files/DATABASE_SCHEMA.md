# DATABASE_SCHEMA.md

## Project

DevLog AI

## Version

V1 MVP

---

# Purpose

This document defines the complete database structure for DevLog AI.

The database acts as the single source of truth for:

* GitHub activity
* Manual learning notes
* Daily learning logs
* AI generated drafts
* User settings

All AI outputs must be derived from data stored in these tables.

---

# Database Engine

SQLite

Database File:

database.db

---

# Design Principles

## Principle 1

Store Evidence Separately From AI Output

Evidence:

* Commits
* Learning Notes

Generated Content:

* Summaries
* Drafts

Generated content can be recreated.

Evidence cannot.

---

## Principle 2

Timeline First

Everything should be representable as a timeline event.

Future integrations should fit naturally into the same structure.

---

## Principle 3

Single User MVP

No multi-user support.

No organizations.

No teams.

No permissions system.

---

# TABLE: evidence

Purpose:

Universal activity table.

Every learning event eventually becomes evidence.

---

Fields

id

INTEGER PRIMARY KEY

---

source

TEXT

Examples:

github

manual_note

future:

youtube

article

course

---

event_type

TEXT

Examples:

commit

learning_note

contribution

---

title

TEXT

Short description.

Examples:

Added Binary Search

Learned STL Vectors

---

content

TEXT

Full event details.

---

metadata

JSON

Example:

{
"repo":"DSA",
"branch":"main"
}

---

event_time

DATETIME

Actual event time.

---

created_at

DATETIME

Record creation time.

---

Example

{
"source":"github",
"event_type":"commit",
"title":"Added Binary Search",
"content":"Implemented iterative binary search",
"event_time":"2026-06-18T20:00:00"
}

---

# TABLE: github_commits

Purpose:

Store complete commit information.

---

Fields

id

INTEGER PRIMARY KEY

---

commit_sha

TEXT UNIQUE

---

repo_name

TEXT

---

branch_name

TEXT

---

commit_message

TEXT

---

commit_url

TEXT

---

author_name

TEXT

---

files_changed

JSON

Example:

[
"binary_search.cpp",
"notes.md"
]

---

timestamp

DATETIME

---

created_at

DATETIME

---

Relationships

Each commit should create:

1 github_commits row

and

1 evidence row

---

# TABLE: learning_notes

Purpose:

Manual user learning input.

---

Fields

id

INTEGER PRIMARY KEY

---

date

DATE

---

concepts_learned

TEXT

---

challenges_faced

TEXT

---

key_insights

TEXT

---

resources_used

TEXT

---

additional_notes

TEXT

---

created_at

DATETIME

---

updated_at

DATETIME

---

Example

Concepts Learned

Binary Search

STL Vector

Challenges

Off-by-one errors

Insights

Think in intervals.

---

# TABLE: daily_logs

Purpose:

Compiled context for one day.

Generated automatically.

---

Fields

id

INTEGER PRIMARY KEY

---

log_date

DATE UNIQUE

---

evidence_count

INTEGER

---

commit_count

INTEGER

---

notes_count

INTEGER

---

compiled_context

TEXT

This becomes AI input.

---

generation_status

TEXT

pending

generated

failed

---

created_at

DATETIME

---

Example

Today:

* Learned Binary Search
* Added binary_search.cpp
* Added test cases
* Learned STL Vector

---

# TABLE: generated_content

Purpose:

Store AI outputs.

---

Fields

id

INTEGER PRIMARY KEY

---

daily_log_id

INTEGER

FK → daily_logs.id

---

content_type

TEXT

Values:

summary

linkedin

twitter

---

content

TEXT

---

model_used

TEXT

Example:

gemini-2.5-flash

---

generation_version

TEXT

Example:

v1

---

generated_at

DATETIME

---

# TABLE: generation_runs

Purpose:

Track AI requests.

Useful for debugging.

---

Fields

id

INTEGER PRIMARY KEY

---

daily_log_id

INTEGER

---

prompt_version

TEXT

---

model_name

TEXT

---

status

TEXT

success

failed

---

input_tokens

INTEGER

---

output_tokens

INTEGER

---

error_message

TEXT

NULLABLE

---

created_at

DATETIME

---

# TABLE: settings

Purpose:

Application configuration.

---

Fields

id

INTEGER PRIMARY KEY

---

setting_key

TEXT UNIQUE

---

setting_value

TEXT

---

Examples

draft_generation_time

11:00 PM

---

theme

light

---

model

gemini-2.5-flash

---

# TABLE: draft_feedback

Purpose:

Track edits and improvements.

Future prompt optimization.

---

Fields

id

INTEGER PRIMARY KEY

---

generated_content_id

INTEGER

---

action

TEXT

approved

edited

regenerated

---

feedback

TEXT

NULLABLE

---

created_at

DATETIME

---

# Relationships

learning_notes

↓

evidence

↓

daily_logs

↓

generated_content

---

github_commits

↓

evidence

↓

daily_logs

↓

generated_content

---

# Indexes

Create Index

github_commits.timestamp

---

Create Index

learning_notes.date

---

Create Index

daily_logs.log_date

---

Create Index

evidence.event_time

---

# Retention Policy

Never delete:

github_commits

learning_notes

daily_logs

evidence

---

Generated drafts may be regenerated.

Evidence must remain permanent.

---

# Future Expansion

The schema must support:

YouTube Learning

Articles

Books

Courses

AI Ingest Exports

without database redesign.

All future sources should create:

evidence records

and integrate naturally into the timeline.

---

# Source of Truth

The following tables are authoritative:

evidence

github_commits

learning_notes

daily_logs

Generated content should never be treated as source data.

Evidence always wins.
