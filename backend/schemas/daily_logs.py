from datetime import date as date_type, datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict

class DailyCommitInfo(BaseModel):
    sha: str = Field(..., description="Commit SHA hash")
    repo: str = Field(..., description="Repository name")
    branch: str = Field(..., description="Branch name")
    message: str = Field(..., description="Commit message")
    author: str = Field(..., description="Author name")
    files_changed: List[str] = Field(default_factory=list, description="Files changed in this commit")
    timestamp: datetime = Field(..., description="Commit timestamp")

    model_config = ConfigDict(from_attributes=True)

class DailyNoteInfo(BaseModel):
    id: int = Field(..., description="Note ID")
    concepts_learned: str = Field(..., description="Concepts learned")
    challenges_faced: str = Field(..., description="Challenges faced")
    key_insights: str = Field(..., description="Key insights")
    resources_used: str = Field(..., description="Resources used")
    additional_notes: str = Field(..., description="Additional notes")

    model_config = ConfigDict(from_attributes=True)

class DailyEvidenceInfo(BaseModel):
    id: int = Field(..., description="Evidence record ID")
    source: str = Field(..., description="Event source e.g. github, manual_note")
    event_type: str = Field(..., description="Event type e.g. commit, learning_note")
    title: str = Field(..., description="Title of the activity")
    content: str = Field(..., description="Details of the activity")
    event_time: datetime = Field(..., description="Event timestamp")

    model_config = ConfigDict(from_attributes=True)

class DailyContext(BaseModel):
    date: date_type = Field(..., description="The date for this daily context")
    summary: Dict[str, int] = Field(..., description="Counts of commits, notes, and evidence")
    commits: List[DailyCommitInfo] = Field(default_factory=list, description="Commits for this day")
    notes: List[DailyNoteInfo] = Field(default_factory=list, description="Notes for this day")
    evidence: List[DailyEvidenceInfo] = Field(default_factory=list, description="Evidence timeline events for this day")

    model_config = ConfigDict(from_attributes=True)

class DailyLogGenerateRequest(BaseModel):
    date: Optional[date_type] = Field(None, description="Optional target date for generation, defaults to today's date")

class DailyLogGenerateResponse(BaseModel):
    daily_log_id: int = Field(..., description="Generated daily log record ID")

class DailyLogTodayResponse(BaseModel):
    context: str = Field(..., description="JSON string representation of DailyContext")
