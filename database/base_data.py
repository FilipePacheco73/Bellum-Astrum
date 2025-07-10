"""
Base data for seeding the Bellum Astrum database.

This module contains all the initial data that will be used to populate
the database, including ships, users, and other game entities.
"""

from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables from database .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Environment variables for users
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
NPC_PASSWORD = os.getenv('NPC_PASSWORD')
NPC_ASTRO_EMAIL = os.getenv('NPC_ASTRO_EMAIL')
NPC_CYBER_EMAIL = os.getenv('NPC_CYBER_EMAIL')
NPC_ORION_EMAIL = os.getenv('NPC_ORION_EMAIL')
NPC_VEGA_EMAIL = os.getenv('NPC_VEGA_EMAIL')
NPC_NEBULA_EMAIL = os.getenv('NPC_NEBULA_EMAIL')
NPC_PULSAR_EMAIL = os.getenv('NPC_PULSAR_EMAIL')
NPC_QUASAR_EMAIL = os.getenv('NPC_QUASAR_EMAIL')
NPC_TITAN_EMAIL = os.getenv('NPC_TITAN_EMAIL')
NPC_SOLARIS_EMAIL = os.getenv('NPC_SOLARIS_EMAIL')
NPC_ANDROMEDA_EMAIL = os.getenv('NPC_ANDROMEDA_EMAIL')

# =============================================================================
# SHIP DATA
# =============================================================================

# Format: (name, attack, shield, evasion, fire_rate, hp, value)
_SHIP_TEMPLATES = [
    # Birds of Prey Series
    ("Falcon", 15, 10, 0.05, 2.0, 1200, 1500),
    ("Eagle", 20, 15, 0.10, 3.0, 1500, 2000),
    ("Hawk", 25, 20, 0.15, 4.0, 1800, 2500),
    ("Condor", 30, 25, 0.20, 5.0, 2000, 3000),
    ("Vulture", 35, 30, 0.25, 6.0, 2200, 3500),
    
    # Raptor Series
    ("Raven", 18, 12, 0.07, 2.5, 1300, 1600),
    ("Osprey", 22, 17, 0.12, 3.2, 1550, 2100),
    ("Kestrel", 27, 22, 0.17, 4.1, 1850, 2600),
    ("Merlin", 32, 27, 0.22, 5.3, 2050, 3100),
    ("Phoenix", 37, 32, 0.27, 6.4, 2250, 3600),
    
    # Mythical Series
    ("Griffin", 19, 13, 0.08, 2.7, 1350, 1700),
    ("Harrier", 23, 18, 0.13, 3.4, 1600, 2200),
    ("Sparrow", 28, 23, 0.18, 4.3, 1900, 2700),
    ("Swift", 33, 28, 0.23, 5.5, 2100, 3200),
    ("Thunder", 38, 33, 0.28, 6.6, 2300, 3700),
    
    # Storm Series
    ("Storm", 21, 14, 0.09, 2.9, 1400, 1800),
    ("Tempest", 24, 19, 0.14, 3.6, 1650, 2300),
    ("Cyclone", 29, 24, 0.19, 4.5, 1950, 2800),
    ("Typhoon", 34, 29, 0.24, 5.7, 2150, 3300),
    ("Blizzard", 39, 34, 0.29, 6.8, 2350, 3800),
    
    # Cosmic Series
    ("Nova", 22, 15, 0.10, 3.1, 1450, 1900),
    ("Comet", 26, 20, 0.15, 4.0, 1750, 2400),
    ("Meteor", 31, 25, 0.20, 5.2, 2000, 2900),
    ("Asteroid", 36, 30, 0.25, 6.3, 2200, 3400),
    ("Pulsar", 41, 35, 0.30, 7.0, 2400, 3900),
    
    # Galactic Series
    ("Nebula", 24, 16, 0.11, 3.3, 1500, 2000),
    ("Quasar", 28, 21, 0.16, 4.2, 1800, 2500),
    ("Galaxy", 33, 26, 0.21, 5.4, 2100, 3000),
    ("Andromeda", 38, 31, 0.26, 6.5, 2300, 3500),
    ("Orion", 43, 36, 0.31, 7.2, 2500, 4000),
]

# Convert tuples to dictionaries
SHIPS_DATA: List[Dict[str, Any]] = [
    {
        "ship_name": name,
        "attack": float(attack),
        "shield": float(shield),
        "evasion": evasion,
        "fire_rate": fire_rate,
        "hp": float(hp),
        "value": value
    }
    for name, attack, shield, evasion, fire_rate, hp, value in _SHIP_TEMPLATES
]

# =============================================================================
# USER DATA
# =============================================================================

# Format: (nickname, email_var, elo, currency)
_USER_TEMPLATES = [
    ("Admin", ADMIN_EMAIL, 1000, 9999999),
    ("NPC_Astro", NPC_ASTRO_EMAIL, 800, 5000),
    ("NPC_Cyber", NPC_CYBER_EMAIL, 950, 7000),
    ("NPC_Orion", NPC_ORION_EMAIL, 1100, 9000),
    ("NPC_Vega", NPC_VEGA_EMAIL, 1250, 11000),
    ("NPC_Nebula", NPC_NEBULA_EMAIL, 1400, 13000),
    ("NPC_Pulsar", NPC_PULSAR_EMAIL, 1550, 15000),
    ("NPC_Quasar", NPC_QUASAR_EMAIL, 1700, 17000),
    ("NPC_Titan", NPC_TITAN_EMAIL, 1850, 19000),
    ("NPC_Solaris", NPC_SOLARIS_EMAIL, 2000, 21000),
    ("NPC_Andromeda", NPC_ANDROMEDA_EMAIL, 2150, 23000),
]

# Convert tuples to dictionaries with common defaults
USERS_DATA: List[Dict[str, Any]] = [
    {
        "nickname": nickname,
        "email": email,
        "password": ADMIN_PASSWORD if nickname == "Admin" else NPC_PASSWORD,
        "elo_rank": float(elo),
        "currency_value": float(currency),
        "victories": 0,
        "defeats": 0,
        "damage_dealt": 0.0,
        "damage_taken": 0.0,
        "ships_destroyed_by_user": 0,
        "ships_lost_by_user": 0
    }
    for nickname, email, elo, currency in _USER_TEMPLATES
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_ships_data() -> List[Dict[str, Any]]:
    """Get all ships data for seeding."""
    return SHIPS_DATA

def get_users_data() -> List[Dict[str, Any]]:
    """Get all users data for seeding."""
    return USERS_DATA

def get_npc_users() -> List[Dict[str, Any]]:
    """Get only NPC users data."""
    return [user for user in USERS_DATA if user["nickname"].startswith("NPC_")]

def get_admin_user() -> Dict[str, Any]:
    """Get admin user data."""
    return next(user for user in USERS_DATA if user["nickname"] == "Admin")

def get_ship_by_name(name: str) -> Dict[str, Any]:
    """Get specific ship data by name."""
    return next((ship for ship in SHIPS_DATA if ship["ship_name"] == name), None)

def get_user_by_nickname(nickname: str) -> Dict[str, Any]:
    """Get specific user data by nickname."""
    return next((user for user in USERS_DATA if user["nickname"] == nickname), None)
