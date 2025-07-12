from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

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
    currency_value: Optional[int] = 2000
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
    model_config = ConfigDict(from_attributes=True)
