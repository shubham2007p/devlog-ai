import hmac
import hashlib
import json
from fastapi.testclient import TestClient
from backend.main import app
from backend.config import settings
from backend.database import SessionLocal
from backend.models.commits import GitHubCommit
from backend.models.evidence import Evidence

client = TestClient(app)

def compute_sha256_signature(payload: dict, secret: str) -> str:
    """
    Computes the X-Hub-Signature-256 header value for a given dictionary payload.
    """
    payload_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    mac = hmac.new(secret.encode('utf-8'), msg=payload_bytes, digestmod=hashlib.sha256)
    return f"sha256={mac.hexdigest()}"

def test_webhook_invalid_signature():
    """
    Test that requests with invalid signatures are rejected with 401 Unauthorized.
    """
    payload = {
        "repository": {"name": "Test-Repo"},
        "ref": "refs/heads/main",
        "commits": []
    }
    # Send request with invalid signature header
    headers = {"X-Hub-Signature-256": "sha256=invalidhash"}
    response = client.post("/webhook/github", json=payload, headers=headers)
    
    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["error"]["code"] == "INVALID_SIGNATURE"

def test_webhook_valid_payload_processing():
    """
    Test that a valid webhook request is verified, stored, and creates evidence logs.
    """
    db = SessionLocal()
    # Ensure test commit SHA is clean
    test_sha = "f00b4r1234567890abcdef1234567890abcdef12"
    db.query(GitHubCommit).filter_by(commit_sha=test_sha).delete()
    db.query(Evidence).filter(Evidence.event_metadata.like(f"%{test_sha}%")).delete()
    db.commit()

    payload = {
        "repository": {"name": "DevLog-AI"},
        "ref": "refs/heads/main",
        "commits": [
            {
                "id": test_sha,
                "message": "Feat: Add webhook unit tests\nDetail explanation of tests.",
                "url": f"https://github.com/shubh/DevLog-AI/commit/{test_sha}",
                "timestamp": "2026-06-18T10:15:30Z",
                "author": {"name": "Shubh Tester", "email": "test@example.com"},
                "added": ["tests/test_webhook.py"],
                "removed": [],
                "modified": ["backend/routes/webhook.py"]
            }
        ]
    }

    # Generate HMAC-SHA256 signature based on local secret
    signature = compute_sha256_signature(payload, settings.WEBHOOK_SECRET)
    headers = {"X-Hub-Signature-256": signature}
    
    # Send POST request
    response = client.post("/webhook/github", json=payload, headers=headers)
    
    # Assert successful HTTP response
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["message"] == "Webhook processed"
    assert response.json()["data"]["details"]["commits_processed"] == 1
    assert response.json()["data"]["details"]["commits_ignored"] == 0

    # Assert database persistence
    commit_record = db.query(GitHubCommit).filter_by(commit_sha=test_sha).first()
    assert commit_record is not None
    assert commit_record.repo_name == "DevLog-AI"
    assert commit_record.branch_name == "main"
    assert commit_record.author_name == "Shubh Tester"
    assert set(commit_record.files_changed) == {"tests/test_webhook.py", "backend/routes/webhook.py"}

    # Assert evidence log entry
    evidence_record = db.query(Evidence).filter(Evidence.event_metadata.like(f"%{test_sha}%")).first()
    assert evidence_record is not None
    assert evidence_record.source == "github"
    assert evidence_record.event_type == "commit"
    assert "Feat: Add webhook unit tests" in evidence_record.title
    
    # Clean up test records
    db.delete(commit_record)
    db.delete(evidence_record)
    db.commit()
    db.close()

def test_webhook_deduplication():
    """
    Test that sending duplicate commit SHAs ignores them during second call.
    """
    db = SessionLocal()
    test_sha = "deadbeef1234567890abcdef1234567890abcdef"
    db.query(GitHubCommit).filter_by(commit_sha=test_sha).delete()
    db.query(Evidence).filter(Evidence.event_metadata.like(f"%{test_sha}%")).delete()
    db.commit()

    payload = {
        "repository": {"name": "DevLog-AI"},
        "ref": "refs/heads/main",
        "commits": [
            {
                "id": test_sha,
                "message": "Fix: Deduplication bug",
                "url": f"https://github.com/shubh/DevLog-AI/commit/{test_sha}",
                "timestamp": "2026-06-18T11:00:00Z",
                "author": {"name": "Shubh Tester"},
                "added": [],
                "removed": [],
                "modified": ["backend/services/github_service.py"]
            }
        ]
    }

    signature = compute_sha256_signature(payload, settings.WEBHOOK_SECRET)
    headers = {"X-Hub-Signature-256": signature}

    # First attempt (should process 1, ignore 0)
    res1 = client.post("/webhook/github", json=payload, headers=headers)
    assert res1.status_code == 200
    assert res1.json()["data"]["details"]["commits_processed"] == 1
    assert res1.json()["data"]["details"]["commits_ignored"] == 0

    # Second attempt (should process 0, ignore 1)
    res2 = client.post("/webhook/github", json=payload, headers=headers)
    assert res2.status_code == 200
    assert res2.json()["data"]["details"]["commits_processed"] == 0
    assert res2.json()["data"]["details"]["commits_ignored"] == 1

    # Clean up
    commit_record = db.query(GitHubCommit).filter_by(commit_sha=test_sha).first()
    evidence_record = db.query(Evidence).filter(Evidence.event_metadata.like(f"%{test_sha}%")).first()
    if commit_record:
        db.delete(commit_record)
    if evidence_record:
        db.delete(evidence_record)
    db.commit()
    db.close()
