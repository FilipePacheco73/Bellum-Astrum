# app/routes/seed.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.app.database import create_database as database_config
from backend.app.crud.seed_crud import seed_ships, seed_users, seed_assign_npc_ships
from backend.app.schemas import SeedShipsResponse, SeedUsersResponse, SeedNPCShipsResponse
from backend.app.utils import log_user_action, log_error, log_event, GameAction, LogCategory, LogLevel
import time

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
def seed_users_route(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint to seed the database with initial user data.
    """
    start_time = time.time()
    
    try:
        result = seed_users(db)
        execution_time = int((time.time() - start_time) * 1000)
        
        # Log seed operation (admin action)
        log_event(
            db=db,
            level=LogLevel.INFO,
            category=LogCategory.AUDIT,
            action=GameAction.REGISTER,  # Using as proxy for user creation
            details={
                "operation": "SEED_USERS",
                "users_created": result.get("users_created", 0),
                "total_users": result.get("total_users", 0),
                "success": True
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time,
            resource_affected="users_table"
        )
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.REGISTER,  # Using as proxy
            error_message=str(e),
            details={
                "operation": "SEED_USERS",
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ships", response_model=SeedShipsResponse)
def seed_ships_route(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint to seed the database with initial ship data.
    """
    start_time = time.time()
    
    try:
        result = seed_ships(db)
        execution_time = int((time.time() - start_time) * 1000)
        
        # Log seed operation (admin action)
        log_event(
            db=db,
            level=LogLevel.INFO,
            category=LogCategory.AUDIT,
            action=GameAction.BUY_SHIP,  # Using as proxy for ship creation
            details={
                "operation": "SEED_SHIPS",
                "ships_created": result.get("ships_created", 0),
                "total_ships": result.get("total_ships", 0),
                "success": True
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time,
            resource_affected="ships_table"
        )
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.BUY_SHIP,  # Using as proxy
            error_message=str(e),
            details={
                "operation": "SEED_SHIPS",
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/npc-ships", response_model=SeedNPCShipsResponse)
def seed_npc_ships_route(request: Request, db: Session = Depends(get_db)):
    """
    Assign compatible ships to all NPCs based on their ELO.
    """
    start_time = time.time()
    
    try:
        result = seed_assign_npc_ships(db)
        execution_time = int((time.time() - start_time) * 1000)
        
        # Log seed operation (admin action)
        log_event(
            db=db,
            level=LogLevel.INFO,
            category=LogCategory.AUDIT,
            action=GameAction.BUY_SHIP,  # Using as proxy for ship assignment
            details={
                "operation": "SEED_NPC_SHIPS",
                "npc_ships_assigned": result.get("npc_ships_assigned", 0),
                "success": True
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time,
            resource_affected="owned_ships_table"
        )
        
        return result
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.BUY_SHIP,  # Using as proxy
            error_message=str(e),
            details={
                "operation": "SEED_NPC_SHIPS",
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail=str(e))