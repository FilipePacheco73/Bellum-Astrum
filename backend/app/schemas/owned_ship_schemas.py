from pydantic import BaseModel, ConfigDict
from typing import Optional

class OwnedShipResponse(BaseModel):
    """
    Response model for owned ships, containing details about the ship owned by a user.

    Attributes:
        ship_number (int): Unique identifier for the owned ship.
        user_id (str): Unique identifier of the user who owns the ship.
        status (str): Status of the ship (e.g., 'owned', 'active').
        ship_id (str): Unique identifier of the ship.
        ship_name (str): Name of the ship owned by the user.
        base_attack (float): Base attack power of the ship.
        base_shield (float): Base shield strength of the ship.
        base_evasion (float): Base evasion capability of the ship.
        base_fire_rate (float): Base rate of fire of the ship's weapons.
        base_hp (float): Base health points of the ship.
        base_value (int): Base monetary or strategic value of the ship.
        actual_attack (float): Actual attack power of the ship after any modifications.
        actual_shield (float): Actual shield strength of the ship after any modifications.
        actual_evasion (float): Actual evasion capability of the ship after any modifications.
        actual_fire_rate (float): Actual rate of fire of the ship's weapons after any modifications.
        actual_hp (float): Actual health points of the ship after any modifications.
        actual_value (int): Actual monetary or strategic value of the ship after any modifications.
    """
    ship_number: int
    user_id: str
    status: str
    ship_id: str
    ship_name: str
    base_attack: float
    base_shield: float
    base_evasion: float
    base_fire_rate: float
    base_hp: float
    base_value: int
    actual_attack: float
    actual_shield: float
    actual_evasion: float
    actual_fire_rate: float
    actual_hp: float
    actual_value: int
    model_config = ConfigDict(from_attributes=True)

class ActivateShipRequest(BaseModel):
    """
    Model for a request to activate a ship for a user.

    Attributes:
        user_id (int): ID of the user.
        ship_number (int): Number of the ship to activate.
    """
    user_id: int
    ship_number: int

class ActivateShipResponse(BaseModel):
    """
    Response model for ship activation.

    Attributes:
        ship_number (int): Number of the activated ship.
        user_id (int): ID of the user.
        status (str): Status after activation.
        ship_id (Optional[int]): Ship ID (if available).
        ship_name (Optional[str]): Ship name (if available).
    """
    ship_number: int
    user_id: int
    status: str
    ship_id: Optional[int]
    ship_name: Optional[str]
    model_config = ConfigDict(from_attributes=True)
