from sqlalchemy import Column, Integer, Float, String
from app.database.create_database import Base

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
    including their nickname, rank, and currency value.
    Attributes:
    user_id (int): Unique identifier of the user. Primary key.
    nickname (str): Unique nickname of the user. Required.
    rank_elo (float): Elo rating of the user, representing their skill level. Default: 1000.
    currency_value (float): Amount of in-game currency the user has. Default: 1500.
    """

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nickname = Column(String, unique=True, nullable=False)
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