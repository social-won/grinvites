from fastapi.testclient import TestClient
import sqlite3
from main import app



client = TestClient(app)

def test_get_me():
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {"name": "John", "id": 1}

def test_get_user():
    response = client.get(f"/user/{1}")
    assert response.status_code == 200
    user = response.json()
    print(user)
    

def test_create_user():
    user_data = {
        "email": "test@example.com",
        "display_name": "Test User",
        "calendar_type": "Outlook",
        "prefer_notify": 1
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    assert created_user["display_name"] == user_data["display_name"]
    assert created_user["calendar_type"] == user_data["calendar_type"]
    assert created_user["prefer_notify"] == user_data["prefer_notify"]
    assert "id" in created_user  # Should have auto-generated ID
    print("Created user:", created_user)



# Run tests
test_get_user()
#test_create_user()