from sqlalchemy.orm import Session
from backend.app import schemas
from backend.app.database import create_schemas as models
from backend.app.utils import get_password_hash, verify_password

# --- User CRUD Operations ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        nickname=user.nickname,
        email=user.email,
        password_hash=hashed_password,
        elo_rank=user.elo_rank,
        currency_value=user.currency_value,
        victories=user.victories,
        defeats=user.defeats,
        damage_dealt=user.damage_dealt,
        damage_taken=user.damage_taken,
        ships_destroyed_by_user=user.ships_destroyed_by_user,
        ships_lost_by_user=user.ships_lost_by_user
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user