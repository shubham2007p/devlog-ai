from datetime import date as date_type
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class NoteBase(BaseModel):
    concepts_learned: str = Field(..., min_length=3, description="Core concepts learned today")
    challenges_faced: Optional[str] = ""
    key_insights: Optional[str] = ""
    resources_used: Optional[str] = ""
    additional_notes: Optional[str] = ""
    date: Optional[date_type] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    concepts_learned: Optional[str] = Field(None, min_length=3, description="Core concepts learned today")
    challenges_faced: Optional[str] = None
    key_insights: Optional[str] = None
    resources_used: Optional[str] = None
    additional_notes: Optional[str] = None
    date: Optional[date_type] = None

class NoteResponse(BaseModel):
    id: int
    date: date_type
    concepts_learned: str
    challenges_faced: str
    key_insights: str
    resources_used: str
    additional_notes: str

    model_config = ConfigDict(from_attributes=True)
