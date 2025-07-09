"""
Utility functions for logging system events and user actions.
Provides convenient methods to log different types of events to the SystemLogs table.
"""

from sqlalchemy.orm import Session
from database import SystemLogs
from datetime import datetime, UTC
import json
from typing import Optional, Dict, Any
from enum import Enum
from backend.app.crud.log_crud import create_log
from backend.app.schemas.log_schemas import SystemLogCreate

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogCategory(Enum):
    USER_ACTION = "USER_ACTION"
    SYSTEM = "SYSTEM"
    GAME_EVENT = "GAME_EVENT"
    SECURITY = "SECURITY"
    PERFORMANCE = "PERFORMANCE"
    AUDIT = "AUDIT"

class GameAction(Enum):
    # User actions
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    REGISTER = "REGISTER"
    
    # Ship actions
    BUY_SHIP = "BUY_SHIP"
    SELL_SHIP = "SELL_SHIP"
    ACTIVATE_SHIP = "ACTIVATE_SHIP"
    
    # Battle actions
    BATTLE_START = "BATTLE_START"
    BATTLE_END = "BATTLE_END"
    
    # Currency actions
    CURRENCY_EARNED = "CURRENCY_EARNED"
    CURRENCY_SPENT = "CURRENCY_SPENT"
    
    # System actions
    DATABASE_ERROR = "DATABASE_ERROR"
    API_ERROR = "API_ERROR"
    PERFORMANCE_ISSUE = "PERFORMANCE_ISSUE"

def log_event(
    db: Session,
    level: LogLevel,
    category: LogCategory,
    action: GameAction,
    user_id: Optional[int] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    session_id: Optional[str] = None,
    resource_affected: Optional[str] = None,
    old_value: Optional[Dict[str, Any]] = None,
    new_value: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None,
    execution_time_ms: Optional[int] = None
) -> SystemLogs:
    """
    Create a new log entry in the SystemLogs table using the CRUD layer.
    
    Args:
        db: Database session
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        category: Log category (USER_ACTION, SYSTEM, GAME_EVENT, etc.)
        action: Specific action performed
        user_id: ID of the user (optional for system events)
        details: Additional details in dictionary format
        ip_address: User's IP address
        user_agent: User's browser/client information
        session_id: Session identifier
        resource_affected: Resource that was affected (e.g., "ship_id:123")
        old_value: Previous value before change
        new_value: New value after change
        error_message: Error message if action failed
        execution_time_ms: Execution time in milliseconds
    
    Returns:
        The created SystemLogs entry
    """
    log_data = SystemLogCreate(
        log_level=level.value,
        log_category=category.value,
        action=action.value,
        user_id=user_id,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
        session_id=session_id,
        resource_affected=resource_affected,
        old_value=old_value,
        new_value=new_value,
        error_message=error_message,
        execution_time_ms=execution_time_ms
    )
    return create_log(db, log_data)

# Convenience functions for common log types

def log_user_action(
    db: Session,
    action: GameAction,
    user_id: int,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    session_id: Optional[str] = None,
    execution_time_ms: Optional[int] = None
) -> SystemLogs:
    """Log a user action."""
    return log_event(
        db=db,
        level=LogLevel.INFO,
        category=LogCategory.USER_ACTION,
        action=action,
        user_id=user_id,
        details=details,
        ip_address=ip_address,
        session_id=session_id,
        execution_time_ms=execution_time_ms
    )

def log_game_event(
    db: Session,
    action: GameAction,
    user_id: Optional[int] = None,
    details: Optional[Dict[str, Any]] = None,
    resource_affected: Optional[str] = None,
    old_value: Optional[Dict[str, Any]] = None,
    new_value: Optional[Dict[str, Any]] = None
) -> SystemLogs:
    """Log a game event."""
    return log_event(
        db=db,
        level=LogLevel.INFO,
        category=LogCategory.GAME_EVENT,
        action=action,
        user_id=user_id,
        details=details,
        resource_affected=resource_affected,
        old_value=old_value,
        new_value=new_value
    )

def log_error(
    db: Session,
    action: GameAction,
    error_message: str,
    user_id: Optional[int] = None,
    details: Optional[Dict[str, Any]] = None
) -> SystemLogs:
    """Log an error event."""
    return log_event(
        db=db,
        level=LogLevel.ERROR,
        category=LogCategory.SYSTEM,
        action=action,
        user_id=user_id,
        details=details,
        error_message=error_message
    )

def log_security_event(
    db: Session,
    action: GameAction,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> SystemLogs:
    """Log a security-related event."""
    return log_event(
        db=db,
        level=LogLevel.WARNING,
        category=LogCategory.SECURITY,
        action=action,
        user_id=user_id,
        ip_address=ip_address,
        details=details
    )

def log_performance_issue(
    db: Session,
    action: GameAction,
    execution_time_ms: int,
    details: Optional[Dict[str, Any]] = None
) -> SystemLogs:
    """Log a performance issue."""
    return log_event(
        db=db,
        level=LogLevel.WARNING,
        category=LogCategory.PERFORMANCE,
        action=action,
        details=details,
        execution_time_ms=execution_time_ms
    )
