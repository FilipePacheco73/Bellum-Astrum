"""
Utilities for user experience, level, and rank progression,
and for applying rank bonuses to ships during battles.
"""
from database.models import UserRank, RankBonus
from sqlalchemy.orm import Session

# Exponential XP growth: XP required for each level increases exponentially
# Example: XP for next level = base_xp * (growth_factor ** (level-1))
BASE_XP = 100
GROWTH_FACTOR = 1.5

def get_level_for_experience(experience: int) -> int:
    """
    Returns the user's level based on accumulated experience (exponential growth).
    Level 1: 0 XP, Level 2: 100 XP, Level 3: 250 XP, Level 4: 475 XP, etc.
    """
    level = 1
    xp_needed = BASE_XP
    total_xp = 0
    while experience >= total_xp + xp_needed:
        total_xp += xp_needed
        xp_needed = int(xp_needed * GROWTH_FACTOR)
        level += 1
    return level

def get_rank_for_level(level: int) -> UserRank:
    """
    Returns the user's rank based on level (Fibonacci-like: 3, 5, 8, 13, 21, 35, 55, 89, 144, ...).
    """
    if level < 3:
        return UserRank.RECRUIT
    elif level < 5:
        return UserRank.ENSIGN
    elif level < 8:
        return UserRank.LIEUTENANT
    elif level < 13:
        return UserRank.LIEUTENANT_COMMANDER
    elif level < 21:
        return UserRank.COMMANDER
    elif level < 35:
        return UserRank.CAPTAIN
    elif level < 55:
        return UserRank.COMMODORE
    elif level < 89:
        return UserRank.REAR_ADMIRAL
    elif level < 144:
        return UserRank.VICE_ADMIRAL
    elif level < 233:
        return UserRank.ADMIRAL
    else:
        return UserRank.FLEET_ADMIRAL

def update_user_progression(user, xp_gained: int) -> bool:
    """
    Updates user's experience, level, and rank.
    Returns True if level or rank changed.
    """
    user.experience += xp_gained
    new_level = get_level_for_experience(user.experience)
    new_rank = get_rank_for_level(new_level)
    changed = False
    if user.level != new_level:
        user.level = new_level
        changed = True
    if user.rank != new_rank:
        user.rank = new_rank
        changed = True
    return changed

def check_rank_promotion(user, db: Session) -> UserRank:
    """
    Checks if the user should be promoted to a new rank based on their current level.
    Returns the new rank if promotion is warranted, or current rank if no change.
    """
    new_rank = get_rank_for_level(user.level)
    return new_rank

def apply_rank_bonus_to_ship_stats(user, ship_stats: dict, db: Session) -> dict:
    """
    Applies the user's rank bonus to all ship battle stats (does not modify DB).
    ship_stats: dict with keys 'attack', 'shield', 'hp', 'evasion', 'fire_rate', 'value', etc.
    db: SQLAlchemy Session for DB access.
    Returns a new dict with bonuses applied. If a bonus is not defined for a stat, it is not changed.
    """
    bonus_obj = db.query(RankBonus).filter_by(rank=user.rank).first()
    stats = ship_stats.copy()
    if bonus_obj:
        for key in ['attack', 'shield', 'hp', 'evasion', 'fire_rate', 'value']:
            bonus = getattr(bonus_obj, key, 0)
            # if bonus is not None and bonus != 0:
            if bonus:
                stats[key] = stats.get(key, 0) * (1 + bonus)
    return stats


def get_max_active_ships_for_user(user, db: Session) -> int:
    """
    Get the maximum number of active ships allowed for a user based on their rank.
    
    Args:
        user: User object with rank information
        db: SQLAlchemy Session for database access
        
    Returns:
        Maximum number of active ships allowed for this user's rank
    """
    bonus_obj = db.query(RankBonus).filter_by(rank=user.rank).first()
    if bonus_obj:
        return bonus_obj.max_active_ships
    # Default fallback if rank bonus not found
    return 1


def count_active_ships_for_user(user_id: int, db: Session) -> int:
    """
    Count the number of currently active ships for a user.
    
    Args:
        user_id: ID of the user
        db: SQLAlchemy Session for database access
        
    Returns:
        Number of ships with status 'active' for this user
    """
    from database.models import OwnedShips
    return db.query(OwnedShips).filter(
        OwnedShips.user_id == user_id,
        OwnedShips.status == 'active'
    ).count()


def can_activate_ship(user, db: Session) -> tuple[bool, str]:
    """
    Check if a user can activate another ship based on their rank limits.
    
    Args:
        user: User object with rank information
        db: SQLAlchemy Session for database access
        
    Returns:
        Tuple of (can_activate: bool, message: str)
    """
    max_allowed = get_max_active_ships_for_user(user, db)
    current_active = count_active_ships_for_user(user.user_id, db)
    
    if current_active >= max_allowed:
        return False, f"Maximum active ships limit reached ({current_active}/{max_allowed}) for rank {user.rank.value}"
    
    return True, f"Can activate ship ({current_active + 1}/{max_allowed})"