from datetime import date, datetime
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import SessionLocal
from backend.models.notes import LearningNote
from backend.models.evidence import Evidence

client = TestClient(app)

def test_create_note_success():
    """
    Test successful creation of a learning note and verification of corresponding evidence logs.
    """
    db = SessionLocal()
    payload = {
        "concepts_learned": "Quick Sort Algorithm",
        "challenges_faced": "Choosing the right pivot element",
        "key_insights": "Randomized pivot achieves O(n log n) expected time",
        "resources_used": "CLRS Book Chapter 7",
        "additional_notes": "Implement randomized quicksort tomorrow",
        "date": "2026-06-19"
    }

    # Send POST request
    response = client.post("/notes", json=payload)
    
    assert response.status_code == 201
    assert response.json()["success"] is True
    note_id = response.json()["data"]["note_id"]
    assert note_id is not None

    try:
        # Assert database persistence in learning_notes table
        note_record = db.query(LearningNote).filter_by(id=note_id).first()
        assert note_record is not None
        assert note_record.concepts_learned == "Quick Sort Algorithm"
        assert note_record.challenges_faced == "Choosing the right pivot element"
        assert note_record.key_insights == "Randomized pivot achieves O(n log n) expected time"
        assert note_record.resources_used == "CLRS Book Chapter 7"
        assert note_record.additional_notes == "Implement randomized quicksort tomorrow"
        assert note_record.date == date(2026, 6, 19)

        # Assert corresponding evidence log entry (TASK-034)
        evidence_records = db.query(Evidence).filter(
            Evidence.source == "manual_note",
            Evidence.event_type == "learning_note"
        ).all()
        
        matching_evidence = None
        for ev in evidence_records:
            if ev.event_metadata and ev.event_metadata.get("note_id") == note_id:
                matching_evidence = ev
                break
                
        assert matching_evidence is not None
        assert matching_evidence.title == "Learned: Quick Sort Algorithm"
        assert "Quick Sort Algorithm" in matching_evidence.content
        assert "CLRS Book Chapter 7" in matching_evidence.content
        assert matching_evidence.event_time.date() == date(2026, 6, 19)
        
    finally:
        # Clean up
        if note_record:
            db.delete(note_record)
        if matching_evidence:
            db.delete(matching_evidence)
        db.commit()
        db.close()


def test_create_note_validation_error():
    """
    Test schema validation error when concepts_learned is shorter than 3 characters.
    """
    payload = {
        "concepts_learned": "Go",  # Length < 3
        "challenges_faced": "None"
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 422  # FastAPI validation error
    assert "detail" in response.json()


def test_get_notes():
    """
    Test retrieving all notes and filtering by date.
    """
    db = SessionLocal()
    
    note1 = LearningNote(
        date=date(2026, 6, 18),
        concepts_learned=f"Temp Note One",
        challenges_faced="",
        key_insights="",
        resources_used="",
        additional_notes=""
    )
    note2 = LearningNote(
        date=date(2026, 6, 19),
        concepts_learned=f"Temp Note Two",
        challenges_faced="",
        key_insights="",
        resources_used="",
        additional_notes=""
    )
    db.add(note1)
    db.add(note2)
    db.commit()
    
    try:
        # Get all notes
        res_all = client.get("/notes")
        assert res_all.status_code == 200
        assert res_all.json()["success"] is True
        notes_list = res_all.json()["data"]
        assert len(notes_list) >= 2
        
        # Filter by date
        res_filtered = client.get("/notes?date=2026-06-18")
        assert res_filtered.status_code == 200
        filtered_list = res_filtered.json()["data"]
        # Ensure only the note matching the date is returned
        for note in filtered_list:
            assert note["date"] == "2026-06-18"
            
    finally:
        db.delete(note1)
        db.delete(note2)
        db.commit()
        db.close()


def test_get_note_by_id():
    """
    Test retrieving a single note by ID and raising 404 for non-existent ones.
    """
    db = SessionLocal()
    note = LearningNote(
        date=date(2026, 6, 19),
        concepts_learned="Retrieved Note",
        challenges_faced="",
        key_insights="",
        resources_used="",
        additional_notes=""
    )
    db.add(note)
    db.commit()
    
    try:
        # Success check
        res_success = client.get(f"/notes/{note.id}")
        assert res_success.status_code == 200
        assert res_success.json()["success"] is True
        assert res_success.json()["data"]["concepts_learned"] == "Retrieved Note"
        
        # 404 check
        res_fail = client.get("/notes/999999")
        assert res_fail.status_code == 404
        assert res_fail.json()["success"] is False
        assert res_fail.json()["error"]["code"] == "NOT_FOUND"
        
    finally:
        db.delete(note)
        db.commit()
        db.close()


def test_update_note():
    """
    Test updating an existing note and verifying evidence sync.
    """
    db = SessionLocal()
    
    # 1. Create a note and evidence
    payload = {
        "concepts_learned": "Red Black Trees",
        "challenges_faced": "Rotation operations",
        "key_insights": "Insights...",
        "resources_used": "CLRS",
        "additional_notes": "",
        "date": "2026-06-19"
    }
    create_res = client.post("/notes", json=payload)
    note_id = create_res.json()["data"]["note_id"]
    
    # 2. Update it
    update_payload = {
        "concepts_learned": "Red Black Trees - Edited",
        "challenges_faced": "Rotation operations resolved",
        "date": "2026-06-20"
    }
    
    try:
        update_res = client.put(f"/notes/{note_id}", json=update_payload)
        assert update_res.status_code == 200
        assert update_res.json()["success"] is True
        
        # Verify database fields updated
        note_record = db.query(LearningNote).filter_by(id=note_id).first()
        assert note_record.concepts_learned == "Red Black Trees - Edited"
        assert note_record.challenges_faced == "Rotation operations resolved"
        assert note_record.date == date(2026, 6, 20)
        
        # Verify corresponding evidence title & content updated
        evidence_records = db.query(Evidence).filter(
            Evidence.source == "manual_note",
            Evidence.event_type == "learning_note"
        ).all()
        
        matching_evidence = None
        for ev in evidence_records:
            if ev.event_metadata and ev.event_metadata.get("note_id") == note_id:
                matching_evidence = ev
                break
                
        assert matching_evidence is not None
        assert matching_evidence.title == "Learned: Red Black Trees - Edited"
        assert "Rotation operations resolved" in matching_evidence.content
        assert matching_evidence.event_time.date() == date(2026, 6, 20)
        
    finally:
        # Cleanup
        note_record = db.query(LearningNote).filter_by(id=note_id).first()
        if note_record:
            db.delete(note_record)
        evidence_records = db.query(Evidence).filter(
            Evidence.source == "manual_note",
            Evidence.event_type == "learning_note"
        ).all()
        for ev in evidence_records:
            if ev.event_metadata and ev.event_metadata.get("note_id") == note_id:
                db.delete(ev)
        db.commit()
        db.close()


def test_delete_note():
    """
    Test deleting a note and verifying evidence is also deleted.
    """
    db = SessionLocal()
    
    payload = {
        "concepts_learned": "Merge Sort",
        "challenges_faced": "",
        "key_insights": "",
        "resources_used": "",
        "additional_notes": "",
        "date": "2026-06-19"
    }
    create_res = client.post("/notes", json=payload)
    note_id = create_res.json()["data"]["note_id"]
    
    try:
        # Delete note
        delete_res = client.delete(f"/notes/{note_id}")
        assert delete_res.status_code == 200
        assert delete_res.json()["success"] is True
        
        # Verify database fields deleted
        note_record = db.query(LearningNote).filter_by(id=note_id).first()
        assert note_record is None
        
        # Verify corresponding evidence deleted
        evidence_records = db.query(Evidence).filter(
            Evidence.source == "manual_note",
            Evidence.event_type == "learning_note"
        ).all()
        
        matching_evidence = None
        for ev in evidence_records:
            if ev.event_metadata and ev.event_metadata.get("note_id") == note_id:
                matching_evidence = ev
                break
        assert matching_evidence is None
        
    finally:
        # Cleanup if needed
        note_record = db.query(LearningNote).filter_by(id=note_id).first()
        if note_record:
            db.delete(note_record)
        evidence_records = db.query(Evidence).filter(
            Evidence.source == "manual_note",
            Evidence.event_type == "learning_note"
        ).all()
        for ev in evidence_records:
            if ev.event_metadata and ev.event_metadata.get("note_id") == note_id:
                db.delete(ev)
        db.commit()
        db.close()
