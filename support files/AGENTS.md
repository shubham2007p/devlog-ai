# AGENTS.md

## Project Name

DevLog AI

---

# Project Overview

DevLog AI is a personal developer activity aggregation and content generation platform.

The system automatically collects development evidence from GitHub activity and manual learning notes.

At the end of each day, DevLog AI creates a structured learning log and generates platform-specific content drafts.

The system is designed for a single user.

The system prioritizes factual accuracy over creativity.

---

# Core Mission

Transform:

Learning Activity
+
Development Activity

into

Daily Knowledge Records
+
Social Content Drafts

with minimal user effort.

---

# Product Philosophy

DevLog AI is NOT:

* A social media scheduler
* A CRM
* A project management tool
* An analytics dashboard
* A team collaboration platform

DevLog AI IS:

* A developer journal
* A learning timeline
* A personal growth tracker
* A knowledge archive

---

# Development Principles

## Principle 1

Evidence Before Content

Every generated statement must be traceable to evidence.

Evidence Sources:

* Manual learning notes
* GitHub commits
* GitHub contribution data

No other assumptions are allowed.

---

## Principle 2

Learning > Posting

The primary product is the learning record.

The generated posts are secondary outputs.

Never design features that prioritize posting over learning.

---

## Principle 3

Simple Architecture

Prefer:

Simple solutions

over

Complex frameworks.

Avoid introducing infrastructure that is not required by MVP.

---

## Principle 4

Single User First

All design decisions should optimize for a single user.

Multi-user support is not part of MVP.

Do not introduce complexity for hypothetical future users.

---

# Technical Stack

Frontend

* HTML
* CSS
* JavaScript

Backend

* FastAPI

Database

* SQLite

Scheduler

* APScheduler

AI

* Gemini API

Version Control

* GitHub

---

# Architecture Overview

GitHub

↓

Webhook Receiver

↓

Database

↑

Learning Notes

↓

Daily Context Builder

↓

AI Generator

↓

Draft Storage

↓

Review Dashboard

---

# Folder Structure

backend/

frontend/

docs/

database/

prompts/

scripts/

tests/

---

# User Journey

User learns.

User pushes code.

GitHub webhook stores commits.

User writes notes.

System builds daily context.

AI generates:

* Summary
* LinkedIn Draft
* X Draft

User reviews.

User copies manually.

No automatic posting.

---

# Design Rules

Follow Notion-inspired design language.

Requirements:

* Warm background
* Minimal color usage
* Large typography
* White cards
* Shallow navigation

Maximum navigation depth:

2 levels

No sidebar nesting.

No admin-style dashboards.

---

# AI Rules

Never invent learning.

Never infer expertise.

Never exaggerate achievements.

Bad Example:

Commit:
Fixed CSS bug

Generated:

"Today I deepened my frontend architecture expertise."

Forbidden.

Good Example:

"Fixed a CSS issue related to component alignment."

Allowed.

---

# Database Rules

Database is the source of truth.

Generated content is disposable.

Evidence is permanent.

Always preserve:

* Commits
* Notes
* Daily Logs

Even if drafts are regenerated.

---

# API Rules

All endpoints must:

Return JSON

Use consistent response structure

Support future expansion

Example:

{
"success": true,
"data": {}
}

---

# Coding Standards

Use:

* Type hints
* Clear naming
* Small functions
* Modular files

Avoid:

* Massive files
* Business logic inside routes
* Duplicate code

---

# Security Rules

Never store API keys in source code.

Use:

.env

for:

* GEMINI_API_KEY
* GITHUB_TOKEN
* WEBHOOK_SECRET

Never commit secrets.

---

# Performance Goals

Page Load:

< 2 seconds

Draft Generation:

< 30 seconds

Webhook Processing:

< 5 seconds

Database Query:

< 200 ms

---

# MVP Scope

Included:

GitHub Webhooks

Learning Notes

Daily Context Generation

AI Draft Generation

Draft Review Dashboard

Archive

Settings

Not Included:

LinkedIn Posting

X Posting

Analytics

Teams

Public Profiles

Notifications

Mobile App

---

# Definition of Success

A user can:

Push code

Add learning notes

Generate drafts

Review drafts

Archive history

within less than 2 minutes per day.

If this is achieved, MVP is successful.
