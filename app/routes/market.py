from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.create_database import get_db
from app.crud.market_crud import buy_ship, sell_ship

router = APIRouter(prefix="/market", tags=["Market"])

@router.post("/buy/{user_id}/{ship_id}")
def buy_ship_route(user_id: int, ship_id: int, db: Session = Depends(get_db)):
    result, message, ship_number = buy_ship(db, user_id, ship_id)
    if not result:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message, "ship_number": ship_number}

@router.post("/sell/{user_id}/{owned_ship_number}")
def sell_ship_route(user_id: int, owned_ship_number: int, db: Session = Depends(get_db)):
    value, message = sell_ship(db, user_id, owned_ship_number)
    if value is None:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message, "value_received": value}