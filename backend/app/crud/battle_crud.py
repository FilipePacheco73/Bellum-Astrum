from sqlalchemy.orm import Session
from database import User, OwnedShips, BattleHistory
from datetime import datetime, UTC
from backend.app.utils.progression_utils import apply_rank_bonus_to_ship_stats
import random

# --- Battle CRUD Operations ---
def battle_between_users(db: Session, user1_id: int, user2_id: int, user1_ship_number: int, user2_ship_number: int):
    user1 = db.query(User).filter(User.user_id == user1_id).first()
    user2 = db.query(User).filter(User.user_id == user2_id).first()
    ship1 = db.query(OwnedShips).filter(OwnedShips.ship_number == user1_ship_number, OwnedShips.user_id == user1_id, OwnedShips.status == 'active').first()
    ship2 = db.query(OwnedShips).filter(OwnedShips.ship_number == user2_ship_number, OwnedShips.user_id == user2_id, OwnedShips.status == 'active').first()
    
    if not user1 or not user2 or not ship1 or not ship2 or user1 == user2:
        return None, "User or ship not found"

    # Apply rank bonus to ship stats
    ship1_stats = {
        'attack': ship1.actual_attack,
        'shield': ship1.actual_shield,
        'hp': ship1.actual_hp,
        'evasion': ship1.actual_evasion,
        'fire_rate': ship1.actual_fire_rate,
        'value': ship1.actual_value
    }
    ship2_stats = {
        'attack': ship2.actual_attack,
        'shield': ship2.actual_shield,
        'hp': ship2.actual_hp,
        'evasion': ship2.actual_evasion,
        'fire_rate': ship2.actual_fire_rate,
        'value': ship2.actual_value
    }
    ship1_stats = apply_rank_bonus_to_ship_stats(user1, ship1_stats, db)
    ship2_stats = apply_rank_bonus_to_ship_stats(user2, ship2_stats, db)

    hp1 = ship1_stats['hp']
    hp2 = ship2_stats['hp']
    total_damage1 = 0
    total_damage2 = 0

    battle_log = [
        f"Battle started: {user1.nickname} ({ship1.ship_name}) vs {user2.nickname} ({ship2.ship_name})"
    ]


    for round_num in range(1, 11):
        if hp1 <= 0 or hp2 <= 0:
            break
        battle_log.append(f"--- Round {round_num} ---")

        # User1 attacks User2
        for _ in range(int(ship1_stats['fire_rate'])):
            if hp2 <= 0:
                break
            if random.random() < (ship2_stats['evasion']):
                battle_log.append(f"{user2.nickname} evaded an attack from {user1.nickname}!")
                continue
            base_damage = ship1_stats['attack'] - (ship2_stats['shield'] * 0.5)
            damage = base_damage * random.uniform(0.85, 1.15)
            damage = max(1, damage)
            hp2 -= damage
            total_damage1 += damage
            battle_log.append(f"{user1.nickname} hits {user2.nickname} for {damage:.1f} damage! ({user2.nickname} HP: {max(0, hp2):.1f})")

        # User2 attacks User1
        for _ in range(int(ship2_stats['fire_rate'])):
            if hp1 <= 0:
                break
            if random.random() < (ship1_stats['evasion']):
                battle_log.append(f"{user1.nickname} evaded an attack from {user2.nickname}!")
                continue
            base_damage = ship2_stats['attack'] - (ship1_stats['shield'] * 0.5)
            damage = base_damage * random.uniform(0.85, 1.15)
            damage = max(0, damage)
            hp1 -= damage
            total_damage2 += damage
            battle_log.append(f"{user2.nickname} hits {user1.nickname} for {damage:.1f} damage! ({user1.nickname} HP: {max(0, hp1):.1f})")

    # Check for destroyed ships and update status
    destroyed_ships = []
    if hp1 <= 0:
        ship1.status = "destroyed"
        ship1.actual_hp = 0
        ship1.actual_attack = 0
        ship1.actual_shield = 0
        ship1.actual_evasion = 0
        ship1.actual_fire_rate = 0
        ship1.actual_value = 0
        destroyed_ships.append(f"{user1.nickname}'s ship ({ship1.ship_name}) was destroyed.")
    if hp2 <= 0:
        ship2.status = "destroyed"
        ship2.actual_hp = 0
        ship2.actual_attack = 0
        ship2.actual_shield = 0
        ship2.actual_evasion = 0
        ship2.actual_fire_rate = 0
        ship2.actual_value = 0
        destroyed_ships.append(f"{user2.nickname}'s ship ({ship2.ship_name}) was destroyed.")

    if destroyed_ships:
        db.commit()
        for msg in destroyed_ships:
            battle_log.append(msg)

    # Determine winner
    if hp1 <= 0 and hp2 <= 0:
        if total_damage1 >= total_damage2:
            winner = user1
            loser = user2
            winner_hp = 0
            loser_hp = 0
            battle_log.append(f"Both ships destroyed! {user1.nickname} wins by higher total damage.")
        else:
            winner = user2
            loser = user1
            winner_hp = 0
            loser_hp = 0
            battle_log.append(f"Both ships destroyed! {user2.nickname} wins by higher total damage.")
    elif hp2 <= 0:
        winner = user1
        loser = user2
        winner_hp = hp1
        loser_hp = 0
        battle_log.append(f"{user1.nickname} destroyed {user2.nickname}'s ship!")
    elif hp1 <= 0:
        winner = user2
        loser = user1
        winner_hp = hp2
        loser_hp = 0
        battle_log.append(f"{user2.nickname} destroyed {user1.nickname}'s ship!")
    else:
        if total_damage1 >= total_damage2:
            winner = user1
            loser = user2
            winner_hp = hp1
            loser_hp = hp2
            battle_log.append(f"No ship destroyed! {user1.nickname} wins by higher total damage.")
        else:
            winner = user2
            loser = user1
            winner_hp = hp2
            loser_hp = hp1
            battle_log.append(f"No ship destroyed! {user2.nickname} wins by higher total damage.")

    # Update stats and currency
    winner.victories += 1
    loser.defeats += 1

    user1.damage_dealt += total_damage1
    user1.damage_taken += total_damage2
    user2.damage_dealt += total_damage2
    user2.damage_taken += total_damage1

    # Currency transfer - NPCs don't gain or lose money
    is_loser_npc = loser.nickname.startswith("NPC_")
    is_winner_npc = winner.nickname.startswith("NPC_")
    percent = random.uniform(0.05, 0.15)
    transfer = int(loser.currency_value * percent)
    transfer = max(0, transfer)
    
    if not is_loser_npc and not is_winner_npc:
        # Human vs Human - normal currency transfer
        loser.currency_value -= transfer
        winner.currency_value += transfer
        battle_log.append(f"{winner.nickname} wins and steals {transfer} credits from {loser.nickname}!")
    elif not is_loser_npc and is_winner_npc:
        # Human loses to NPC - human loses money, NPC doesn't gain
        loser.currency_value -= transfer
        battle_log.append(f"NPC {winner.nickname} wins! {loser.nickname} loses {transfer} credits!")
    elif is_loser_npc and not is_winner_npc:
        # Human beats NPC - human gains money, NPC doesn't lose
        winner.currency_value += transfer
        battle_log.append(f"{winner.nickname} wins and receives {transfer} credits for defeating NPC {loser.nickname}!")
    else:
        # NPC vs NPC - no currency transfer
        battle_log.append(f"NPC {winner.nickname} defeats NPC {loser.nickname} - no currency transfer between NPCs")
    
    winner_id = winner.user_id

    # Update ships destroyed/lost stats
    if hp1 <= 0:
        user1.ships_lost_by_user += 1
        user2.ships_destroyed_by_user += 1
    if hp2 <= 0:
        user2.ships_lost_by_user += 1
        user1.ships_destroyed_by_user += 1

    db.commit()

    # ELO Rank update - NPCs get special handling
    def calculate_elo(winner_elo, loser_elo, k=32):
        expected_win = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
        new_winner_elo = winner_elo + k * (1 - expected_win)
        new_loser_elo = loser_elo + k * (0 - (1 - expected_win))
        return new_winner_elo, new_loser_elo

    is_winner_npc = winner.nickname.startswith("NPC_")
    is_loser_npc = loser.nickname.startswith("NPC_")
    
    if not is_winner_npc and not is_loser_npc:
        # Both are human players - normal ELO calculation
        new_winner_elo, new_loser_elo = calculate_elo(winner.elo_rank, loser.elo_rank)
        winner.elo_rank = new_winner_elo
        loser.elo_rank = new_loser_elo
        battle_log.append(f"Setting ELO - Winner after: {winner.elo_rank:.1f}")
        battle_log.append(f"Setting ELO - Loser after: {loser.elo_rank:.1f}")
    elif not is_winner_npc and is_loser_npc:
        # Human beats NPC - only human gains ELO
        new_winner_elo, _ = calculate_elo(winner.elo_rank, loser.elo_rank)
        winner.elo_rank = new_winner_elo
        battle_log.append(f"Setting ELO - {winner.nickname} after: {winner.elo_rank:.1f}")
        battle_log.append(f"NPC {loser.nickname} ELO unchanged: {loser.elo_rank:.1f}")
    elif is_winner_npc and not is_loser_npc:
        # NPC beats Human - only human loses ELO
        _, new_loser_elo = calculate_elo(winner.elo_rank, loser.elo_rank)
        loser.elo_rank = new_loser_elo
        battle_log.append(f"NPC {winner.nickname} ELO unchanged: {winner.elo_rank:.1f}")
        battle_log.append(f"Setting ELO - {loser.nickname} after: {loser.elo_rank:.1f}")
    else:
        # Both NPCs - no ELO changes
        battle_log.append(f"Both NPCs - ELO unchanged: {winner.nickname}: {winner.elo_rank:.1f}, {loser.nickname}: {loser.elo_rank:.1f}")

    # XP Gain calculation - NPCs don't gain XP
    def calculate_xp_gain(winner_level, loser_level, base_xp_winner=50, base_xp_loser=10):
        """
        Calculate XP gain for both winner and loser based on level difference.
        Winner always gets more XP, but fighting higher level opponents gives more XP.
        Fighting lower level opponents gives less XP.
        """
        level_diff = loser_level - winner_level
        
        # XP multiplier based on level difference
        if level_diff > 0:  # Fighting higher level opponent
            multiplier = 1 + (level_diff * 0.15)  # +15% per level difference
        elif level_diff < 0:  # Fighting lower level opponent
            multiplier = max(0.3, 1 + (level_diff * 0.1))  # -10% per level, minimum 30%
        else:  # Same level
            multiplier = 1.0
        
        winner_xp = int(base_xp_winner * multiplier)
        loser_xp = int(base_xp_loser * multiplier)
        
        return winner_xp, loser_xp

    # Apply XP gain - only for human players
    if not is_winner_npc:
        winner_xp_gain, _ = calculate_xp_gain(winner.level, loser.level)
        winner.experience += winner_xp_gain
        battle_log.append(f"{winner.nickname} gained {winner_xp_gain} XP! (Total: {winner.experience})")
    else:
        battle_log.append(f"NPC {winner.nickname} does not gain XP")
    
    if not is_loser_npc:
        _, loser_xp_gain = calculate_xp_gain(winner.level, loser.level)
        loser.experience += loser_xp_gain
        battle_log.append(f"{loser.nickname} gained {loser_xp_gain} XP! (Total: {loser.experience})")
    else:
        battle_log.append(f"NPC {loser.nickname} does not gain XP")

    # Check for level ups - only for human players
    from backend.app.utils.progression_utils import get_level_for_experience, check_rank_promotion

    # Check winner level up
    if not is_winner_npc:
        new_winner_level = get_level_for_experience(winner.experience)
        if new_winner_level > winner.level:
            winner.level = new_winner_level
            battle_log.append(f"🎉 {winner.nickname} leveled up to level {new_winner_level}!")
            
            # Check for rank promotion
            new_rank = check_rank_promotion(winner, db)
            if new_rank and new_rank != winner.rank:
                old_rank = winner.rank.value
                winner.rank = new_rank
                battle_log.append(f"🏆 {winner.nickname} promoted to {new_rank.value}!")

    # Check loser level up
    if not is_loser_npc:
        new_loser_level = get_level_for_experience(loser.experience)
        if new_loser_level > loser.level:
            loser.level = new_loser_level
            battle_log.append(f"🎉 {loser.nickname} leveled up to level {new_loser_level}!")
            
            # Check for rank promotion
            new_rank = check_rank_promotion(loser, db)
            if new_rank and new_rank != loser.rank:
                old_rank = loser.rank.value
                loser.rank = new_rank
                battle_log.append(f"🏆 {loser.nickname} promoted to {new_rank.value}!")

    db.commit()

    # Save battle history
    battle_history = BattleHistory(
        timestamp=datetime.now(UTC),
        participants=[
            {
                "user_id": user1.user_id, "nickname": user1.nickname, "ship_number": ship1.ship_number,
                "ship_name": ship1.ship_name, "attack": ship1.actual_attack, "shield": ship1.actual_shield,
                "evasion": ship1.actual_evasion, "fire_rate": ship1.actual_fire_rate, "hp": ship1.actual_hp, "value": ship1.actual_value
            },
            {
                "user_id": user2.user_id, "nickname": user2.nickname, "ship_number": ship2.ship_number,
                "ship_name": ship2.ship_name, "attack": ship2.actual_attack, "shield": ship2.actual_shield,
                "evasion": ship2.actual_evasion, "fire_rate": ship2.actual_fire_rate, "hp": ship2.actual_hp, "value": ship2.actual_value
            }
        ],
        winner_user_id=winner_id,
        battle_log=battle_log,
        extra={
            "final_hp": {user1.nickname: max(0, hp1), user2.nickname: max(0, hp2)},
            "total_damage": {user1.nickname: total_damage1, user2.nickname: total_damage2}
        }
    )
    db.add(battle_history)
    db.commit()
    db.refresh(battle_history)

    # Update ships' 'actual_' attributes after battle - NPCs don't degrade
    for ship, hp, user in [(ship1, hp1, user1), (ship2, hp2, user2)]:
        is_ship_owner_npc = user.nickname.startswith("NPC_")
        
        if ship.status != "destroyed":
            if not is_ship_owner_npc:
                # Human player ship - normal degradation based on damage
                percent = max(0, hp / ship.base_hp)
                ship.actual_hp = max(0, hp)
                ship.actual_attack = ship.base_attack * percent
                ship.actual_shield = ship.base_shield * percent
                ship.actual_evasion = ship.base_evasion * percent
                ship.actual_fire_rate = ship.base_fire_rate * percent
                ship.actual_value = int(ship.base_value * percent)
            else:
                # NPC ship - restore to full stats for next battle
                ship.actual_hp = ship.base_hp
                ship.actual_attack = ship.base_attack
                ship.actual_shield = ship.base_shield
                ship.actual_evasion = ship.base_evasion
                ship.actual_fire_rate = ship.base_fire_rate
                ship.actual_value = ship.base_value
                battle_log.append(f"NPC {user.nickname}'s ship {ship.ship_name} restored to full condition")
        elif is_ship_owner_npc:
            # NPC ship was destroyed - restore it completely
            ship.status = "active"
            ship.actual_hp = ship.base_hp
            ship.actual_attack = ship.base_attack
            ship.actual_shield = ship.base_shield
            ship.actual_evasion = ship.base_evasion
            ship.actual_fire_rate = ship.base_fire_rate
            ship.actual_value = ship.base_value
            battle_log.append(f"NPC {user.nickname}'s destroyed ship {ship.ship_name} has been restored and reactivated")
    
    db.commit()

    return battle_history, "Battle finished"

def activate_owned_ship(db: Session, user_id: int, ship_number: int):
    """
    Set the status of a user's owned ship to 'active'.
    """
    owned_ship = db.query(OwnedShips).filter(
        OwnedShips.user_id == user_id,
        OwnedShips.ship_number == ship_number,
        OwnedShips.status == 'owned'
    ).first()
    if not owned_ship:
        return None, "Owned ship not found or not available to activate"
    owned_ship.status = 'active'
    db.commit()
    db.refresh(owned_ship)
    return owned_ship, "Ship activated successfully"