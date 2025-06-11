from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.create_database import get_db
from app.crud import battle_between_users
from app.schemas import BattleHistoryResponse

router = APIRouter(prefix="/battle", tags=["Battle"])

@router.post("/", response_model=BattleHistoryResponse)
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