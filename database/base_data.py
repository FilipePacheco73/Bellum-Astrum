"""
Base data for seeding the Bellum Astrum database.

This module contains all the initial data that will be used to populate
the database, including ships, users, and other game entities.
"""

from typing import List, Dict, Any
from .config import (
    ADMIN_EMAIL, ADMIN_PASSWORD, NPC_PASSWORD,
    NPC_ASTRO_EMAIL, NPC_CYBER_EMAIL, NPC_ORION_EMAIL, NPC_VEGA_EMAIL,
    NPC_NEBULA_EMAIL, NPC_PULSAR_EMAIL, NPC_QUASAR_EMAIL, NPC_TITAN_EMAIL,
    NPC_SOLARIS_EMAIL, NPC_ANDROMEDA_EMAIL, NPC_CENTAURI_EMAIL
)

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

# Format: (nickname, email_var, elo, currency, experience, level, rank_name, formation)
_USER_TEMPLATES = [
    ("Admin", ADMIN_EMAIL, 1000, 9999999, 0, 1, "RECRUIT", "TACTICAL"),                                 # Admin especial - Tactical
    ("NPC_Astro", NPC_ASTRO_EMAIL, 800, 2500, 0, 1, "RECRUIT", "AGGRESSIVE"),                           # Level 1 - Recruit - Aggressive novato
    ("NPC_Cyber", NPC_CYBER_EMAIL, 950, 4000, 250, 3, "ENSIGN", "TACTICAL"),                            # Level 3 - Ensign - Tactical tech
    ("NPC_Orion", NPC_ORION_EMAIL, 1100, 8000, 625, 5, "LIEUTENANT", "DEFENSIVE"),                      # Level 5 - Lieutenant - Defensive hunter
    ("NPC_Vega", NPC_VEGA_EMAIL, 1250, 20000, 1562, 8, "LIEUTENANT_COMMANDER", "AGGRESSIVE"),           # Level 8 - Aggressive star
    ("NPC_Nebula", NPC_NEBULA_EMAIL, 1400, 35000, 5859, 13, "COMMANDER", "DEFENSIVE"),                  # Level 13 - Defensive cloud
    ("NPC_Pulsar", NPC_PULSAR_EMAIL, 1550, 60000, 28515, 21, "CAPTAIN", "AGGRESSIVE"),                  # Level 21 - Aggressive pulse
    ("NPC_Quasar", NPC_QUASAR_EMAIL, 1700, 100000, 185937, 35, "COMMODORE", "TACTICAL"),                # Level 35 - Tactical energy
    ("NPC_Titan", NPC_TITAN_EMAIL, 1850, 180000, 1532031, 55, "REAR_ADMIRAL", "DEFENSIVE"),             # Level 55 - Defensive giant
    ("NPC_Solaris", NPC_SOLARIS_EMAIL, 2000, 300000, 13672265, 89, "VICE_ADMIRAL", "AGGRESSIVE"),       # Level 89 - Aggressive solar
    ("NPC_Andromeda", NPC_ANDROMEDA_EMAIL, 2150, 500000, 125000000, 144, "ADMIRAL", "TACTICAL"),        # Level 144 - Tactical galaxy
    ("NPC_Centauri", NPC_CENTAURI_EMAIL, 2500, 1000000, 500000000, 250, "FLEET_ADMIRAL", "TACTICAL"),   # Level 250 - Master Tactical
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
        "default_formation": formation,
        "victories": 0,
        "defeats": 0,
        "damage_dealt": 0.0,
        "damage_taken": 0.0,
        "ships_destroyed_by_user": 0,
        "ships_lost_by_user": 0
    }
    for nickname, email, elo, currency, experience, level, rank_name, formation in _USER_TEMPLATES
]

# =============================================================================
# RANK BONUS DATA
# =============================================================================

# Format: (rank, min_level, attack_mult%, shield_mult%, hp_mult%, evasion_bonus, fire_rate_mult%, value_mult%, max_active_ships)

# Format: (rank, min_level, attack, shield, hp, evasion, fire_rate, value, max_active_ships, work_income, work_cooldown_minutes)
_RANK_BONUS_TEMPLATES = [
    (UserRank.RECRUIT, 1, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1, 700, 2),
    (UserRank.ENSIGN, 3, 0.05, 0.05, 0.05, 0.01, 0.05, 0.10, 2, 1000, 3),
    (UserRank.LIEUTENANT, 5, 0.10, 0.10, 0.10, 0.02, 0.10, 0.20, 3, 1400, 3),
    (UserRank.LIEUTENANT_COMMANDER, 8, 0.15, 0.15, 0.15, 0.03, 0.15, 0.30, 4, 1900, 4),
    (UserRank.COMMANDER, 13, 0.20, 0.20, 0.20, 0.04, 0.20, 0.40, 5, 2600, 4),
    (UserRank.CAPTAIN, 21, 0.25, 0.25, 0.25, 0.05, 0.25, 0.50, 6, 3500, 5),
    (UserRank.COMMODORE, 35, 0.30, 0.30, 0.30, 0.06, 0.30, 0.60, 8, 4750, 6),
    (UserRank.REAR_ADMIRAL, 55, 0.35, 0.35, 0.35, 0.07, 0.35, 0.70, 10, 6500, 7),
    (UserRank.VICE_ADMIRAL, 89, 0.40, 0.40, 0.40, 0.08, 0.40, 0.80, 12, 8750, 8),
    (UserRank.ADMIRAL, 144, 0.50, 0.50, 0.50, 0.10, 0.50, 1.00, 15, 12500, 10),
    (UserRank.FLEET_ADMIRAL, 233, 0.60, 0.60, 0.60, 0.12, 0.60, 1.20, 20, 17500, 12),
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
        "max_active_ships": int(max_active_ships),
        "work_income": int(work_income),
        "work_cooldown_minutes": int(work_cooldown_minutes),
    }
    for rank, min_level, attack, shield, hp, evasion, fire_rate, value, max_active_ships, work_income, work_cooldown_minutes in _RANK_BONUS_TEMPLATES
]


# =============================================================================
# OWNED SHIPS DATA (Hardcoded assignments based on rank)
# =============================================================================

# Ship assignments based on rank - users get ships according to their rank limits
# Format: (nickname, ship_name)
_OWNED_SHIPS_ASSIGNMENTS = [
    # Admin gets a balanced mid-tier ship (Storm series) - RECRUIT rank = 1 ship
    ("Admin", "Breeze"),
    
    # RECRUIT (1 ship max) - Tier 1
    ("NPC_Astro", "Falcon"),
    
    # ENSIGN (2 ships max) - Tier 1-2
    ("NPC_Cyber", "Sparrow"),
    ("NPC_Cyber", "Hawk"),
    
    # LIEUTENANT (3 ships max) - Tier 1-2
    ("NPC_Orion", "Kestrel"),
    ("NPC_Orion", "Eagle"),
    ("NPC_Orion", "Swift"),
    
    # LIEUTENANT_COMMANDER (4 ships max) - Tier 2-3
    ("NPC_Vega", "Breeze"),
    ("NPC_Vega", "Osprey"),
    ("NPC_Vega", "Harrier"),
    ("NPC_Vega", "Raven"),
    
    # COMMANDER (5 ships max) - Tier 2-3
    ("NPC_Nebula", "Lightning"),
    ("NPC_Nebula", "Thunder"),
    ("NPC_Nebula", "Tempest"),
    ("NPC_Nebula", "Storm"),
    ("NPC_Nebula", "Sparrow"),
    
    # CAPTAIN (6 ships max) - Tier 3-4
    ("NPC_Pulsar", "Comet"),
    ("NPC_Pulsar", "Breeze"),
    ("NPC_Pulsar", "Nova"),
    ("NPC_Pulsar", "Meteor"),
    ("NPC_Pulsar", "Pulsar"),
    ("NPC_Pulsar", "Asteroid"),
    
    # COMMODORE (8 ships max) - Tier 3-4
    ("NPC_Quasar", "Nova"),
    ("NPC_Quasar", "Lightning"),
    ("NPC_Quasar", "Thunder"),
    ("NPC_Quasar", "Tempest"),
    ("NPC_Quasar", "Comet"),
    ("NPC_Quasar", "Meteor"),
    ("NPC_Quasar", "Pulsar"),
    ("NPC_Quasar", "Asteroid"),
    
    # REAR_ADMIRAL (10 ships max) - Tier 4-5
    ("NPC_Titan", "Galaxy"),
    ("NPC_Titan", "Comet"),
    ("NPC_Titan", "Nova"),
    ("NPC_Titan", "Meteor"),
    ("NPC_Titan", "Pulsar"),
    ("NPC_Titan", "Asteroid"),
    ("NPC_Titan", "Quasar"),
    ("NPC_Titan", "Nebula"),
    ("NPC_Titan", "Vortex"),
    ("NPC_Titan", "Supernova"),
    
    # VICE_ADMIRAL (12 ships max) - Tier 4-5
    ("NPC_Solaris", "Quasar"),
    ("NPC_Solaris", "Galaxy"),
    ("NPC_Solaris", "Nebula"),
    ("NPC_Solaris", "Vortex"),
    ("NPC_Solaris", "Supernova"),
    ("NPC_Solaris", "Comet"),
    ("NPC_Solaris", "Nova"),
    ("NPC_Solaris", "Meteor"),
    ("NPC_Solaris", "Pulsar"),
    ("NPC_Solaris", "Asteroid"),
    ("NPC_Solaris", "Lightning"),
    ("NPC_Solaris", "Thunder"),
    
    # ADMIRAL (15 ships max) - Tier 5-6
    ("NPC_Andromeda", "Orion"),
    ("NPC_Andromeda", "Galaxy"),
    ("NPC_Andromeda", "Quasar"),
    ("NPC_Andromeda", "Nebula"),
    ("NPC_Andromeda", "Vortex"),
    ("NPC_Andromeda", "Supernova"),
    ("NPC_Andromeda", "Phoenix"),
    ("NPC_Andromeda", "Titan"),
    ("NPC_Andromeda", "Seraph"),
    ("NPC_Andromeda", "Leviathan"),
    ("NPC_Andromeda", "Comet"),
    ("NPC_Andromeda", "Nova"),
    ("NPC_Andromeda", "Meteor"),
    ("NPC_Andromeda", "Pulsar"),
    ("NPC_Andromeda", "Asteroid"),
    
    # FLEET_ADMIRAL (20 ships max) - Tier 4-6 (Full arsenal)
    ("NPC_Centauri", "Phoenix"),
    ("NPC_Centauri", "Orion"),
    ("NPC_Centauri", "Titan"),
    ("NPC_Centauri", "Seraph"),
    ("NPC_Centauri", "Leviathan"),
    ("NPC_Centauri", "Galaxy"),
    ("NPC_Centauri", "Quasar"),
    ("NPC_Centauri", "Nebula"),
    ("NPC_Centauri", "Vortex"),
    ("NPC_Centauri", "Supernova"),
    ("NPC_Centauri", "Comet"),
    ("NPC_Centauri", "Nova"),
    ("NPC_Centauri", "Meteor"),
    ("NPC_Centauri", "Pulsar"),
    ("NPC_Centauri", "Asteroid"),
    ("NPC_Centauri", "Lightning"),
    ("NPC_Centauri", "Thunder"),
    ("NPC_Centauri", "Tempest"),
    ("NPC_Centauri", "Storm"),
    ("NPC_Centauri", "Breeze"),
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
