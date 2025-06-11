# app/crud.py
from sqlalchemy.orm import Session
from app import schemas
from app.database import create_schemas as models
from app.database.create_schemas import User, Ship, OwnedShips, BattleHistory
from datetime import datetime
import random

# --- Ship CRUD Operations ---
def get_ship(db: Session, ship_id: int):
    return db.query(models.Ship).filter(models.Ship.ship_id == ship_id).first()

def get_ships(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ship).offset(skip).limit(limit).all()

def create_ship(db: Session, ship: schemas.ShipCreate):
    db_ship = models.Ship(**ship.dict())
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship

def update_ship(db: Session, ship_id: int, ship_data: schemas.ShipCreate):
    db_ship = db.query(models.Ship).filter(models.Ship.ship_id == ship_id).first()
    if db_ship:
        for key, value in ship_data.dict(exclude_unset=True).items():
            setattr(db_ship, key, value)
        db.commit()
        db.refresh(db_ship)
    return db_ship

def delete_ship(db: Session, ship_id: int):
    db_ship = db.query(models.Ship).filter(models.Ship.ship_id == ship_id).first()
    if db_ship:
        db.delete(db_ship)
        db.commit()
        return True
    return False

# --- User CRUD Operations ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Market CRUD Operations ---
def buy_ship(db: Session, user_id: int, ship_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    ship = db.query(Ship).filter(Ship.ship_id == ship_id).first()
    if not user or not ship:
        return None, "User or Ship not found"
    if user.currency_value < ship.value:
        return None, "Insufficient funds"
    user.currency_value -= ship.value
    owned_ship = OwnedShips(
        user_id=user_id,
        ship_id=ship_id,
        status='owned',
        ship_name=ship.ship_name,
        attack=ship.attack,
        shield=ship.shield,
        evasion=ship.evasion,
        fire_rate=ship.fire_rate,
        hp=ship.hp,
        value=ship.value
    )
    db.add(owned_ship)
    db.commit()
    db.refresh(owned_ship)
    return owned_ship, "Ship purchased successfully"

def sell_ship(db: Session, user_id: int, owned_ship_id: int):
    owned_ship = db.query(OwnedShips).filter(
        OwnedShips.ship_number == owned_ship_id,
        OwnedShips.user_id == user_id,
        OwnedShips.status == 'owned'
    ).first()
    if not owned_ship:
        return None, "Owned ship not found or already sold"
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None, "User not found"
    sell_value = int(owned_ship.value * 0.4)
    user.currency_value += sell_value
    owned_ship.status = 'sold'
    db.commit()
    return sell_value, "Ship sold successfully"

# --- Battle CRUD Operations ---
def battle_between_users(db: Session, user1_id: int, user2_id: int, user1_ship_number: int, user2_ship_number: int):
    user1 = db.query(User).filter(User.user_id == user1_id).first()
    user2 = db.query(User).filter(User.user_id == user2_id).first()
    ship1 = db.query(OwnedShips).filter(OwnedShips.ship_number == user1_ship_number, OwnedShips.user_id == user1_id, OwnedShips.status == 'owned').first()
    ship2 = db.query(OwnedShips).filter(OwnedShips.ship_number == user2_ship_number, OwnedShips.user_id == user2_id, OwnedShips.status == 'owned').first()
    
    if not user1 or not user2 or not ship1 or not ship2 or user1 == user2:
        return None, "User or ship not found"

    hp1 = ship1.hp
    hp2 = ship2.hp
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
        for _ in range(int(ship1.fire_rate)):
            if hp2 <= 0:
                break
            if random.random() < (ship2.evasion / 100):
                battle_log.append(f"{user2.nickname} evaded an attack from {user1.nickname}!")
                continue
            base_damage = ship1.attack - (ship2.shield * 0.5)
            damage = base_damage * random.uniform(0.85, 1.15)
            damage = max(0, damage)
            hp2 -= damage
            total_damage1 += damage
            battle_log.append(f"{user1.nickname} hits {user2.nickname} for {damage:.1f} damage! ({user2.nickname} HP: {max(0, hp2):.1f})")

        # User2 attacks User1
        for _ in range(int(ship2.fire_rate)):
            if hp1 <= 0:
                break
            if random.random() < (ship1.evasion / 100):
                battle_log.append(f"{user1.nickname} evaded an attack from {user2.nickname}!")
                continue
            base_damage = ship2.attack - (ship1.shield * 0.5)
            damage = base_damage * random.uniform(0.85, 1.15)
            damage = max(0, damage)
            hp1 -= damage
            total_damage2 += damage
            battle_log.append(f"{user2.nickname} hits {user1.nickname} for {damage:.1f} damage! ({user1.nickname} HP: {max(0, hp1):.1f})")

    # Check for destroyed ships and update status
    destroyed_ships = []
    if hp1 <= 0:
        ship1.status = "destroyed"
        destroyed_ships.append(f"{user1.nickname}'s ship ({ship1.ship_name}) was destroyed.")
    if hp2 <= 0:
        ship2.status = "destroyed"
        destroyed_ships.append(f"{user2.nickname}'s ship ({ship2.ship_name}) was destroyed.")

    # Add destroyed ships info to battle log
    if destroyed_ships:
        for msg in destroyed_ships:
            battle_log.append(msg)

    # Determine winner
    if hp1 <= 0 and hp2 <= 0:
        # Both destroyed, decide by total damage
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
        # No ship destroyed, decide by total damage
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

    # Save battle history
    battle_history = BattleHistory(
        timestamp=datetime.utcnow(),
        participants=[
            {
                "user_id": user1.user_id, "nickname": user1.nickname, "ship_number": ship1.ship_number,
                "ship_name": ship1.ship_name, "attack": ship1.attack, "shield": ship1.shield,
                "evasion": ship1.evasion, "fire_rate": ship1.fire_rate, "hp": ship1.hp, "value": ship1.value
            },
            {
                "user_id": user2.user_id, "nickname": user2.nickname, "ship_number": ship2.ship_number,
                "ship_name": ship2.ship_name, "attack": ship2.attack, "shield": ship2.shield,
                "evasion": ship2.evasion, "fire_rate": ship2.fire_rate, "hp": ship2.hp, "value": ship2.value
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
    return battle_history, "Battle finished"