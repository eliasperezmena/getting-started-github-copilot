from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    # Expect that activities dict is returned and has known keys
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_user@example.com"

    # Ensure user is not in participants initially
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    resp_signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_signup.status_code == 200
    assert resp_signup.json().get("message")
    assert email in activities[activity]["participants"]

    # Signup again should fail (already signed up)
    resp_signup_again = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_signup_again.status_code == 400

    # Unregister
    resp_unregister = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_unregister.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregister again should fail
    resp_unregister_again = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_unregister_again.status_code == 400
