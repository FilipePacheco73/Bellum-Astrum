from pydantic import BaseModel, ConfigDict
from typing import Optional

class ShipBase(BaseModel):
    """
    Base model for Ship, defining common ship attributes.

    Attributes:
        ship_name (str): Name of the ship.
        attack (float, optional): Attack power. Default is 10.
        shield (float, optional): Shield strength. Default is 5.
        evasion (float, optional): Evasion capability. Default is 0.
        fire_rate (float, optional): Weapon fire rate. Default is 1.
        hp (float, optional): Health points. Default is 100.
        value (int, optional): Monetary or strategic value. Default is 1000.
    """
    ship_name: str
    attack: Optional[float] = 10
    shield: Optional[float] = 5
    evasion: Optional[float] = 0
    fire_rate: Optional[float] = 1
    hp: Optional[float] = 100
    value: Optional[int] = 1000

class ShipCreate(ShipBase):
    """
    Model for creating a new ship.
    Inherits all attributes from ShipBase.
    """
    pass

class ShipResponse(ShipBase):
    """
    Response model for ship data returned by the API.

    Attributes:
        ship_id (int): Unique ship identifier.
    """
    ship_id: int
    model_config = ConfigDict(from_attributes=True)

class OwnedShipResponse(BaseModel):
    """
    Response model for owned ships, containing details about the ship owned by a user.

    Attributes:
        ship_number (int): Unique identifier for the owned ship.
        user_id (int): Unique identifier of the user who owns the ship.
        status (str): Status of the ship (e.g., 'owned', 'active').
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
    user_id: int
    status: str
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
        ship_name (Optional[str]): Ship name (if available).
    """
    ship_number: int
    user_id: int
    status: str
    ship_name: Optional[str]
    model_config = ConfigDict(from_attributes=True)
