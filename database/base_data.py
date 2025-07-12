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
NPC_CENTAURI_EMAIL = os.getenv('NPC_CENTAURI_EMAIL')

# =============================================================================
# SHIP DATA
# =============================================================================

# Format: (name, attack, shield, evasion, fire_rate, hp, value)
# Each series has 5 ships with different strategies:
# 1st: Balanced starter
# 2nd: High Attack / Glass Cannon
# 3rd: High Defense / Tank
# 4th: High Speed / Hit & Run
# 5th: High HP / Bruiser

_SHIP_TEMPLATES = [
    # Birds of Prey Series - Entry Level (Tier 1) - Starter ships
    ("Falcon", 12, 8, 0.05, 1.8, 1000, 1500),          # Balanced
    ("Hawk", 18, 5, 0.03, 2.2, 800, 1800),             # Glass Cannon
    ("Eagle", 10, 15, 0.02, 1.5, 900, 1700),           # Tank
    ("Swift", 14, 6, 0.15, 3.0, 700, 1650),            # Hit & Run
    ("Condor", 11, 10, 0.04, 1.6, 1400, 1600),         # Bruiser
    
    # Raptor Series - Light Fighters (Tier 2) - Early game progression
    ("Sparrow", 20, 12, 0.08, 2.0, 1300, 3500),        # Balanced
    ("Kestrel", 30, 8, 0.05, 2.5, 1100, 4000),         # Glass Cannon
    ("Osprey", 16, 22, 0.03, 1.7, 1200, 3800),         # Tank
    ("Harrier", 22, 10, 0.18, 3.2, 1000, 3700),        # Hit & Run
    ("Raven", 18, 15, 0.06, 1.8, 1700, 3600),          # Bruiser
    
    # Storm Series - Medium Fighters (Tier 3) - Mid game powerhouse
    ("Breeze", 32, 18, 0.10, 2.2, 1600, 8000),         # Balanced
    ("Lightning", 48, 12, 0.07, 2.8, 1400, 9000),      # Glass Cannon
    ("Thunder", 26, 35, 0.04, 1.9, 1500, 8500),        # Tank
    ("Tempest", 35, 15, 0.20, 3.5, 1300, 8200),        # Hit & Run
    ("Storm", 30, 22, 0.08, 2.0, 2100, 8800),          # Bruiser
    
    # Cosmic Series - Heavy Fighters (Tier 4) - High-end combat
    ("Comet", 45, 25, 0.12, 2.4, 2000, 18000),         # Balanced
    ("Nova", 68, 16, 0.08, 3.0, 1800, 20000),          # Glass Cannon
    ("Meteor", 38, 48, 0.05, 2.1, 1900, 19000),        # Tank
    ("Pulsar", 50, 20, 0.22, 3.8, 1700, 18500),        # Hit & Run
    ("Asteroid", 42, 30, 0.10, 2.2, 2600, 19500),      # Bruiser
    
    # Galactic Series - Elite Ships (Tier 5) - Elite warfare
    ("Galaxy", 60, 35, 0.15, 2.6, 2400, 45000),        # Balanced
    ("Quasar", 90, 22, 0.10, 3.2, 2200, 50000),        # Glass Cannon
    ("Nebula", 48, 65, 0.06, 2.3, 2300, 48000),        # Tank
    ("Vortex", 65, 25, 0.25, 4.0, 2100, 47000),        # Hit & Run
    ("Supernova", 55, 40, 0.12, 2.4, 3200, 52000),     # Bruiser
    
    # Legendary Series - Ultimate Ships (Tier 6) - Endgame dominance
    ("Orion", 80, 50, 0.18, 2.8, 3000, 120000),        # Balanced
    ("Phoenix", 125, 30, 0.12, 3.5, 2800, 135000),     # Glass Cannon
    ("Titan", 65, 95, 0.08, 2.5, 2900, 130000),        # Tank
    ("Seraph", 85, 35, 0.28, 4.2, 2700, 125000),       # Hit & Run
    ("Leviathan", 75, 55, 0.15, 2.6, 4200, 140000),    # Bruiser
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

# Format: (nickname, email_var, elo, currency, experience, level, rank_name)
_USER_TEMPLATES = [
    ("Admin", ADMIN_EMAIL, 1000, 9999999, 0, 1, "RECRUIT"),                                 # Admin especial
    ("NPC_Astro", NPC_ASTRO_EMAIL, 800, 2500, 0, 1, "RECRUIT"),                             # Level 1 - Recruit
    ("NPC_Cyber", NPC_CYBER_EMAIL, 950, 4000, 250, 3, "ENSIGN"),                            # Level 3 - Ensign
    ("NPC_Orion", NPC_ORION_EMAIL, 1100, 8000, 625, 5, "LIEUTENANT"),                       # Level 5 - Lieutenant
    ("NPC_Vega", NPC_VEGA_EMAIL, 1250, 20000, 1562, 8, "LIEUTENANT_COMMANDER"),             # Level 8
    ("NPC_Nebula", NPC_NEBULA_EMAIL, 1400, 35000, 5859, 13, "COMMANDER"),                   # Level 13
    ("NPC_Pulsar", NPC_PULSAR_EMAIL, 1550, 60000, 28515, 21, "CAPTAIN"),                    # Level 21
    ("NPC_Quasar", NPC_QUASAR_EMAIL, 1700, 100000, 185937, 35, "COMMODORE"),                # Level 35
    ("NPC_Titan", NPC_TITAN_EMAIL, 1850, 180000, 1532031, 55, "REAR_ADMIRAL"),              # Level 55
    ("NPC_Solaris", NPC_SOLARIS_EMAIL, 2000, 300000, 13672265, 89, "VICE_ADMIRAL"),         # Level 89
    ("NPC_Andromeda", NPC_ANDROMEDA_EMAIL, 2150, 500000, 125000000, 144, "ADMIRAL"),        # Level 144
    ("NPC_Centauri", NPC_CENTAURI_EMAIL, 2500, 1000000, 500000000, 250, "FLEET_ADMIRAL"),   # Level 250
]

# Convert tuples to dictionaries with common defaults
from .models import UserRank

def get_rank_enum(rank_name: str) -> UserRank:
    """Convert rank name string to UserRank enum"""
    return getattr(UserRank, rank_name)

USERS_DATA: List[Dict[str, Any]] = [
    {
        "nickname": nickname,
        "email": email,
        "password": ADMIN_PASSWORD if nickname == "Admin" else NPC_PASSWORD,
        "elo_rank": float(elo),
        "currency_value": int(currency),
        "experience": int(experience),
        "level": int(level),
        "rank": get_rank_enum(rank_name),
        "victories": 0,
        "defeats": 0,
        "damage_dealt": 0.0,
        "damage_taken": 0.0,
        "ships_destroyed_by_user": 0,
        "ships_lost_by_user": 0
    }
    for nickname, email, elo, currency, experience, level, rank_name in _USER_TEMPLATES
]

# =============================================================================
# RANK BONUS DATA
# =============================================================================

# Format: (rank, min_level, attack_mult%, shield_mult%, hp_mult%, evasion_bonus, fire_rate_mult%, value_mult%)

_RANK_BONUS_TEMPLATES = [
    (UserRank.RECRUIT, 1, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    (UserRank.ENSIGN, 3, 0.05, 0.05, 0.05, 0.01, 0.05, 0.10),
    (UserRank.LIEUTENANT, 5, 0.10, 0.10, 0.10, 0.02, 0.10, 0.20),
    (UserRank.LIEUTENANT_COMMANDER, 8, 0.15, 0.15, 0.15, 0.03, 0.15, 0.30),
    (UserRank.COMMANDER, 13, 0.20, 0.20, 0.20, 0.04, 0.20, 0.40),
    (UserRank.CAPTAIN, 21, 0.25, 0.25, 0.25, 0.05, 0.25, 0.50),
    (UserRank.COMMODORE, 35, 0.30, 0.30, 0.30, 0.06, 0.30, 0.60),
    (UserRank.REAR_ADMIRAL, 55, 0.35, 0.35, 0.35, 0.07, 0.35, 0.70),
    (UserRank.VICE_ADMIRAL, 89, 0.40, 0.40, 0.40, 0.08, 0.40, 0.80),
    (UserRank.ADMIRAL, 144, 0.50, 0.50, 0.50, 0.10, 0.50, 1.00),
    (UserRank.FLEET_ADMIRAL, 233, 0.60, 0.60, 0.60, 0.12, 0.60, 1.20),
]

RANK_BONUSES_DATA: List[Dict[str, Any]] = [
    {
        "rank": rank,
        "min_level": min_level,
        "attack": float(attack),
        "shield": float(shield),
        "hp": float(hp),
        "evasion": float(evasion),
        "fire_rate": float(fire_rate),
        "value": float(value),
    }
    for rank, min_level, attack, shield, hp, evasion, fire_rate, value in _RANK_BONUS_TEMPLATES
]


# =============================================================================
# OWNED SHIPS DATA (Hardcoded assignments based on rank)
# =============================================================================

# Ship assignments based on rank - each user gets a specific ship based on their rank
# Format: (nickname, ship_name)
_OWNED_SHIPS_ASSIGNMENTS = [
    # Admin gets a balanced mid-tier ship (Storm series)
    ("Admin", "Breeze"),
    
    # NPCs get ships appropriate to their rank
    ("NPC_Astro", "Falcon"),        # RECRUIT - Tier 1 Balanced
    ("NPC_Cyber", "Sparrow"),       # ENSIGN - Tier 2 Balanced
    ("NPC_Orion", "Kestrel"),       # LIEUTENANT - Tier 2 Glass Cannon
    ("NPC_Vega", "Breeze"),         # LIEUTENANT_COMMANDER - Tier 3 Balanced
    ("NPC_Nebula", "Lightning"),    # COMMANDER - Tier 3 Glass Cannon
    ("NPC_Pulsar", "Comet"),        # CAPTAIN - Tier 4 Balanced
    ("NPC_Quasar", "Nova"),         # COMMODORE - Tier 4 Glass Cannon
    ("NPC_Titan", "Galaxy"),        # REAR_ADMIRAL - Tier 5 Balanced
    ("NPC_Solaris", "Quasar"),      # VICE_ADMIRAL - Tier 5 Glass Cannon
    ("NPC_Andromeda", "Orion"),     # ADMIRAL - Tier 6 Balanced
    ("NPC_Centauri", "Phoenix"),    # FLEET_ADMIRAL - Tier 6 Glass Cannon
]

OWNED_SHIPS_ASSIGNMENTS: List[Dict[str, Any]] = [
    {
        "user_nickname": nickname,
        "ship_name": ship_name,
        "status": "active"
    }
    for nickname, ship_name in _OWNED_SHIPS_ASSIGNMENTS
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

def get_rank_bonuses_data() -> List[Dict[str, Any]]:
    """Get all rank bonus data for seeding."""
    return RANK_BONUSES_DATA

def get_owned_ships_assignments() -> List[Dict[str, Any]]:
    """Get hardcoded owned ships assignments for seeding."""
    return OWNED_SHIPS_ASSIGNMENTS
