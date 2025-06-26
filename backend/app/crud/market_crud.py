from sqlalchemy.orm import Session
from backend.app import schemas
from backend.app.database.create_schemas import User, Ship, OwnedShips

# --- Market CRUD Operations ---
def buy_ship(db: Session, user_id: int, ship_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    ship = db.query(Ship).filter(Ship.ship_id == ship_id).first()
    if not user or not ship:
        return False, "User or ship not found", None
    if user.currency_value < ship.value:
        return False, "Not enough currency to buy this ship", None

    # Deduct currency
    user.currency_value -= ship.value

    # Create owned ship with base_ and actual_ stats
    owned_ship = OwnedShips(
        user_id=user_id,
        ship_id=ship_id,
        ship_name=ship.ship_name,
        status='owned',
        base_attack=ship.attack,
        base_shield=ship.shield,
        base_evasion=ship.evasion,
        base_fire_rate=ship.fire_rate,
        base_hp=ship.hp,
        base_value=ship.value,
        actual_attack=ship.attack,
        actual_shield=ship.shield,
        actual_evasion=ship.evasion,
        actual_fire_rate=ship.fire_rate,
        actual_hp=ship.hp,
        actual_value=ship.value
    )
    db.add(owned_ship)
    db.commit()
    db.refresh(owned_ship)
    return True, "Ship bought successfully", owned_ship.ship_number

def sell_ship(db: Session, user_id: int, owned_ship_id: int):
    owned_ship = db.query(OwnedShips).filter(
        OwnedShips.ship_number == owned_ship_id,
        OwnedShips.user_id == user_id,
        OwnedShips.status != 'destroyed'
    ).first()
    if not owned_ship:
        return None, "Owned ship not found or already sold"
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None, "User not found"
    sell_value = int(owned_ship.actual_value * 0.4)
    user.currency_value += sell_value
    owned_ship.status = 'sold'
    db.commit()
    return sell_value, "Ship sold successfully"