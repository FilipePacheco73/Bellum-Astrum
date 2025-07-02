# app/routes/ships.py
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from backend.app.database import create_schemas as models
from backend.app.database import create_database as database_config
from backend.app import schemas
from backend.app.crud import ship_crud
from backend.app.utils import log_user_action, log_error, log_event, GameAction, LogCategory, LogLevel
import time

router = APIRouter(
    prefix="/ships",
    tags=["Ships"],
)

def get_db():
    """
    Dependency to get the database session.
    """
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ShipResponse)
def create_ship_route(ship: schemas.ShipCreate, request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    
    try:
        new_ship = ship_crud.create_ship(db=db, ship=ship)
        execution_time = int((time.time() - start_time) * 1000)
        
        # Log ship creation (admin action)
        log_event(
            db=db,
            level=LogLevel.INFO,
            category=LogCategory.AUDIT,
            action=GameAction.BUY_SHIP,  # Usando BUY_SHIP como proxy para criação
            details={
                "ship_name": ship.ship_name,
                "ship_id": new_ship.ship_id,
                "operation": "CREATE_SHIP",
                "ship_stats": {
                    "attack": ship.attack,
                    "shield": ship.shield,
                    "evasion": ship.evasion,
                    "fire_rate": ship.fire_rate,
                    "hp": ship.hp,
                    "value": ship.value
                },
                "success": True
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time,
            resource_affected=f"ship_id:{new_ship.ship_id}"
        )
        
        return new_ship
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.BUY_SHIP,  # Usando como proxy
            error_message=str(e),
            details={
                "ship_name": ship.ship_name,
                "operation": "CREATE_SHIP",
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail="Ship creation failed")

@router.get("/", response_model=list[schemas.ShipResponse])
def list_ships_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ships = ship_crud.get_ships(db=db, skip=skip, limit=limit)
    return ships

@router.get("/{ship_id}", response_model=schemas.ShipResponse)
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
        raise HTTPException(status_code=500, detail="Ship lookup failed")

@router.put("/{ship_id}", response_model=schemas.ShipResponse)
def update_ship_route(ship_id: int, ship_data: schemas.ShipCreate, request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    
    try:
        db_ship = ship_crud.update_ship(db=db, ship_id=ship_id, ship_data=ship_data)
        execution_time = int((time.time() - start_time) * 1000)
        
        if db_ship is None:
            # Log failed update attempt
            log_error(
                db=db,
                action=GameAction.SELL_SHIP,  # Using as proxy for ship management
                error_message="Ship not found or update failed",
                details={
                    "ship_id": ship_id,
                    "operation": "UPDATE_SHIP",
                    "ship_data": {
                        "ship_name": ship_data.ship_name,
                        "attack": ship_data.attack,
                        "shield": ship_data.shield,
                        "evasion": ship_data.evasion,
                        "fire_rate": ship_data.fire_rate,
                        "hp": ship_data.hp,
                        "value": ship_data.value
                    },
                    "success": False,
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=404, detail="Ship not found or update failed")
        
        # Log successful ship update (admin action)
        log_event(
            db=db,
            level=LogLevel.INFO,
            category=LogCategory.AUDIT,
            action=GameAction.SELL_SHIP,  # Using as proxy
            details={
                "ship_id": ship_id,
                "ship_name": ship_data.ship_name,
                "operation": "UPDATE_SHIP",
                "updated_stats": {
                    "attack": ship_data.attack,
                    "shield": ship_data.shield,
                    "evasion": ship_data.evasion,
                    "fire_rate": ship_data.fire_rate,
                    "hp": ship_data.hp,
                    "value": ship_data.value
                },
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
            action=GameAction.SELL_SHIP,  # Using as proxy
            error_message=str(e),
            details={
                "ship_id": ship_id,
                "operation": "UPDATE_SHIP",
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail="Ship update failed")

@router.delete("/{ship_id}")
def delete_ship_route(ship_id: int, request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    
    try:
        # Get ship info before deletion for logging
        ship_to_delete = ship_crud.get_ship(db=db, ship_id=ship_id)
        
        if not ship_crud.delete_ship(db=db, ship_id=ship_id):
            execution_time = int((time.time() - start_time) * 1000)
            log_error(
                db=db,
                action=GameAction.SELL_SHIP,  # Usando como proxy para deleção
                error_message="Ship not found",
                details={
                    "ship_id": ship_id,
                    "operation": "DELETE_SHIP",
                    "success": False,
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=404, detail="Ship not found")
        
        execution_time = int((time.time() - start_time) * 1000)
        
        # Log ship deletion (admin action)
        log_event(
            db=db,
            level=LogLevel.WARNING,
            category=LogCategory.AUDIT,
            action=GameAction.SELL_SHIP,  # Usando como proxy
            details={
                "ship_id": ship_id,
                "ship_name": ship_to_delete.ship_name if ship_to_delete else "Unknown",
                "operation": "DELETE_SHIP",
                "success": True
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time,
            resource_affected=f"ship_id:{ship_id}"
        )
        
        return {"message": "Ship deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.SELL_SHIP,  # Usando como proxy
            error_message=str(e),
            details={
                "ship_id": ship_id,
                "operation": "DELETE_SHIP",
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail="Ship deletion failed")
    return {"detail": "Ship deleted"}