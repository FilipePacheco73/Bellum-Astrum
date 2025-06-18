from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.create_database import get_db
from backend.app.crud.battle_crud import battle_between_users, activate_owned_ship
from backend.app.schemas import BattleHistoryResponse, ActivateShipResponse

router = APIRouter(prefix="/battle", tags=["Battle"])

@router.post("/activate-ship/", response_model=ActivateShipResponse)
def activate_ship_route(
    user_id: int,
    ship_number: int,
    db: Session = Depends(get_db)
):
    ship, message = activate_owned_ship(db, user_id, ship_number)
    if not ship:
        raise HTTPException(status_code=404, detail=message)
    return ship

@router.post("/battle", response_model=BattleHistoryResponse)
def battle_route(
    user1_id: int,
    user2_id: int,
    user1_ship_number: int,
    user2_ship_number: int,
    db: Session = Depends(get_db)
):
    result, message = battle_between_users(db, user1_id, user2_id, user1_ship_number, user2_ship_number)
    if not result:
        raise HTTPException(status_code=400, detail=message)
    return result
