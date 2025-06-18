# app/routes/ships.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import create_database as database_config
from backend.app.crud.seed_crud import seed_ships, seed_users, seed_assign_npc_ships
from backend.app.schemas import SeedShipsResponse, SeedUsersResponse, SeedNPCShipsResponse

router = APIRouter(
    prefix="/seed",
    tags=["Seed"],
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

@router.post("/users", response_model=SeedUsersResponse)
def seed_users_route(db: Session = Depends(get_db)):
    """
    Endpoint to seed the database with initial user data.
    """
    return seed_users(db)

@router.post("/ships", response_model=SeedShipsResponse)
def seed_ships_route(db: Session = Depends(get_db)):
    """
    Endpoint to seed the database with initial ship data.
    """
    return seed_ships(db)

@router.post("/npc-ships", response_model=SeedNPCShipsResponse)
def seed_npc_ships_route(db: Session = Depends(get_db)):
    """
    Assign compatible ships to all NPCs based on their ELO.
    """
    return seed_assign_npc_ships(db)