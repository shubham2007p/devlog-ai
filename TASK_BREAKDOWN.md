# TASK_BREAKDOWN.md

## Purpose

Convert roadmap into executable tasks.

Rules:

* One task = one objective
* Each task should be completable in 30–120 minutes
* No task should require understanding the entire system
* Tasks should be Cursor/Claude Code friendly

---

# PHASE 0

Project Setup

---

TASK-001

Create Repository

Acceptance

Repository exists.

---

TASK-002

Create Folder Structure

Acceptance

Matches PROJECT_STRUCTURE.md

---

TASK-003

Create .gitignore

Include:

venv

.env

database.db

**pycache**

Acceptance

Files ignored correctly.

---

TASK-004

Create Python Virtual Environment

Acceptance

venv created.

---

TASK-005

Install Dependencies

Acceptance

requirements.txt created.

---

TASK-006

Create FastAPI App

Acceptance

GET /health works.

---

TASK-007

Create Environment Variable Loader

Acceptance

.env variables accessible.

---

TASK-008

Create Configuration Module

Acceptance

Config values loaded from env.

---

# PHASE 1

Database

---

TASK-009

Create SQLite Connection

Acceptance

Database connects.

---

TASK-010

Create Base Model Setup

Acceptance

ORM operational.

---

TASK-011

Create Evidence Model

Acceptance

Table created.

---

TASK-012

Create GitHub Commits Model

Acceptance

Table created.

---

TASK-013

Create Learning Notes Model

Acceptance

Table created.

---

TASK-014

Create Daily Logs Model

Acceptance

Table created.

---

TASK-015

Create Generated Content Model

Acceptance

Table created.

---

TASK-016

Create Settings Model

Acceptance

Table created.

---

TASK-017

Create Database Initialization Script

Acceptance

Tables created automatically.

---

TASK-018

Create Seed Script

Acceptance

Test data inserted.

---

# PHASE 2

GitHub Integration

---

TASK-019

Create Webhook Route

Acceptance

POST endpoint exists.

---

TASK-020

Validate GitHub Signature

Acceptance

Invalid requests rejected.

---

TASK-021

Parse Push Event

Acceptance

Repository data extracted.

---

TASK-022

Extract Commit Data

Acceptance

Commits parsed correctly.

---

TASK-023

Store Commits

Acceptance

Rows added to github_commits.

---

TASK-024

Create Evidence From Commit

Acceptance

Evidence record created.

---

TASK-025

Prevent Duplicate Commits

Acceptance

Same SHA ignored.

---

TASK-026

Create Webhook Logging

Acceptance

Events logged.

---

TASK-027

Test GitHub Integration

Acceptance

Real push appears in database.

---

# PHASE 3

Learning Notes

---

TASK-028

Create Notes Schema

Acceptance

Validation working.

---

TASK-029

Create POST /notes

Acceptance

Note saved.

---

TASK-030

Create GET /notes

Acceptance

Notes returned.

---

TASK-031

Create GET /notes/{id}

Acceptance

Single note returned.

---

TASK-032

Create PUT /notes/{id}

Acceptance

Note updated.

---

TASK-033

Create DELETE /notes/{id}

Acceptance

Note deleted.

---

TASK-034

Create Evidence From Note

Acceptance

Evidence record created.

---

TASK-035

Create Notes Service Layer

Acceptance

Business logic isolated.

---

# PHASE 4

Timeline

---

TASK-036

Create Timeline Service

Acceptance

Events aggregated.

---

TASK-037

Fetch Evidence Events

Acceptance

All evidence returned.

---

TASK-038

Sort Timeline Chronologically

Acceptance

Correct order.

---

TASK-039

Create GET /timeline/today

Acceptance

Returns events.

---

TASK-040

Create GET /timeline/{date}

Acceptance

Returns historical events.

---

TASK-041

Create Timeline DTO

Acceptance

Consistent response.

---

# PHASE 5

Frontend Foundation

---

TASK-042

Create Base Layout

Acceptance

Header visible.

---

TASK-043

Create Navigation

Acceptance

All pages accessible.

---

TASK-044

Create Today Page

Acceptance

Page renders.

---

TASK-045

Create Notes Form UI

Acceptance

Form visible.

---

TASK-046

Connect Notes API

Acceptance

Notes save successfully.

---

TASK-047

Create Timeline UI

Acceptance

Events displayed.

---

TASK-048

Create Loading States

Acceptance

Visible during API calls.

---

TASK-049

Create Error States

Acceptance

Errors displayed properly.

---

# PHASE 6

Daily Context Builder

---

TASK-050

Create Context Builder Service

Acceptance

Service callable.

---

TASK-051

Fetch Daily Notes

Acceptance

Notes retrieved.

---

TASK-052

Fetch Daily Commits

Acceptance

Commits retrieved.

---

TASK-053

Generate Daily Context

Acceptance

Context created.

---

TASK-054

Store Daily Log

Acceptance

Database updated.

---

TASK-055

Create POST /daily-log/generate

Acceptance

Endpoint functional.

---

TASK-056

Create GET /daily-log/today

Acceptance

Context retrievable.

---

# PHASE 7

Gemini Integration

---

TASK-057

Connect Gemini API

Acceptance

API responds.

---

TASK-058

Load Prompt Templates

Acceptance

Prompts loaded from files.

---

TASK-059

Generate Summary

Acceptance

Summary created.

---

TASK-060

Generate LinkedIn Draft

Acceptance

Draft created.

---

TASK-061

Generate X Draft

Acceptance

Draft created.

---

TASK-062

Store Generated Content

Acceptance

Database updated.

---

TASK-063

Store Generation Metadata

Acceptance

generation_runs populated.

---

TASK-064

Implement Retry Logic

Acceptance

Failures retried.

---

# PHASE 8

Draft Dashboard

---

TASK-065

Create Drafts Page

Acceptance

Page renders.

---

TASK-066

Display Summary Draft

Acceptance

Visible.

---

TASK-067

Display LinkedIn Draft

Acceptance

Visible.

---

TASK-068

Display X Draft

Acceptance

Visible.

---

TASK-069

Create Copy Button

Acceptance

Clipboard works.

---

TASK-070

Create Edit Draft Feature

Acceptance

Draft editable.

---

TASK-071

Create Regenerate Draft Feature

Acceptance

New version generated.

---

TASK-072

Create Approve Draft Feature

Acceptance

Approval saved.

---

# PHASE 9

Archive

---

TASK-073

Create Archive Page

Acceptance

Page visible.

---

TASK-074

List Historical Days

Acceptance

Records displayed.

---

TASK-075

Search Archive

Acceptance

Results filtered.

---

TASK-076

Open Historical Day

Acceptance

Timeline visible.

---

TASK-077

View Historical Drafts

Acceptance

Drafts visible.

---

# PHASE 10

Settings

---

TASK-078

Create Settings Page

Acceptance

Page visible.

---

TASK-079

Save Gemini Key

Acceptance

Stored.

---

TASK-080

Save Theme Preference

Acceptance

Stored.

---

TASK-081

Save Generation Time

Acceptance

Stored.

---

# PHASE 11

Scheduler

---

TASK-082

Install APScheduler

Acceptance

Operational.

---

TASK-083

Create Nightly Job

Acceptance

Runs automatically.

---

TASK-084

Generate Daily Context Automatically

Acceptance

Daily log created.

---

TASK-085

Generate Drafts Automatically

Acceptance

Drafts created.

---

# PHASE 12

Testing

---

TASK-086

Test Webhooks

---

TASK-087

Test Notes CRUD

---

TASK-088

Test Timeline

---

TASK-089

Test Context Generation

---

TASK-090

Test Gemini Integration

---

TASK-091

Test Draft Workflow

---

TASK-092

Test Archive

---

TASK-093

Test Settings

---

TASK-094

Fix Critical Bugs

---

# PHASE 13

Deployment

---

TASK-095

Deploy To Railway

---

TASK-096

Configure Environment Variables

---

TASK-097

Update GitHub Webhook URL

---

TASK-098

Verify Production Health Endpoint

---

TASK-099

Verify Production Draft Generation

---

TASK-100

Production Smoke Test

Acceptance

Entire workflow succeeds.

---

# MVP Completion Definition

All tasks:

001–100

Completed

AND

All acceptance criteria pass

THEN

DevLog AI MVP = COMPLETE.

