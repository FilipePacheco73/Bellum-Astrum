"""
Utility functions for the work system.

This module contains helper functions for determining work types,
calculating income, managing cooldowns, and other work-related operations.
"""

from database.models import UserRank
from typing import List, Dict, Tuple
import random


def get_work_type_for_rank(rank: UserRank) -> str:
    """
    Get the work type for a specific rank.
    
    Args:
        rank: User's current rank
        
    Returns:
        String representing the work type for this rank
    """
    work_mapping = {
        UserRank.RECRUIT: "maintenance",
        UserRank.ENSIGN: "patrol",
        UserRank.LIEUTENANT: "trading",
        UserRank.LIEUTENANT_COMMANDER: "escort",
        UserRank.COMMANDER: "reconnaissance",
        UserRank.CAPTAIN: "command",
        UserRank.COMMODORE: "command",
        UserRank.REAR_ADMIRAL: "strategy",
        UserRank.VICE_ADMIRAL: "strategy",
        UserRank.ADMIRAL: "strategy",
        UserRank.FLEET_ADMIRAL: "strategy"
    }
    
    return work_mapping.get(rank, "maintenance")


def get_work_description(work_type: str) -> Dict[str, str]:
    """
    Get description and narrative for a specific work type.
    
    Args:
        work_type: The type of work
        
    Returns:
        Dictionary with description and success message for the work type
    """
    descriptions = {
        "maintenance": {
            "description": "Perform routine maintenance on space stations and ships",
            "success_message": "Completed essential maintenance tasks efficiently"
        },
        "patrol": {
            "description": "Conduct security patrols in assigned sectors",
            "success_message": "Patrol completed successfully, sector secured"
        },
        "trading": {
            "description": "Facilitate trade negotiations and cargo transport",
            "success_message": "Trade missions completed with excellent profit margins"
        },
        "escort": {
            "description": "Provide protection for important convoys and dignitaries",
            "success_message": "Escort mission accomplished without incidents"
        },
        "reconnaissance": {
            "description": "Gather intelligence and survey unknown territories",
            "success_message": "Valuable intelligence gathered from reconnaissance mission"
        },
        "command": {
            "description": "Lead tactical operations and coordinate fleet movements",
            "success_message": "Command operations executed with strategic precision"
        },
        "strategy": {
            "description": "Develop long-term strategic plans for galactic operations",
            "success_message": "Strategic analysis completed with comprehensive recommendations"
        }
    }
    
    return descriptions.get(work_type, {
        "description": "Perform assigned duties",
        "success_message": "Work completed successfully"
    })


def get_work_descriptions() -> Dict[str, Dict[str, str]]:
    """
    Get descriptions and narratives for different work types.
    
    Returns:
        Dictionary mapping work types to their descriptions and success messages
    """
    return {
        "maintenance": {
            "description": "Perform routine maintenance on space stations and ships",
            "success_message": "Completed essential maintenance tasks efficiently"
        },
        "patrol": {
            "description": "Conduct security patrols in assigned sectors",
            "success_message": "Patrol completed successfully, sector secured"
        },
        "trading": {
            "description": "Facilitate trade negotiations and cargo transport",
            "success_message": "Trade missions completed with excellent profit margins"
        },
        "escort": {
            "description": "Provide protection for important convoys and dignitaries",
            "success_message": "Escort mission accomplished without incidents"
        },
        "reconnaissance": {
            "description": "Gather intelligence and survey unknown territories",
            "success_message": "Valuable intelligence gathered from reconnaissance mission"
        },
        "command": {
            "description": "Lead tactical operations and coordinate fleet movements",
            "success_message": "Command operations executed with strategic precision"
        },
        "strategy": {
            "description": "Develop long-term strategic plans for galactic operations",
            "success_message": "Strategic analysis completed with comprehensive recommendations"
        }
    }


def calculate_work_income_with_variance(base_income: int, variance_percent: float = 20.0) -> int:
    """
    Calculate work income with random variance.
    
    Args:
        base_income: Base income amount from rank bonus
        variance_percent: Percentage variance to apply (default 20%)
        
    Returns:
        Final income amount with variance applied
    """
    variance = base_income * (variance_percent / 100.0)
    min_income = int(base_income - variance)
    max_income = int(base_income + variance)
    
    return random.randint(min_income, max_income)


def get_work_income_range_for_rank(rank: UserRank, base_income: int) -> Tuple[int, int]:
    """
    Get the income range for a specific rank.
    
    Args:
        rank: User's current rank
        base_income: Base income from rank bonus
        
    Returns:
        Tuple of (min_income, max_income)
    """
    variance = base_income * 0.2  # 20% variance
    min_income = int(base_income - variance)
    max_income = int(base_income + variance)
    
    return (min_income, max_income)


def format_work_success_message(work_type: str, income_earned: int, rank: UserRank) -> str:
    """
    Format a success message for completed work.
    
    Args:
        work_type: Type of work performed
        income_earned: Amount of currency earned
        rank: User's rank
        
    Returns:
        Formatted success message string
    """
    description = get_work_description(work_type)
    base_message = description.get("success_message", "Work completed successfully")
    
    return f"{base_message}. Earned {income_earned:,} credits as a {rank.value}."
