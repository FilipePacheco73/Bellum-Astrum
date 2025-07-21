from sqlalchemy.orm import Session
from database.models import User, OwnedShips, BattleHistory
from datetime import datetime, UTC
from backend.app.utils.progression_utils import apply_rank_bonus_to_ship_stats
import random
from typing import Union, List
from backend.app.utils.constants import BASE_XP_WIN, BASE_XP_LOSS, DIFFICULTY_MULTIPLIERS
from backend.app.utils.constants import FORMATION_MODIFIERS, SHIELD_DAMAGE_REDUCTION, DAMAGE_VARIATION_RANGE, CREDITS_AWARDED_MULTIPLIER
from backend.app.utils.constants import ELO_BASE_CHANGE, ELO_EXPECTED_SCORE_DIVISOR


# --- Formation System Helper Functions ---
def get_formation_evasion_modifier(formation: str) -> float:
    """
    Get evasion modifier based on formation type.
    DEFENSIVE: +20% evasion (impacts enemy's hit chance)
    AGGRESSIVE: Normal evasion (no modifier)
    TACTICAL: -10% evasion (penalty for focusing on high-attack targets)
    """
    return FORMATION_MODIFIERS.get(formation, 1.0)


def select_target_by_formation(formation: str, enemy_ships: List[dict]) -> dict:
    """
    Select target ship based on formation strategy.
    DEFENSIVE: Target ship with lowest HP (finish weak enemies first)
    AGGRESSIVE: Random target (spread damage)
    TACTICAL: Target ship with highest attack (eliminate threats first)
    """
    if not enemy_ships:
        return None
    
    if formation == "DEFENSIVE":
        # Target ship with lowest current HP
        return min(enemy_ships, key=lambda s: s['current_hp'])
    elif formation == "TACTICAL":
        # Target ship with highest attack value
        return max(enemy_ships, key=lambda s: s['attack'])
    else:  # AGGRESSIVE or default
        # Random target
        return random.choice(enemy_ships)


def get_ships_by_numbers(db: Session, user_id: int, ship_numbers: Union[int, List[int]]) -> List[OwnedShips]:
    """
    Get ships by their numbers, ensuring they are active and belong to the user.
    Handles both single ship (int) and multiple ships (List[int]) input.
    """
    # Convert single ship number to list for consistency
    if isinstance(ship_numbers, int):
        ship_numbers = [ship_numbers]
    
    # Query only active ships that belong to the user
    ships = db.query(OwnedShips).filter(
        OwnedShips.user_id == user_id,
        OwnedShips.ship_number.in_(ship_numbers),
        OwnedShips.status == 'active'  # Only active ships can battle
    ).all()
    
    return ships


def prepare_ship_stats(ship: OwnedShips, user: User, db: Session) -> dict:
    """
    Prepare ship stats dictionary with rank bonuses applied.
    """
    base_stats = {
        'ship_number': ship.ship_number,
        'ship_name': ship.ship_name,
        'attack': ship.actual_attack,
        'shield': ship.actual_shield,
        'hp': ship.actual_hp,
        'evasion': ship.actual_evasion,
        'fire_rate': ship.actual_fire_rate,
        'value': ship.actual_value,
        'current_hp': ship.actual_hp,  # Track current HP during battle
        'ship_obj': ship  # Keep reference to original ship object
    }
    
    # Apply rank bonuses
    enhanced_stats = apply_rank_bonus_to_ship_stats(user, base_stats, db)
    enhanced_stats['current_hp'] = enhanced_stats['hp']  # Set initial current HP
    enhanced_stats['ship_obj'] = ship  # Preserve ship object reference
    
    return enhanced_stats


def calculate_elo_change(winner_elo: float, loser_elo: float) -> tuple[float, float]:
    """
    Calculate the Elo rating change for the winner and loser of a match.

    Args:
        winner_elo (float): Current Elo rating of the winner.
        loser_elo (float): Current Elo rating of the loser.

    Returns:
        tuple[float, float]: Updated Elo ratings for the winner and loser.
    """
    expected_winner_score = 1 / (1 + 10 ** ((loser_elo - winner_elo) / ELO_EXPECTED_SCORE_DIVISOR))
    expected_loser_score = 1 / (1 + 10 ** ((winner_elo - loser_elo) / ELO_EXPECTED_SCORE_DIVISOR))

    winner_elo_change = ELO_BASE_CHANGE * (1 - expected_winner_score)
    loser_elo_change = ELO_BASE_CHANGE * (0 - expected_loser_score)

    return winner_elo + winner_elo_change, loser_elo + loser_elo_change


def calculate_xp_gain(winner_level, loser_level, base_xp_winner=BASE_XP_WIN, base_xp_loser=BASE_XP_LOSS):
    """
    Calculate XP gain for both winner and loser based on level difference.
    Winner always gets more XP, but fighting higher level opponents gives more XP.
    Fighting lower level opponents gives less XP.
    """
    level_diff = loser_level - winner_level

    # XP multiplier based on level difference
    if level_diff > 0:  # Fighting higher level opponent
        multiplier = 1 + (level_diff * DIFFICULTY_MULTIPLIERS['higher_level'])  # +15% per level difference
    elif level_diff < 0:  # Fighting lower level opponent
        multiplier = max(DIFFICULTY_MULTIPLIERS['min_multiplier'], 1 + (level_diff * DIFFICULTY_MULTIPLIERS['lower_level']))  # -10% per level, minimum 30%
    else:  # Same level
        multiplier = 1.0

    winner_xp = int(base_xp_winner * multiplier)
    loser_xp = int(base_xp_loser * multiplier)

    return winner_xp, loser_xp


# --- Battle CRUD Operations ---
def battle_between_users(
    db: Session,
    user1_id: int,
    user2_id: int,
    user1_ship_numbers: Union[int, List[int]], 
    user2_ship_numbers: Union[int, List[int]],
    user1_formation: str = None,
    user2_formation: str = None
):
    """
    Unified battle system supporting 1v1 to 20v20 battles with tactical formations.
    
    Args:
        db: Database session
        user1_id, user2_id: User IDs of the combatants
        user1_ship_numbers, user2_ship_numbers: Ship number(s) - int for single ship, List[int] for fleet
        user1_formation, user2_formation: Formation strategy ("DEFENSIVE", "AGGRESSIVE", "TACTICAL")
                                         If None, uses user's default_formation
    
    Formations:
        - DEFENSIVE: +20% evasion, targets lowest HP ships (finish weak enemies)
        - AGGRESSIVE: Normal evasion, random targeting (spread damage)
        - TACTICAL: -10% evasion, targets highest attack ships (eliminate threats)
    
    Returns:
        Tuple of (BattleHistory, message) or (None, error_message)
    """
    # Get users
    user1 = db.query(User).filter(User.user_id == user1_id).first()
    user2 = db.query(User).filter(User.user_id == user2_id).first()
    
    if not user1 or not user2:
        return None, "User not found"
    
    # Use user's default formation if not specified
    if user1_formation is None:
        user1_formation = user1.default_formation
    if user2_formation is None:
        user2_formation = user2.default_formation
    
    if user1 == user2:
        return None, "Same user battle not allowed"
    
    # Get ships - only active ships are retrieved
    user1_ships = get_ships_by_numbers(db, user1_id, user1_ship_numbers)
    user2_ships = get_ships_by_numbers(db, user2_id, user2_ship_numbers)
    
    if not user1_ships or not user2_ships:
        return None, "No active ships found for battle"
    
    # Prepare fleet stats with rank bonuses
    user1_fleet = [prepare_ship_stats(ship, user1, db) for ship in user1_ships]
    user2_fleet = [prepare_ship_stats(ship, user2, db) for ship in user2_ships]
    
    # Battle initialization
    total_damage1 = 0
    total_damage2 = 0
    
    # Determine battle type for logging
    battle_type = "1v1" if len(user1_fleet) == 1 and len(user2_fleet) == 1 else "Fleet"
    fleet_info = f"({len(user1_fleet)}v{len(user2_fleet)})"
    
    battle_log = [
        f"{battle_type} Battle {fleet_info} started: {user1.nickname} vs {user2.nickname}",
        f"{user1.nickname} formation: {user1_formation} ({len(user1_fleet)} ships)",
        f"{user2.nickname} formation: {user2_formation} ({len(user2_fleet)} ships)"
    ]
    
    # Battle loop - maximum 20 rounds to prevent infinite battles
    for round_num in range(1, 21):
        # Check if any fleet is completely destroyed
        user1_active = [ship for ship in user1_fleet if ship['current_hp'] > 0]
        user2_active = [ship for ship in user2_fleet if ship['current_hp'] > 0]
        
        if not user1_active or not user2_active:
            break
        
        battle_log.append(f"--- Round {round_num} ---")
        battle_log.append(f"{user1.nickname}: {len(user1_active)} ships active, {user2.nickname}: {len(user2_active)} ships active")
        
        # User1 fleet attacks User2 fleet
        for attacking_ship in user1_active:
            if not user2_active:  # Check if enemy fleet still exists
                break
            
            # Select target based on formation strategy
            target_ship = select_target_by_formation(user1_formation, user2_active)
            if not target_ship:
                continue
            
            # Calculate evasion with formation modifier (DEFENSIVE impacts enemy evasion)
            target_evasion = target_ship['evasion'] * get_formation_evasion_modifier(user2_formation)
            
            # Each ship attacks based on its fire rate
            for _ in range(int(attacking_ship['fire_rate'])):
                if target_ship['current_hp'] <= 0:
                    break
                
                # Evasion check
                if random.random() < target_evasion:
                    battle_log.append(f"{target_ship['ship_name']} evaded attack from {attacking_ship['ship_name']}!")
                    continue
                
                # Calculate damage
                base_damage = attacking_ship['attack'] - (target_ship['shield'] * SHIELD_DAMAGE_REDUCTION)
                damage = base_damage * random.uniform(*DAMAGE_VARIATION_RANGE)
                damage = max(1, damage)
                
                # Apply damage
                target_ship['current_hp'] -= damage
                total_damage1 += damage
                
                battle_log.append(
                    f"{attacking_ship['ship_name']} hits {target_ship['ship_name']} for {damage:.1f} damage! "
                    f"({target_ship['ship_name']} HP: {max(0, target_ship['current_hp']):.1f})"
                )
                
                # Remove destroyed ship from active list
                if target_ship['current_hp'] <= 0:
                    battle_log.append(f"{target_ship['ship_name']} destroyed!")
                    user2_active.remove(target_ship)
                    break
        
        # Check if User2 fleet is destroyed
        if not user2_active:
            break
        
        # User2 fleet attacks User1 fleet
        for attacking_ship in user2_active:
            if not user1_active:  # Check if enemy fleet still exists
                break
            
            # Select target based on formation strategy
            target_ship = select_target_by_formation(user2_formation, user1_active)
            if not target_ship:
                continue
            
            # Calculate evasion with formation modifier (DEFENSIVE impacts enemy evasion)
            target_evasion = target_ship['evasion'] * get_formation_evasion_modifier(user1_formation)
            
            # Each ship attacks based on its fire rate
            for _ in range(int(attacking_ship['fire_rate'])):
                if target_ship['current_hp'] <= 0:
                    break
                
                # Evasion check
                if random.random() < target_evasion:
                    battle_log.append(f"{target_ship['ship_name']} evaded attack from {attacking_ship['ship_name']}!")
                    continue
                
                # Calculate damage
                base_damage = attacking_ship['attack'] - (target_ship['shield'] * SHIELD_DAMAGE_REDUCTION)
                damage = base_damage * random.uniform(*DAMAGE_VARIATION_RANGE)
                damage = max(1, damage)

                # Apply damage
                target_ship['current_hp'] -= damage
                total_damage2 += damage

                battle_log.append(
                    f"{attacking_ship['ship_name']} hits {target_ship['ship_name']} for {damage:.1f} damage! "
                    f"({target_ship['ship_name']} HP: {max(0, target_ship['current_hp']):.1f})"
                )

                # Remove destroyed ship from active list
                if target_ship['current_hp'] <= 0:
                    battle_log.append(f"{target_ship['ship_name']} destroyed!")
                    user1_active.remove(target_ship)
                    break
    
    # Determine winner based on remaining ships or total damage
    user1_survivors = [ship for ship in user1_fleet if ship['current_hp'] > 0]
    user2_survivors = [ship for ship in user2_fleet if ship['current_hp'] > 0]
    
    if user1_survivors and not user2_survivors:
        winner = user1
        loser = user2
        battle_log.append(f"{user1.nickname} wins! All enemy ships destroyed.")
    elif user2_survivors and not user1_survivors:
        winner = user2
        loser = user1
        battle_log.append(f"{user2.nickname} wins! All enemy ships destroyed.")
    elif total_damage1 > total_damage2:
        winner = user1
        loser = user2
        battle_log.append(f"{user1.nickname} wins by total damage! ({total_damage1:.1f} vs {total_damage2:.1f})")
    elif total_damage2 > total_damage1:
        winner = user2
        loser = user1
        battle_log.append(f"{user2.nickname} wins by total damage! ({total_damage2:.1f} vs {total_damage1:.1f})")
    else:
        # Tie-breaker: user with more surviving ships wins
        if len(user1_survivors) > len(user2_survivors):
            winner = user1
            loser = user2
            battle_log.append(f"{user1.nickname} wins by more surviving ships!")
        elif len(user2_survivors) > len(user1_survivors):
            winner = user2
            loser = user1
            battle_log.append(f"{user2.nickname} wins by more surviving ships!")
        else:
            # Final tie-breaker: random
            winner = random.choice([user1, user2])
            loser = user2 if winner == user1 else user1
            battle_log.append(f"{winner.nickname} wins by chance in a perfect tie!")
    
    # Update ship statuses and stats in database
    destroyed_ships = []
    ships_destroyed_by_user1 = 0
    ships_destroyed_by_user2 = 0
    ships_lost_by_user1 = 0
    ships_lost_by_user2 = 0
    
    # Process User1's ships
    for ship_stats in user1_fleet:
        ship_obj = ship_stats['ship_obj']
        if ship_stats['current_hp'] <= 0:
            ship_obj.status = "destroyed"
            ship_obj.actual_hp = 0
            ship_obj.actual_attack = 0
            ship_obj.actual_shield = 0
            ship_obj.actual_evasion = 0
            ship_obj.actual_fire_rate = 0
            ship_obj.actual_value = 0
            destroyed_ships.append(f"{user1.nickname}'s {ship_obj.ship_name} was destroyed.")
            ships_lost_by_user1 += 1
            ships_destroyed_by_user2 += 1
        else:
            # Apply damage degradation for surviving ships (only for humans, not NPCs)
            is_user1_npc = user1.nickname.startswith("NPC_")
            if not is_user1_npc:
                percent = max(0, ship_stats['current_hp'] / ship_stats['hp'])
                ship_obj.actual_hp = max(0, ship_stats['current_hp'])
                ship_obj.actual_attack = ship_obj.base_attack * percent
                ship_obj.actual_shield = ship_obj.base_shield * percent
                ship_obj.actual_evasion = ship_obj.base_evasion * percent
                ship_obj.actual_fire_rate = ship_obj.base_fire_rate * percent
                ship_obj.actual_value = int(ship_obj.base_value * percent)
            else:
                # NPC ships restore to full condition
                ship_obj.actual_hp = ship_obj.base_hp
                ship_obj.actual_attack = ship_obj.base_attack
                ship_obj.actual_shield = ship_obj.base_shield
                ship_obj.actual_evasion = ship_obj.base_evasion
                ship_obj.actual_fire_rate = ship_obj.base_fire_rate
                ship_obj.actual_value = ship_obj.base_value
    
    # Process User2's ships
    for ship_stats in user2_fleet:
        ship_obj = ship_stats['ship_obj']
        if ship_stats['current_hp'] <= 0:
            ship_obj.status = "destroyed"
            ship_obj.actual_hp = 0
            ship_obj.actual_attack = 0
            ship_obj.actual_shield = 0
            ship_obj.actual_evasion = 0
            ship_obj.actual_fire_rate = 0
            ship_obj.actual_value = 0
            destroyed_ships.append(f"{user2.nickname}'s {ship_obj.ship_name} was destroyed.")
            ships_lost_by_user2 += 1
            ships_destroyed_by_user1 += 1
        else:
            # Apply damage degradation for surviving ships (only for humans, not NPCs)
            is_user2_npc = user2.nickname.startswith("NPC_")
            if not is_user2_npc:
                percent = max(0, ship_stats['current_hp'] / ship_stats['hp'])
                ship_obj.actual_hp = max(0, ship_stats['current_hp'])
                ship_obj.actual_attack = ship_obj.base_attack * percent
                ship_obj.actual_shield = ship_obj.base_shield * percent
                ship_obj.actual_evasion = ship_obj.base_evasion * percent
                ship_obj.actual_fire_rate = ship_obj.base_fire_rate * percent
                ship_obj.actual_value = int(ship_obj.base_value * percent)
            else:
                # NPC ships restore to full condition
                ship_obj.actual_hp = ship_obj.base_hp
                ship_obj.actual_attack = ship_obj.base_attack
                ship_obj.actual_shield = ship_obj.base_shield
                ship_obj.actual_evasion = ship_obj.base_evasion
                ship_obj.actual_fire_rate = ship_obj.base_fire_rate
                ship_obj.actual_value = ship_obj.base_value
    
    # Special NPC restoration for destroyed ships
    is_user1_npc = user1.nickname.startswith("NPC_")
    is_user2_npc = user2.nickname.startswith("NPC_")
    
    if is_user1_npc:
        for ship_stats in user1_fleet:
            ship_obj = ship_stats['ship_obj']
            if ship_obj.status == "destroyed":
                ship_obj.status = "active"
                ship_obj.actual_hp = ship_obj.base_hp
                ship_obj.actual_attack = ship_obj.base_attack
                ship_obj.actual_shield = ship_obj.base_shield
                ship_obj.actual_evasion = ship_obj.base_evasion
                ship_obj.actual_fire_rate = ship_obj.base_fire_rate
                ship_obj.actual_value = ship_obj.base_value
                battle_log.append(f"NPC {user1.nickname}'s {ship_obj.ship_name} restored and reactivated")
    
    if is_user2_npc:
        for ship_stats in user2_fleet:
            ship_obj = ship_stats['ship_obj']
            if ship_obj.status == "destroyed":
                ship_obj.status = "active"
                ship_obj.actual_hp = ship_obj.base_hp
                ship_obj.actual_attack = ship_obj.base_attack
                ship_obj.actual_shield = ship_obj.base_shield
                ship_obj.actual_evasion = ship_obj.base_evasion
                ship_obj.actual_fire_rate = ship_obj.base_fire_rate
                ship_obj.actual_value = ship_obj.base_value
                battle_log.append(f"NPC {user2.nickname}'s {ship_obj.ship_name} restored and reactivated")
    
    # Log destroyed ships
    for msg in destroyed_ships:
        battle_log.append(msg)
    
    # Update user statistics
    winner.victories += 1
    loser.defeats += 1
    
    user1.damage_dealt += total_damage1
    user1.damage_taken += total_damage2
    user2.damage_dealt += total_damage2
    user2.damage_taken += total_damage1
    
    user1.ships_destroyed_by_user += ships_destroyed_by_user1
    user1.ships_lost_by_user += ships_lost_by_user1
    user2.ships_destroyed_by_user += ships_destroyed_by_user2
    user2.ships_lost_by_user += ships_lost_by_user2
    
    # Award credits for victories
    if winner.nickname.startswith("NPC_"):
        # NPC winner doesn't get credits
        pass
    else:
        loser_value = sum(ship_stats['value'] for ship_stats in 
                         (user2_fleet if winner == user1 else user1_fleet))
        credits_awarded = loser_value * CREDITS_AWARDED_MULTIPLIER
        winner.currency_value += credits_awarded
        battle_log.append(f"{winner.nickname} awarded {credits_awarded:.0f} credits!")
    
    # Calculate and update Elo ratings
    winner.elo_rank, loser.elo_rank = calculate_elo_change(winner.elo_rank, loser.elo_rank)
    
    # Calculate XP gain for winner and loser
    if not winner.nickname.startswith("NPC_"):
        winner_xp, _ = calculate_xp_gain(winner.level, loser.level)
        winner.experience += winner_xp
        battle_log.append(f"{winner.nickname} gains {winner_xp} XP!")

    if not loser.nickname.startswith("NPC_"):
        _, loser_xp = calculate_xp_gain(winner.level, loser.level)
        loser.experience += loser_xp
        battle_log.append(f"{loser.nickname} gains {loser_xp} XP!")
    
    # Create and save battle history
    final_user1_hp = sum(max(0, ship['current_hp']) for ship in user1_fleet)
    final_user2_hp = sum(max(0, ship['current_hp']) for ship in user2_fleet)
    
    # Prepare ship data for battle history
    user1_ship_data = []
    user2_ship_data = []
    
    for ship_stats in user1_fleet:
        ship_obj = ship_stats['ship_obj']
        user1_ship_data.append({
            "user_id": user1.user_id, 
            "nickname": user1.nickname, 
            "ship_number": ship_obj.ship_number,
            "ship_name": ship_obj.ship_name, 
            "attack": ship_stats['attack'], 
            "shield": ship_stats['shield'],
            "evasion": ship_stats['evasion'], 
            "fire_rate": ship_stats['fire_rate'], 
            "hp": ship_stats['hp'], 
            "value": ship_stats['value']
        })
    
    for ship_stats in user2_fleet:
        ship_obj = ship_stats['ship_obj']
        user2_ship_data.append({
            "user_id": user2.user_id, 
            "nickname": user2.nickname, 
            "ship_number": ship_obj.ship_number,
            "ship_name": ship_obj.ship_name, 
            "attack": ship_stats['attack'], 
            "shield": ship_stats['shield'],
            "evasion": ship_stats['evasion'], 
            "fire_rate": ship_stats['fire_rate'], 
            "hp": ship_stats['hp'], 
            "value": ship_stats['value']
        })
    
    battle_history = BattleHistory(
        participants=user1_ship_data + user2_ship_data,
        battle_log=battle_log,
        winner_user_id=winner.user_id,
        extra={
            "formations": {"user1": user1_formation, "user2": user2_formation},
            "final_hp": {user1.nickname: final_user1_hp, user2.nickname: final_user2_hp},
            "total_damage": {user1.nickname: total_damage1, user2.nickname: total_damage2},
            "winner": winner.nickname,
            "battle_type": f"{battle_type} {fleet_info}",
            "ships_destroyed": {"user1": ships_lost_by_user1, "user2": ships_lost_by_user2}
        }
    )
    
    db.add(battle_history)
    db.commit()
    
    return battle_history, f"{winner.nickname} wins the {battle_type.lower()} battle {fleet_info}!"


def activate_owned_ship(db: Session, user_id: int, ship_number: int):
    """
    Set the status of a user's owned ship to 'active'.
    Now includes validation of maximum active ships based on user rank.
    """
    from backend.app.utils.progression_utils import can_activate_ship
    
    # Get the user to check rank limits
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None, "User not found"
    
    # Check if user can activate another ship based on rank limits
    can_activate, limit_message = can_activate_ship(user, db)
    if not can_activate:
        return None, limit_message
    
    # Find the ship to activate
    owned_ship = db.query(OwnedShips).filter(
        OwnedShips.user_id == user_id,
        OwnedShips.ship_number == ship_number,
        OwnedShips.status == 'owned'
    ).first()
    
    if not owned_ship:
        return None, "Owned ship not found or not available to activate"
    
    # Activate the ship
    owned_ship.status = 'active'
    db.commit()
    db.refresh(owned_ship)
    
    return owned_ship, f"Ship activated successfully! {limit_message}"


def deactivate_owned_ship(db: Session, user_id: int, ship_number: int):
    """
    Set the status of a user's owned ship from 'active' to 'owned'.
    Allows users to free up active ship slots.
    """
    owned_ship = db.query(OwnedShips).filter(
        OwnedShips.user_id == user_id,
        OwnedShips.ship_number == ship_number,
        OwnedShips.status == 'active'
    ).first()
    
    if not owned_ship:
        return None, "Active ship not found or not available to deactivate"
    
    # Deactivate the ship
    owned_ship.status = 'owned'
    db.commit()
    db.refresh(owned_ship)
    
    return owned_ship, "Ship deactivated successfully"


def get_user_ship_limits_info(db: Session, user_id: int):
    """
    Get information about a user's ship limits and current usage.
    Useful for frontend display.
    """
    from backend.app.utils.progression_utils import get_max_active_ships_for_user, count_active_ships_for_user
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    
    max_allowed = get_max_active_ships_for_user(user, db)
    current_active = count_active_ships_for_user(user_id, db)
    
    return {
        "user_rank": user.rank.value,
        "user_level": user.level,
        "max_active_ships": max_allowed,
        "current_active_ships": current_active,
        "can_activate_more": current_active < max_allowed,
        "slots_remaining": max_allowed - current_active
    }