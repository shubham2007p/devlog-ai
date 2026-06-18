from pydantic import BaseModel, Field

class TimelineEvent(BaseModel):
    type: str = Field(..., description="Type of event, e.g. commit or learning_note")
    title: str = Field(..., description="Short descriptive title of the activity")
    time: str = Field(..., description="Formatted event timestamp (HH:MM)")

    model_config = {
        "from_attributes": True
    }
