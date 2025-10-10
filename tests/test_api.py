import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Signup
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200
    assert email in signup.json()["message"]
    # Unregister
    unregister = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister.status_code == 200
    assert email in unregister.json()["message"]


def test_signup_duplicate():
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Second signup should fail
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity}/unregister?email={email}")


def test_unregister_not_found():
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 404
    assert "Participant not found" in resp.json()["detail"]
