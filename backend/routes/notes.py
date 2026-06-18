from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.notes import NoteCreate, NoteUpdate, NoteResponse
from backend.services import notes_service
from backend.utils.logger import get_logger

router = APIRouter()
logger = get_logger("notes_route")

@router.post("/notes", status_code=status.HTTP_201_CREATED)
def create_new_note(note_data: NoteCreate, db: Session = Depends(get_db)):
    """
    POST /notes
    Create a new learning note and generate its evidence log.
    """
    try:
        db_note = notes_service.create_note(db, note_data)
        return {
            "success": True,
            "data": {
                "note_id": db_note.id
            }
        }
    except Exception as e:
        logger.error(f"Error creating note: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": "Failed to create learning note"
                }
            }
        )

@router.get("/notes")
def get_notes(
    date: Optional[date] = Query(None, description="Filter notes by date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    GET /notes
    Retrieve all learning notes, optionally filtered by date.
    """
    try:
        notes = notes_service.get_all_notes(db, date)
        note_responses = [NoteResponse.model_validate(note) for note in notes]
        return {
            "success": True,
            "data": note_responses
        }
    except Exception as e:
        logger.error(f"Error retrieving notes: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Failed to retrieve learning notes"
                }
            }
        )

@router.get("/notes/{id}")
def get_note(id: int, db: Session = Depends(get_db)):
    """
    GET /notes/{id}
    Retrieve a single learning note by ID.
    """
    db_note = notes_service.get_note_by_id(db, id)
    if not db_note:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Note with ID {id} not found"
                }
            }
        )
    return {
        "success": True,
        "data": NoteResponse.model_validate(db_note)
    }

@router.put("/notes/{id}")
def update_existing_note(id: int, note_data: NoteUpdate, db: Session = Depends(get_db)):
    """
    PUT /notes/{id}
    Update a learning note by ID.
    """
    try:
        db_note = notes_service.update_note(db, id, note_data)
        if not db_note:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f"Note with ID {id} not found"
                    }
                }
            )
        return {
            "success": True
        }
    except Exception as e:
        logger.error(f"Error updating note ID {id}: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": "Failed to update learning note"
                }
            }
        )

@router.delete("/notes/{id}")
def delete_existing_note(id: int, db: Session = Depends(get_db)):
    """
    DELETE /notes/{id}
    Delete a learning note by ID.
    """
    try:
        success = notes_service.delete_note(db, id)
        if not success:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f"Note with ID {id} not found"
                    }
                }
            )
        return {
            "success": True
        }
    except Exception as e:
        logger.error(f"Error deleting note ID {id}: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": "Failed to delete learning note"
                }
            }
        )
