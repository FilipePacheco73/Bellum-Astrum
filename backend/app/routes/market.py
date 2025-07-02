from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from backend.app.crud.market_crud import buy_ship, sell_ship
from backend.app.schemas import MarketBuyRequest, MarketBuyResponse, MarketSellRequest, MarketSellResponse
from backend.app.utils import log_user_action, log_error, GameAction
import time

router = APIRouter(prefix="/market", tags=["Market"])

@router.post("/buy/{user_id}/{ship_id}")
def buy_ship_route(user_id: int, ship_id: int, request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    
    try:
        result, message, ship_number = buy_ship(db, user_id, ship_id)
        execution_time = int((time.time() - start_time) * 1000)
        
        if not result:
            # Log failed purchase attempt
            log_error(
                db=db,
                action=GameAction.BUY_SHIP,
                error_message=message,
                user_id=user_id,
                details={
                    "ship_id": ship_id,
                    "success": False,
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=400, detail=message)
        
        # Log successful purchase
        log_user_action(
            db=db,
            action=GameAction.BUY_SHIP,
            user_id=user_id,
            details={
                "ship_id": ship_id,
                "ship_number": ship_number,
                "success": True
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time
        )
        
        return {"message": message, "ship_number": ship_number}
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.BUY_SHIP,
            error_message=str(e),
            user_id=user_id,
            details={
                "ship_id": ship_id,
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/sell/{user_id}/{owned_ship_number}")
def sell_ship_route(user_id: int, owned_ship_number: int, request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    
    try:
        value, message = sell_ship(db, user_id, owned_ship_number)
        execution_time = int((time.time() - start_time) * 1000)
        
        if value is None:
            # Log failed sale attempt
            log_error(
                db=db,
                action=GameAction.SELL_SHIP,
                error_message=message,
                user_id=user_id,
                details={
                    "owned_ship_number": owned_ship_number,
                    "success": False,
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=400, detail=message)
        
        # Log successful sale
        log_user_action(
            db=db,
            action=GameAction.SELL_SHIP,
            user_id=user_id,
            details={
                "owned_ship_number": owned_ship_number,
                "value_received": value,
                "success": True
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time
        )
        
        return {"message": message, "value_received": value}
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.SELL_SHIP,
            error_message=str(e),
            user_id=user_id,
            details={
                "owned_ship_number": owned_ship_number,
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail="Internal server error")