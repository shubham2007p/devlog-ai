# ERROR_HANDLING.md

## Purpose

Define how the system responds to failures.

Goals:

* No data loss
* Graceful recovery
* Clear user feedback
* Recoverable operations

---

# Error Severity Levels

## Critical

Application cannot function.

Examples:

Database unavailable

Corrupted database

Startup failure

---

Action

Block operation.

Show error screen.

Write log.

Notify developer.

---

## Major

Feature unavailable.

Examples:

Gemini outage

GitHub API failure

Webhook failure

---

Action

Allow app usage.

Disable affected feature.

Show retry option.

---

## Minor

Temporary inconvenience.

Examples:

Slow response

Search timeout

Archive loading delay

---

Action

Retry automatically.

Show loading state.

---

# Database Failures

## Database Connection Failure

Detection

Connection cannot be established.

---

System Response

Block writes.

Disable generation.

Show:

"Database unavailable."

---

Recovery

Reconnect every 30 seconds.

---

# Duplicate Commit

Cause

GitHub retries webhook.

---

System Response

Check commit_sha.

If exists:

Ignore.

Return success.

---

# Corrupted Data

Detection

Schema mismatch.

Invalid JSON.

---

Action

Skip record.

Log error.

Continue processing.

---

# GitHub Failures

## Invalid Webhook Signature

Action

Reject request.

HTTP 401.

Log attempt.

---

## Webhook Timeout

Action

Return failure.

GitHub retries.

---

## Missing Commit Data

Action

Store partial data.

Flag for review.

---

# Gemini Failures

## API Key Invalid

Action

Block generation.

Show:

"Invalid Gemini API Key."

---

## Rate Limit Reached

Action

Retry after delay.

Show:

"Generation temporarily unavailable."

---

Retry Strategy

Attempt 1

Immediate

---

Attempt 2

30 seconds

---

Attempt 3

2 minutes

---

Fail after third attempt.

---

## Empty Response

Action

Discard.

Retry generation.

---

# Timeline Failures

## Evidence Missing

Action

Display available events.

Show warning.

---

## Sort Failure

Action

Fallback to created_at.

---

# Archive Failures

## Search Failure

Action

Return recent entries.

Display warning.

---

# Frontend Failures

## API Unavailable

Action

Show offline banner.

Disable actions.

---

## Network Loss

Action

Retry requests.

Preserve unsaved content.

---

# Logging Requirements

Every error must log:

timestamp

severity

service

message

stack trace

---

# Recovery Principles

1. Never lose evidence.

2. Retry external services.

3. Fail gracefully.

4. Preserve user work.

5. Log everything.

---

# Success Criteria

A failure should never destroy:

commits

notes

daily logs

evidence

These are permanent records.
