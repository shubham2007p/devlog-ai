# API_SPEC.md

## Project

DevLog AI

## Version

1.0 MVP

---

# Purpose

This document defines all backend API endpoints.

The API layer serves as the communication bridge between:

Frontend

↓

Backend

↓

Database

↓

AI Services

---

# API Design Principles

## Principle 1

JSON Only

All requests and responses must use JSON.

---

## Principle 2

Consistent Response Format

Success Response:

{
"success": true,
"data": {}
}

Failure Response:

{
"success": false,
"error": {
"code": "ERROR_CODE",
"message": "Human readable error"
}
}

---

## Principle 3

Source of Truth

API never returns AI-generated assumptions.

Only database-backed information.

---

# Base URL

Development

http://localhost:8000

---

Production

TBD

---

# HEALTH ENDPOINTS

## GET /health

Purpose:

Check backend status.

Response:

{
"success": true,
"data": {
"status": "healthy"
}
}

---

# GITHUB WEBHOOKS

## POST /webhook/github

Purpose:

Receive GitHub push events.

Source:

GitHub Webhooks

Authentication:

Webhook Secret Validation

---

Request Example

{
"repository": {},
"commits": []
}

---

Response

{
"success": true,
"data": {
"message": "Webhook processed"
}
}

---

Errors

401

Invalid Signature

---

500

Webhook Processing Failed

---

# LEARNING NOTES

## POST /notes

Purpose:

Create a learning note.

---

Request

{
"concepts_learned": "Binary Search",
"challenges_faced": "Off-by-one errors",
"key_insights": "Think in intervals",
"resources_used": "NeetCode",
"additional_notes": "Need more practice"
}

---

Validation

concepts_learned

Required

Minimum Length

3

---

Response

{
"success": true,
"data": {
"note_id": 12
}
}

---

## GET /notes

Purpose:

Get all notes.

---

Query Parameters

date

Optional

Example:

/notes?date=2026-06-18

---

Response

{
"success": true,
"data": [
{}
]
}

---

## GET /notes/{id}

Purpose:

Get single note.

---

Response

{
"success": true,
"data": {}
}

---

## PUT /notes/{id}

Purpose:

Update note.

---

Request

{
"concepts_learned": "Updated Content"
}

---

Response

{
"success": true
}

---

## DELETE /notes/{id}

Purpose:

Delete note.

---

Response

{
"success": true
}

---

# TIMELINE

## GET /timeline/today

Purpose:

Return today's timeline.

---

Response

{
"success": true,
"data": [
{
"type": "commit",
"title": "Added Binary Search",
"time": "14:30"
},
{
"type": "learning_note",
"title": "Learned STL Vector",
"time": "17:00"
}
]
}

---

## GET /timeline/{date}

Purpose:

Retrieve timeline for a specific day.

---

Example

/timeline/2026-06-18

---

Response

{
"success": true,
"data": []
}

---

# COMMITS

## GET /commits

Purpose:

Fetch commits.

---

Query Parameters

date

repo

limit

page

---

Example

/commits?repo=DSA

---

Response

{
"success": true,
"data": []
}

---

## GET /commits/{sha}

Purpose:

Get specific commit.

---

Response

{
"success": true,
"data": {}
}

---

# DAILY LOGS

## POST /daily-log/generate

Purpose:

Generate today's daily context.

---

Process

Collect Evidence

↓

Build Context

↓

Save Daily Log

---

Response

{
"success": true,
"data": {
"daily_log_id": 15
}
}

---

## GET /daily-log/today

Purpose:

Retrieve today's compiled context.

---

Response

{
"success": true,
"data": {
"context": "..."
}
}

---

## GET /daily-log/{date}

Purpose:

Retrieve historical log.

---

Example

/daily-log/2026-06-18

---

# AI GENERATION

## POST /generate/drafts

Purpose:

Generate all content drafts.

---

Input

{
"daily_log_id": 15
}

---

Process

Daily Context

↓

Gemini

↓

Store Drafts

---

Response

{
"success": true,
"data": {
"summary_id": 11,
"linkedin_id": 12,
"twitter_id": 13
}
}

---

## POST /generate/summary

Purpose:

Generate summary only.

---

Response

{
"success": true
}

---

## POST /generate/linkedin

Purpose:

Generate LinkedIn draft only.

---

Response

{
"success": true
}

---

## POST /generate/twitter

Purpose:

Generate X draft only.

---

Response

{
"success": true
}

---

# DRAFTS

## GET /drafts/today

Purpose:

Retrieve today's generated drafts.

---

Response

{
"success": true,
"data": {
"summary": "...",
"linkedin": "...",
"twitter": "..."
}
}

---

## GET /drafts/{date}

Purpose:

Retrieve historical drafts.

---

Response

{
"success": true,
"data": {}
}

---

## PUT /drafts/{id}

Purpose:

Edit generated draft.

---

Request

{
"content": "Updated draft content"
}

---

Response

{
"success": true
}

---

## POST /drafts/{id}/approve

Purpose:

Approve draft.

---

Response

{
"success": true
}

---

## POST /drafts/{id}/regenerate

Purpose:

Generate a new version.

---

Response

{
"success": true
}

---

# ARCHIVE

## GET /archive

Purpose:

Retrieve historical days.

---

Parameters

page

limit

search

---

Example

/archive?search=binary

---

Response

{
"success": true,
"data": []
}

---

# SETTINGS

## GET /settings

Purpose:

Retrieve application settings.

---

Response

{
"success": true,
"data": {
"theme": "light",
"model": "gemini"
}
}

---

## PUT /settings

Purpose:

Update settings.

---

Request

{
"theme": "dark"
}

---

Response

{
"success": true
}

---

# STATISTICS

## GET /stats/today

Purpose:

Dashboard statistics.

---

Response

{
"success": true,
"data": {
"commits": 6,
"notes": 2,
"timeline_events": 8
}
}

---

# ERROR CODES

INVALID_REQUEST

MISSING_FIELD

NOT_FOUND

INVALID_SIGNATURE

DATABASE_ERROR

GENERATION_FAILED

AI_PROVIDER_ERROR

INTERNAL_SERVER_ERROR

---

# HTTP STATUS CODES

200

Success

---

201

Created

---

400

Bad Request

---

401

Unauthorized

---

404

Not Found

---

422

Validation Error

---

500

Server Error

---

# MVP Endpoint Count

Health

1

GitHub

1

Notes

5

Timeline

2

Commits

2

Daily Logs

3

Generation

4

Drafts

5

Archive

1

Settings

2

Stats

1

Total

27 Endpoints

---

# API Completion Criteria

The API layer is considered complete when:

✓ GitHub webhooks work

✓ Notes CRUD works

✓ Timeline renders correctly

✓ Daily log generation works

✓ Gemini integration works

✓ Draft generation works

✓ Archive retrieval works

✓ Settings persist correctly
