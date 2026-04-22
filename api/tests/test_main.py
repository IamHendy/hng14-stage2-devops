from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with patch("redis.Redis") as mock_redis:
    mock_instance = MagicMock()
    mock_redis.return_value = mock_instance
    from main import app

client = TestClient(app)


def test_health_check():
    """Test health endpoint returns ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job():
    """Test job creation returns a job_id"""
    with patch("main.r") as mock_r:
        mock_r.lpush.return_value = 1
        mock_r.hset.return_value = 1
        response = client.post("/jobs")
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert len(data["job_id"]) == 36


def test_get_job_not_found():
    """Test getting a non-existent job returns error"""
    with patch("main.r") as mock_r:
        mock_r.hget.return_value = None
        response = client.get("/jobs/nonexistent-id")
        assert response.status_code == 200
        assert response.json() == {"error": "not found"}


def test_get_job_found():
    """Test getting an existing job returns status"""
    with patch("main.r") as mock_r:
        mock_r.hget.return_value = b"completed"
        response = client.get("/jobs/some-valid-id")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["job_id"] == "some-valid-id"
