"""Tests for authentication endpoints"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_signup():
    """Test user signup"""
    response = client.post(
        "/auth/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login():
    """Test user login"""
    # First, signup
    client.post(
        "/auth/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    # Then, login
    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
