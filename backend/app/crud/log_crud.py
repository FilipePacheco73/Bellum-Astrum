from sqlalchemy.orm import Session
from database import SystemLogs
from backend.app.schemas.log_schemas import SystemLogCreate, LogQueryRequest
from typing import List, Optional, Tuple

def create_log(db: Session, log: SystemLogCreate) -> SystemLogs:
    db_log = SystemLogs(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_log(db: Session, log_id: int) -> Optional[SystemLogs]:
    return db.query(SystemLogs).filter(SystemLogs.log_id == log_id).first()

def get_logs(db: Session, query_params: LogQueryRequest) -> Tuple[List[SystemLogs], int]:
    """
    Get logs with filtering and pagination
    Returns tuple of (logs_list, total_count)
    """
    # Build base query
    query = db.query(SystemLogs)
    
    # Apply filters
    if query_params.user_id is not None:
        query = query.filter(SystemLogs.user_id == query_params.user_id)
    
    if query_params.log_level:
        query = query.filter(SystemLogs.log_level == query_params.log_level)
    
    if query_params.log_category:
        query = query.filter(SystemLogs.log_category == query_params.log_category)
    
    if query_params.action:
        query = query.filter(SystemLogs.action.ilike(f"%{query_params.action}%"))
    
    if query_params.start_date:
        query = query.filter(SystemLogs.timestamp >= query_params.start_date)
    
    if query_params.end_date:
        query = query.filter(SystemLogs.timestamp <= query_params.end_date)
    
    # Get total count before applying pagination
    total_count = query.count()
    
    # Apply pagination and ordering (most recent first)
    logs = query.order_by(SystemLogs.timestamp.desc()).offset(query_params.offset).limit(query_params.limit).all()
    
    return logs, total_count

def delete_log(db: Session, log_id: int) -> bool:
    db_log = db.query(SystemLogs).filter(SystemLogs.log_id == log_id).first()
    if db_log:
        db.delete(db_log)
        db.commit()
        return True
    return False
