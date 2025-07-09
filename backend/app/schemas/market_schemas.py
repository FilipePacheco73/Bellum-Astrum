from pydantic import BaseModel
from typing import Optional

class MarketBuyRequest(BaseModel):
    """
    Model for a request to buy a ship from the market.

    Attributes:
        user_id (int): ID of the user making the purchase.
        ship_id (int): ID of the ship to buy.
    """
    user_id: int
    ship_id: int

class MarketBuyResponse(BaseModel):
    """
    Response model for a successful ship purchase.

    Attributes:
        message (str): Success message.
    """
    message: str

class MarketSellRequest(BaseModel):
    """
    Model for a request to sell an owned ship in the market.

    Attributes:
        user_id (int): ID of the user selling the ship.
        owned_ship_number (int): Unique number of the owned ship.
    """
    user_id: int
    owned_ship_number: int

class MarketSellResponse(BaseModel):
    """
    Response model for a successful ship sale.

    Attributes:
        message (str): Success message.
        value_received (int): Value received from the sale.
    """
    message: str
    value_received: int
