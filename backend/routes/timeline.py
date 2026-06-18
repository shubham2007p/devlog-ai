from datetime import date as date_type
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.timeline import TimelineEvent
from backend.services import timeline_service
from backend.utils.logger import get_logger

router = APIRouter()
logger = get_logger("timeline_route")

@router.get("/timeline/today")
def get_today_timeline(db: Session = Depends(get_db)):
    """
    GET /timeline/today
    Retrieve the timeline events for today.
    """
    try:
        # Get current date in UTC to match database event_time timezone
        today_date = datetime.now(timezone.utc).date()
        events = timeline_service.get_timeline_events(db, today_date)
        
        timeline_dto = [
            TimelineEvent(
                type=ev.event_type,
                title=ev.title,
                time=ev.event_time.strftime("%H:%M") if ev.event_time else "00:00"
            )
            for ev in events
        ]
        return {
            "success": True,
            "data": timeline_dto
        }
    except Exception as e:
        logger.error(f"Error fetching today's timeline: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Failed to fetch today's timeline"
                }
            }
        )

@router.get("/timeline/{date}")
def get_timeline_by_date(date: date_type, db: Session = Depends(get_db)):
    """
    GET /timeline/{date}
    Retrieve the timeline events for a specific date (YYYY-MM-DD).
    """
    try:
        events = timeline_service.get_timeline_events(db, date)
        
        timeline_dto = [
            TimelineEvent(
                type=ev.event_type,
                title=ev.title,
                time=ev.event_time.strftime("%H:%M") if ev.event_time else "00:00"
            )
            for ev in events
        ]
        return {
            "success": True,
            "data": timeline_dto
        }
    except Exception as e:
        logger.error(f"Error fetching timeline for date {date}: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": f"Failed to fetch timeline for {date}"
                }
            }
        )
