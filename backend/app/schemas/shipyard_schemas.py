from pydantic import BaseModel

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
