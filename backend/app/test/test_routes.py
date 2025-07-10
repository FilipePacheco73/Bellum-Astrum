import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
import random
import string
from sqlalchemy import text
from database import engine

client = TestClient(app)

# Test API and database health via /health endpoint (should be the first test)
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["api"] == "running"
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

# Utility function to generate random strings
def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Fixture to create two users and return their ids
def create_users():
    user1 = {
        "nickname": f"test_user_1_{random_string()}",
        "email": f"test_user_1_{random_string()}@email.com",
        "password": random_string(12)
    }
    user2 = {
        "nickname": f"test_user_2_{random_string()}",
        "email": f"test_user_2_{random_string()}@email.com",
        "password": random_string(12)
    }
    client.post("/api/v1/users/register", json=user1)
    client.post("/api/v1/users/register", json=user2)
    users_response = client.get("/api/v1/users/")
    users = users_response.json()
    user1_id = next(u["user_id"] for u in users if u["nickname"] == user1["nickname"])
    user2_id = next(u["user_id"] for u in users if u["nickname"] == user2["nickname"])
    return user1_id, user2_id

@pytest.fixture(scope="module")
def user_ids():
    return create_users()

@pytest.fixture(scope="module")
def ship_numbers(user_ids):
    user1_id, user2_id = user_ids
    buy1 = client.post(f"/api/v1/market/buy/{user1_id}/1")
    assert buy1.status_code == 200
    ship_number1 = buy1.json().get("ship_number")
    assert ship_number1 is not None
    buy2 = client.post(f"/api/v1/market/buy/{user2_id}/1")
    assert buy2.status_code == 200
    ship_number2 = buy2.json().get("ship_number")
    assert ship_number2 is not None
    return (user1_id, ship_number1), (user2_id, ship_number2)

# Test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# Test user creation
def test_create_users(user_ids):
    user1_id, user2_id = user_ids
    assert isinstance(user1_id, int)
    assert isinstance(user2_id, int)

# Test buying a ship for both users
def test_buy_ships(ship_numbers):
    (user1_id, ship_number1), (user2_id, ship_number2) = ship_numbers
    assert ship_number1 is not None
    assert ship_number2 is not None

# Test activating ships for battle
def test_activate_ships(ship_numbers):
    (user1_id, ship_number1), (user2_id, ship_number2) = ship_numbers
    activate1 = client.post("/api/v1/battle/activate-ship/", params={"user_id": user1_id, "ship_number": ship_number1})
    assert activate1.status_code == 200
    activate2 = client.post("/api/v1/battle/activate-ship/", params={"user_id": user2_id, "ship_number": ship_number2})
    assert activate2.status_code == 200

# Test battle between two users
def test_battle_between_two_users(ship_numbers):
    (user1_id, ship_number1), (user2_id, ship_number2) = ship_numbers
    battle = client.post(
        "/api/v1/battle/battle",
        params={
            "user1_id": user1_id,
            "user2_id": user2_id,
            "user1_ship_number": ship_number1,
            "user2_ship_number": ship_number2
        }
    )
    assert battle.status_code == 200
    data = battle.json()
    assert "battle_id" in data
    assert "participants" in data
    assert "winner_user_id" in data
    assert "battle_log" in data

# Test selling a ship for both users
def test_sell_ships(ship_numbers):
    (user1_id, ship_number1), (user2_id, ship_number2) = ship_numbers
    sell_response1 = client.post(f"/api/v1/market/sell/{user1_id}/{ship_number1}")
    assert sell_response1.status_code == 200
    assert "message" in sell_response1.json()
    assert "value_received" in sell_response1.json()
    sell_response2 = client.post(f"/api/v1/market/sell/{user2_id}/{ship_number2}")
    assert sell_response2.status_code == 200
    assert "message" in sell_response2.json()
    assert "value_received" in sell_response2.json()

created_log_id = None

# Test log creation
def test_create_log():
    global created_log_id
    log_data = {
        "log_level": "INFO",
        "log_category": "SYSTEM",
        "action": "REGISTER",
        "details": {"test": "log"},
        "user_id": None
    }
    response = client.post("/api/v1/logs/", json=log_data)
    assert response.status_code == 200
    data = response.json()
    assert data["log_id"]
    assert data["log_level"] == "INFO"
    created_log_id = data["log_id"]

# Test log listing
def test_list_logs():
    global created_log_id
    response = client.get("/api/v1/logs/")
    assert response.status_code == 200
    data = response.json()
    assert "logs" in data
    assert any(log["log_id"] == created_log_id for log in data["logs"])

# Test get log by id
def test_get_log_by_id():
    global created_log_id
    response = client.get(f"/api/v1/logs/{created_log_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["log_id"] == created_log_id

# Test delete log
def test_delete_log():
    global created_log_id
    response = client.delete(f"/api/v1/logs/{created_log_id}")
    assert response.status_code == 200
    # Confirm deletion
    response = client.get(f"/api/v1/logs/{created_log_id}")
    assert response.status_code == 404
