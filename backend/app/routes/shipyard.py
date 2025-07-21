from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.crud.shipyard_crud import get_last_shipyard_log, update_shipyard_log, repair_owned_ship, can_repair_ship
from database.models import OwnedShips
from backend.app.schemas.shipyard_schemas import ShipRepairResponse
from backend.app.utils.auth_utils import get_current_user
from backend.app.utils import log_user_action, log_error, GameAction
from backend.app.database import get_db

router = APIRouter(
    prefix="/shipyard",
    tags=["shipyard"]
)

@router.post("/repair", response_model=ShipRepairResponse)
def repair_ship(
    ship_number: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Get the ship
    ship = db.query(OwnedShips).filter_by(ship_number=ship_number, user_id=current_user.user_id).first()
    if not ship:
        log_error(
            db=db,
            action=GameAction.PERFORMANCE_ISSUE,
            error_message="Ship not found.",
            user_id=current_user.user_id,
            details={"ship_number": ship_number}
        )
        raise HTTPException(status_code=404, detail="Ship not found.")
    if ship.status in ["destroyed", "sold"]:
        log_error(
            db=db,
            action=GameAction.PERFORMANCE_ISSUE,
            error_message="Ship cannot be repaired (destroyed or sold).",
            user_id=current_user.user_id,
            details={"ship_number": ship_number, "status": ship.status}
        )
        raise HTTPException(status_code=400, detail="Ship cannot be repaired (destroyed or sold).")

    # Check cooldown
    log = get_last_shipyard_log(db, current_user.user_id, ship_number)
    can_repair, wait_seconds = can_repair_ship(log)
    if not can_repair:
        log_error(
            db=db,
            action=GameAction.PERFORMANCE_ISSUE,
            error_message=f"Cooldown not finished. Wait {wait_seconds} seconds.",
            user_id=current_user.user_id,
            details={"ship_number": ship_number, "wait_seconds": wait_seconds}
        )
        raise HTTPException(
            status_code=429,
            detail=f"You must wait {wait_seconds} seconds before repairing this ship again."
        )

    # Repair
    repair_owned_ship(db, ship)
    update_shipyard_log(db, current_user.user_id, ship_number, ship.ship_id)

    log_user_action(
        db=db,
        action=GameAction.PERFORMANCE_ISSUE,
        user_id=current_user.user_id,
        details={"ship_number": ship_number, "ship_id": ship.ship_id}
    )

    return ShipRepairResponse(
        success=True,
        message="Ship repaired successfully!",
        ship_number=ship.ship_number,
        user_id=ship.user_id,
        ship_id=ship.ship_id
    )
