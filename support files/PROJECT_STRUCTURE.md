# PROJECT_STRUCTURE.md

## Purpose

Defines exact project organization.

No files should exist outside this structure without approval.

---

# Root

devlog-ai/

---

# Backend

backend/

Purpose

API and business logic.

Structure

backend/

├── main.py

├── config.py

├── database.py

├── dependencies.py

├── scheduler.py

│

├── routes/

│   ├── notes.py
│   ├── commits.py
│   ├── drafts.py
│   ├── settings.py
│   ├── timeline.py
│   └── webhook.py

│

├── services/

│   ├── github_service.py
│   ├── ai_service.py
│   ├── timeline_service.py
│   ├── draft_service.py
│   └── context_builder.py

│

├── models/

│   ├── evidence.py
│   ├── commits.py
│   ├── notes.py
│   ├── drafts.py
│   └── settings.py

│

├── schemas/

│   ├── notes.py
│   ├── drafts.py
│   ├── timeline.py
│   └── settings.py

│

└── utils/

```
├── logger.py
├── validators.py
└── helpers.py
```

---

# Frontend

frontend/

Purpose

User interface.

Structure

frontend/

├── index.html

├── drafts.html

├── archive.html

├── settings.html

│

├── css/

│   ├── globals.css
│   ├── layout.css
│   ├── components.css
│   └── theme.css

│

├── js/

│   ├── api.js
│   ├── timeline.js
│   ├── drafts.js
│   ├── archive.js
│   └── settings.js

│

└── assets/

```
├── icons/
└── images/
```

---

# Database

database/

database.db

migrations/

seed/

---

# AI Prompts

prompts/

summary.txt

linkedin.txt

twitter.txt

---

# Documentation

docs/

PRD.md

TECH_ARCHITECTURE.md

UX_NAVIGATION.md

DESIGN_SYSTEM.md

AGENTS.md

DATABASE_SCHEMA.md

API_SPEC.md

AI_PROMPTS.md

USER_FLOWS.md

COMPONENTS.md

PROJECT_STRUCTURE.md

---

# Tests

tests/

test_notes.py

test_commits.py

test_drafts.py

test_webhook.py

---

# Scripts

scripts/

seed_database.py

reset_database.py

backup_database.py

---

# Environment

.env

.env.example

.gitignore

---

# Architecture Rules

Routes

↓

Services

↓

Models

↓

Database

Never:

Route

↓

Database Directly

---

# File Ownership

Routes

HTTP only

---

Services

Business Logic

---

Models

Database

---

Schemas

Validation

---

Utils

Shared Helpers

---

# Future Expansion

future/

youtube/

articles/

courses/

ai_ingest/

Only after MVP completion.

