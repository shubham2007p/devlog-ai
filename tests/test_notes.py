from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    """
    Test that GET /health returns standard success response structure.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {
            "status": "healthy"
        }
    }
