from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from backend.app.crud import ship_crud, user_crud
from backend.app.database.create_database import SessionLocal
from backend.app.database.create_schemas import User, Ship, OwnedShips
from backend.app import schemas
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
NPC_PASSWORD = os.getenv('NPC_PASSWORD')
NPC_ASTRO_EMAIL = os.getenv('NPC_ASTRO_EMAIL')
NPC_CYBER_EMAIL = os.getenv('NPC_CYBER_EMAIL')
NPC_ORION_EMAIL = os.getenv('NPC_ORION_EMAIL')
NPC_VEGA_EMAIL = os.getenv('NPC_VEGA_EMAIL')
NPC_NEBULA_EMAIL = os.getenv('NPC_NEBULA_EMAIL')
NPC_PULSAR_EMAIL = os.getenv('NPC_PULSAR_EMAIL')
NPC_QUASAR_EMAIL = os.getenv('NPC_QUASAR_EMAIL')
NPC_TITAN_EMAIL = os.getenv('NPC_TITAN_EMAIL')
NPC_SOLARIS_EMAIL = os.getenv('NPC_SOLARIS_EMAIL')
NPC_ANDROMEDA_EMAIL = os.getenv('NPC_ANDROMEDA_EMAIL')

# --- Seed CRUD Operations ---
def seed_ships(db: Session) -> dict:
    """
    Seed the database with initial ship data if no ships exist.
    This function checks if the 'ships' table is empty and populates it with predefined ship data.
    Returns:
        dict: A dictionary indicating the result of the seeding operation.
    """
    db: Session = SessionLocal()
    try:
        if not db.query(Ship).first():
            ships = [
                schemas.ShipCreate(ship_name="Falcon", attack=15, shield=10, evasion=5, fire_rate=2, hp=1200, value=1500),
                schemas.ShipCreate(ship_name="Eagle", attack=20, shield=15, evasion=10, fire_rate=3, hp=1500, value=2000),
                schemas.ShipCreate(ship_name="Hawk", attack=25, shield=20, evasion=15, fire_rate=4, hp=1800, value=2500),
                schemas.ShipCreate(ship_name="Condor", attack=30, shield=25, evasion=20, fire_rate=5, hp=2000, value=3000),
                schemas.ShipCreate(ship_name="Vulture", attack=35, shield=30, evasion=25, fire_rate=6, hp=2200, value=3500),
                schemas.ShipCreate(ship_name="Raven", attack=18, shield=12, evasion=7, fire_rate=2.5, hp=1300, value=1600),
                schemas.ShipCreate(ship_name="Osprey", attack=22, shield=17, evasion=12, fire_rate=3.2, hp=1550, value=2100),
                schemas.ShipCreate(ship_name="Kestrel", attack=27, shield=22, evasion=17, fire_rate=4.1, hp=1850, value=2600),
                schemas.ShipCreate(ship_name="Merlin", attack=32, shield=27, evasion=22, fire_rate=5.3, hp=2050, value=3100),
                schemas.ShipCreate(ship_name="Phoenix", attack=37, shield=32, evasion=27, fire_rate=6.4, hp=2250, value=3600),
                schemas.ShipCreate(ship_name="Griffin", attack=19, shield=13, evasion=8, fire_rate=2.7, hp=1350, value=1700),
                schemas.ShipCreate(ship_name="Harrier", attack=23, shield=18, evasion=13, fire_rate=3.4, hp=1600, value=2200),
                schemas.ShipCreate(ship_name="Sparrow", attack=28, shield=23, evasion=18, fire_rate=4.3, hp=1900, value=2700),
                schemas.ShipCreate(ship_name="Swift", attack=33, shield=28, evasion=23, fire_rate=5.5, hp=2100, value=3200),
                schemas.ShipCreate(ship_name="Thunder", attack=38, shield=33, evasion=28, fire_rate=6.6, hp=2300, value=3700),
                schemas.ShipCreate(ship_name="Storm", attack=21, shield=14, evasion=9, fire_rate=2.9, hp=1400, value=1800),
                schemas.ShipCreate(ship_name="Tempest", attack=24, shield=19, evasion=14, fire_rate=3.6, hp=1650, value=2300),
                schemas.ShipCreate(ship_name="Cyclone", attack=29, shield=24, evasion=19, fire_rate=4.5, hp=1950, value=2800),
                schemas.ShipCreate(ship_name="Typhoon", attack=34, shield=29, evasion=24, fire_rate=5.7, hp=2150, value=3300),
                schemas.ShipCreate(ship_name="Blizzard", attack=39, shield=34, evasion=29, fire_rate=6.8, hp=2350, value=3800),
                schemas.ShipCreate(ship_name="Nova", attack=22, shield=15, evasion=10, fire_rate=3.1, hp=1450, value=1900),
                schemas.ShipCreate(ship_name="Comet", attack=26, shield=20, evasion=15, fire_rate=4.0, hp=1750, value=2400),
                schemas.ShipCreate(ship_name="Meteor", attack=31, shield=25, evasion=20, fire_rate=5.2, hp=2000, value=2900),
                schemas.ShipCreate(ship_name="Asteroid", attack=36, shield=30, evasion=25, fire_rate=6.3, hp=2200, value=3400),
                schemas.ShipCreate(ship_name="Pulsar", attack=41, shield=35, evasion=30, fire_rate=7.0, hp=2400, value=3900),
                schemas.ShipCreate(ship_name="Nebula", attack=24, shield=16, evasion=11, fire_rate=3.3, hp=1500, value=2000),
                schemas.ShipCreate(ship_name="Quasar", attack=28, shield=21, evasion=16, fire_rate=4.2, hp=1800, value=2500),
                schemas.ShipCreate(ship_name="Galaxy", attack=33, shield=26, evasion=21, fire_rate=5.4, hp=2100, value=3000),
                schemas.ShipCreate(ship_name="Andromeda", attack=38, shield=31, evasion=26, fire_rate=6.5, hp=2300, value=3500),
                schemas.ShipCreate(ship_name="Orion", attack=43, shield=36, evasion=31, fire_rate=7.2, hp=2500, value=4000),
            ]
            for ship in ships:
                ship_crud.create_ship(db=db, ship=ship)
            return {"message": "Ships seeded successfully.", "ships_seeded": len(ships)}
        else:
            count = db.query(Ship).count()
            return {"message": "Ships already seeded.", "ships_seeded": count}
    except SQLAlchemyError as e:
        return {"message": f"Error: {str(e)}", "ships_seeded": 0}
    finally:
        db.close()

def seed_users(db: Session) -> dict:
    """
    Seed the database with initial user data if no users exist.
    This function checks if the 'users' table is empty and populates it with predefined user data.
    Returns:
        dict: A dictionary indicating the result of the seeding operation.
    """
    db: Session = SessionLocal()
    try:
        if not db.query(User).first():
            users = [
                schemas.UserCreate(nickname="Admin", email=ADMIN_EMAIL, password=ADMIN_PASSWORD, elo_rank=1000, currency_value=9999999, victories=0, defeats=0, damage_dealt=0, damage_taken=0, ships_destroyed_by_user=0, ships_lost_by_user=0),
                schemas.UserCreate(nickname="NPC_Astro", email=NPC_ASTRO_EMAIL, password=NPC_PASSWORD, elo_rank=800, currency_value=5000, victories=0, defeats=0, damage_dealt=0, damage_taken=0, ships_destroyed_by_user=0, ships_lost_by_user=0),
                schemas.UserCreate(nickname="NPC_Cyber", email=NPC_CYBER_EMAIL, password=NPC_PASSWORD, elo_rank=950, currency_value=7000, victories=0, defeats=0, damage_dealt=0, damage_taken=0, ships_destroyed_by_user=0, ships_lost_by_user=0),
                schemas.UserCreate(nickname="NPC_Orion", email=NPC_ORION_EMAIL, password=NPC_PASSWORD, elo_rank=1100, currency_value=9000, victories=0, defeats=0, damage_dealt=0, damage_taken=0, ships_destroyed_by_user=0, ships_lost_by_user=0),
                schemas.UserCreate(nickname="NPC_Vega", email=NPC_VEGA_EMAIL, password=NPC_PASSWORD, elo_rank=1250, currency_value=11000, victories=0, defeats=0, damage_dealt=0, damage_taken=0, ships_destroyed_by_user=0, ships_lost_by_user=0),
                schemas.UserCreate(nickname="NPC_Nebula", email=NPC_NEBULA_EMAIL, password=NPC_PASSWORD, elo_rank=1400, currency_value=13000, victories=0, defeats=0, damage_dealt=0, damage_taken=0, ships_destroyed_by_user=0, ships_lost_by_user=0),
                schemas.UserCreate(nickname="NPC_Pulsar", email=NPC_PULSAR_EMAIL, password=NPC_PASSWORD, elo_rank=1550, currency_value=15000, victories=0, defeats=0, damage_dealt=0, damage_taken=0, ships_destroyed_by_user=0, ships_lost_by_user=0),
                schemas.UserCreate(nickname="NPC_Quasar", email=NPC_QUASAR_EMAIL, password=NPC_PASSWORD, elo_rank=1700, currency_value=17000, victories=0, defeats=0, damage_dealt=0, damage_taken=0, ships_destroyed_by_user=0, ships_lost_by_user=0),
                schemas.UserCreate(nickname="NPC_Titan", email=NPC_TITAN_EMAIL, password=NPC_PASSWORD, elo_rank=1850, currency_value=19000, victories=0, defeats=0, damage_dealt=0, damage_taken=0, ships_destroyed_by_user=0, ships_lost_by_user=0),
                schemas.UserCreate(nickname="NPC_Solaris", email=NPC_SOLARIS_EMAIL, password=NPC_PASSWORD, elo_rank=2000, currency_value=21000, victories=0, defeats=0, damage_dealt=0, damage_taken=0, ships_destroyed_by_user=0, ships_lost_by_user=0),
                schemas.UserCreate(nickname="NPC_Andromeda", email=NPC_ANDROMEDA_EMAIL, password=NPC_PASSWORD, elo_rank=2150, currency_value=23000, victories=0, defeats=0, damage_dealt=0, damage_taken=0, ships_destroyed_by_user=0, ships_lost_by_user=0),
            ]
            for user in users:
                user_crud.create_user(db, user)
            return {"message": "Users seeded successfully.", "users_seeded": len(users)}
        else:
            count = db.query(User).count()
            return {"message": "Users already seeded.", "users_seeded": count}
    except SQLAlchemyError as e:
        return {"message": f"Error: {str(e)}", "users_seeded": 0}
    finally:
        db.close()

def seed_assign_npc_ships(db: Session):
    npcs = db.query(User).filter(User.nickname.like("NPC_%")).all()
    assigned = 0
    for npc in npcs:
        # Select the ship most compatible with the NPC's ELO
        ship = db.query(Ship).order_by(func.abs(Ship.attack - (npc.elo_rank / 50))).first()
        if ship:
            # Check if you already have this ship
            already_owned = db.query(OwnedShips).filter_by(user_id=npc.user_id, ship_id=ship.ship_id).first()
            if not already_owned:
                owned_ship = OwnedShips(
                    user_id=npc.user_id,
                    ship_id=ship.ship_id,
                    ship_name=ship.ship_name,
                    status='owned',
                    base_attack=ship.attack,
                    base_shield=ship.shield,
                    base_evasion=ship.evasion,
                    base_fire_rate=ship.fire_rate,
                    base_hp=ship.hp,
                    base_value=ship.value,
                    actual_attack=ship.attack,
                    actual_shield=ship.shield,
                    actual_evasion=ship.evasion,
                    actual_fire_rate=ship.fire_rate,
                    actual_hp=ship.hp,
                    actual_value=ship.value
                )
                db.add(owned_ship)
                assigned += 1
    db.commit()
    return {"message": "NPC ships assigned successfully.", "npc_ships_assigned": assigned}