# USER_FLOWS.md

## Purpose

Defines complete user journeys and system interactions.

Every feature implementation must follow these flows.

---

# Flow 1: First Time Setup

User Opens App

↓

Settings Page

↓

Enter Gemini API Key

↓

Save

↓

Backend validates key

↓

Store in settings table

↓

Success Message

---

Connect GitHub

↓

Generate Webhook URL

↓

User Adds Webhook In Repository

↓

GitHub Sends Test Event

↓

Webhook Verified

↓

Connection Status = Active

---

Success Criteria

User can generate drafts.

GitHub events arrive successfully.

---

# Flow 2: GitHub Commit Collection

User

↓

git push

↓

GitHub

↓

Webhook Event

↓

POST /webhook/github

↓

Validate Signature

↓

Store github_commits

↓

Create evidence record

↓

Update timeline

↓

Return success

---

Success Criteria

Commit visible within 10 seconds.

---

# Flow 3: Add Learning Note

Today Page

↓

Click Add Note

↓

Form Opens

↓

Fill Fields

* Concepts
* Challenges
* Insights
* Resources

↓

Save

↓

POST /notes

↓

Store learning_notes

↓

Create evidence record

↓

Update timeline

↓

Show Success

---

Success Criteria

New note appears instantly in timeline.

---

# Flow 4: Generate Daily Context

User Clicks Generate Draft

↓

POST /daily-log/generate

↓

Collect Notes

↓

Collect Commits

↓

Collect Evidence

↓

Build Context

↓

Save daily_log

↓

Return ID

---

Success Criteria

Daily context generated.

---

# Flow 5: Generate Drafts

User Clicks Generate

↓

POST /generate/drafts

↓

Load Daily Context

↓

Gemini API

↓

Generate Summary

↓

Generate LinkedIn

↓

Generate X

↓

Store generated_content

↓

Return Success

---

Success Criteria

All drafts created.

---

# Flow 6: Approve Draft

Draft Page

↓

Review Content

↓

Approve

↓

draft_feedback

action=approved

↓

Archive

---

Success Criteria

Draft marked approved.

---

# Flow 7: Regenerate Draft

Draft Page

↓

Regenerate

↓

Load Original Context

↓

Gemini

↓

New Version

↓

Save

↓

Replace Display

---

Rules

Facts cannot change.

Only wording changes.

---

# Flow 8: Archive Search

Archive Page

↓

Search

↓

Backend Query

↓

Return Matching Logs

↓

Open Day

↓

View Timeline

↓

View Drafts

---

Success Criteria

Historical data accessible.

---

# Empty States

No Commits

"Push your first commit."

---

No Notes

"What did you learn today?"

---

No Drafts

"Generate your first draft."

---

# Error Flow

Gemini Failure

↓

Retry

↓

If Failure

↓

Show Error

↓

Allow Retry

No data loss allowed.
