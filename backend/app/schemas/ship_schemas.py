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
