# SETUP.md

## Purpose

Local development setup.

---

# Requirements

Python

3.11+

Git

GitHub Account

Gemini API Key

---

# Clone Repository

git clone <repo-url>

cd devlog-ai

---

# Create Virtual Environment

Windows

python -m venv venv

venv\Scripts\activate

---

Mac/Linux

python3 -m venv venv

source venv/bin/activate

---

# Install Dependencies

pip install fastapi

pip install uvicorn

pip install sqlalchemy

pip install apscheduler

pip install google-generativeai

pip install python-dotenv

pip install requests

pip install pydantic

---

# Environment Variables

Create

.env

---

Required Variables

GEMINI_API_KEY=

GITHUB_TOKEN=

WEBHOOK_SECRET=

DATABASE_URL=sqlite:///database.db

---

# Run Backend

uvicorn backend.main:app --reload

---

Expected

http://localhost:8000

---

# Verify Backend

Open

http://localhost:8000/health

Expected

{
"status":"healthy"
}

---

# Configure GitHub Webhook

Repository

↓

Settings

↓

Webhooks

↓

Add Webhook

---

Payload URL

https://your-domain.com/webhook/github

---

Content Type

application/json

---

Secret

WEBHOOK_SECRET

---

Events

Push Events Only

---

# Gemini Setup

Open Google AI Studio

Create API Key

Add To

.env

---

Test

POST /generate/summary

Expected

Successful generation.

---

# Frontend Development

Open

frontend/index.html

or

Use VS Code Live Server

---

# Database Setup

Automatic

SQLite file created on startup.

---

# Useful Commands

Start Backend

uvicorn backend.main:app --reload

---

Run Tests

pytest

---

Reset Database

python scripts/reset_database.py

---

Seed Test Data

python scripts/seed_database.py

---

Backup Database

python scripts/backup_database.py

---

# Troubleshooting

Gemini Error

Check API key

---

Webhook Error

Check secret

Check URL

---

Database Error

Delete database.db

Restart application

---

# Local Development Checklist

✓ Backend Running

✓ Database Created

✓ Gemini Connected

✓ GitHub Connected

✓ Health Endpoint Working

✓ Notes Endpoint Working

✓ Draft Generation Working

Ready For Development.
