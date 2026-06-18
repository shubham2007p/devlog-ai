# DEPLOYMENT.md

## Purpose

Deploy DevLog AI safely.

---

# Deployment Stages

Local

↓

Railway

↓

Render

↓

VPS (Future)

---

# Environment Variables

Required

GEMINI_API_KEY

GITHUB_TOKEN

WEBHOOK_SECRET

DATABASE_URL

---

# Railway Deployment

## Create Project

Connect GitHub Repository.

---

## Configure Variables

Add all environment variables.

---

## Build Command

pip install -r requirements.txt

---

## Start Command

uvicorn backend.main:app --host 0.0.0.0 --port $PORT

---

# Render Deployment

Alternative option.

Same environment variables.

Same startup command.

---

# Domain Setup

Generate public URL.

Example

https://devlog-ai.up.railway.app

---

# GitHub Webhook Update

Repository

↓

Settings

↓

Webhooks

↓

Replace local URL

with

Production URL

---

# Database Backups

Daily backup.

Store:

database.db

---

Backup Location

backups/

YYYY-MM-DD.db

---

Retention

30 days

---

# Monitoring

Monitor

API uptime

Webhook success

Generation success

Database growth

---

# Deployment Checklist

✓ Backend Starts

✓ Database Connects

✓ Health Endpoint Works

✓ Gemini Works

✓ Webhook Works

✓ Timeline Works

✓ Draft Generation Works

---

# Rollback Strategy

If deployment fails:

Revert to previous commit.

Redeploy.

Restore latest backup.

---

# Production Success Criteria

User can:

Receive commits

Save notes

Generate drafts

Search archive

without errors.
