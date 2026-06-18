from datetime import date, datetime, time
from typing import List
from sqlalchemy.orm import Session
from backend.models.evidence import Evidence
from backend.utils.logger import get_logger

logger = get_logger("timeline_service")

def get_timeline_events(db: Session, query_date: date) -> List[Evidence]:
    """
    Fetch all evidence events for a specific date and sort them chronologically.
    """
    start_dt = datetime.combine(query_date, time.min)
    end_dt = datetime.combine(query_date, time.max)
    
    logger.info(f"Fetching timeline events between {start_dt} and {end_dt} for date {query_date}")
    
    events = db.query(Evidence).filter(
        Evidence.event_time >= start_dt,
        Evidence.event_time <= end_dt
    ).order_by(Evidence.event_time.asc()).all()
    
    return events
