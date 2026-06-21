from datetime import date as date_type, datetime, time
from typing import List
from sqlalchemy.orm import Session
from backend.models.commits import GitHubCommit
from backend.models.notes import LearningNote
from backend.models.evidence import Evidence
from backend.models.drafts import DailyLog
from backend.schemas.daily_logs import DailyContext, DailyCommitInfo, DailyNoteInfo, DailyEvidenceInfo
from backend.services import timeline_service, notes_service
from backend.utils.logger import get_logger

logger = get_logger("context_builder_service")

def fetch_daily_notes(db: Session, target_date: date_type) -> List[LearningNote]:
    """
    Fetch all manual notes created on the specified date.
    """
    logger.info(f"Fetching notes for date: {target_date}")
    return notes_service.get_all_notes(db, date_filter=target_date)

def fetch_daily_commits(db: Session, target_date: date_type) -> List[GitHubCommit]:
    """
    Fetch all GitHub commits pushed on the specified date (UTC boundary 00:00 to 23:59).
    """
    start_dt = datetime.combine(target_date, time.min)
    end_dt = datetime.combine(target_date, time.max)
    logger.info(f"Fetching commits between {start_dt} and {end_dt}")
    return db.query(GitHubCommit).filter(
        GitHubCommit.timestamp >= start_dt,
        GitHubCommit.timestamp <= end_dt
    ).order_by(GitHubCommit.timestamp.asc()).all()

def fetch_daily_evidence(db: Session, target_date: date_type) -> List[Evidence]:
    """
    Fetch all chronological timeline evidence events for the specified date.
    """
    logger.info(f"Fetching timeline evidence for date: {target_date}")
    return timeline_service.get_timeline_events(db, target_date)

def generate_daily_context(
    db: Session,
    target_date: date_type,
    notes: List[LearningNote],
    commits: List[GitHubCommit],
    evidence: List[Evidence]
) -> DailyContext:
    """
    Assemble notes, commits, and timeline evidence into a structured DailyContext DTO.
    """
    logger.info(f"Generating structured daily context for {target_date}")
    
    commit_infos = [
        DailyCommitInfo(
            sha=c.commit_sha,
            repo=c.repo_name,
            branch=c.branch_name,
            message=c.commit_message,
            author=c.author_name,
            files_changed=c.files_changed,
            timestamp=c.timestamp
        )
        for c in commits
    ]
    
    note_infos = [
        DailyNoteInfo(
            id=n.id,
            concepts_learned=n.concepts_learned,
            challenges_faced=n.challenges_faced or "",
            key_insights=n.key_insights or "",
            resources_used=n.resources_used or "",
            additional_notes=n.additional_notes or ""
        )
        for n in notes
    ]
    
    evidence_infos = [
        DailyEvidenceInfo(
            id=e.id,
            source=e.source,
            event_type=e.event_type,
            title=e.title,
            content=e.content,
            event_time=e.event_time
        )
        for e in evidence
    ]
    
    return DailyContext(
        date=target_date,
        summary={
            "commit_count": len(commits),
            "notes_count": len(notes),
            "evidence_count": len(evidence)
        },
        commits=commit_infos,
        notes=note_infos,
        evidence=evidence_infos
    )

def store_daily_log(db: Session, target_date: date_type, context: DailyContext) -> DailyLog:
    """
    Persist or update the compiled DailyContext JSON in the daily_logs table.
    Ensures that generating context is idempotent for any given date.
    """
    logger.info(f"Storing daily log context for {target_date} in the database")
    
    # Check if a log for this date already exists (unique date constraint)
    db_log = db.query(DailyLog).filter(DailyLog.log_date == target_date).first()
    compiled_context_str = context.model_dump_json()
    
    if db_log:
        logger.info(f"Daily log for {target_date} already exists. Overwriting with fresh context.")
        db_log.evidence_count = context.summary["evidence_count"]
        db_log.commit_count = context.summary["commit_count"]
        db_log.notes_count = context.summary["notes_count"]
        db_log.compiled_context = compiled_context_str
        db_log.generation_status = "pending"  # reset status to pending when rebuilt
    else:
        logger.info(f"Creating new daily log record for {target_date}.")
        db_log = DailyLog(
            log_date=target_date,
            evidence_count=context.summary["evidence_count"],
            commit_count=context.summary["commit_count"],
            notes_count=context.summary["notes_count"],
            compiled_context=compiled_context_str,
            generation_status="pending"
        )
        db.add(db_log)
        
    try:
        db.commit()
        db.refresh(db_log)
        return db_log
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while saving daily log for {target_date}: {e}")
        raise e

def build_daily_context(db: Session, target_date: date_type) -> DailyLog:
    """
    Coordinates context building for the specified target date.
    Retrieves all records, constructs structured DailyContext object, and stores it.
    """
    logger.info(f"Executing build_daily_context pipeline for {target_date}")
    notes = fetch_daily_notes(db, target_date)
    commits = fetch_daily_commits(db, target_date)
    evidence = fetch_daily_evidence(db, target_date)
    context = generate_daily_context(db, target_date, notes, commits, evidence)
    return store_daily_log(db, target_date, context)
