import json
from datetime import date, datetime, time, timezone
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import SessionLocal
from backend.models.commits import GitHubCommit
from backend.models.notes import LearningNote
from backend.models.evidence import Evidence
from backend.models.drafts import DailyLog

client = TestClient(app)

def cleanup_date_data(db, target_date: date):
    """Helper to clean up any test records on the target date."""
    # Delete daily logs
    db.query(DailyLog).filter(DailyLog.log_date == target_date).delete()
    
    # Delete commits
    start_dt = datetime.combine(target_date, time.min)
    end_dt = datetime.combine(target_date, time.max)
    db.query(GitHubCommit).filter(
        GitHubCommit.timestamp >= start_dt,
        GitHubCommit.timestamp <= end_dt
    ).delete()
    
    # Delete learning notes
    db.query(LearningNote).filter(LearningNote.date == target_date).delete()
    
    # Delete evidence
    db.query(Evidence).filter(
        Evidence.event_time >= start_dt,
        Evidence.event_time <= end_dt
    ).delete()
    db.commit()

def test_generate_daily_log_empty():
    """
    Test generating a daily log for a date with no developer activity or notes.
    """
    db = SessionLocal()
    target_date = date(2026, 6, 25)
    cleanup_date_data(db, target_date)
    db.close()

    try:
        # POST generate
        response = client.post("/daily-log/generate", json={"date": target_date.isoformat()})
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["success"] is True
        log_id = res_json["data"]["daily_log_id"]
        assert log_id is not None
        
        # GET by date
        get_res = client.get(f"/daily-log/{target_date.isoformat()}")
        assert get_res.status_code == 200
        get_json = get_res.json()
        assert get_json["success"] is True
        
        context_data = json.loads(get_json["data"]["context"])
        assert context_data["date"] == target_date.isoformat()
        assert context_data["summary"]["commit_count"] == 0
        assert context_data["summary"]["notes_count"] == 0
        assert context_data["summary"]["evidence_count"] == 0
        assert len(context_data["commits"]) == 0
        assert len(context_data["notes"]) == 0
        assert len(context_data["evidence"]) == 0

    finally:
        db = SessionLocal()
        cleanup_date_data(db, target_date)
        db.close()

def test_generate_daily_log_with_activities():
    """
    Test generating daily context log compiling commits, notes, and timeline evidence.
    """
    db = SessionLocal()
    target_date = date(2026, 6, 26)
    cleanup_date_data(db, target_date)
    
    # 1. Setup commit
    commit_time = datetime.combine(target_date, time(11, 0))
    commit = GitHubCommit(
        commit_sha="testsha1234567890",
        repo_name="test-repo",
        branch_name="main",
        commit_message="Refactor auth pipeline",
        commit_url="https://github.com/test/repo/commit/testsha1234567890",
        author_name="test-author",
        files_changed=["auth.py", "main.py"],
        timestamp=commit_time
    )
    db.add(commit)
    
    # 2. Setup learning note
    note = LearningNote(
        date=target_date,
        concepts_learned="OAuth2 Flows",
        challenges_faced="Token expiration handling",
        key_insights="Use refresh token flow",
        resources_used="RFC 6749",
        additional_notes="Implement tomorrow"
    )
    db.add(note)
    
    # 3. Setup separate evidence timeline records
    evidence1 = Evidence(
        source="github",
        event_type="commit",
        title="Commit: Refactor auth pipeline",
        content="Refactor auth pipeline in main",
        event_time=commit_time
    )
    evidence2 = Evidence(
        source="manual_note",
        event_type="learning_note",
        title="Learned: OAuth2 Flows",
        content="OAuth2 Flows details",
        event_time=datetime.combine(target_date, time(18, 30))
    )
    db.add(evidence1)
    db.add(evidence2)
    
    db.commit()
    db.close()

    try:
        # Generate the daily log
        response = client.post("/daily-log/generate", json={"date": target_date.isoformat()})
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["success"] is True
        log_id = res_json["data"]["daily_log_id"]
        
        # Retrieve the log
        get_res = client.get(f"/daily-log/{target_date.isoformat()}")
        assert get_res.status_code == 200
        get_json = get_res.json()
        assert get_json["success"] is True
        
        context_data = json.loads(get_json["data"]["context"])
        assert context_data["date"] == target_date.isoformat()
        assert context_data["summary"]["commit_count"] == 1
        assert context_data["summary"]["notes_count"] == 1
        assert context_data["summary"]["evidence_count"] == 2
        
        # Verify Commit info in context
        assert len(context_data["commits"]) == 1
        assert context_data["commits"][0]["sha"] == "testsha1234567890"
        assert context_data["commits"][0]["repo"] == "test-repo"
        assert "auth.py" in context_data["commits"][0]["files_changed"]
        
        # Verify Note info in context
        assert len(context_data["notes"]) == 1
        assert context_data["notes"][0]["concepts_learned"] == "OAuth2 Flows"
        assert context_data["notes"][0]["challenges_faced"] == "Token expiration handling"
        
        # Verify Evidence timeline events in context (sorted chronologically: 11:00 before 18:30)
        assert len(context_data["evidence"]) == 2
        assert context_data["evidence"][0]["title"] == "Commit: Refactor auth pipeline"
        assert context_data["evidence"][1]["title"] == "Learned: OAuth2 Flows"

    finally:
        db = SessionLocal()
        cleanup_date_data(db, target_date)
        db.close()

def test_generate_daily_log_idempotent_overwrite():
    """
    Test that generating multiple times for the same date updates/overwrites
    the daily log instead of throwing unique constraint errors.
    """
    db = SessionLocal()
    target_date = date(2026, 6, 27)
    cleanup_date_data(db, target_date)
    
    # 1. Setup initial note
    note = LearningNote(
        date=target_date,
        concepts_learned="Initial Concept",
        challenges_faced="",
        key_insights="",
        resources_used="",
        additional_notes=""
    )
    db.add(note)
    db.commit()
    db.close()
    
    try:
        # First generate
        res1 = client.post("/daily-log/generate", json={"date": target_date.isoformat()})
        assert res1.status_code == 200
        id1 = res1.json()["data"]["daily_log_id"]
        
        # Add another note to trigger change in context builder
        db = SessionLocal()
        note2 = LearningNote(
            date=target_date,
            concepts_learned="Second Concept",
            challenges_faced="",
            key_insights="",
            resources_used="",
            additional_notes=""
        )
        db.add(note2)
        db.commit()
        db.close()
        
        # Second generate (overwrite)
        res2 = client.post("/daily-log/generate", json={"date": target_date.isoformat()})
        assert res2.status_code == 200
        id2 = res2.json()["data"]["daily_log_id"]
        
        # Verify it updated the exact same daily log ID
        assert id1 == id2
        
        # Retrieve context and verify it has 2 notes now
        get_res = client.get(f"/daily-log/{target_date.isoformat()}")
        context_data = json.loads(get_res.json()["data"]["context"])
        assert context_data["summary"]["notes_count"] == 2
        
    finally:
        db = SessionLocal()
        cleanup_date_data(db, target_date)
        db.close()

def test_get_today_daily_log_not_found():
    """
    Test GET /daily-log/today returns 404 error when not generated yet.
    """
    db = SessionLocal()
    today_date = date.today()
    cleanup_date_data(db, today_date)
    db.close()
    
    response = client.get("/daily-log/today")
    assert response.status_code == 404
    res_json = response.json()
    assert res_json["success"] is False
    assert res_json["error"]["code"] == "NOT_FOUND"

def test_get_today_daily_log_success():
    """
    Test GET /daily-log/today returns the compiled context after POST generation.
    """
    db = SessionLocal()
    today_date = date.today()
    cleanup_date_data(db, today_date)
    db.close()
    
    try:
        # Generate for today
        res_post = client.post("/daily-log/generate")
        assert res_post.status_code == 200
        
        # GET today
        res_get = client.get("/daily-log/today")
        assert res_get.status_code == 200
        res_json = res_get.json()
        assert res_json["success"] is True
        
        context_data = json.loads(res_json["data"]["context"])
        assert context_data["date"] == today_date.isoformat()
        
    finally:
        db = SessionLocal()
        cleanup_date_data(db, today_date)
        db.close()
