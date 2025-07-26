from sqlalchemy.orm import Session
from backend.app.schemas.ship_schemas import ShipCreate
from database import Ship

# --- Ship CRUD Operations ---
def get_ship(db: Session, ship_id: int):
    return db.query(Ship).filter(Ship.ship_id == ship_id).first()

def get_ships(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ship).offset(skip).limit(limit).all()

def create_ship(db: Session, ship: ShipCreate):
    db_ship = Ship(**ship.dict())
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship

def update_ship(db: Session, ship_id: int, ship_data: ShipCreate):
    db_ship = db.query(Ship).filter(Ship.ship_id == ship_id).first()
    if db_ship:
        for key, value in ship_data.dict(exclude_unset=True).items():
            setattr(db_ship, key, value)
        db.commit()
        db.refresh(db_ship)
    return db_ship

def delete_ship(db: Session, ship_id: int):
    db_ship = db.query(Ship).filter(Ship.ship_id == ship_id).first()
    if db_ship:
        db.delete(db_ship)
        db.commit()
        return True
    return False