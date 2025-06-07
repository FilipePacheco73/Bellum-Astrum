from pydantic import BaseModel
from typing import Optional

# Pydantic models for Ship
class ShipBase(BaseModel):
    """
    Base model for Ship, defining the common attributes.
    Attributes:
    ship_name (str): Name of the ship. Required.
    attack (float): Attack power of the ship. Default: 10.
    shield (float): Shield strength of the ship. Default: 5.
    evasion (float): Evasion capability of the ship. Default: 0.
    fire_rate (float): Rate of fire of the ship's weapons. Default: 1.
    hp (float): Health points of the ship. Default: 100.
    value (int): Monetary or strategic value of the ship. Default: 1000.
    """
    ship_name: str
    attack: Optional[float] = 10
    shield: Optional[float] = 5
    evasion: Optional[float] = 0
    fire_rate: Optional[float] = 1
    hp: Optional[float] = 100
    value: Optional[int] = 1000

class ShipCreate(ShipBase):
    pass

class ShipResponse(ShipBase):
    ship_id: int

    class Config:
        orm_mode = True

# Pydantic models for User
class UserBase(BaseModel):
    """
    Base model for User, defining the common attributes.
    Attributes:
    nickname (str): Unique nickname of the user. Required.
    rank_elo (float): Elo rating of the user, representing their skill level. Default: 1000.
    currency_value (float): Amount of in-game currency the user has. Default: 1500.
    """
    nickname: str
    rank_elo: Optional[float] = 1000
    currency_value: Optional[float] = 1500

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    user_id: int

    class Config:
        orm_mode = True