from pydantic import BaseModel
from typing import Optional

# Pydantic models for Ship
class ShipBase(BaseModel):
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
    nickname: str
    rank_elo: Optional[float] = 1000
    currency_value: Optional[float] = 1500

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    user_id: int

    class Config:
        orm_mode = True
