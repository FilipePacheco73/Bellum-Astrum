# app/routes/ships.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import create_database as database_config
from app.database.start_table_value import seed_ships, seed_users
from app.schemas import SeedShipsResponse, SeedUsersResponse

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

@router.post("/ships", response_model=SeedShipsResponse)
def seed_ships_route(db: Session = Depends(get_db)):
    """
    Endpoint to seed the database with initial ship data.
    """
    return seed_ships(db)

@router.post("/users", response_model=SeedUsersResponse)
def seed_users_route(db: Session = Depends(get_db)):
    """
    Endpoint to seed the database with initial user data.
    """
    return seed_users(db)