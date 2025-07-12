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
    # Login both users to get JWT tokens
    login1 = client.post("/api/v1/users/login", json={"email": user1["email"], "password": user1["password"]})
    print("LOGIN1 STATUS:", login1.status_code, "RESPONSE:", login1.text)
    assert login1.status_code == 200, f"Login1 failed: {login1.text}"
    login2 = client.post("/api/v1/users/login", json={"email": user2["email"], "password": user2["password"]})
    print("LOGIN2 STATUS:", login2.status_code, "RESPONSE:", login2.text)
    assert login2.status_code == 200, f"Login2 failed: {login2.text}"
    token1 = login1.json().get("access_token")
    token2 = login2.json().get("access_token")
    assert token1 is not None, f"Token1 is None. Login1 response: {login1.text}"
    assert token2 is not None, f"Token2 is None. Login2 response: {login2.text}"
    users_response = client.get("/api/v1/users/")
    users = users_response.json()
    user1_id = next(u["user_id"] for u in users if u["nickname"] == user1["nickname"])
    user2_id = next(u["user_id"] for u in users if u["nickname"] == user2["nickname"])
    return (user1_id, token1), (user2_id, token2)

@pytest.fixture(scope="module")
def user_ids():
    return create_users()

@pytest.fixture(scope="module")
def ship_numbers(user_ids):
    (user1_id, token1), (user2_id, token2) = user_ids
    buy1 = client.post(f"/api/v1/market/buy/1", headers={"Authorization": f"Bearer {token1}"})
    assert buy1.status_code == 200
    ship_number1 = buy1.json().get("ship_number")
    assert ship_number1 is not None
    buy2 = client.post(f"/api/v1/market/buy/1", headers={"Authorization": f"Bearer {token2}"})
    assert buy2.status_code == 200
    ship_number2 = buy2.json().get("ship_number")
    assert ship_number2 is not None
    return (user1_id, token1, ship_number1), (user2_id, token2, ship_number2)

# Test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# Test user creation
def test_create_users(user_ids):
 (user1_id, _), (user2_id, _) = user_ids
 assert isinstance(user1_id, int)
 assert isinstance(user2_id, int)

# Test buying a ship for both users
def test_buy_ships(ship_numbers):
    (user1_id, token1, ship_number1), (user2_id, token2, ship_number2) = ship_numbers
    # Already tested in fixture, just assert ship numbers
    assert ship_number1 is not None
    assert ship_number2 is not None

# Test activating ships for battle
def test_activate_ships(ship_numbers):
    (user1_id, token1, ship_number1), (user2_id, token2, ship_number2) = ship_numbers
    activate1 = client.post(
        "/api/v1/battle/activate-ship/",
        params={"ship_number": ship_number1},
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert activate1.status_code == 200
    activate2 = client.post(
        "/api/v1/battle/activate-ship/",
        params={"ship_number": ship_number2},
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert activate2.status_code == 200

# Test battle between two users
def test_battle_between_two_users(ship_numbers):
    (user1_id, token1, ship_number1), (user2_id, token2, ship_number2) = ship_numbers
    battle = client.post(
        "/api/v1/battle/battle",
        params={
            "opponent_user_id": user2_id,
            "user_ship_number": ship_number1,
            "opponent_ship_number": ship_number2
        },
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert battle.status_code == 200
    data = battle.json()
    assert "battle_id" in data
    assert "participants" in data
    assert "winner_user_id" in data
    assert "battle_log" in data

# Test repairing ships for both users before selling
def test_repair_ships_before_selling(ship_numbers):
    (user1_id, token1, ship_number1), (user2_id, token2, ship_number2) = ship_numbers
    # User 1 repairs ship
    repair1 = client.post("/api/v1/shipyard/repair", params={"ship_number": ship_number1}, headers={"Authorization": f"Bearer {token1}"})
    assert repair1.status_code == 200
    data1 = repair1.json()
    assert data1["success"] is True
    assert data1["ship_number"] == ship_number1
    # User 2 repairs ship
    repair2 = client.post("/api/v1/shipyard/repair", params={"ship_number": ship_number2}, headers={"Authorization": f"Bearer {token2}"})
    assert repair2.status_code == 200
    data2 = repair2.json()
    assert data2["success"] is True
    assert data2["ship_number"] == ship_number2

# Test selling a ship for both users
def test_sell_ships(ship_numbers):
    (user1_id, token1, ship_number1), (user2_id, token2, ship_number2) = ship_numbers
    sell_response1 = client.post(
        f"/api/v1/market/sell/{ship_number1}",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert sell_response1.status_code == 200
    assert "message" in sell_response1.json()
    assert "value_received" in sell_response1.json()
    sell_response2 = client.post(
        f"/api/v1/market/sell/{ship_number2}",
        headers={"Authorization": f"Bearer {token2}"}
    )
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
    
# Test log retrieval by id
def test_log_retrieval_by_id():
    response_id = client.get(f"/api/v1/logs/{created_log_id}")
    assert response_id.status_code == 200
    data_id = response_id.json()
    assert data_id["log_id"] == created_log_id

# Test delete log
def test_delete_log():
    global created_log_id
    response = client.delete(f"/api/v1/logs/{created_log_id}")
    assert response.status_code == 200
    # Confirm deletion
    response = client.get(f"/api/v1/logs/{created_log_id}")
    assert response.status_code == 404