from sqlalchemy.orm import Session
from database import SystemLogs
from backend.app.schemas.log_schemas import SystemLogCreate
from typing import List, Optional

def create_log(db: Session, log: SystemLogCreate) -> SystemLogs:
    db_log = SystemLogs(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_log(db: Session, log_id: int) -> Optional[SystemLogs]:
    return db.query(SystemLogs).filter(SystemLogs.log_id == log_id).first()

def get_logs(db: Session, skip: int = 0, limit: int = 100) -> List[SystemLogs]:
    return db.query(SystemLogs).offset(skip).limit(limit).all()

def delete_log(db: Session, log_id: int) -> bool:
    db_log = db.query(SystemLogs).filter(SystemLogs.log_id == log_id).first()
    if db_log:
        db.delete(db_log)
        db.commit()
        return True
    return False
