from datetime import date as date_type
from datetime import datetime
from sqlalchemy import Date, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base

class LearningNote(Base):
    """
    Stores manual user learning inputs and notes.
    """
    __tablename__ = "learning_notes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[date_type] = mapped_column(Date, index=True, nullable=False)
    concepts_learned: Mapped[str] = mapped_column(Text, nullable=False)
    challenges_faced: Mapped[str] = mapped_column(Text, nullable=False)
    key_insights: Mapped[str] = mapped_column(Text, nullable=False)
    resources_used: Mapped[str] = mapped_column(Text, nullable=False)
    additional_notes: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )
