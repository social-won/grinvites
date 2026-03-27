from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_me():
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {"name": "John", "id": 1}