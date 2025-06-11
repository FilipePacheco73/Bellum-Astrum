from sqlalchemy import Column, Integer, Float, String, DateTime, JSON
from app.database.create_database import Base
from datetime import datetime

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

    ship_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ship_name = Column(String, unique=True, nullable=False)
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
    """
    Class representing the 'users' table in the database.
    This class is mapped to store information about users in the game,
    including their nickname, rank, currency value, and battle statistics.
    Attributes:
    user_id (int): Unique identifier of the user. Primary key.
    nickname (str): Unique nickname of the user. Required.
    rank_elo (float): Elo rating of the user, representing their skill level. Default: 1000.
    currency_value (float): Amount of in-game currency the user has. Default: 1500.
    victories (int): Number of victories. Default: 0.
    defeats (int): Number of defeats. Default: 0.
    damage_dealt (float): Total damage dealt by the user. Default: 0.
    damage_taken (float): Total damage taken by the user. Default: 0.
    ships_destroyed_by_user (int): Number of ships destroyed by the user. Default: 0.
    ships_lost_by_user (int): Number of ships lost by the user. Default: 0.
    """

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nickname = Column(String, unique=True, nullable=False)
    rank_elo = Column(Float, default=1000)
    currency_value = Column(Float, default=1500)
    victories = Column(Integer, default=0)
    defeats = Column(Integer, default=0)
    damage_dealt = Column(Float, default=0)
    damage_taken = Column(Float, default=0)
    ships_destroyed_by_user = Column(Integer, default=0)
    ships_lost_by_user = Column(Integer, default=0)

    def __repr__(self) -> str:
        """
        Textual representation of the user, useful for debugging and logging.

        Returns:
        str: String containing the main attributes of the user.
        """
        return f"<User(user_id={self.user_id}, nickname={self.nickname}, rank_elo={self.rank_elo}, currency_value={self.currency_value}, victories={self.victories}, defeats={self.defeats}, damage_dealt={self.damage_dealt}, damage_taken={self.damage_taken}, ships_destroyed_by_user={self.ships_destroyed_by_user}, ships_lost_by_user={self.ships_lost_by_user})>"
        
class OwnedShips(Base):
    """
    Class representing the 'owned_ships' table in the database.
    This class is mapped to store information about ships owned by users,
    including the user ID, ship ID, and ship name.
    Attributes:
    ship_number (int): Unique identifier for the owned ship. Primary key.
    user_id (str): Unique identifier of the user who owns the ship. Foreign key to 'users'. 
    ship_id (str): Unique identifier of the ship. Foreign key to 'ships'.
    ship_name (str): Name of the ship owned by the user.
    attack (float): Attack power of the ship.
    shield (float): Defensive capability of the ship (shield).
    evasion (float): Evasion capability of the ship.
    fire_rate (float): Firing speed.
    hp (float): Hit points (maximum health).
    value (int): Monetary or strategic value of the ship.
    """

    __tablename__ = 'owned_ships'

    ship_number = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String)
    status = Column(String, default='owned')
    ship_id = Column(String)
    ship_name = Column(String)
    attack = Column(Float)
    shield = Column(Float)
    evasion = Column(Float)
    fire_rate = Column(Float)
    hp = Column(Float)
    value = Column(Integer)
    
    def __repr__(self) -> str:
        """
        Textual representation of the ship, useful for debugging and logging.

        Returns:
        str: String containing the main attributes of the ship.
        """
        return f"""<OwnedShips(ship_number={self.ship_number}"""
    
class BattleHistory(Base):
    """
    Class representing the 'battle_history' table in the database.
    Stores information about each battle, including participants, ship stats, and battle details.
    """
    __tablename__ = 'battle_history'

    battle_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    winner_user_id = Column(Integer, nullable=True)
    participants = Column(JSON, nullable=False)  # List of participants and their ships (as dict)
    battle_log = Column(JSON, nullable=True)     # List of battle events/texts
    extra = Column(JSON, nullable=True)          # Flexible field for other data (e.g. total damage, rounds, etc.)

    def __repr__(self) -> str:
        return f"<BattleHistory(battle_id={self.battle_id}, timestamp={self.timestamp}, winner_user_id={self.winner_user_id})>"