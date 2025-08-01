from sqlalchemy.orm import Session
from database import Ship
from database.models import OwnedShips
from typing import List

# --- Ship CRUD Operations ---
def get_ship(db: Session, ship_id: int):
    return db.query(Ship).filter(Ship.ship_id == ship_id).first()

def get_ships(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ship).offset(skip).limit(limit).all()

def get_user_owned_ships(db: Session, user_id: int, status_filter: List[str] = None) -> List[OwnedShips]:
    """
    Get owned ships for a user with optional status filtering.
    
    Args:
        db: Database session
        user_id: ID of the user
        status_filter: List of status to include. If None, defaults to ['active', 'owned']
                      Common values: ['active', 'owned', 'destroyed']
    
    Returns:
        List of OwnedShips matching the criteria
    """
    if status_filter is None:
        status_filter = ['active', 'owned']  # Default: exclude destroyed ships
    
    ships = db.query(OwnedShips).filter(
        OwnedShips.user_id == user_id,
        OwnedShips.status.in_(status_filter)
    ).all()
    
    return ships

def get_owned_ship_by_number(db: Session, ship_number: int) -> OwnedShips:
    """
    Get owned ship data by ship_number regardless of owner.
    Used for battle log purposes to fetch base stats of any ship.
    
    Args:
        db: Database session
        ship_number: Ship number to search for
    
    Returns:
        OwnedShips object if found, None otherwise
    """
    ship = db.query(OwnedShips).filter(
        OwnedShips.ship_number == ship_number
    ).first()
    
    return ship