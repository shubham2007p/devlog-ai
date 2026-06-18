# DevLog AI - Technical Architecture Report (V1)

## Version

1.0

## Status

Planning Phase

---

# Executive Summary

DevLog AI is a personal automation system designed to transform a developer's daily activity into structured learning logs and platform-specific content drafts.

The system continuously collects development evidence from GitHub and manual learning notes, consolidates the information into a daily context, and generates social media drafts using AI.

The primary goal is to reduce the time required to document learning progress while maintaining factual accuracy.

---

# Core Principle

The system does not generate content from assumptions.

Every generated statement must be traceable to one of two sources:

1. User-written learning notes
2. GitHub activity

This ensures generated content remains authentic and avoids AI hallucination.

---

# High Level Architecture

```
                GitHub
                   │
                   ▼
          Webhook Receiver
                   │
                   ▼
               Database
                   ▲
                   │
         Learning Notes UI
                   │
                   ▼
         Daily Context Builder
                   │
                   ▼
             Gemini API
                   │
                   ▼
           Generated Drafts
                   │
                   ▼
            Review Dashboard
```

---

# System Components

The system consists of five primary components:

1. Activity Collection Layer
2. Data Storage Layer
3. Context Generation Layer
4. AI Generation Layer
5. Review and Archive Layer

---

# Technology Stack

## Frontend

Technology:

* HTML
* CSS
* JavaScript

Reasoning:

The application is intended for a single user and does not require complex frontend architecture.

Advantages:

* Fast development
* Minimal complexity
* Easy deployment
* Easier debugging
* No framework overhead

Future Upgrade Path:

* React
* Next.js

Not required for MVP.

---

## Backend

Technology:

FastAPI

Reasoning:

FastAPI provides:

* High performance
* Easy REST API development
* Native Python support
* Automatic API documentation
* Easy integration with AI services

Responsibilities:

* Receive GitHub webhooks
* Handle note submissions
* Generate daily contexts
* Manage AI requests
* Serve dashboard data

---

## Database

Technology:

SQLite

Reasoning:

The application is designed for a single user.

Advantages:

* Zero setup
* No database server
* Single file storage
* Easy backups
* Lightweight

Database File:

database.db

Expected Capacity:

More than sufficient for years of personal usage.

Future Upgrade Path:

PostgreSQL

Only if multi-user support is introduced.

---

# External Integrations

## GitHub Webhooks

Purpose:

Receive development activity immediately after code is pushed.

Cost:

Free

Required Configuration:

Repository Settings
→ Webhooks
→ Add Webhook

Example Endpoint:

POST /webhook/github

Data Received:

* Repository name
* Commit message
* Commit author
* Commit SHA
* Branch
* Timestamp
* Files changed

Benefits:

* Real-time updates
* No polling required
* No API quota usage

---

## GitHub API

Purpose:

Retrieve supplementary development data.

Examples:

* Contribution counts
* Repository information
* Historical commits
* User profile information

Authentication:

GitHub Personal Access Token

Cost:

Free

Expected Usage:

Low

Risk Level:

Low

---

## Gemini API

Purpose:

Generate:

* Daily summaries
* LinkedIn drafts
* X drafts
* Learning reports

Provider:

Google AI Studio

Required:

API Key

Cost:

Free tier sufficient for MVP

Expected Usage:

1 generation per day

Estimated Cost:

Near zero

Risk Level:

Low

Alternative Options:

* Ollama
* Qwen
* Gemma
* Local LLMs

---

# APIs Not Required

The following services should not be used during MVP development:

LinkedIn API

Reason:

Complex authentication
Unnecessary complexity

---

X API

Reason:

Paid restrictions
Not required for draft generation

---

Zapier

Reason:

Adds complexity
Not needed

---

n8n

Reason:

Useful later
Not required for MVP

---

Redis

Reason:

No caching requirements

---

Vector Databases

Reason:

No retrieval system exists in MVP

---

LangChain

Reason:

Unnecessary abstraction

---

Docker

Reason:

Not needed during initial development

---

# Backend Modules

## Module 1

GitHub Webhook Receiver

Purpose:

Receive push events.

Endpoint:

POST /webhook/github

Workflow:

GitHub Push
→ Receive Payload
→ Validate Request
→ Store Commit Data

Output:

Commit records stored in database.

---

## Module 2

Learning Notes Service

Purpose:

Capture user learning.

Endpoint:

POST /notes

Fields:

* Concepts learned
* Challenges faced
* Key insights
* Resources used
* Additional notes

Output:

Stored learning note.

---

## Module 3

Activity Processor

Purpose:

Normalize activity records.

Responsibilities:

* Parse commits
* Extract metadata
* Associate commits with dates
* Create activity timeline

Output:

Structured activity data

---

## Module 4

Daily Context Builder

Purpose:

Combine all evidence into a single source of truth.

Inputs:

Learning Notes

*

GitHub Activity

*

Contribution Data

Output:

Daily Context

Example:

Today:

* Learned Binary Search
* Implemented Binary Search
* Added test coverage
* Solved edge case bugs

This becomes AI input.

---

## Module 5

AI Generation Service

Purpose:

Generate content.

Input:

Daily Context

Output:

Daily Summary
LinkedIn Draft
X Draft

Generation Pipeline:

Raw Evidence
→ Factual Summary
→ Platform Drafts

This approach reduces hallucinations.

---

## Module 6

Review Dashboard

Purpose:

Human approval layer.

Capabilities:

View Drafts

Edit Drafts

Regenerate Drafts

Approve Drafts

Copy Drafts

No automatic publishing.

---

# Scheduler

Technology:

APScheduler

Purpose:

Automate nightly processing.

Execution Time:

11:00 PM

Workflow:

Fetch Activities
→ Build Context
→ Generate Drafts
→ Save Results

Output:

Ready-to-review content.

---

# Database Schema

## Commits Table

Fields:

id

repo_name

commit_sha

commit_message

timestamp

files_changed

created_at

---

## Learning Notes Table

Fields:

id

date

concepts

challenges

insights

resources

additional_notes

---

## Daily Logs Table

Fields:

id

date

compiled_context

created_at

---

## Generated Content Table

Fields:

id

date

summary

linkedin_post

x_post

generated_at

---

# Frontend Pages

## Home

Purpose:

Overview of today's activity.

Displays:

* Commit count
* Learning notes count
* Draft status

---

## Notes Page

Purpose:

Manual learning entry.

Actions:

Create

Edit

Delete

---

## Drafts Page

Purpose:

Review generated content.

Actions:

Approve

Edit

Copy

Regenerate

---

## Activity Feed

Purpose:

View all collected commits.

---

## Archive

Purpose:

Historical records.

Search by:

Date

Repository

Keyword

---

## Settings

Purpose:

Manage:

GitHub token

Gemini API key

Webhook settings

---

# Security Considerations

Store API keys in environment variables.

Never commit:

.env

database backups

API keys

Authentication tokens

Use webhook signature verification.

Validate all incoming requests.

---

# Development Roadmap

Phase 1

Backend Setup

* FastAPI
* SQLite
* Project Structure

Estimated:
1 Day

---

Phase 2

GitHub Integration

* Webhooks
* Commit Storage

Estimated:
1-2 Days

---

Phase 3

Learning Notes Module

* UI
* Database Integration

Estimated:
1 Day

---

Phase 4

Daily Context Builder

Estimated:
1 Day

---

Phase 5

Gemini Integration

Estimated:
1 Day

---

Phase 6

Draft Dashboard

Estimated:
1-2 Days

---

Phase 7

Testing and Deployment

Estimated:
1 Day

---

Total MVP Development Time

Approximately:

7-10 Days

For a solo developer working part-time.

---

# MVP Success Criteria

A successful MVP must achieve:

1. Automatically capture GitHub activity.

2. Allow manual learning note entry.

3. Build daily learning contexts.

4. Generate LinkedIn and X drafts.

5. Allow user review before publishing.

6. Require less than two minutes of daily user effort.

If all six conditions are met, the MVP is considered successful.
