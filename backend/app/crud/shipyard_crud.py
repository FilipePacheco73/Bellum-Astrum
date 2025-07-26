from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from database.models import OwnedShips, ShipyardLog

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
def can_repair_ship(log: ShipyardLog, cooldown_seconds: int = 60):
    if not log:
        return True, 0
    now = datetime.now(timezone.utc)
    elapsed = (now - log.last_used_at).total_seconds()
    if elapsed >= cooldown_seconds:
        return True, 0
    return False, int(cooldown_seconds - elapsed)
