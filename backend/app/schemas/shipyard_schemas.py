from pydantic import BaseModel
from typing import List, Optional

class ShipRepairResponse(BaseModel):
    """
    Response model for shipyard repair endpoint.

    Attributes:
        success (bool): Indicates if the repair was successful.
        message (str): Informational message about the repair result.
        ship_number (int): Unique identifier of the repaired ship instance.
        user_id (int): ID of the user who owns the ship.
        ship_id (int): Type ID of the repaired ship.
    """
    success: bool
    message: str
    ship_number: int
    user_id: int
    ship_id: int

class ShipCooldownStatus(BaseModel):
    """
    Cooldown status for a specific ship.
    
    Attributes:
        ship_number (int): Unique identifier of the ship instance.
        can_repair (bool): Whether the ship can be repaired now.
        cooldown_seconds (int): Remaining cooldown time in seconds (0 if can repair).
        needs_repair (bool): Whether the ship actually needs repair.
    """
    ship_number: int
    can_repair: bool
    cooldown_seconds: int
    needs_repair: bool

class ShipyardStatusResponse(BaseModel):
    """
    Response model for shipyard status endpoint.
    
    Attributes:
        ships (List[ShipCooldownStatus]): List of ships with their cooldown status.
        total_ships (int): Total number of ships owned by the user.
        ships_needing_repair (int): Number of ships that need repair.
        ships_in_cooldown (int): Number of ships currently in cooldown.
    """
    ships: List[ShipCooldownStatus]
    total_ships: int
    ships_needing_repair: int
    ships_in_cooldown: int
