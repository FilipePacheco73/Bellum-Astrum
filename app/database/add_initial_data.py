from create_database import SessionLocal
from create_schemas import Ship, User
from sqlalchemy.exc import SQLAlchemyError

def add_ships(ships_data: list[dict]):
    """
    Add multiple Ships into the database.

    :param ships_data: List of dictionaries with ship attributes.
    """
    with SessionLocal() as db:
        try:
            ships = []
            for data in ships_data:
                new_ship = Ship(**data)
                db.add(new_ship)
                ships.append(new_ship)
            db.commit()
            for ship in ships:
                db.refresh(ship)
                print(f"Ship created: {ship}")
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error adding ships: {e}")

def add_users(users_data: list[dict]):
    """
    Add multiple Users into the database.

    :param users_data: List of dictionaries with user attributes.
    """
    with SessionLocal() as db:
        try:
            users = []
            for data in users_data:
                new_user = User(**data)
                db.add(new_user)
                users.append(new_user)
            db.commit()
            for user in users:
                db.refresh(user)
                print(f"User created: {user}")
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error adding users: {e}")