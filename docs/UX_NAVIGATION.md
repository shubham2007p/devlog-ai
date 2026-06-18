# DevLog AI – UX & Navigation Architecture Report

## Design Philosophy

DevLog AI should feel like:

* A developer journal
* A learning notebook
* A personal workspace

It should NOT feel like:

* A CRM
* An admin dashboard
* A social media scheduler
* A corporate analytics platform

Core feeling:

"Open app → instantly see what I learned today."

---

# Design Principles

## Principle 1: Today's Work First

Every screen should answer:

"What did I do today?"

before showing anything else.

---

## Principle 2: Shallow Navigation

Maximum depth:

2 levels

Bad:

Dashboard
→ Learning
→ Logs
→ Daily Logs
→ June
→ Day

Good:

Today
Archive

---

## Principle 3: Journal First

Commits should not feel like database entries.

Commits become timeline events.

Example:

10:15 AM
Added binary_search.cpp

2:40 PM
Learned STL vectors

8:30 PM
Fixed edge case bug

Everything becomes part of a story.

---

## Principle 4: Drafts Are Outputs

The main product is not LinkedIn posts.

The main product is learning history.

Posts are generated outcomes.

---

# Information Architecture

Primary Navigation

1. Today
2. Drafts
3. Archive
4. Settings

Nothing else.

No nested menus.

No sidebar categories.

No analytics page.

No reports page.

---

# Layout Structure

Desktop

┌───────────────────────────────┐
│ Logo          User            │
├───────────────────────────────┤
│ Today Drafts Archive Settings │
├───────────────────────────────┤
│                               │
│ Main Content                  │
│                               │
└───────────────────────────────┘

---

Mobile

☰ DevLog AI

Today

Drafts

Archive

Settings

---

# Page 1: Today

Purpose:

Single source of truth.

This becomes the home page.

---

Hero Section

Today

June 18, 2026

Learning Streak: 14 Days

Commits Today: 6

Notes Added: 2

---

Quick Actions

[ Add Learning Note ]

[ Generate Draft ]

---

Activity Timeline

09:00

Learned Binary Search

---

11:20

Commit

Added binary_search.cpp

---

14:00

Learned STL Vector

---

17:40

Commit

Added test cases

---

20:10

Commit

Fixed edge case

---

This timeline occupies most of the page.

---

# Learning Note Input

Appears inline.

Not a separate page.

Click:

Add Learning Note

Expands:

What did you learn today?

[ Text Area ]

Challenges Faced

[ Text Area ]

Key Insight

[ Text Area ]

Save

This keeps context visible.

---

# Daily Context Card

At bottom of timeline.

Generated automatically.

Summary:

Today you worked on Binary Search,
implemented solutions, added tests,
and explored STL vectors.

Source count:

2 Learning Notes

6 Commits

Status:

Ready for Draft Generation

---

# Page 2: Drafts

Purpose:

Review generated content.

No timeline.

No commits.

Only generated outputs.

---

Sections

LinkedIn Draft

[ Content ]

Copy

Edit

Regenerate

---

X Draft

[ Content ]

Copy

Edit

Regenerate

---

Daily Summary

[ Content ]

---

Design Style

Document-like editor.

Not cards inside cards inside cards.

---

# Page 3: Archive

Purpose:

Historical memory.

---

Top Search Bar

Search:

Binary Search

FastAPI

AI Ingest

GitHub

---

Date List

June 18

June 17

June 16

June 15

---

Clicking a day opens:

Timeline

Notes

Generated drafts

All on one page.

No further nesting.

---

# Page 4: Settings

Very small page.

Sections:

GitHub

Webhook URL

Connection Status

---

AI

Gemini API Key

Model Selection

---

Scheduler

Generate Draft Time

Default:

11:00 PM

---

Theme

Light

Dark

System

---

# Visual Design System

Background

Warm Paper

#F6F5F4

---

Cards

White

12px Radius

Very light border

No heavy shadows

---

Typography

Inter

Large headings

Readable body text

Notion-style hierarchy

---

Colors

Primary Blue

Actions only

Generate

Save

Copy

---

Green

Success

---

Red

Errors

---

Everything else

Neutral grayscale

---

# Empty States

No Commits Yet

"Push your first commit today."

---

No Notes Yet

"What did you learn today?"

---

No Drafts Yet

"Generate your first learning summary."

---

# Future Expansion

Without changing navigation:

Today
Drafts
Archive
Settings

Future features fit naturally:

Weekly Reports

inside Archive

---

Monthly Reports

inside Archive

---

Resume Generator

inside Drafts

---

Portfolio Generator

inside Drafts

Navigation remains unchanged.

---

# Final UX Goal

The user should be able to:

Open App

↓

See Today's Activity

↓

Add Learning Note

↓

Generate Draft

↓

Review Draft

↓

Leave

within 60 seconds.

If a new user needs more than 60 seconds to understand where to click, the interface is too complicated.
