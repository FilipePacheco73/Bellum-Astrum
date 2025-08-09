"""
Database lifecycle management and health monitoring.

This module handles database initialization, cleanup, health checks, 
and initial data seeding. Centralizes all database lifecycle concerns.
"""

from .config import engine, Base
from .session import create_session
from .models import User, Ship, OwnedShips, SystemLogs, ShipyardLog, RankBonus, UserRank, WorkLog
from .base_data import get_ships_data, get_users_data, get_npc_users, get_rank_bonuses_data, get_owned_ships_assignments
from sqlalchemy import func, text
import logging
import time
import hashlib
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple password hashing (you should use proper password hashing in production)
def get_password_hash(password: str) -> str:
    """Hash a password using SHA-256. For production, use bcrypt or similar."""
    salt = secrets.token_hex(16)
    return hashlib.sha256((password + salt).encode()).hexdigest() + ':' + salt

def log_system_event(session, action: str, details: dict = None, log_level: str = "INFO", 
                    category: str = "SYSTEM", execution_time_ms: int = None) -> None:
    """
    Log system events to the SystemLogs table.
    
    Args:
        session: Database session
        action: Action being performed (e.g., 'SEED_SHIPS', 'SEED_USERS')
        details: Additional details about the action
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        category: Log category (SYSTEM, AUDIT, etc.)
        execution_time_ms: Execution time in milliseconds
    """
    try:
        system_log = SystemLogs(
            user_id=None,  # System actions don't have a user
            log_level=log_level,
            log_category=category,
            action=action,
            details=details or {},
            execution_time_ms=execution_time_ms
        )
        session.add(system_log)
        # Don't commit here - let the caller handle the transaction
    except Exception as e:
        logger.error(f"Failed to create system log entry: {e}")
        # Don't raise - logging failure shouldn't break the main operation

def initialize_database(with_seed: bool = False) -> None:
    """
    Initialize the database by creating all tables.
    
    This function should be called during application startup
    to ensure all necessary tables exist. It's idempotent - 
    safe to call multiple times.
    
    Args:
        with_seed: If True, also populate initial data after creating tables
    
    Raises:
        Exception: If database initialization fails
    """
    start_time = time.time()
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Log database initialization (we need a session after tables are created)
        session = create_session()
        try:
            execution_time_ms = int((time.time() - start_time) * 1000)
            log_system_event(
                session,
                action="DATABASE_INIT",
                details={
                    "message": "Database tables initialized successfully",
                    "with_seed": with_seed
                },
                category="SYSTEM",
                execution_time_ms=execution_time_ms
            )
            session.commit()
        except Exception as log_error:
            logger.warning(f"Failed to log database initialization: {log_error}")
        finally:
            session.close()
        
        if with_seed:
            seed_initial_data()
            
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def shutdown_database() -> None:
    """
    Cleanup database connections during application shutdown.
    
    This function should be called during application shutdown
    to properly close database connections and free resources.
    """
    try:
        logger.info("Shutting down database connections...")
        engine.dispose()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Error shutting down database: {e}")

def check_database_health() -> bool:
    """
    Check if the database is accessible and healthy.
    
    Performs a simple connectivity test to verify the database
    is responding and accessible.
    
    Returns:
        bool: True if database is healthy, False otherwise
    """
    try:
        # Simple connection test with a basic query
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

def reset_database() -> None:
    """
    Reset the database by dropping and recreating all tables.
    
    ⚠️  WARNING: This will DELETE ALL DATA in the database!
    Use only for testing or development environments.
    
    Raises:
        Exception: If database reset fails
    """
    start_time = time.time()
    try:
        logger.warning("RESETTING DATABASE - ALL DATA WILL BE LOST!")
        
        # Try to log before dropping tables (if tables exist)
        try:
            session = create_session()
            log_system_event(
                session,
                action="DATABASE_RESET_START",
                details={"message": "Starting database reset - all data will be lost"},
                log_level="WARNING",
                category="SYSTEM"
            )
            session.commit()
            session.close()
        except:
            pass  # Tables might not exist yet
        
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        # Log after recreation
        session = create_session()
        try:
            execution_time_ms = int((time.time() - start_time) * 1000)
            log_system_event(
                session,
                action="DATABASE_RESET_COMPLETE",
                details={"message": "Database reset completed successfully"},
                log_level="WARNING",
                category="SYSTEM",
                execution_time_ms=execution_time_ms
            )
            session.commit()
        except Exception as log_error:
            logger.warning(f"Failed to log database reset: {log_error}")
        finally:
            session.close()
            
        logger.info("Database reset completed successfully")
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise

# =============================================================================
# SEED DATA FUNCTIONS
# =============================================================================

def seed_initial_data() -> None:
    """
    Populate the database with initial game data.
    
    This function seeds the database with:
    - Basic ship templates
    - Admin/test users
    - Sample owned ships for testing
    
    Safe to call multiple times - checks for existing data.
    """
    start_time = time.time()
    logger.info("Starting database seeding...")
    session = create_session()
    try:
        # Log the start of seeding process
        log_system_event(
            session, 
            action="SEED_START",
            details={"message": "Starting database seeding process"},
            category="SYSTEM"
        )
        ships_count = seed_ships(session)
        users_count = seed_users(session)
        # Flush to ensure all IDs are available for foreign key references
        session.flush()
        owned_ships_count = seed_owned_ships(session)
        # Seed rank bonuses
        rank_bonus_count = seed_rank_bonuses(session)
        # Calculate total execution time
        execution_time_ms = int((time.time() - start_time) * 1000)
        # Log the completion of seeding process
        log_system_event(
            session,
            action="SEED_COMPLETE",
            details={
                "message": "Database seeding completed successfully",
                "ships_seeded": ships_count,
                "users_seeded": users_count,
                "owned_ships_seeded": owned_ships_count,
                "rank_bonuses_seeded": rank_bonus_count,
                "total_records": ships_count + users_count + owned_ships_count
            },
            category="SYSTEM",
            execution_time_ms=execution_time_ms
        )
        session.commit()
        logger.info("Database seeding completed successfully")
    except Exception as e:
        session.rollback()
        # Log the error
        execution_time_ms = int((time.time() - start_time) * 1000)
        log_system_event(
            session,
            action="SEED_ERROR",
            details={
                "message": "Database seeding failed",
                "error": str(e)
            },
            log_level="ERROR",
            category="SYSTEM",
            execution_time_ms=execution_time_ms
        )
        try:
            session.commit()  # Try to save the error log
        except:
            pass  # If we can't log, at least don't hide the original error
        raise e
    finally:
        session.close()

def seed_rank_bonuses(session) -> int:
    """Seed the RankBonus table with default values for each UserRank if not present."""
    try:
        existing_count = session.query(RankBonus).count()
        if existing_count > 0:
            logger.info("RankBonus entries already exist, skipping rank bonus seeding")
            log_system_event(
                session,
                action="SEED_RANKBONUS_SKIPPED",
                details={
                    "message": "RankBonus entries already exist in database",
                    "existing_count": existing_count
                },
                category="SYSTEM"
            )
            return 0
    except Exception as e:
        # If count fails (e.g., during schema migration), assume table is empty and proceed
        logger.info(f"Could not check existing RankBonus count (likely fresh table): {e}")
        logger.info("Proceeding with rank bonus seeding...")

    logger.info("Seeding rank bonuses...")
    bonuses = get_rank_bonuses_data()
    count = 0
    for bonus in bonuses:
        rb = RankBonus(**bonus)
        session.add(rb)
        count += 1
    log_system_event(
        session,
        action="SEED_RANKBONUS",
        details={
            "message": "RankBonus seeded successfully",
            "rank_bonuses_added": count,
            "total_available": len(bonuses)
        },
        category="SYSTEM"
    )
    logger.info(f"Added {count} rank bonuses")
    return count

def seed_ships(session) -> int:
    """Seed basic ship templates using data from base_data.py."""
    start_time = time.time()
    
    # Check if ships already exist
    existing_count = session.query(Ship).count()
    if existing_count > 0:
        logger.info("Ships already exist, skipping ship seeding")
        log_system_event(
            session,
            action="SEED_SHIPS_SKIPPED",
            details={
                "message": "Ships already exist in database",
                "existing_count": existing_count
            },
            category="SYSTEM"
        )
        return 0
    
    logger.info("Seeding ship templates...")
    
    ships_data = get_ships_data()
    ships_added = 0
    
    for ship_data in ships_data:
        try:
            ship = Ship(**ship_data)
            session.add(ship)
            ships_added += 1
        except Exception as e:
            logger.error(f"Failed to add ship {ship_data.get('ship_name', 'unknown')}: {e}")
    
    execution_time_ms = int((time.time() - start_time) * 1000)
    
    log_system_event(
        session,
        action="SEED_SHIPS",
        details={
            "message": "Ship templates seeded successfully",
            "ships_added": ships_added,
            "total_available": len(ships_data)
        },
        category="SYSTEM",
        execution_time_ms=execution_time_ms
    )
    
    logger.info(f"Added {ships_added} ship templates")
    return ships_added

def seed_users(session) -> int:
    """Seed admin and NPC users using data from base_data.py."""
    start_time = time.time()
    
    # Check if users already exist
    existing_count = session.query(User).count()
    if existing_count > 0:
        logger.info("Users already exist, skipping user seeding")
        log_system_event(
            session,
            action="SEED_USERS_SKIPPED",
            details={
                "message": "Users already exist in database",
                "existing_count": existing_count
            },
            category="SYSTEM"
        )
        return 0
    
    logger.info("Seeding users...")
    
    users_data = get_users_data()
    users_added = 0
    admin_count = 0
    npc_count = 0
    
    for user_data in users_data:
        try:
            # Hash the password before creating user
            user_dict = user_data.copy()
            user_dict["password_hash"] = get_password_hash(user_data["password"])
            del user_dict["password"]  # Remove plain password
            
            user = User(**user_dict)
            session.add(user)
            users_added += 1
            
            # Count user types for logging
            if user_data["nickname"] == "Admin":
                admin_count += 1
            elif user_data["nickname"].startswith("NPC_"):
                npc_count += 1
                
        except Exception as e:
            logger.error(f"Failed to add user {user_data.get('nickname', 'unknown')}: {e}")
    
    execution_time_ms = int((time.time() - start_time) * 1000)
    
    log_system_event(
        session,
        action="SEED_USERS",
        details={
            "message": "Users seeded successfully",
            "users_added": users_added,
            "admin_count": admin_count,
            "npc_count": npc_count,
            "total_available": len(users_data)
        },
        category="SYSTEM",
        execution_time_ms=execution_time_ms
    )
    
    logger.info(f"Added {users_added} users")
    return users_added

def seed_owned_ships(session) -> int:
    """Seed owned ships using hardcoded assignments from base_data."""
    start_time = time.time()
    
    # Check if owned ships already exist
    existing_count = session.query(OwnedShips).count()
    if existing_count > 0:
        logger.info("Owned ships already exist, skipping owned ships seeding")
        log_system_event(
            session,
            action="SEED_OWNED_SHIPS_SKIPPED",
            details={
                "message": "Owned ships already exist in database",
                "existing_count": existing_count
            },
            category="SYSTEM"
        )
        return 0
    
    logger.info("Seeding owned ships using hardcoded assignments...")
    
    # Get hardcoded assignments from base_data
    assignments = get_owned_ships_assignments()
    assigned = 0
    ship_assignments = []
    
    for assignment in assignments:
        try:
            user_nickname = assignment["user_nickname"]
            ship_name = assignment["ship_name"]
            status = assignment["status"]
            
            # Get user and ship from database
            user = session.query(User).filter(User.nickname == user_nickname).first()
            ship = session.query(Ship).filter(Ship.ship_name == ship_name).first()
            
            if not user:
                logger.warning(f"User {user_nickname} not found, skipping ship assignment")
                continue
                
            if not ship:
                logger.warning(f"Ship {ship_name} not found, skipping assignment for {user_nickname}")
                continue
            
            logger.debug(f"Assigning {ship_name} to {user_nickname} (Level: {user.level}, Rank: {user.rank.value})")
            
            # Create owned ship
            owned_ship = OwnedShips(
                user_id=user.user_id,
                ship_id=ship.ship_id,
                ship_name=ship.ship_name,
                status=status,
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
            session.add(owned_ship)
            assigned += 1
            
            ship_assignments.append({
                "user_nickname": user_nickname,
                "user_id": user.user_id,
                "user_level": user.level,
                "user_rank": user.rank.value,
                "ship_name": ship_name,
                "ship_id": ship.ship_id,
                "ship_attack": ship.attack
            })
            
            logger.debug(f"Successfully assigned {ship_name} to {user_nickname}")
            
        except Exception as e:
            logger.error(f"Failed to assign ship {assignment.get('ship_name', 'unknown')} to {assignment.get('user_nickname', 'unknown')}: {e}")
    
    execution_time_ms = int((time.time() - start_time) * 1000)
    
    log_system_event(
        session,
        action="SEED_OWNED_SHIPS",
        details={
            "message": "Owned ships seeded successfully using hardcoded assignments",
            "ships_assigned": assigned,
            "total_assignments": len(assignments),
            "ship_assignments": ship_assignments
        },
        category="SYSTEM",
        execution_time_ms=execution_time_ms
    )
    
    logger.info(f"Added {assigned} owned ships from {len(assignments)} assignments")
    return assigned

def clear_all_data() -> None:
    """
    Clear all data from the database.
    
    ⚠️  WARNING: This will DELETE ALL DATA but keep table structure!
    Use only for testing or development environments.
    """
    start_time = time.time()
    try:
        logger.warning("CLEARING ALL DATABASE DATA!")
        
        session = create_session()
        try:
            # Count existing data before deletion
            users_count = session.query(User).count()
            ships_count = session.query(Ship).count()
            owned_ships_count = session.query(OwnedShips).count()
            work_logs_count = session.query(WorkLog).count()
            
            # Log the start of data clearing
            log_system_event(
                session,
                action="CLEAR_DATA_START",
                details={
                    "message": "Starting database data clearing",
                    "users_to_delete": users_count,
                    "ships_to_delete": ships_count,
                    "owned_ships_to_delete": owned_ships_count,
                    "work_logs_to_delete": work_logs_count
                },
                log_level="WARNING",
                category="SYSTEM"
            )
            
            # Delete in order to respect foreign key constraints
            session.query(WorkLog).delete()
            session.query(OwnedShips).delete()
            session.query(User).delete()
            session.query(Ship).delete()
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Log the completion of data clearing
            log_system_event(
                session,
                action="CLEAR_DATA_COMPLETE",
                details={
                    "message": "Database data cleared successfully",
                    "users_deleted": users_count,
                    "ships_deleted": ships_count,
                    "owned_ships_deleted": owned_ships_count,
                    "work_logs_deleted": work_logs_count,
                    "total_records_deleted": users_count + ships_count + owned_ships_count + work_logs_count
                },
                log_level="WARNING",
                category="SYSTEM",
                execution_time_ms=execution_time_ms
            )
            
            session.commit()
            logger.info("All database data cleared successfully")
        except Exception as e:
            session.rollback()
            
            # Log the error
            execution_time_ms = int((time.time() - start_time) * 1000)
            log_system_event(
                session,
                action="CLEAR_DATA_ERROR",
                details={
                    "message": "Database data clearing failed",
                    "error": str(e)
                },
                log_level="ERROR",
                category="SYSTEM",
                execution_time_ms=execution_time_ms
            )
            
            try:
                session.commit()  # Try to save the error log
            except:
                pass
                
            raise e
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error clearing database data: {e}")
        raise
