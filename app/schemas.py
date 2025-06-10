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
        from_attributes = True

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
        from_attributes = True

class MarketBuyRequest(BaseModel):
    user_id: int
    ship_id: int

class MarketBuyResponse(BaseModel):
    message: str

class MarketSellRequest(BaseModel):
    user_id: int
    owned_ship_number: int

class MarketSellResponse(BaseModel):
    message: str
    value_received: int

class OwnedShipResponse(BaseModel):
    ship_number: int
    user_id: str
    status: str
    ship_id: str
    ship_name: str
    attack: float
    shield: float
    evasion: float
    fire_rate: float
    hp: float
    value: int

    class Config:
        from_attributes = True

class SeedShipsResponse(BaseModel):
    message: str
    ships_seeded: int

    class Config:
        schema_extra = {
            "example": {
                "message": "Ships seeded successfully.",
                "ships_seeded": 5
            }
        }

class SeedUsersResponse(BaseModel):
    message: str
    users_seeded: int

    class Config:
        schema_extra = {
            "example": {
                "message": "Users seeded successfully.",
                "users_seeded": 3
            }
        }