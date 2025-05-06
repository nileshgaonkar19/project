import pytest
from fastapi.testclient import TestClient
from api_service.main import app

client = TestClient(app)

def test_get_users_default_params():
    response = client.get("/users?pageno=1&pagesize=5")
    assert response.status_code == 200
    json_data = response.json()
    assert "users" in json_data
    assert isinstance(json_data["users"], list)
    assert "total_count" in json_data

def test_get_users_with_name_match():
    response = client.get("/users?pageno=1&pagesize=10&name=Sheryl")
    assert response.status_code == 200
    data = response.json()["users"]
    for user in data:
        assert "sheryl" in user["firstname"].lower() or "sheryl" in user["lastname"].lower()

def test_get_users_with_name_no_match():
    response = client.get("/users?pageno=1&pagesize=10&name=nonexistentnamexyz")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["users"] == []
    assert json_data["total_count"] == 0

def test_get_users_invalid_page():
    response = client.get("/users?pageno=-1&pagesize=10")
    assert response.status_code == 422  # FastAPI will throw a validation error

def test_get_users_missing_params():
    response = client.get("/users")
    assert response.status_code == 422  # required query params missing
