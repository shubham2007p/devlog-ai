from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base

class Evidence(Base):
    """
    Polymorphic universal timeline events evidence table.
    """
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String, nullable=False)  # e.g., 'github', 'manual_note'
    event_type: Mapped[str] = mapped_column(String, nullable=False)  # e.g., 'commit', 'learning_note'
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Map the python attribute 'event_metadata' to DB column 'metadata' to avoid base collision.
    event_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column("metadata", JSON, nullable=True)
    
    event_time: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
