from sqlalchemy.orm import Session
from database.models import OwnedShips, ShipyardLog
from datetime import datetime, timezone
from backend.app.utils.constants import SHIPYARD_REPAIR_COOLDOWN_SECONDS

# Get the last shipyard log for a user and ship
def get_last_shipyard_log(db: Session, user_id: int, ship_number: int):
    return db.query(ShipyardLog).filter_by(user_id=user_id, ship_number=ship_number).order_by(ShipyardLog.last_used_at.desc()).first()

# Create or update the shipyard log
def update_shipyard_log(db: Session, user_id: int, ship_number: int, ship_id: int):
    now = datetime.now(timezone.utc)
    log = get_last_shipyard_log(db, user_id, ship_number)
    if log:
        log.last_used_at = now
    else:
        log = ShipyardLog(user_id=user_id, ship_number=ship_number, ship_id=ship_id, last_used_at=now)
        db.add(log)
    db.commit()
    db.refresh(log)
    return log

# Repair the ship: set all actual_* fields to base_*
def repair_owned_ship(db: Session, ship: OwnedShips):
    ship.actual_attack = ship.base_attack
    ship.actual_shield = ship.base_shield
    ship.actual_evasion = ship.base_evasion
    ship.actual_fire_rate = ship.base_fire_rate
    ship.actual_hp = ship.base_hp
    ship.actual_value = ship.base_value
    db.commit()
    db.refresh(ship)
    return ship

# Check if the ship can be repaired (1 minute cooldown)
def can_repair_ship(log: ShipyardLog, cooldown_seconds: int = SHIPYARD_REPAIR_COOLDOWN_SECONDS):
    if not log:
        return True, 0
    
    now = datetime.now(timezone.utc)
    
    # Ensure both datetimes have timezone info
    last_used = log.last_used_at
    if last_used.tzinfo is None:
        # If the stored datetime is naive, assume it's UTC
        last_used = last_used.replace(tzinfo=timezone.utc)
    
    elapsed = (now - last_used).total_seconds()
    if elapsed >= cooldown_seconds:
        return True, 0
    return False, int(cooldown_seconds - elapsed)

# Check if a ship needs repair (any actual stat is less than base stat)
def ship_needs_repair(ship: OwnedShips) -> bool:
    return (ship.actual_attack < ship.base_attack or
            ship.actual_shield < ship.base_shield or
            ship.actual_hp < ship.base_hp or
            ship.actual_fire_rate < ship.base_fire_rate or
            ship.actual_evasion < ship.base_evasion)

# Get cooldown status for all user ships
def get_user_ships_cooldown_status(db: Session, user_id: int, cooldown_seconds: int = SHIPYARD_REPAIR_COOLDOWN_SECONDS):
    # Get all user ships that are not destroyed or sold
    ships = db.query(OwnedShips).filter(
        OwnedShips.user_id == user_id,
        OwnedShips.status.in_(['active', 'owned'])
    ).all()
    
    ship_statuses = []
    ships_needing_repair = 0
    ships_in_cooldown = 0
    
    for ship in ships:
        # Check if ship needs repair
        needs_repair = ship_needs_repair(ship)
        if needs_repair:
            ships_needing_repair += 1
        
        # Check cooldown status
        log = get_last_shipyard_log(db, user_id, ship.ship_number)
        can_repair, wait_seconds = can_repair_ship(log, cooldown_seconds)
        
        if not can_repair:
            ships_in_cooldown += 1
        
        ship_statuses.append({
            'ship_number': ship.ship_number,
            'can_repair': can_repair,
            'cooldown_seconds': wait_seconds,
            'needs_repair': needs_repair
        })
    
    return {
        'ships': ship_statuses,
        'total_ships': len(ships),
        'ships_needing_repair': ships_needing_repair,
        'ships_in_cooldown': ships_in_cooldown
    }
