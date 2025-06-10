# app/crud.py
from sqlalchemy.orm import Session
from app import schemas
from app.database import create_schemas as models
from app.database.create_schemas import Ship, User, OwnedShips


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