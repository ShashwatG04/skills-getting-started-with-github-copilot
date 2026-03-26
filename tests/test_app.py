from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def setup_function():
    # Reset the in-memory state before each test
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
    })


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_success():
    response = client.post("/activities/Chess%20Club/signup?email=new@mergington.edu")
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up new@mergington.edu for Chess Club"
    assert "new@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_for_activity_duplicate_fails():
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant_success():
    response = client.delete("/activities/Chess%20Club/participants?email=daniel@mergington.edu")
    assert response.status_code == 200
    assert response.json()["message"] == "Removed daniel@mergington.edu from Chess Club"
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]


def test_remove_participant_not_found():
    response = client.delete("/activities/Chess%20Club/participants?email=unknown@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"