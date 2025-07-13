"""
Pydantic schemas for work-related API endpoints.

This module contains request and response models for the work system,
including work performance, status checks, and work history.
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from database.models import UserRank


class WorkPerformResponse(BaseModel):
    """
    Response model for work performance.
    
    Attributes:
        success (bool): Whether the work was performed successfully
        income_earned (int): Amount of currency earned from the work
        work_type (str): Type of work that was performed
        new_currency_balance (int): User's currency balance after the work
        cooldown_until (datetime): When the user can work again
        next_available_in_hours (float): Hours until next work is available
    """
    success: bool
    income_earned: int
    work_type: str
    new_currency_balance: int
    cooldown_until: datetime
    next_available_in_hours: float
    model_config = ConfigDict(from_attributes=True)


class WorkStatusResponse(BaseModel):
    """
    Response model for work status check.
    
    Attributes:
        can_work (bool): Whether the user can currently perform work
        time_until_available (float): Hours until work becomes available (0 if available now)
        last_work_performed (datetime, optional): When the user last performed work
        estimated_income (int): Estimated income for next work based on current rank
        work_type (str): Type of work available for user's rank
    """
    can_work: bool
    time_until_available: float
    last_work_performed: Optional[datetime]
    estimated_income: int
    work_type: str
    current_rank: str
    work_cooldown_hours: int
    model_config = ConfigDict(from_attributes=True)


class WorkHistoryEntry(BaseModel):
    """
    Single work history entry.
    
    Attributes:
        id (int): Work log entry ID
        work_type (str): Type of work performed
        income_earned (int): Currency earned from this work
        performed_at (datetime): When the work was performed
        rank_at_time (str): User's rank when the work was performed
    """
    id: int
    work_type: str
    income_earned: int
    performed_at: datetime
    rank_at_time: str
    model_config = ConfigDict(from_attributes=True)


class WorkHistoryResponse(BaseModel):
    """
    Response model for work history.
    
    Attributes:
        total_work_sessions (int): Total number of work sessions performed
        total_income_earned (int): Total currency earned from all work
        work_history (List[WorkHistoryEntry]): List of recent work entries
        average_income_per_session (float): Average income per work session
    """
    total_work_sessions: int
    total_income_earned: int
    work_history: List[WorkHistoryEntry]
    average_income_per_session: float
    model_config = ConfigDict(from_attributes=True)


class AvailableWorkTypesResponse(BaseModel):
    """
    Response model for available work type based on user rank.
    
    Attributes:
        user_rank (str): User's current rank
        work_type (str): Work type available for this rank
        estimated_income_range (dict): Min and max income range for this rank
        cooldown_hours (int): Hours between work sessions for this rank
    """
    user_rank: str
    work_type: str
    estimated_income_range: dict
    cooldown_hours: int
    model_config = ConfigDict(from_attributes=True)
