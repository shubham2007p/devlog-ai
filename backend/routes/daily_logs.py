from datetime import date as date_type
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.daily_logs import (
    DailyLogGenerateRequest,
    DailyLogGenerateResponse,
    DailyLogTodayResponse
)
from backend.services import context_builder
from backend.models.drafts import DailyLog
from backend.utils.logger import get_logger

router = APIRouter()
logger = get_logger("daily_logs_route")

@router.post("/daily-log/generate", response_model=None, status_code=status.HTTP_200_OK)
def generate_daily_log(
    payload: DailyLogGenerateRequest = None,
    db: Session = Depends(get_db)
):
    """
    POST /daily-log/generate
    Compile activities (notes, commits, timeline evidence) for a specific date (defaults to today)
    into a structured daily context log and save/update it.
    """
    try:
        # Use target date from payload if provided, otherwise default to current local date
        target_date = payload.date if (payload and payload.date) else date_type.today()
        
        logger.info(f"Triggering daily log generation for {target_date}")
        db_log = context_builder.build_daily_context(db, target_date)
        
        return {
            "success": True,
            "data": {
                "daily_log_id": db_log.id
            }
        }
    except Exception as e:
        logger.error(f"Error generating daily log: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": f"Failed to generate daily log: {str(e)}"
                }
            }
        )

@router.get("/daily-log/today", response_model=None)
def get_today_daily_log(db: Session = Depends(get_db)):
    """
    GET /daily-log/today
    Retrieve today's compiled context. Returns 404 if not yet generated.
    """
    try:
        today_date = date_type.today()
        logger.info(f"Retrieving today's daily log context ({today_date})")
        
        db_log = db.query(DailyLog).filter(DailyLog.log_date == today_date).first()
        if not db_log:
            logger.warning(f"No daily log record found for {today_date}")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f"Daily log for today ({today_date}) not found. Please generate it first."
                    }
                }
            )
            
        return {
            "success": True,
            "data": {
                "context": db_log.compiled_context
            }
        }
    except Exception as e:
        logger.error(f"Error fetching today's daily log: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Failed to retrieve today's daily log"
                }
            }
        )

@router.get("/daily-log/{date}", response_model=None)
def get_historical_daily_log(date: date_type, db: Session = Depends(get_db)):
    """
    GET /daily-log/{date}
    Retrieve historical log context for a specific date (YYYY-MM-DD). Returns 404 if not found.
    """
    try:
        logger.info(f"Retrieving daily log context for {date}")
        
        db_log = db.query(DailyLog).filter(DailyLog.log_date == date).first()
        if not db_log:
            logger.warning(f"No daily log record found for date {date}")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f"Daily log for date {date} not found"
                    }
                }
            )
            
        return {
            "success": True,
            "data": {
                "context": db_log.compiled_context
            }
        }
    except Exception as e:
        logger.error(f"Error fetching daily log for date {date}: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": f"Failed to retrieve daily log for {date}"
                }
            }
        )
