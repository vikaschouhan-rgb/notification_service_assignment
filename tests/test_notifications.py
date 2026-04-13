import pytest

# -----------------------------
# Test: Create Notification
# -----------------------------
def test_create_notification(client):
    payload = {
        "user_id": 1,
        "channel": "email",
        "message": "Test message",
        "priority": "high",
        "recipient": "test@example.com"
    }

    response = client.post("/notifications", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["user_id"] == 1
    assert data["channel"] == "email"
    assert data["status"] in ["pending", "sent", "failed"]


# -----------------------------
# Test: Get All Notifications
# -----------------------------
def test_get_notifications(client):
    response = client.get("/notifications")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# -----------------------------
# Test: Get Notification by ID
# -----------------------------
def test_get_notification_by_id(client):
    # First create one
    payload = {
        "user_id": 2,
        "channel": "sms",
        "message": "Hello",
        "priority": "normal",
        "recipient": "9999999999"
    }

    create_res = client.post("/notifications", json=payload)
    notification_id = create_res.json()["id"]

    # Fetch it
    response = client.get(f"/notifications/{notification_id}")

    assert response.status_code == 200
    assert response.json()["id"] == notification_id


# -----------------------------
# Test: Notification Not Found
# -----------------------------
def test_notification_not_found(client):
    response = client.get("/notifications/999999")

    assert response.status_code == 404


# -----------------------------
# Test: Get User Notifications
# -----------------------------
def test_get_user_notifications(client):
    user_id = 5

    # Create one notification
    payload = {
        "user_id": user_id,
        "channel": "push",
        "message": "User test",
        "priority": "low",
        "recipient": "device_token"
    }

    client.post("/notifications", json=payload)

    response = client.get(f"/users/{user_id}/notifications")

    assert response.status_code == 200
    assert isinstance(response.json(), list)