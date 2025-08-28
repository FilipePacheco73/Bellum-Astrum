import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
import random
import string
from sqlalchemy import text
from backend.app.database import engine

client = TestClient(app)

# Test API and database health via /health endpoint (should be the first test)
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["api"] == "running"
    assert data["status"] == "healthy"
    assert data["database"]["status"] == "healthy"

# Test root endpoint
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "author" in data
    assert data["author"] == "FilipePacheco73"
    assert "Welcome to the Bellum Astrum API!" in data["message"]

# Test version endpoint
def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    
    # Check all required fields are present
    assert "name" in data
    assert "version" in data
    assert "api_title" in data
    assert "description" in data
    assert "author" in data
    
    # Check specific values
    assert data["name"] == "Bellum Astrum"
    assert data["author"] == "FilipePacheco73"
    assert data["api_title"] == "Space Battle Game API"
    assert "API for managing game resources" in data["description"]
    
    # Check version format (should be semantic versioning like x.y.z)
    import re
    version_pattern = r'^\d+\.\d+\.\d+$'
    assert re.match(version_pattern, data["version"]), f"Version '{data['version']}' doesn't match semantic versioning pattern"
    
    print(f"DEBUG: Version endpoint returned version: {data['version']}")

# Test version consistency between endpoints
def test_version_consistency():
    # Get version from /version endpoint
    version_response = client.get("/version")
    assert version_response.status_code == 200
    version_data = version_response.json()
    
    # Get version from /health endpoint
    health_response = client.get("/health")
    assert health_response.status_code == 200
    health_data = health_response.json()
    
    # Get version from root endpoint
    root_response = client.get("/")
    assert root_response.status_code == 200
    root_data = root_response.json()
    
    # All endpoints should return the same version
    assert version_data["version"] == health_data["version"], "Version mismatch between /version and /health endpoints"
    assert version_data["version"] == root_data["version"], "Version mismatch between /version and root endpoints"
    
    print(f"DEBUG: All endpoints consistently return version: {version_data['version']}")

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

# Test version endpoint
def test_version_endpoint():
    """Test that the version endpoint returns correct project information"""
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    
    # Check all required fields are present
    required_fields = ["name", "version", "api_title", "description", "author"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"
    
    # Check field types and basic content validation
    assert isinstance(data["name"], str), "Name should be a string"
    assert isinstance(data["version"], str), "Version should be a string"
    assert isinstance(data["api_title"], str), "API title should be a string"
    assert isinstance(data["description"], str), "Description should be a string"
    assert isinstance(data["author"], str), "Author should be a string"
    
    # Check specific expected values
    assert data["name"] == "Bellum Astrum", f"Expected 'Bellum Astrum', got '{data['name']}'"
    assert data["author"] == "FilipePacheco73", f"Expected 'FilipePacheco73', got '{data['author']}'"
    
    # Version should be in semantic versioning format (X.Y.Z)
    import re
    version_pattern = r'^\d+\.\d+\.\d+$'
    assert re.match(version_pattern, data["version"]), f"Version '{data['version']}' is not in X.Y.Z format"
    
    print(f"✅ Version endpoint test passed. Current version: {data['version']}")

def test_version_endpoint_matches_changelog():
    """Test that the version endpoint returns the same version as extracted from CHANGELOG.md"""
    from backend.app.version import get_version_from_changelog
    
    # Get version from the API endpoint
    response = client.get("/version")
    assert response.status_code == 200
    api_version = response.json()["version"]
    
    # Get version directly from the changelog function
    changelog_version = get_version_from_changelog()
    
    # They should match
    assert api_version == changelog_version, f"API version '{api_version}' doesn't match changelog version '{changelog_version}'"
    
    print(f"✅ Version consistency test passed. Both API and changelog report version: {api_version}")

def test_version_endpoint_public_access():
    """Test that the version endpoint doesn't require authentication"""
    # This test ensures the endpoint works without any authentication headers
    # (it should be publicly accessible)
    response = client.get("/version")
    assert response.status_code == 200
    
    # Should not return authentication errors
    data = response.json()
    assert "detail" not in data or "authentication" not in str(data.get("detail", "")).lower()
    
    print("✅ Version endpoint public access test passed")

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
    battle_request = {
        "opponent_user_id": user2_id,
        "user_ship_numbers": ship_number1,
        "opponent_ship_numbers": ship_number2,
        "user_formation": "AGGRESSIVE",
        "opponent_formation": "DEFENSIVE"
    }
    battle = client.post(
        "/api/v1/battle/battle",
        json=battle_request,
        headers={"Authorization": f"Bearer {token1}"}
    )
    print(f"DEBUG: Battle response status: {battle.status_code}")
    print(f"DEBUG: Battle response text: {battle.text}")
    assert battle.status_code == 200
    data = battle.json()
    assert "battle_id" in data
    assert "participants" in data
    assert "winner_user_id" in data
    assert "battle_log" in data

# Test battle against NPC (User1 vs NPC_Astro)
def test_battle_against_npc(ship_numbers):
    (user1_id, token1, ship_number1), (user2_id, token2, ship_number2) = ship_numbers
    
    # Hardcoded NPC values for simplicity
    npc_astro_id = 2
    npc_ship_number = 2
    
    # User1 battles against NPC_Astro
    print(f"\nDEBUG: user1_id={user1_id}, npc_astro_id={npc_astro_id}")
    print(f"DEBUG: ship_number1={ship_number1}, npc_ship_number={npc_ship_number}")
    
    battle_request = {
        "opponent_user_id": npc_astro_id,
        "user_ship_numbers": ship_number1,
        "opponent_ship_numbers": npc_ship_number
        # Don't specify formations, should use users' default formations
    }
    
    battle = client.post(
        "/api/v1/battle/battle",
        json=battle_request,
        headers={"Authorization": f"Bearer {token1}"}
    )
    print(f"DEBUG: Battle response status: {battle.status_code}")
    print(f"DEBUG: Battle response text: {battle.text}")
    assert battle.status_code == 200
    data = battle.json()
    assert "battle_id" in data
    assert "participants" in data
    assert "winner_user_id" in data
    assert "battle_log" in data
    
    # Print battle log to verify NPC special handling
    battle_log = data["battle_log"]
    print("\n=== BATTLE LOG vs NPC ===")
    for log_entry in battle_log:
        print(log_entry)
    print("=== END BATTLE LOG ===\n")
    
    # Verify that NPC appears in participants
    participants = data["participants"]
    npc_participant = next((p for p in participants if p["nickname"] == "NPC_Astro"), None)
    assert npc_participant is not None, "NPC_Astro not found in battle participants"

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

# Test work system status check
def test_work_status(user_ids):
    (user1_id, token1), (user2_id, token2) = user_ids
    response = client.get(
        "/api/v1/work/status",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "can_work" in data
    assert "work_type" in data
    assert "current_rank" in data
    assert "estimated_income" in data
    assert "work_cooldown_minutes" in data
    print(f"DEBUG: Work status - {data}")

# Test work types for user rank
def test_work_types(user_ids):
    (user1_id, token1), (user2_id, token2) = user_ids
    response = client.get(
        "/api/v1/work/types",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_rank" in data
    assert "work_type" in data
    assert "estimated_income_range" in data
    assert "cooldown_minutes" in data
    print(f"DEBUG: Available work type - {data}")

# Test performing work
def test_perform_work(user_ids):
    (user1_id, token1), (user2_id, token2) = user_ids
    response = client.post(
        "/api/v1/work/perform",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "work_type" in data
    assert "income_earned" in data
    assert "new_currency_balance" in data
    assert "cooldown_until" in data
    print(f"DEBUG: Work performed - Income: {data['income_earned']}, Type: {data['work_type']}")

# Test work history
def test_work_history(user_ids):
    (user1_id, token1), (user2_id, token2) = user_ids
    response = client.get(
        "/api/v1/work/history",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "work_history" in data
    assert "total_income_earned" in data
    assert "total_work_sessions" in data
    # Should have at least 1 work session from previous test
    assert data["total_work_sessions"] >= 1
    print(f"DEBUG: Work history - Sessions: {data['total_work_sessions']}, Total income: {data['total_income_earned']}")

# Test work cooldown (should fail if trying to work again immediately)
def test_work_cooldown(user_ids):
    (user1_id, token1), (user2_id, token2) = user_ids
    # Try to work again immediately after previous work
    response = client.post(
        "/api/v1/work/perform",
        headers={"Authorization": f"Bearer {token1}"}
    )
    # Should fail due to cooldown
    assert response.status_code == 400
    assert "cooldown" in response.json()["detail"].lower() or "wait" in response.json()["detail"].lower()
    print(f"DEBUG: Cooldown test passed - {response.json()['detail']}")

# Test work status after performing work (should show cooldown)
def test_work_status_after_work(user_ids):
    (user1_id, token1), (user2_id, token2) = user_ids
    response = client.get(
        "/api/v1/work/status",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["can_work"] is False  # Should be false due to cooldown
    assert "time_until_available" in data
    assert data["time_until_available"] > 0  # Should have time remaining
    print(f"DEBUG: Work status after work - Can work: {data['can_work']}, Time until available: {data['time_until_available']:.2f} minutes")

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