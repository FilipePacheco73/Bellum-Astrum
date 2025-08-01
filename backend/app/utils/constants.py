# Centralized constants for the Bellum Astrum project

# Experience points for battles
BASE_XP_WIN = 100  # Experience points for winning a battle
BASE_XP_LOSS = 50  # Experience points for losing a battle

# Difficulty multipliers for XP calculation
DIFFICULTY_MULTIPLIERS = {
    "higher_level": 0.15,  # +15% XP per level difference when fighting higher-level opponents
    "lower_level": -0.10, # -10% XP per level difference when fighting lower-level opponents
    "min_multiplier": 0.3 # Minimum XP multiplier (30%)
}

# Base XP and growth factor for level progression
BASE_XP = 100
GROWTH_FACTOR = 1.5

# Formation modifiers
FORMATION_MODIFIERS = {
    "DEFENSIVE": 1.2,   # +20% evasion
    "AGGRESSIVE": 1.0,  # Normal evasion
    "TACTICAL": 0.9     # -10% evasion
}

# Damage calculation constants
SHIELD_DAMAGE_REDUCTION = 0.5
DAMAGE_VARIATION_RANGE = (0.85, 1.15)

# Credits awarded multiplier
CREDITS_AWARDED_MULTIPLIER = 0.1

# Shipyard constants
SHIPYARD_REPAIR_COOLDOWN_SECONDS = 60  # Cooldown between ship repairs

# Ship sell value multiplier
SELL_VALUE_MULTIPLIER = 0.4

# Elo calculation constants
ELO_BASE_CHANGE = 32  # Base change in Elo rating per match
ELO_EXPECTED_SCORE_DIVISOR = 400  # Divisor for expected score calculation
