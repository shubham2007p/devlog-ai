from datetime import date, datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.notes import LearningNote
from backend.models.evidence import Evidence
from backend.schemas.notes import NoteCreate, NoteUpdate
from backend.utils.logger import get_logger

logger = get_logger("notes_service")

def create_note(db: Session, note_data: NoteCreate) -> LearningNote:
    # Use provided date, or default to current date
    note_date = note_data.date if note_data.date else date.today()
    
    db_note = LearningNote(
        date=note_date,
        concepts_learned=note_data.concepts_learned,
        challenges_faced=note_data.challenges_faced or "",
        key_insights=note_data.key_insights or "",
        resources_used=note_data.resources_used or "",
        additional_notes=note_data.additional_notes or ""
    )
    db.add(db_note)
    db.flush()  # Populates db_note.id
    
    # Create corresponding timeline evidence record (TASK-034)
    first_line_concept = note_data.concepts_learned.split("\n")[0] if note_data.concepts_learned else ""
    title = f"Learned: {first_line_concept[:50]}"
    
    # Combine content fields into a structured details text
    content_parts = [
        f"Concepts Learned: {note_data.concepts_learned}"
    ]
    if note_data.challenges_faced:
        content_parts.append(f"Challenges Faced: {note_data.challenges_faced}")
    if note_data.key_insights:
        content_parts.append(f"Key Insights: {note_data.key_insights}")
    if note_data.resources_used:
        content_parts.append(f"Resources Used: {note_data.resources_used}")
    if note_data.additional_notes:
        content_parts.append(f"Additional Notes: {note_data.additional_notes}")
    content = "\n".join(content_parts)
    
    # Combine note date with current UTC time to keep it accurate for chronological sorting
    utc_now_time = datetime.now(timezone.utc).time()
    event_time = datetime.combine(note_date, utc_now_time)
    
    db_evidence = Evidence(
        source="manual_note",
        event_type="learning_note",
        title=title,
        content=content,
        event_metadata={"note_id": db_note.id},
        event_time=event_time
    )
    db.add(db_evidence)
    db.commit()
    db.refresh(db_note)
    logger.info(f"Created note ID {db_note.id} and linked evidence record.")
    return db_note

def get_note_by_id(db: Session, note_id: int) -> Optional[LearningNote]:
    return db.query(LearningNote).filter(LearningNote.id == note_id).first()

def get_all_notes(db: Session, date_filter: Optional[date] = None) -> List[LearningNote]:
    query = db.query(LearningNote)
    if date_filter:
        query = query.filter(LearningNote.date == date_filter)
    return query.all()

def update_note(db: Session, note_id: int, note_data: NoteUpdate) -> Optional[LearningNote]:
    db_note = get_note_by_id(db, note_id)
    if not db_note:
        return None
    
    # Update note fields
    if note_data.concepts_learned is not None:
        db_note.concepts_learned = note_data.concepts_learned
    if note_data.challenges_faced is not None:
        db_note.challenges_faced = note_data.challenges_faced
    if note_data.key_insights is not None:
        db_note.key_insights = note_data.key_insights
    if note_data.resources_used is not None:
        db_note.resources_used = note_data.resources_used
    if note_data.additional_notes is not None:
        db_note.additional_notes = note_data.additional_notes
    if note_data.date is not None:
        db_note.date = note_data.date

    # Update corresponding evidence record
    evidence_records = db.query(Evidence).filter(
        Evidence.source == "manual_note",
        Evidence.event_type == "learning_note"
    ).all()
    
    db_evidence = None
    for ev in evidence_records:
        if ev.event_metadata and ev.event_metadata.get("note_id") == note_id:
            db_evidence = ev
            break
            
    if db_evidence:
        first_line_concept = db_note.concepts_learned.split("\n")[0] if db_note.concepts_learned else ""
        db_evidence.title = f"Learned: {first_line_concept[:50]}"
        
        content_parts = [
            f"Concepts Learned: {db_note.concepts_learned}"
        ]
        if db_note.challenges_faced:
            content_parts.append(f"Challenges Faced: {db_note.challenges_faced}")
        if db_note.key_insights:
            content_parts.append(f"Key Insights: {db_note.key_insights}")
        if db_note.resources_used:
            content_parts.append(f"Resources Used: {db_note.resources_used}")
        if db_note.additional_notes:
            content_parts.append(f"Additional Notes: {db_note.additional_notes}")
        db_evidence.content = "\n".join(content_parts)
        
        # Keep original event time but adjust date if the note's date was modified
        orig_time = db_evidence.event_time.time() if db_evidence.event_time else datetime.now(timezone.utc).time()
        db_evidence.event_time = datetime.combine(db_note.date, orig_time)
        db.add(db_evidence)
        
    db_note.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    logger.info(f"Updated note ID {db_note.id} and synchronized evidence record.")
    return db_note

def delete_note(db: Session, note_id: int) -> bool:
    db_note = get_note_by_id(db, note_id)
    if not db_note:
        return False
        
    # Delete matching evidence record
    evidence_records = db.query(Evidence).filter(
        Evidence.source == "manual_note",
        Evidence.event_type == "learning_note"
    ).all()
    
    for ev in evidence_records:
        if ev.event_metadata and ev.event_metadata.get("note_id") == note_id:
            db.delete(ev)
            break
            
    db.delete(db_note)
    db.commit()
    logger.info(f"Deleted note ID {note_id} and its linked evidence record.")
    return True
