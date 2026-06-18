from datetime import date as date_type
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base

class DailyLog(Base):
    """
    Stores the daily contexts constructed automatically or manually.
    """
    __tablename__ = "daily_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    log_date: Mapped[date_type] = mapped_column(Date, unique=True, index=True, nullable=False)
    evidence_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    commit_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    notes_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    compiled_context: Mapped[str] = mapped_column(Text, nullable=False)
    generation_status: Mapped[str] = mapped_column(String, default="pending", nullable=False)  # pending, generated, failed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    generated_contents: Mapped[List["GeneratedContent"]] = relationship(
        "GeneratedContent", 
        back_populates="daily_log", 
        cascade="all, delete-orphan"
    )
    generation_runs: Mapped[List["GenerationRun"]] = relationship(
        "GenerationRun", 
        back_populates="daily_log", 
        cascade="all, delete-orphan"
    )


class GeneratedContent(Base):
    """
    Stores the AI-generated summaries and platform drafts (LinkedIn/Twitter).
    """
    __tablename__ = "generated_content"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    daily_log_id: Mapped[int] = mapped_column(ForeignKey("daily_logs.id"), nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)  # e.g., 'summary', 'linkedin', 'twitter'
    content: Mapped[str] = mapped_column(Text, nullable=False)
    model_used: Mapped[str] = mapped_column(String, nullable=False)  # e.g., 'gemini-2.5-flash'
    generation_version: Mapped[str] = mapped_column(String, nullable=False)  # e.g., 'v1'
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    daily_log: Mapped["DailyLog"] = relationship("DailyLog", back_populates="generated_contents")
    feedbacks: Mapped[List["DraftFeedback"]] = relationship(
        "DraftFeedback", 
        back_populates="generated_content", 
        cascade="all, delete-orphan"
    )


class GenerationRun(Base):
    """
    Tracks AI request execution statistics and status for transparency/debugging.
    """
    __tablename__ = "generation_runs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    daily_log_id: Mapped[int] = mapped_column(ForeignKey("daily_logs.id"), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String, nullable=False)
    model_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)  # e.g., 'success', 'failed'
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    daily_log: Mapped["DailyLog"] = relationship("DailyLog", back_populates="generation_runs")


class DraftFeedback(Base):
    """
    Tracks changes or interactions performed on generated drafts.
    """
    __tablename__ = "draft_feedback"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    generated_content_id: Mapped[int] = mapped_column(ForeignKey("generated_content.id"), nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)  # e.g., 'approved', 'edited', 'regenerated'
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    generated_content: Mapped["GeneratedContent"] = relationship("GeneratedContent", back_populates="feedbacks")
