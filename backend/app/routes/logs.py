from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.crud.log_crud import create_log, get_log, get_logs, delete_log
from backend.app.schemas.log_schemas import SystemLogCreate, SystemLogResponse, LogQueryRequest, LogQueryResponse
from typing import List

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.post("/", response_model=SystemLogResponse)
def create_log_route(log: SystemLogCreate, db: Session = Depends(get_db)):
    return create_log(db, log)

@router.get("/", response_model=LogQueryResponse)
def list_logs_route(
    user_id: int = None,
    log_level: str = None,
    log_category: str = None,
    action: str = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    # Create query parameters object
    query_params = LogQueryRequest(
        user_id=user_id,
        log_level=log_level,
        log_category=log_category,
        action=action,
        limit=limit,
        offset=offset
    )
    
    logs, total_count = get_logs(db, query_params)
    
    return LogQueryResponse(
        logs=logs,
        total_count=total_count,
        page=offset // limit + 1 if limit else 1,
        per_page=limit
    )

@router.get("/{log_id}", response_model=SystemLogResponse)
def get_log_route(log_id: int, db: Session = Depends(get_db)):
    log = get_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log

@router.delete("/{log_id}")
def delete_log_route(log_id: int, db: Session = Depends(get_db)):
    if not delete_log(db, log_id):
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log deleted"}
