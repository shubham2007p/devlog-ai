from datetime import datetime
from typing import List
from sqlalchemy import String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base

class GitHubCommit(Base):
    """
    Stores detailed commit information from webhook events.
    """
    __tablename__ = "github_commits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    commit_sha: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    repo_name: Mapped[str] = mapped_column(String, nullable=False)
    branch_name: Mapped[str] = mapped_column(String, nullable=False)
    commit_message: Mapped[str] = mapped_column(Text, nullable=False)
    commit_url: Mapped[str] = mapped_column(String, nullable=False)
    author_name: Mapped[str] = mapped_column(String, nullable=False)
    files_changed: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
