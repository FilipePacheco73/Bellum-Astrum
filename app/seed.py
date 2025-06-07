from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.create_database import SessionLocal
from app import schemas, crud

def seed_ships() -> dict:
    """
    Seed the database with initial ship data if no ships exist.
    This function checks if the 'ships' table is empty and populates it with predefined ship data.
    Returns:
        dict: A dictionary indicating the result of the seeding operation.
    """
    db: Session = SessionLocal()
    try:
        if not db.query(crud.models.Ship).first():
            ships = [
                schemas.ShipCreate(ship_name="Falcon", attack=15, shield=10, evasion=5, fire_rate=2, hp=120, value=1500),
                schemas.ShipCreate(ship_name="Eagle", attack=20, shield=15, evasion=10, fire_rate=3, hp=150, value=2000),
                schemas.ShipCreate(ship_name="Hawk", attack=25, shield=20, evasion=15, fire_rate=4, hp=180, value=2500)
            ]
            for ship in ships:
                crud.create_ship(db=db, ship=ship)
            return {"detail": "Ships seeded successfully"}
        else:
            return {"detail": "Ships already seeded"}
    except SQLAlchemyError as e:
        return {"error": str(e)}
    finally:
        db.close()

def seed_users() -> dict:
    """
    Seed the database with initial user data if no users exist.
    This function checks if the 'users' table is empty and populates it with predefined user data.
    Returns:
        dict: A dictionary indicating the result of the seeding operation.
    """
    db: Session = SessionLocal()
    try:
        if not db.query(crud.models.User).first():
            users = [
                schemas.UserCreate(nickname="Admin", rank_elo=1000, currency_value=1500),
                schemas.UserCreate(nickname="Pilot1", rank_elo=1000, currency_value=1500),
                schemas.UserCreate(nickname="Pilot2", rank_elo=1000, currency_value=1500),
                schemas.UserCreate(nickname="Pilot3", rank_elo=1000, currency_value=1500)
            ]
            for user in users:
                crud.create_user(db=db, user=user)
            return {"detail": "Users seeded successfully"}
        else:
            return {"detail": "Users already seeded"}
    except SQLAlchemyError as e:
        return {"error": str(e)}
    finally:
        db.close()