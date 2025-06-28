# app/routes/users.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.database import create_schemas as models
from backend.app.database import create_database as database_config
from backend.app import schemas
from backend.app.crud import user_crud
from backend.app.utils_auth import create_access_token

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

def get_db():
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    
    existing_nickname = db.query(models.User).filter(models.User.nickname == user.nickname).first()
    
    errors = []
    if existing_email:
        errors.append("Email already registered")
    if existing_nickname:
        errors.append("Nickname already registered")
    
    if errors:
        error_message = "; ".join(errors)
        raise HTTPException(status_code=400, detail=error_message)
    
    return user_crud.create_user(db=db, user=user)

@router.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user.email, "user_id": db_user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=list[schemas.UserResponse])
def list_users_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db=db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user