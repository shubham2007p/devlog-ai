from datetime import date, datetime, time, timezone
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import SessionLocal
from backend.models.evidence import Evidence

client = TestClient(app)

def test_get_timeline_today_empty():
    """
    Test GET /timeline/today returns empty when no events are logged for today.
    """
    db = SessionLocal()
    today_date = datetime.now(timezone.utc).date()
    
    # Temporarily remove any existing evidence for today in the test db
    start_dt = datetime.combine(today_date, time.min)
    end_dt = datetime.combine(today_date, time.max)
    db.query(Evidence).filter(
        Evidence.event_time >= start_dt,
        Evidence.event_time <= end_dt
    ).delete()
    db.commit()
    db.close()

    response = client.get("/timeline/today")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"] == []


def test_get_timeline_today_with_events():
    """
    Test GET /timeline/today returns events sorted chronologically.
    """
    db = SessionLocal()
    today_date = datetime.now(timezone.utc).date()
    
    # Setup test events at specific times
    ev1 = Evidence(
        source="manual_note",
        event_type="learning_note",
        title="Learned: Binary Search",
        content="Concepts...",
        event_time=datetime.combine(today_date, time(15, 30))
    )
    ev2 = Evidence(
        source="github",
        event_type="commit",
        title="Commit: Added Binary Search implementation",
        content="Code...",
        event_time=datetime.combine(today_date, time(10, 15))
    )
    
    db.add(ev1)
    db.add(ev2)
    db.commit()

    try:
        response = client.get("/timeline/today")
        assert response.status_code == 200
        assert response.json()["success"] is True
        data = response.json()["data"]
        
        # Verify both events are returned
        assert len(data) >= 2
        
        # Verify chronological sorting (10:15 should come before 15:30)
        times = [event["time"] for event in data if event["title"] in ["Learned: Binary Search", "Commit: Added Binary Search implementation"]]
        assert times == ["10:15", "15:30"]
        
        # Verify DTO structure
        commit_event = next(e for e in data if e["title"] == "Commit: Added Binary Search implementation")
        assert commit_event["type"] == "commit"
        assert commit_event["time"] == "10:15"
        
    finally:
        db.delete(ev1)
        db.delete(ev2)
        db.commit()
        db.close()


def test_get_timeline_by_date():
    """
    Test GET /timeline/{date} filters by specific date.
    """
    db = SessionLocal()
    target_date = date(2026, 6, 18)
    
    ev = Evidence(
        source="github",
        event_type="commit",
        title="Commit: Old task completed",
        content="Old Code...",
        event_time=datetime.combine(target_date, time(14, 45))
    )
    db.add(ev)
    db.commit()

    try:
        # Fetch for matching date
        res_match = client.get(f"/timeline/{target_date.isoformat()}")
        assert res_match.status_code == 200
        assert res_match.json()["success"] is True
        assert len(res_match.json()["data"]) == 1
        assert res_match.json()["data"][0]["title"] == "Commit: Old task completed"
        assert res_match.json()["data"][0]["time"] == "14:45"
        
        # Fetch for date with no events
        res_empty = client.get("/timeline/2026-06-17")
        assert res_empty.status_code == 200
        assert res_empty.json()["success"] is True
        assert res_empty.json()["data"] == []
        
        # Fetch with invalid date format (raises validation error)
        res_invalid = client.get("/timeline/invalid-date-format")
        assert res_invalid.status_code == 422
        
    finally:
        db.delete(ev)
        db.commit()
        db.close()
