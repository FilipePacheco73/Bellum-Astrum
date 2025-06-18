import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

# Test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# Test seeding ships
def test_seed_ships():
    response = client.post("/api/v1/seed/ships")
    assert response.status_code == 200
    assert "message" in response.json()

# Test seeding users
def test_seed_users():
    response = client.post("/api/v1/seed/users")
    assert response.status_code == 200
    assert "message" in response.json()

# Test buying a ship
def test_buy_ship():
    # Ensure user and ship exist before buying
    client.post("/api/v1/seed/users")
    client.post("/api/v1/seed/ships")
    # Admin has user_id=1, Falcon has ship_id=1
    response = client.post("/api/v1/market/buy/1/1")
    assert response.status_code == 200
    assert "message" in response.json()

# Test selling a ship
def test_sell_ship():
    # Ensure user and ship exist and ship is bought before selling
    client.post("/api/v1/seed/users")
    client.post("/api/v1/seed/ships")
    # Admin (user_id=1) buys Falcon (ship_id=1)
    buy_response = client.post("/api/v1/market/buy/1/1")
    assert buy_response.status_code == 200
    ship_number = buy_response.json().get("ship_number")
    assert ship_number is not None
    # Admin sells the ship he just bought
    sell_response = client.post(f"/api/v1/market/sell/1/{ship_number}")
    assert sell_response.status_code == 200
    assert "message" in sell_response.json()
    assert "value_received" in sell_response.json()