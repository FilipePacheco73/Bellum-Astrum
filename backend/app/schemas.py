from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

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
    model_config = ConfigDict(from_attributes=True)

# Pydantic models for User
class UserBase(BaseModel):
    """
    Base model for User, defining the common attributes.
    Attributes:
    nickname (str): Unique nickname of the user. Required.
    elo_rank (float): Elo rating of the user, representing their skill level. Default: 1000.
    currency_value (int): Amount of in-game currency the user has. Default: 2000.
    victories (int): Number of victories. Default: 0.
    defeats (int): Number of defeats. Default: 0.
    damage_dealt (float): Total damage dealt by the user. Default: 0.
    damage_taken (float): Total damage taken by the user. Default: 0.
    ships_destroyed_by_user (int): Number of ships destroyed by the user. Default: 0.
    ships_lost_by_user (int): Number of ships lost by the user. Default: 0.
    """
    nickname: str
    elo_rank: Optional[float] = 1000
    currency_value: Optional[int] = 2000
    victories: Optional[int] = 0
    defeats: Optional[int] = 0
    damage_dealt: Optional[float] = 0
    damage_taken: Optional[float] = 0
    ships_destroyed_by_user: Optional[int] = 0
    ships_lost_by_user: Optional[int] = 0

class UserCreate(BaseModel):
    nickname: str
    email: EmailStr
    password: str
    elo_rank: Optional[float] = 1000
    currency_value: Optional[int] = 2000
    victories: Optional[int] = 0
    defeats: Optional[int] = 0
    damage_dealt: Optional[float] = 0
    damage_taken: Optional[float] = 0
    ships_destroyed_by_user: Optional[int] = 0
    ships_lost_by_user: Optional[int] = 0

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: int
    nickname: str
    email: EmailStr
    elo_rank: float
    currency_value: int
    victories: int
    defeats: int
    damage_dealt: float
    damage_taken: float
    ships_destroyed_by_user: int
    ships_lost_by_user: int
    model_config = ConfigDict(from_attributes=True)

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

class BattleParticipant(BaseModel):
    user_id: int
    nickname: str
    ship_number: int
    ship_name: str
    attack: float
    shield: float
    evasion: float
    fire_rate: float
    hp: float
    value: int

class BattleHistoryResponse(BaseModel):
    battle_id: int
    timestamp: datetime
    participants: List[BattleParticipant]
    winner_user_id: Optional[int]
    battle_log: List[str]
    extra: Optional[Dict[str, Any]]
    model_config = ConfigDict(from_attributes=True)

class ActivateShipRequest(BaseModel):
    user_id: int
    ship_number: int

class ActivateShipResponse(BaseModel):
    ship_number: int
    user_id: int
    status: str
    ship_id: Optional[int]
    ship_name: Optional[str]
    model_config = ConfigDict(from_attributes=True)

# Log Schemas
class SystemLogBase(BaseModel):
    log_level: str
    log_category: str
    action: str
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    resource_affected: Optional[str] = None
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[int] = None

class SystemLogCreate(SystemLogBase):
    user_id: Optional[int] = None

class SystemLogResponse(SystemLogBase):
    log_id: int
    timestamp: datetime
    user_id: Optional[int]
    model_config = ConfigDict(from_attributes=True)

class LogQueryRequest(BaseModel):
    user_id: Optional[int] = None
    log_level: Optional[str] = None
    log_category: Optional[str] = None
    action: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 100
    offset: int = 0

class LogQueryResponse(BaseModel):
    logs: List[SystemLogResponse]
    total_count: int
    page: int
    per_page: int