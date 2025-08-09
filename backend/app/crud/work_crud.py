"""
CRUD operations for the work system.

This module contains database operations for work logging,
cooldown management, and work history tracking.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import User, WorkLog, RankBonus, UserRank
from backend.app.utils.work_utils import (
    get_work_type_for_rank,
    calculate_work_income_with_variance,
    get_work_description,
    get_work_income_range_for_rank
)
from datetime import datetime, UTC, timedelta
from typing import Optional, List, Tuple, Dict


def get_user_work_status(db: Session, user_id: int) -> Optional[Dict]:
    """
    Get the current work status for a user.
    
    Args:
        db: Database session
        user_id: User ID to check
        
    Returns:
        Dictionary with work status information or None if user not found
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    
    # Get rank bonus information
    rank_bonus = db.query(RankBonus).filter(RankBonus.rank == user.rank).first()
    if not rank_bonus:
        return None
    
    # Get last work log entry
    last_work = db.query(WorkLog).filter(
        WorkLog.user_id == user_id
    ).order_by(WorkLog.performed_at.desc()).first()
    
    now = datetime.now(UTC)
    can_work = True
    time_until_available = 0.0
    
    if last_work and last_work.cooldown_until.replace(tzinfo=UTC) > now:
        can_work = False
        time_remaining = last_work.cooldown_until.replace(tzinfo=UTC) - now
        time_until_available = time_remaining.total_seconds() / 60.0  # Convert to minutes
    
    work_type = get_work_type_for_rank(user.rank)
    min_income, max_income = get_work_income_range_for_rank(user.rank, rank_bonus.work_income)
    
    return {
        "can_work": can_work,
        "time_until_available": time_until_available,
        "last_work_performed": last_work.performed_at if last_work else None,
        "estimated_income": rank_bonus.work_income,
        "estimated_income_range": {"min": min_income, "max": max_income},
        "work_type": work_type,
        "current_rank": user.rank.value,
        "work_cooldown_minutes": rank_bonus.work_cooldown_minutes
    }


def can_user_work(db: Session, user_id: int) -> Tuple[bool, str]:
    """
    Check if a user can currently perform work.
    
    Args:
        db: Database session
        user_id: User ID to check
        
    Returns:
        Tuple of (can_work: bool, message: str)
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return False, "User not found"
    
    # Get last work entry
    last_work = db.query(WorkLog).filter(
        WorkLog.user_id == user_id
    ).order_by(WorkLog.performed_at.desc()).first()
    
    if not last_work:
        return True, "No previous work found, can work immediately"
    
    now = datetime.now(UTC)
    if last_work.cooldown_until.replace(tzinfo=UTC) <= now:
        return True, "Cooldown period has expired, can work now"
    
    time_remaining = last_work.cooldown_until.replace(tzinfo=UTC) - now
    minutes_remaining = time_remaining.total_seconds() / 60.0
    return False, f"Must wait {minutes_remaining:.1f} minutes before working again"


def perform_work(db: Session, user_id: int) -> Tuple[Optional[Dict], str]:
    """
    Perform work for a user and update their currency.
    
    Args:
        db: Database session
        user_id: User ID performing work
        
    Returns:
        Tuple of (work_result: Dict or None, message: str)
    """
    # Check if user can work
    can_work, message = can_user_work(db, user_id)
    if not can_work:
        return None, message
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None, "User not found"
    
    # Get rank bonus
    rank_bonus = db.query(RankBonus).filter(RankBonus.rank == user.rank).first()
    if not rank_bonus:
        return None, "Rank bonus configuration not found"
    
    # Get work type for this rank (no selection needed, one per rank)
    work_type = get_work_type_for_rank(user.rank)
    
    # Calculate income with variance
    base_income = rank_bonus.work_income
    income_earned = calculate_work_income_with_variance(base_income)
    
    # Calculate cooldown
    now = datetime.now(UTC)
    cooldown_until = now + timedelta(minutes=rank_bonus.work_cooldown_minutes)
    
    # Update user currency
    user.currency_value += income_earned
    
    # Create work log entry
    work_log = WorkLog(
        user_id=user_id,
        work_type=work_type,
        income_earned=income_earned,
        performed_at=now,
        rank_at_time=user.rank,
        cooldown_until=cooldown_until
    )
    
    db.add(work_log)
    db.commit()
    db.refresh(work_log)
    db.refresh(user)
    
    return {
        "success": True,
        "income_earned": income_earned,
        "work_type": work_type,
        "new_currency_balance": user.currency_value,
        "cooldown_until": cooldown_until,
        "next_available_in_minutes": rank_bonus.work_cooldown_minutes
    }, "Work completed successfully"


def get_user_work_history(db: Session, user_id: int, limit: int = 20) -> Optional[Dict]:
    """
    Get work history for a user.
    
    Args:
        db: Database session
        user_id: User ID
        limit: Maximum number of entries to return
        
    Returns:
        Dictionary with work history information or None if user not found
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    
    # Get work history
    work_entries = db.query(WorkLog).filter(
        WorkLog.user_id == user_id
    ).order_by(WorkLog.performed_at.desc()).limit(limit).all()
    
    # Calculate statistics
    total_work_sessions = db.query(WorkLog).filter(WorkLog.user_id == user_id).count()
    total_income = db.query(WorkLog).filter(WorkLog.user_id == user_id).with_entities(
        func.sum(WorkLog.income_earned)
    ).scalar() or 0
    
    average_income = total_income / total_work_sessions if total_work_sessions > 0 else 0
    
    # Format work entries
    formatted_entries = []
    for entry in work_entries:
        formatted_entries.append({
            "id": entry.id,
            "work_type": entry.work_type,
            "income_earned": entry.income_earned,
            "performed_at": entry.performed_at,
            "rank_at_time": entry.rank_at_time.value
        })
    
    return {
        "total_work_sessions": total_work_sessions,
        "total_income_earned": total_income,
        "work_history": formatted_entries,
        "average_income_per_session": round(average_income, 2)
    }


def get_available_work_types_for_user(db: Session, user_id: int) -> Optional[Dict]:
    """
    Get available work types and information for a user.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        Dictionary with available work types information or None if user not found
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    
    rank_bonus = db.query(RankBonus).filter(RankBonus.rank == user.rank).first()
    if not rank_bonus:
        return None
    
    work_type = get_work_type_for_rank(user.rank)
    min_income, max_income = get_work_income_range_for_rank(user.rank, rank_bonus.work_income)
    
    return {
        "user_rank": user.rank.value,
        "work_type": work_type,
        "estimated_income_range": {"min": min_income, "max": max_income},
        "cooldown_minutes": rank_bonus.work_cooldown_minutes
    }
