import sys
import os
from datetime import datetime, date, timedelta

# Include the project root directory in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models.evidence import Evidence
from backend.models.commits import GitHubCommit
from backend.models.notes import LearningNote
from backend.models.drafts import DailyLog, GeneratedContent, GenerationRun, DraftFeedback
from backend.models.settings import Setting

def seed_data():
    """
    Clears existing tables and populates them with sample seed data.
    """
    session = SessionLocal()
    try:
        print("Clearing existing tables...")
        session.query(DraftFeedback).delete()
        session.query(GenerationRun).delete()
        session.query(GeneratedContent).delete()
        session.query(DailyLog).delete()
        session.query(LearningNote).delete()
        session.query(GitHubCommit).delete()
        session.query(Evidence).delete()
        session.query(Setting).delete()
        session.commit()

        print("Seeding settings...")
        settings = [
            Setting(setting_key="theme", setting_value="light"),
            Setting(setting_key="model", setting_value="gemini-2.5-flash"),
            Setting(setting_key="draft_generation_time", setting_value="11:00 PM")
        ]
        session.add_all(settings)

        print("Seeding learning notes...")
        today = date.today()
        note = LearningNote(
            date=today,
            concepts_learned="Binary Search, STL Vector",
            challenges_faced="Off-by-one errors with indexes",
            key_insights="Think in intervals instead of index offsets",
            resources_used="NeetCode, C++ Reference",
            additional_notes="Need to practice more binary search edge cases tomorrow."
        )
        session.add(note)
        session.commit()  # commit to generate ID for referencing

        print("Seeding GitHub commits...")
        commit = GitHubCommit(
            commit_sha="a1b2c3d4e5f678901234567890abcdef12345678",
            repo_name="DevLog-AI",
            branch_name="main",
            commit_message="Added webhook parser and SQLite base connection",
            commit_url="https://github.com/shubh/DevLog-AI/commit/a1b2c3d4e5f678901234567890abcdef12345678",
            author_name="Shubh",
            files_changed=["backend/routes/webhook.py", "backend/database.py"],
            timestamp=datetime.utcnow()
        )
        session.add(commit)
        session.commit()  # commit to generate ID

        print("Seeding evidence...")
        evidences = [
            Evidence(
                source="github",
                event_type="commit",
                title="Commit: Added webhook parser",
                content="Added webhook parser and SQLite base connection in DevLog-AI repository",
                event_metadata={"repo": "DevLog-AI", "branch": "main", "sha": "a1b2c3d4"},
                event_time=datetime.utcnow() - timedelta(hours=4)
            ),
            Evidence(
                source="manual_note",
                event_type="learning_note",
                title="Note: Learned Binary Search",
                content="Learned Binary Search, STL Vector. Insight: Think in intervals.",
                event_metadata={"note_id": note.id},
                event_time=datetime.utcnow() - timedelta(hours=2)
            )
        ]
        session.add_all(evidences)

        print("Seeding daily logs...")
        daily_log = DailyLog(
            log_date=today,
            evidence_count=2,
            commit_count=1,
            notes_count=1,
            compiled_context="""--- Daily Context ---
Date: 2026-06-18
GitHub Activity:
- Repository: DevLog-AI | Branch: main
  Commit: Added webhook parser and SQLite base connection
  Files: backend/routes/webhook.py, backend/database.py

Learning Notes:
- Concepts: Binary Search, STL Vector
- Challenges: Off-by-one errors with indexes
- Insights: Think in intervals instead of index offsets
""",
            generation_status="generated"
        )
        session.add(daily_log)
        session.commit()  # commit to generate ID for drafts

        print("Seeding generated drafts...")
        drafts = [
            GeneratedContent(
                daily_log_id=daily_log.id,
                content_type="summary",
                content="Today, I worked on setting up the webhook parser and SQLite database logic for DevLog-AI. I also studied Binary Search and STL Vectors, realizing it is more intuitive to think in terms of intervals to avoid indexing off-by-one errors.",
                model_used="gemini-2.5-flash",
                generation_version="v1"
            ),
            GeneratedContent(
                daily_log_id=daily_log.id,
                content_type="linkedin",
                content="""🚀 DevLog Day 1: Setup and Algorithms

Today, I laid down the foundations for DevLog-AI by writing the GitHub webhook listener and setting up SQLite.

🧠 Learning update:
Spent time reviewing Binary Search. Off-by-one errors are a classic trap. My biggest insight today was to shift my mental model—thinking about search spaces as intervals rather than raw indices makes the logic much cleaner and less error-prone.

Onto the next challenge tomorrow!

#developer #learninginpublic #algorithms #fastapi""",
                model_used="gemini-2.5-flash",
                generation_version="v1"
            ),
            GeneratedContent(
                daily_log_id=daily_log.id,
                content_type="twitter",
                content="Spent today setting up the webhook receiver & SQLite config for my DevLog project. Also brushed up on Binary Search and STL Vectors. Key takeaway: think in intervals to solve indexing bugs. #learninginpublic",
                model_used="gemini-2.5-flash",
                generation_version="v1"
            )
        ]
        session.add_all(drafts)
        session.commit()

        print("Database seeding completed successfully.")

    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()
