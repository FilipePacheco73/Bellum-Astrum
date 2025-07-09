# app/routes/users.py
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import get_db, User
from backend.app.schemas.user_schemas import UserCreate, UserLogin, UserResponse
from backend.app.crud import user_crud
from backend.app.utils import create_access_token, log_user_action, log_security_event, log_error, GameAction
import time

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    
    try:
        existing_email = db.query(User).filter(User.email == user.email).first()
        existing_nickname = db.query(User).filter(User.nickname == user.nickname).first()
        
        errors = []
        if existing_email:
            errors.append("Email already registered")
        if existing_nickname:
            errors.append("Nickname already registered")
        
        if errors:
            error_message = "; ".join(errors)
            execution_time = int((time.time() - start_time) * 1000)
            
            # Log failed registration attempt
            log_security_event(
                db=db,
                action=GameAction.REGISTER,
                ip_address=request.client.host,
                details={
                    "email": user.email,
                    "nickname": user.nickname,
                    "errors": errors,
                    "success": False,
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=400, detail=error_message)
        
        # Create user
        new_user = user_crud.create_user(db=db, user=user)
        execution_time = int((time.time() - start_time) * 1000)
        
        # Log successful registration
        log_user_action(
            db=db,
            action=GameAction.REGISTER,
            user_id=new_user.user_id,
            details={
                "email": user.email,
                "nickname": user.nickname,
                "success": True
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time
        )
        
        return new_user
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.REGISTER,
            error_message=str(e),
            details={
                "email": user.email,
                "nickname": user.nickname,
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login")
def login_user(user: UserLogin, request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    
    try:
        db_user = user_crud.authenticate_user(db, user.email, user.password)
        execution_time = int((time.time() - start_time) * 1000)
        
        if not db_user:
            # Log failed login attempt
            log_security_event(
                db=db,
                action=GameAction.LOGIN,
                ip_address=request.client.host,
                details={
                    "email": user.email,
                    "success": False,
                    "reason": "Invalid credentials",
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Generate access token
        access_token = create_access_token({"sub": db_user.email, "user_id": db_user.user_id})
        
        # Log successful login
        log_user_action(
            db=db,
            action=GameAction.LOGIN,
            user_id=db_user.user_id,
            details={
                "email": user.email,
                "success": True,
                "nickname": db_user.nickname
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.LOGIN,
            error_message=str(e),
            details={
                "email": user.email,
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail="Login failed")

@router.get("/", response_model=list[UserResponse])
def list_users_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db=db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user