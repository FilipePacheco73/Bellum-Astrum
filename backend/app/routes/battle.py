from fastapi import APIRouter, Depends, HTTPException, Request
from backend.app.utils.auth_utils import get_current_user
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.crud.battle_crud import battle_between_users, activate_owned_ship, deactivate_owned_ship, get_user_ship_limits_info
from backend.app.schemas.battle_schemas import BattleHistoryResponse, BattleRequest
from backend.app.schemas.owned_ship_schemas import ActivateShipResponse
from backend.app.schemas.user_schemas import UserShipLimitsResponse
from backend.app.utils import log_user_action, log_game_event, log_error, GameAction
import time

router = APIRouter(prefix="/battle", tags=["Battle"])

@router.post("/activate-ship/", response_model=ActivateShipResponse)
def activate_ship_route(
    ship_number: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    start_time = time.time()
    
    try:
        ship, message = activate_owned_ship(db, current_user.user_id, ship_number)
        execution_time = int((time.time() - start_time) * 1000)
        
        if not ship:
            # Log failed activation
            log_error(
                db=db,
                action=GameAction.ACTIVATE_SHIP,
                error_message=message,
                user_id=current_user.user_id,
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
            user_id=current_user.user_id,
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
            user_id=current_user.user_id,
            details={
                "ship_number": ship_number,
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail=f"Ship activation failed: {str(e)}")


@router.post("/battle", response_model=BattleHistoryResponse)
def battle_route(
    battle_request: BattleRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Unified battle system supporting 1v1 to 20v20 battles with tactical formations.
    
    Supports:
    - Single ship battles (1v1): user_ship_numbers: int, opponent_ship_numbers: int
    - Multi-ship battles (up to 20v20): user_ship_numbers: [1,2,3], opponent_ship_numbers: [1,2]
    - Formation strategies: DEFENSIVE, AGGRESSIVE, TACTICAL
    - Only active ships can participate in battles
    """
    start_time = time.time()
    
    try:
        result, message = battle_between_users(
            db=db,
            user1_id=current_user.user_id,
            user2_id=battle_request.opponent_user_id,
            user1_ship_numbers=battle_request.user_ship_numbers,
            user2_ship_numbers=battle_request.opponent_ship_numbers,
            user1_formation=battle_request.user_formation,
            user2_formation=battle_request.opponent_formation
        )
        execution_time = int((time.time() - start_time) * 1000)
        
        if not result:
            # Log failed battle attempt
            log_error(
                db=db,
                action=GameAction.BATTLE_START,
                error_message=message,
                user_id=current_user.user_id,
                details={
                    "user1_id": current_user.user_id,
                    "user2_id": battle_request.opponent_user_id,
                    "user1_ship_numbers": battle_request.user_ship_numbers,
                    "user2_ship_numbers": battle_request.opponent_ship_numbers,
                    "user1_formation": battle_request.user_formation,
                    "user2_formation": battle_request.opponent_formation,
                    "success": False,
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=400, detail=message)
        
        # Log successful battle
        log_game_event(
            db=db,
            action=GameAction.BATTLE_END,
            user_id=current_user.user_id,
            details={
                "battle_id": result.battle_id,
                "user1_id": current_user.user_id,
                "user2_id": battle_request.opponent_user_id,
                "user1_ship_numbers": battle_request.user_ship_numbers,
                "user2_ship_numbers": battle_request.opponent_ship_numbers,
                "user1_formation": battle_request.user_formation,
                "user2_formation": battle_request.opponent_formation,
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
            user_id=current_user.user_id,
            details={
                "user1_id": current_user.user_id,
                "user2_id": battle_request.opponent_user_id,
                "user1_ship_numbers": battle_request.user_ship_numbers,
                "user2_ship_numbers": battle_request.opponent_ship_numbers,
                "user1_formation": battle_request.user_formation,
                "user2_formation": battle_request.opponent_formation,
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail=f"Battle failed: {str(e)}")


@router.post("/deactivate-ship/", response_model=ActivateShipResponse)
def deactivate_ship_route(
    ship_number: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Deactivate an active ship to free up an active slot."""
    start_time = time.time()
    
    try:
        ship, message = deactivate_owned_ship(db, current_user.user_id, ship_number)
        execution_time = int((time.time() - start_time) * 1000)
        
        if not ship:
            log_error(
                db=db,
                action=GameAction.ACTIVATE_SHIP,  # Reusing the same action for logging
                error_message=message,
                user_id=current_user.user_id,
                details={
                    "ship_number": ship_number,
                    "action": "deactivate",
                    "success": False,
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=404, detail=message)
        
        log_user_action(
            db=db,
            action=GameAction.ACTIVATE_SHIP,
            user_id=current_user.user_id,
            details={
                "ship_number": ship_number,
                "ship_id": ship.ship_id,
                "ship_name": ship.ship_name,
                "action": "deactivate",
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
            user_id=current_user.user_id,
            details={
                "ship_number": ship_number,
                "action": "deactivate",
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail=f"Ship deactivation failed: {str(e)}")


@router.get("/ship-limits/", response_model=UserShipLimitsResponse)
def get_ship_limits_route(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get information about user's ship limits and current usage."""
    try:
        limits_info = get_user_ship_limits_info(db, current_user.user_id)
        
        if not limits_info:
            raise HTTPException(status_code=404, detail="User not found")
        
        return limits_info
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            db=db,
            action=GameAction.ACTIVATE_SHIP,
            error_message=str(e),
            user_id=current_user.user_id,
            details={
                "action": "get_ship_limits",
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail=f"Failed to get ship limits: {str(e)}")
