from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from backend.app.crud.log_crud import create_log, get_log, get_logs, delete_log
from backend.app.schemas.log_schemas import SystemLogCreate, SystemLogResponse, LogQueryRequest, LogQueryResponse
from typing import List

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.post("/", response_model=SystemLogResponse)
def create_log_route(log: SystemLogCreate, db: Session = Depends(get_db)):
    return create_log(db, log)

@router.get("/", response_model=LogQueryResponse)
def list_logs_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = get_logs(db, skip=skip, limit=limit)
    return LogQueryResponse(
        logs=logs,
        total_count=len(logs),
        page=skip // limit + 1 if limit else 1,
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
