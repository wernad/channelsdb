"""Tests for ping endpoint."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, base_url="http://testserver/api/v1")


def test_ping():
    """Test that ping endpoint returns 200 OK."""
    response = client.get("/health/ping")
    assert response.status_code == 200
    assert response.json() is None
