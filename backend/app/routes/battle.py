from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.app.database.create_database import get_db
from backend.app.crud.battle_crud import battle_between_users, activate_owned_ship
from backend.app.schemas import BattleHistoryResponse, ActivateShipResponse
from backend.app.utils import log_user_action, log_game_event, log_error, GameAction
import time

router = APIRouter(prefix="/battle", tags=["Battle"])

@router.post("/activate-ship/", response_model=ActivateShipResponse)
def activate_ship_route(
    user_id: int,
    ship_number: int,
    request: Request,
    db: Session = Depends(get_db)
):
    start_time = time.time()
    
    try:
        ship, message = activate_owned_ship(db, user_id, ship_number)
        execution_time = int((time.time() - start_time) * 1000)
        
        if not ship:
            # Log failed activation
            log_error(
                db=db,
                action=GameAction.ACTIVATE_SHIP,
                error_message=message,
                user_id=user_id,
                details={
                    "ship_number": ship_number,
                    "success": False,
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=404, detail=message)
        
        # Log successful activation
        log_user_action(
            db=db,
            action=GameAction.ACTIVATE_SHIP,
            user_id=user_id,
            details={
                "ship_number": ship_number,
                "ship_id": ship.ship_id,
                "ship_name": ship.ship_name,
                "success": True
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time
        )
        
        return ship
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.ACTIVATE_SHIP,
            error_message=str(e),
            user_id=user_id,
            details={
                "ship_number": ship_number,
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail="Ship activation failed")

@router.post("/battle", response_model=BattleHistoryResponse)
def battle_route(
    user1_id: int,
    user2_id: int,
    user1_ship_number: int,
    user2_ship_number: int,
    request: Request,
    db: Session = Depends(get_db)
):
    start_time = time.time()
    
    try:
        result, message = battle_between_users(db, user1_id, user2_id, user1_ship_number, user2_ship_number)
        execution_time = int((time.time() - start_time) * 1000)
        
        if not result:
            # Log failed battle attempt
            log_error(
                db=db,
                action=GameAction.BATTLE_START,
                error_message=message,
                user_id=user1_id,
                details={
                    "user1_id": user1_id,
                    "user2_id": user2_id,
                    "user1_ship_number": user1_ship_number,
                    "user2_ship_number": user2_ship_number,
                    "success": False,
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=400, detail=message)
        
        # Log successful battle
        log_game_event(
            db=db,
            action=GameAction.BATTLE_END,
            user_id=user1_id,
            details={
                "battle_id": result.battle_id,
                "user1_id": user1_id,
                "user2_id": user2_id,
                "user1_ship_number": user1_ship_number,
                "user2_ship_number": user2_ship_number,
                "winner_user_id": result.winner_user_id,
                "participants": result.participants,
                "success": True,
                "execution_time_ms": execution_time
            },
            resource_affected=f"battle_id:{result.battle_id}"
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.BATTLE_START,
            error_message=str(e),
            user_id=user1_id,
            details={
                "user1_id": user1_id,
                "user2_id": user2_id,
                "user1_ship_number": user1_ship_number,
                "user2_ship_number": user2_ship_number,
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail="Battle failed")
