# app/routes/ships.py
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.schemas.ship_schemas import ShipResponse, OwnedShipResponse
from backend.app.crud import ship_crud
from backend.app.utils import log_error, log_event, GameAction, LogCategory, LogLevel
import time

router = APIRouter(
    prefix="/ships",
    tags=["Ships"],
)

@router.get("/", response_model=list[ShipResponse])
def list_ships_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ships = ship_crud.get_ships(db=db, skip=skip, limit=limit)
    return ships

@router.get("/{ship_id}", response_model=ShipResponse)
def get_ship_route(ship_id: int, request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    
    try:
        db_ship = ship_crud.get_ship(db=db, ship_id=ship_id)
        execution_time = int((time.time() - start_time) * 1000)
        
        if db_ship is None:
            # Log failed lookup attempt
            log_error(
                db=db,
                action=GameAction.BUY_SHIP,  # Using as proxy for ship access
                error_message="Ship not found",
                details={
                    "ship_id": ship_id,
                    "operation": "GET_SHIP",
                    "success": False,
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=404, detail="Ship not found")
        
        # Log successful ship access (optional for read operations, but useful for auditing)
        log_event(
            db=db,
            level=LogLevel.DEBUG,
            category=LogCategory.GAME,
            action=GameAction.BUY_SHIP,  # Using as proxy
            details={
                "ship_id": ship_id,
                "ship_name": db_ship.ship_name,
                "operation": "GET_SHIP",
                "success": True
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time,
            resource_affected=f"ship_id:{ship_id}"
        )
        
        return db_ship
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.BUY_SHIP,  # Using as proxy
            error_message=str(e),
            details={
                "ship_id": ship_id,
                "operation": "GET_SHIP",
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail=f"Ship lookup failed: {str(e)}")

@router.get("/user/{user_id}/ships", response_model=list[OwnedShipResponse])
def get_user_ships_route(
    user_id: int, 
    db: Session = Depends(get_db),
    status: str = None
):
    """Get owned ships for a specific user with optional status filtering
    
    Args:
        user_id: ID of the user
        status: Optional comma-separated list of status to include (e.g., "active,owned,destroyed")
                If not provided, defaults to "active,owned" (excludes destroyed ships)
    """
    status_filter = None
    if status:
        status_filter = [s.strip() for s in status.split(',')]
    
    ships = ship_crud.get_user_owned_ships(db=db, user_id=user_id, status_filter=status_filter)
    return ships

@router.get("/owned/{ship_number}", response_model=OwnedShipResponse)
def get_owned_ship_by_number_route(ship_number: int, db: Session = Depends(get_db)):
    """Get owned ship data by ship_number (for battle log purposes)
    
    This endpoint allows fetching ship data by ship_number regardless of owner,
    which is useful for displaying base stats in battle logs for NPC ships.
    """
    try:
        ship = ship_crud.get_owned_ship_by_number(db=db, ship_number=ship_number)
        if not ship:
            raise HTTPException(status_code=404, detail="Ship not found")
        return ship
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            db=db,
            action=GameAction.ACTIVATE_SHIP,  # Reusing existing action
            error_message=str(e),
            user_id=None,
            details={
                "ship_number": ship_number,
                "action": "get_ship_by_number",
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail=f"Failed to get ship data: {str(e)}")