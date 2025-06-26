from sqlalchemy.orm import Session
from backend.app import schemas
from backend.app.database import create_schemas as models
from backend.app.database.create_schemas import User, OwnedShips, BattleHistory
from datetime import datetime, UTC
import random

# --- Battle CRUD Operations ---
def battle_between_users(db: Session, user1_id: int, user2_id: int, user1_ship_number: int, user2_ship_number: int):
    user1 = db.query(User).filter(User.user_id == user1_id).first()
    user2 = db.query(User).filter(User.user_id == user2_id).first()
    ship1 = db.query(OwnedShips).filter(OwnedShips.ship_number == user1_ship_number, OwnedShips.user_id == user1_id, OwnedShips.status == 'active').first()
    ship2 = db.query(OwnedShips).filter(OwnedShips.ship_number == user2_ship_number, OwnedShips.user_id == user2_id, OwnedShips.status == 'active').first()
    
    if not user1 or not user2 or not ship1 or not ship2 or user1 == user2:
        return None, "User or ship not found"

    # Use actual_ stats for the battle
    hp1 = ship1.actual_hp
    hp2 = ship2.actual_hp
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
        for _ in range(int(ship1.actual_fire_rate)):
            if hp2 <= 0:
                break
            if random.random() < (ship2.actual_evasion / 100):
                battle_log.append(f"{user2.nickname} evaded an attack from {user1.nickname}!")
                continue
            base_damage = ship1.actual_attack - (ship2.actual_shield * 0.5)
            damage = base_damage * random.uniform(0.85, 1.15)
            damage = max(1, damage)
            hp2 -= damage
            total_damage1 += damage
            battle_log.append(f"{user1.nickname} hits {user2.nickname} for {damage:.1f} damage! ({user2.nickname} HP: {max(0, hp2):.1f})")

        # User2 attacks User1
        for _ in range(int(ship2.actual_fire_rate)):
            if hp1 <= 0:
                break
            if random.random() < (ship1.actual_evasion / 100):
                battle_log.append(f"{user1.nickname} evaded an attack from {user2.nickname}!")
                continue
            base_damage = ship2.actual_attack - (ship1.actual_shield * 0.5)
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

    percent = random.uniform(0.05, 0.15)
    transfer = int(loser.currency_value * percent)
    transfer = max(0, transfer)
    loser.currency_value -= transfer
    winner.currency_value += transfer
    battle_log.append(f"{winner.nickname} wins and steals {transfer} credits from {loser.nickname}!")
    winner_id = winner.user_id

    # Update ships destroyed/lost stats
    if hp1 <= 0:
        loser.ships_lost_by_user += 1
        winner.ships_destroyed_by_user += 1
    if hp2 <= 0:
        winner.ships_destroyed_by_user += 1
        loser.ships_lost_by_user += 1

    db.commit()

    # ELO Rank update
    def calculate_elo(winner_elo, loser_elo, k=32):
        expected_win = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
        new_winner_elo = winner_elo + k * (1 - expected_win)
        new_loser_elo = loser_elo + k * (0 - (1 - expected_win))
        return new_winner_elo, new_loser_elo

    new_winner_elo, new_loser_elo = calculate_elo(winner.elo_rank, loser.elo_rank)
    winner.elo_rank = new_winner_elo
    loser.elo_rank = new_loser_elo
    battle_log.append(f"Setting ELO - Winner after: {winner.elo_rank}")
    battle_log.append(f"Setting ELO - Loser after: {loser.elo_rank}")
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

    # Update ships' 'actual_' attributes after battle
    for ship, hp, user in [(ship1, hp1, user1), (ship2, hp2, user2)]:
        if ship.status != "destroyed":
            # Calculates the percentage of remaining HP relative to the base
            percent = max(0, hp / ship.base_hp)
            # Update current HP
            ship.actual_hp = max(0, hp)
            # Updates other attributes proportional to remaining HP
            ship.actual_attack = ship.base_attack * percent
            ship.actual_shield = ship.base_shield * percent
            ship.actual_evasion = ship.base_evasion * percent
            ship.actual_fire_rate = ship.base_fire_rate * percent
            ship.actual_value = int(ship.base_value * percent)
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