"""
Database module for Bellum Astrum space battle game.

This module provides clean, organized access to all database components:
- Configuration and engine setup
- Session management and dependency injection  
- SQLAlchemy models for all game entities
- Database lifecycle management and health monitoring

Usage:
    # Clean imports for common use cases
    from database import get_db, User, Ship
    from database import initialize_database, check_database_health
"""

# Configuration and engine
from .config import (
    engine,
    Base,
    DATABASE_URL,
    DATABASE_NAME
)

# Session management
from .session import (
    SessionLocal,
    get_db,
    create_session
)

# Database models
from .models import (
    User,
    Ship,
    OwnedShips,
    BattleHistory,
    SystemLogs,
    utc_now
)

# Base data for seeding
from .base_data import (
    get_ships_data,
    get_users_data,
    get_npc_users,
    get_admin_user,
    SHIPS_DATA,
    USERS_DATA
)

# Lifecycle management
from .lifecycle import (
    initialize_database,
    shutdown_database,
    check_database_health,
    reset_database,
    seed_initial_data,
    clear_all_data
)

# Organized exports for clean imports
__all__ = [
    # Configuration
    "engine",
    "Base", 
    "DATABASE_URL",
    "DATABASE_NAME",
    
    # Session management
    "SessionLocal",
    "get_db",
    "create_session",
    
    # Models
    "User",
    "Ship",
    "OwnedShips", 
    "BattleHistory",
    "SystemLogs",
    "utc_now",
    
    # Base data
    "get_ships_data",
    "get_users_data", 
    "get_npc_users",
    "get_admin_user",
    "SHIPS_DATA",
    "USERS_DATA",
    
    # Lifecycle
    "initialize_database",
    "shutdown_database",
    "check_database_health",
    "reset_database",
    "seed_initial_data",
    "clear_all_data"
]
