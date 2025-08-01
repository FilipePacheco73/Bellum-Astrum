from pydantic import BaseModel, EmailStr, ConfigDict, field_serializer, field_validator
from typing import Optional, Any

class UserBase(BaseModel):
    """
    Base model for User, defining common user attributes.

    Attributes:
        nickname (str): Unique nickname of the user.
        elo_rank (float, optional): Elo rating representing user skill. Default is 1000.
        currency_value (int, optional): In-game currency amount. Default is 2000.
        victories (int, optional): Number of victories. Default is 0.
        defeats (int, optional): Number of defeats. Default is 0.
        damage_dealt (float, optional): Total damage dealt. Default is 0.
        damage_taken (float, optional): Total damage taken. Default is 0.
        ships_destroyed_by_user (int, optional): Ships destroyed by the user. Default is 0.
        ships_lost_by_user (int, optional): Ships lost by the user. Default is 0.
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
    """
    Model for creating a new user.

    Attributes:
        nickname (str): Unique nickname of the user.
        email (EmailStr): Email address of the user.
        password (str): User password (plain text, will be hashed).
        elo_rank (float, optional): Elo rating. Default is 1000.
        currency_value (int, optional): In-game currency. Default is 2000.
        victories (int, optional): Number of victories. Default is 0.
        defeats (int, optional): Number of defeats. Default is 0.
        damage_dealt (float, optional): Total damage dealt. Default is 0.
        damage_taken (float, optional): Total damage taken. Default is 0.
        ships_destroyed_by_user (int, optional): Ships destroyed. Default is 0.
        ships_lost_by_user (int, optional): Ships lost. Default is 0.
    """
    nickname: str
    email: EmailStr
    password: str
    elo_rank: Optional[float] = 1000
    currency_value: Optional[int] = 20000
    victories: Optional[int] = 0
    defeats: Optional[int] = 0
    damage_dealt: Optional[float] = 0
    damage_taken: Optional[float] = 0
    ships_destroyed_by_user: Optional[int] = 0
    ships_lost_by_user: Optional[int] = 0

class UserLogin(BaseModel):
    """
    Model for user login credentials.

    Attributes:
        email (EmailStr): User email address.
        password (str): User password.
    """
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """
    Response model for user data returned by the API.

    Attributes:
        user_id (int): Unique user identifier.
        nickname (str): User nickname.
        email (EmailStr): User email address.
        elo_rank (float): User Elo rating.
        currency_value (int): In-game currency.
        victories (int): Number of victories.
        defeats (int): Number of defeats.
        damage_dealt (float): Total damage dealt.
        damage_taken (float): Total damage taken.
        ships_destroyed_by_user (int): Ships destroyed by the user.
        ships_lost_by_user (int): Ships lost by the user.
        experience (int): User experience points.
        level (int): User level.
        rank (Any): User rank.
    """
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
    experience: int
    level: int
    rank: Any
    default_formation: str
    
    @field_serializer('rank')
    def serialize_rank(self, rank: Any) -> str:
        """Convert UserRank enum to string value."""
        if hasattr(rank, 'value'):
            return rank.value
        return str(rank)
    
    model_config = ConfigDict(from_attributes=True)


class UpdateFormationRequest(BaseModel):
    """
    Request model for updating user's default formation.
    
    Attributes:
        default_formation (str): Formation strategy ("DEFENSIVE", "AGGRESSIVE", "TACTICAL")
    """
    default_formation: str
    
    @field_validator('default_formation')
    @classmethod
    def validate_formation(cls, v: str) -> str:
        """Validate formation is one of the allowed values."""
        allowed_formations = ["DEFENSIVE", "AGGRESSIVE", "TACTICAL"]
        if v.upper() not in allowed_formations:
            raise ValueError(f"Formation must be one of: {', '.join(allowed_formations)}")
        return v.upper()


class UserShipLimitsResponse(BaseModel):
    """
    Response model for user ship limits information.
    
    Provides information about a user's ship activation limits
    based on their rank and current usage.
    
    Attributes:
        user_rank (str): Current user rank name
        user_level (int): Current user level
        max_active_ships (int): Maximum ships allowed to be active
        current_active_ships (int): Number of currently active ships
        can_activate_more (bool): Whether user can activate more ships
        slots_remaining (int): Number of remaining activation slots
    """
    user_rank: str
    user_level: int
    max_active_ships: int
    current_active_ships: int
    can_activate_more: bool
    slots_remaining: int
    model_config = ConfigDict(from_attributes=True)
