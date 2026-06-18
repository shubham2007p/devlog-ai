from backend.database import SessionLocal
from backend.models.commits import GitHubCommit

def test_query_seeded_commit():
    """
    Assert that the seeded commit data is retrievable from SQLite using SQLAlchemy model mapping.
    """
    db = SessionLocal()
    try:
        commit = db.query(GitHubCommit).filter_by(
            commit_sha="a1b2c3d4e5f678901234567890abcdef12345678"
        ).first()
        
        assert commit is not None
        assert commit.repo_name == "DevLog-AI"
        assert commit.author_name == "Shubh"
        assert "backend/database.py" in commit.files_changed
    finally:
        db.close()
