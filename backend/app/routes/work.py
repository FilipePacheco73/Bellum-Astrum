"""
Work system API routes.

This module contains FastAPI routes for the work system,
including work performance, status checks, and history.
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.utils.auth_utils import get_current_user
from backend.app.crud.work_crud import (
    perform_work,
    get_user_work_status,
    get_user_work_history,
    get_available_work_types_for_user
)
from backend.app.schemas.work_schemas import (
    WorkPerformResponse,
    WorkStatusResponse,
    WorkHistoryResponse,
    AvailableWorkTypesResponse
)
from backend.app.utils import log_user_action, log_error, GameAction
from backend.app.utils.work_utils import format_work_success_message
import time

router = APIRouter(prefix="/work", tags=["Work"])


@router.post("/perform", response_model=WorkPerformResponse)
def perform_work_route(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Perform work to earn currency based on user's rank.
    
    The work system allows users to earn currency by performing tasks
    appropriate to their rank. Higher ranks earn more but have longer cooldowns.
    Each rank has a specific work type automatically assigned.
    """
    start_time = time.time()
    
    try:
        result, message = perform_work(
            db=db, 
            user_id=current_user.user_id
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        if not result:
            log_error(
                db=db,
                action=GameAction.WORK_PERFORM,
                error_message=message,
                user_id=current_user.user_id,
                details={
                    "user_rank": current_user.rank.value,
                    "success": False,
                    "execution_time_ms": execution_time
                }
            )
            raise HTTPException(status_code=400, detail=message)
        
        # Log successful work
        log_user_action(
            db=db,
            action=GameAction.WORK_PERFORM,
            user_id=current_user.user_id,
            details={
                "work_type": result["work_type"],
                "income_earned": result["income_earned"],
                "new_currency_balance": result["new_currency_balance"],
                "user_rank": current_user.rank.value,
                "cooldown_minutes": result["next_available_in_minutes"],
                "success": True
            },
            ip_address=request.client.host,
            execution_time_ms=execution_time
        )
        
        return WorkPerformResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        log_error(
            db=db,
            action=GameAction.WORK_PERFORM,
            error_message=str(e),
            user_id=current_user.user_id,
            details={
                "execution_time_ms": execution_time,
                "exception_type": type(e).__name__
            }
        )
        raise HTTPException(status_code=500, detail=f"Work performance failed: {str(e)}")


@router.get("/status", response_model=WorkStatusResponse)
def get_work_status_route(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get the current work status for the authenticated user.
    
    Returns information about whether the user can currently work,
    cooldown timers, and estimated income for their rank.
    """
    try:
        status = get_user_work_status(db=db, user_id=current_user.user_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="User work status not found")
        
        return WorkStatusResponse(**status)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get work status: {str(e)}")


@router.get("/history", response_model=WorkHistoryResponse)
def get_work_history_route(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get work history for the authenticated user.
    
    Returns a list of recent work activities, including total earnings
    and statistics about the user's work performance.
    """
    try:
        if limit < 1 or limit > 100:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
        
        history = get_user_work_history(db=db, user_id=current_user.user_id, limit=limit)
        
        if not history:
            raise HTTPException(status_code=404, detail="User work history not found")
        
        return WorkHistoryResponse(**history)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get work history: {str(e)}")


@router.get("/types", response_model=AvailableWorkTypesResponse)
def get_available_work_types_route(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get available work type for the authenticated user's rank.
    
    Returns the type of work available for the user's current rank,
    along with estimated income range and cooldown information.
    """
    try:
        work_types = get_available_work_types_for_user(db=db, user_id=current_user.user_id)
        
        if not work_types:
            raise HTTPException(status_code=404, detail="User work types not found")
        
        return AvailableWorkTypesResponse(**work_types)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get available work types: {str(e)}")
