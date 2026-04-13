import pytest

# -----------------------------
# Test: Set Preferences (Create)
# -----------------------------
def test_create_preferences(client):
    user_id = 10

    payload = {
        "email": True,
        "sms": False,
        "push": True
    }

    response = client.post(f"/users/{user_id}/preferences", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] == user_id
    assert data["email"] is True
    assert data["sms"] is False


# -----------------------------
# Test: Update Preferences
# -----------------------------
def test_update_preferences(client):
    user_id = 11

    # Create first
    payload = {
        "email": True,
        "sms": True,
        "push": True
    }
    client.post(f"/users/{user_id}/preferences", json=payload)

    # Update
    updated_payload = {
        "email": False,
        "sms": False,
        "push": True
    }

    response = client.post(f"/users/{user_id}/preferences", json=updated_payload)

    assert response.status_code == 200
    data = response.json()

    assert data["email"] is False
    assert data["sms"] is False


# -----------------------------
# Test: Get Preferences
# -----------------------------
def test_get_preferences(client):
    user_id = 12

    payload = {
        "email": True,
        "sms": False,
        "push": True
    }

    client.post(f"/users/{user_id}/preferences", json=payload)

    response = client.get(f"/users/{user_id}/preferences")

    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] == user_id
    assert data["email"] is True


# -----------------------------
# Test: Preferences Not Found
# -----------------------------
def test_preferences_not_found(client):
    response = client.get("/users/99999/preferences")

    assert response.status_code == 404