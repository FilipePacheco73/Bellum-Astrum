from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class SystemLogBase(BaseModel):
    """
    Base model for system logs, defining common log attributes.

    Attributes:
        log_level (str): Severity level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_category (str): Log category (SYSTEM, USER_ACTION, etc).
        action (str): Action or event being logged.
        details (Optional[Dict[str, Any]]): Additional details about the event.
        ip_address (Optional[str]): IP address of the user/client.
        user_agent (Optional[str]): User agent string.
        session_id (Optional[str]): Session identifier.
        resource_affected (Optional[str]): Resource affected by the event.
        old_value (Optional[Dict[str, Any]]): Previous value before change.
        new_value (Optional[Dict[str, Any]]): New value after change.
        error_message (Optional[str]): Error message if applicable.
        execution_time_ms (Optional[int]): Execution time in milliseconds.
    """
    log_level: str
    log_category: str
    action: str
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    resource_affected: Optional[str] = None
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[int] = None

class SystemLogCreate(SystemLogBase):
    """
    Model for creating a new system log entry.

    Attributes:
        user_id (Optional[int]): ID of the user related to the log (if any).
    """
    user_id: Optional[int] = None

class SystemLogResponse(SystemLogBase):
    """
    Response model for system log data returned by the API.

    Attributes:
        log_id (int): Unique log identifier.
        timestamp (datetime): Timestamp of the log entry.
        user_id (Optional[int]): ID of the user related to the log (if any).
    """
    log_id: int
    timestamp: datetime
    user_id: Optional[int]
    model_config = ConfigDict(from_attributes=True)

class LogQueryRequest(BaseModel):
    """
    Model for querying logs with filters.

    Attributes:
        user_id (Optional[int]): Filter by user ID.
        log_level (Optional[str]): Filter by log level.
        log_category (Optional[str]): Filter by log category.
        action (Optional[str]): Filter by action.
        start_date (Optional[datetime]): Filter logs after this date.
        end_date (Optional[datetime]): Filter logs before this date.
        limit (int): Maximum number of logs to return. Default is 100.
        offset (int): Number of logs to skip. Default is 0.
    """
    user_id: Optional[int] = None
    log_level: Optional[str] = None
    log_category: Optional[str] = None
    action: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 100
    offset: int = 0

class LogQueryResponse(BaseModel):
    """
    Response model for a paginated list of logs.

    Attributes:
        logs (List[SystemLogResponse]): List of log entries.
        total_count (int): Total number of logs matching the query.
        page (int): Current page number.
        per_page (int): Number of logs per page.
    """
    logs: List[SystemLogResponse]
    total_count: int
    page: int
    per_page: int
