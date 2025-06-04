'''
SQL Alchemy Models: Ship, Fleets tables
'''

from sqlalchemy import Column, Integer, Float, String
from create_database import Base # Import database from database.py

class Ship(Base):
    """
    Class representing the 'ships' table in the database.

    This class is mapped to store information about spaceships,
    including combat characteristics, endurance, and value.

    Attributes:
    id (int): Unique identifier of the ship. Primary key.
    name (str): Name of the ship. Required.
    attack (float): Attack power of the ship. Default: 10.
    shield (float): Defensive capability of the ship (shield). Default: 5.
    evasion (float): Evasion capability of the ship. Default: 0.
    fire_rate (float): Firing speed. Default: 1.
    hp (float): Hit points (maximum health). Default: 100.
    value (int): Monetary or strategic value of the ship. Default: 1000.
    """

    __tablename__ = 'ships'

    ship_id = Column(Integer, primary_key=True, index=True)
    ship_name = Column(String, nullable=False)
    attack = Column(Float, default=10)
    shield = Column(Float, default=5)
    evasion = Column(Float, default=0)
    fire_rate = Column(Float, default=1)
    hp = Column(Float, default=100)
    value = Column(Integer, default = 1000)

    def __repr__(self) -> str:
        """
        Textual representation of the ship, useful for debugging and logging.

        Returns:
        str: String containing the main attributes of the ship.
        """
        return f"""<Ship(name={self.ship_name}, attack={self.attack}, shield={self.shield}, evasion={self.evasion}, fire_rate={self.fire_rate}, hp={self.hp}, value={self.value}"""
    
class User(Base):

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, nullable=False)
    rank_elo = Column(Float, default=1000)
    currency_value = Column(Float, default=1500)

    def __repr__(self) -> str:
        """
        Textual representation of the ship, useful for debugging and logging.

        Returns:
        str: String containing the main attributes of the ship.
        """
        return f"""<User(name={self.nickname}, rank_elo={self.rank_elo}, currency_value={self.currency_value}"""
    
class OwnedShips(Base):

    __tablename__ = 'owned_ships'

    ship_number = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    ship_id = Column(String)
    ship_name = Column(String)
    
    def __repr__(self) -> str:
        """
        Textual representation of the ship, useful for debugging and logging.

        Returns:
        str: String containing the main attributes of the ship.
        """
        return f"""<OwnedShips(ship_number={self.ship_number}"""