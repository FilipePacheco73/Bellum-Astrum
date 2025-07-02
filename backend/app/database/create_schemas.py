from sqlalchemy import Column, Integer, Float, String, DateTime, JSON, ForeignKey, Index, CheckConstraint
from backend.app.database.create_database import Base
from datetime import datetime, UTC

def utc_now():
    """Helper function to return current UTC datetime for SQLAlchemy defaults"""
    return datetime.now(UTC)

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
    ship_name = Column(String(100), unique=True, nullable=False)
    attack = Column(Float, default=10, nullable=False)
    shield = Column(Float, default=5, nullable=False)
    evasion = Column(Float, default=0, nullable=False)
    fire_rate = Column(Float, default=1, nullable=False)
    hp = Column(Float, default=100, nullable=False)
    value = Column(Integer, default=1000, nullable=False)

    # Constraints para garantir valores válidos
    __table_args__ = (
        CheckConstraint('attack >= 0', name='check_attack_positive'),
        CheckConstraint('shield >= 0', name='check_shield_positive'),
        CheckConstraint('evasion >= 0 AND evasion <= 1', name='check_evasion_range'),
        CheckConstraint('fire_rate > 0', name='check_fire_rate_positive'),
        CheckConstraint('hp > 0', name='check_hp_positive'),
        CheckConstraint('value >= 0', name='check_value_positive'),
        Index('idx_ship_name', 'ship_name'),
        Index('idx_ship_value', 'value'),
    )

    def __repr__(self) -> str:
        """
        Textual representation of the ship, useful for debugging and logging.

        Returns:
        str: String containing the main attributes of the ship.
        """
        return f"<Ship(ship_id={self.ship_id}, name={self.ship_name}, attack={self.attack}, shield={self.shield}, evasion={self.evasion}, fire_rate={self.fire_rate}, hp={self.hp}, value={self.value})>"
    
class User(Base):
    """
    Class representing the 'users' table in the database.
    This class is mapped to store information about users in the game,
    including their nickname, rank, currency value, and battle statistics.
    Attributes:
    user_id (int): Unique identifier of the user. Primary key.
    nickname (str): Unique nickname of the user. Required.
    email (str): Unique email of the user. Required.
    password_hash (str): Hash of the user's password. Required for authentication.
    elo_rank (float): Elo rating of the user, representing their skill level. Default: 1000.
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
    nickname = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    elo_rank = Column(Float, default=1000, nullable=False)
    currency_value = Column(Float, default=1500, nullable=False)
    victories = Column(Integer, default=0, nullable=False)
    defeats = Column(Integer, default=0, nullable=False)
    damage_dealt = Column(Float, default=0, nullable=False)
    damage_taken = Column(Float, default=0, nullable=False)
    ships_destroyed_by_user = Column(Integer, default=0, nullable=False)
    ships_lost_by_user = Column(Integer, default=0, nullable=False)

    # Constraints para garantir valores válidos
    __table_args__ = (
        CheckConstraint('elo_rank >= 0', name='check_elo_positive'),
        CheckConstraint('currency_value >= 0', name='check_currency_positive'),
        CheckConstraint('victories >= 0', name='check_victories_positive'),
        CheckConstraint('defeats >= 0', name='check_defeats_positive'),
        CheckConstraint('damage_dealt >= 0', name='check_damage_dealt_positive'),
        CheckConstraint('damage_taken >= 0', name='check_damage_taken_positive'),
        CheckConstraint('ships_destroyed_by_user >= 0', name='check_ships_destroyed_positive'),
        CheckConstraint('ships_lost_by_user >= 0', name='check_ships_lost_positive'),
        Index('idx_user_nickname', 'nickname'),
        Index('idx_user_email', 'email'),
        Index('idx_user_elo_rank', 'elo_rank'),
        Index('idx_user_currency', 'currency_value'),
    )

    def __repr__(self) -> str:
        """
        Textual representation of the user, useful for debugging and logging.

        Returns:
        str: String containing the main attributes of the user.
        """
        return f"<User(user_id={self.user_id}, nickname={self.nickname}, elo_rank={self.elo_rank}, currency_value={self.currency_value}, victories={self.victories}, defeats={self.defeats}, damage_dealt={self.damage_dealt}, damage_taken={self.damage_taken}, ships_destroyed_by_user={self.ships_destroyed_by_user}, ships_lost_by_user={self.ships_lost_by_user})>"
        
class OwnedShips(Base):
    """
    Class representing the 'owned_ships' table in the database.
    This class is mapped to store information about ships owned by users,
    including the user ID, ship ID, and ship name.
    Attributes:
    ship_number (int): Unique identifier for the owned ship. Primary key.
    user_id (int): Unique identifier of the user who owns the ship. Foreign key to 'users'. 
    ship_id (int): Unique identifier of the ship. Foreign key to 'ships'.
    ship_name (str): Name of the ship owned by the user.
    status (str): Status of the ship (e.g., 'owned', 'active', 'destroyed', 'upgrading', 'sold'). Default: 'owned'.
    base_attack (float): Base attack power of the ship. Default: 10.
    base_shield (float): Base shield power of the ship. Default: 5.
    base_evasion (float): Base evasion capability of the ship. Default: 0.
    base_fire_rate (float): Base firing rate of the ship. Default: 1.
    base_hp (float): Base hit points of the ship. Default: 100.
    base_value (int): Base value of the ship. Default: 1000.
    actual_attack (float): Actual attack power of the ship, which can be modified by upgrades or damage. Default: 10.
    actual_shield (float): Actual shield power of the ship, which can be modified by upgrades or damage. Default: 5.
    actual_evasion (float): Actual evasion capability of the ship, which can be modified by upgrades or damage. Default: 0.
    actual_fire_rate (float): Actual firing rate of the ship, which can be modified by upgrades or damage. Default: 1.  
    actual_hp (float): Actual hit points of the ship, which can be modified by upgrades or damage. Default: 100.
    actual_value (int): Actual value of the ship, which can be modified by upgrades or damage. Default: 1000.
    """

    __tablename__ = 'owned_ships'

    ship_number = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    ship_id = Column(Integer, ForeignKey('ships.ship_id'), nullable=False)
    status = Column(String(20), default='owned', nullable=False)
    ship_name = Column(String(100), nullable=False)
    base_attack = Column(Float, default=10, nullable=False)
    base_shield = Column(Float, default=5, nullable=False)
    base_evasion = Column(Float, default=0, nullable=False)
    base_fire_rate = Column(Float, default=1, nullable=False)
    base_hp = Column(Float, default=100, nullable=False)
    base_value = Column(Integer, default=1000, nullable=False)
    actual_attack = Column(Float, default=10, nullable=False)
    actual_shield = Column(Float, default=5, nullable=False)
    actual_evasion = Column(Float, default=0, nullable=False)
    actual_fire_rate = Column(Float, default=1, nullable=False)
    actual_hp = Column(Float, default=100, nullable=False)
    actual_value = Column(Integer, default=1000, nullable=False)
    
    # Constraints e índices
    __table_args__ = (
        CheckConstraint('base_attack >= 0', name='check_base_attack_positive'),
        CheckConstraint('base_shield >= 0', name='check_base_shield_positive'),
        CheckConstraint('base_evasion >= 0 AND base_evasion <= 1', name='check_base_evasion_range'),
        CheckConstraint('base_fire_rate > 0', name='check_base_fire_rate_positive'),
        CheckConstraint('base_hp > 0', name='check_base_hp_positive'),
        CheckConstraint('base_value >= 0', name='check_base_value_positive'),
        CheckConstraint('actual_attack >= 0', name='check_actual_attack_positive'),
        CheckConstraint('actual_shield >= 0', name='check_actual_shield_positive'),
        CheckConstraint('actual_evasion >= 0 AND actual_evasion <= 1', name='check_actual_evasion_range'),
        CheckConstraint('actual_fire_rate > 0', name='check_actual_fire_rate_positive'),
        CheckConstraint('actual_hp >= 0', name='check_actual_hp_positive'),
        CheckConstraint('actual_value >= 0', name='check_actual_value_positive'),
        CheckConstraint("status IN ('owned', 'active', 'destroyed', 'upgrading', 'sold')", name='check_status_valid'),
        Index('idx_owned_ships_user', 'user_id'),
        Index('idx_owned_ships_ship', 'ship_id'),
        Index('idx_owned_ships_status', 'status'),
        Index('idx_owned_ships_user_status', 'user_id', 'status'),
    )
    
    def __repr__(self) -> str:
        """
        Textual representation of the owned ship, useful for debugging and logging.

        Returns:
        str: String containing the main attributes of the owned ship.
        """
        return f"<OwnedShips(ship_number={self.ship_number}, user_id={self.user_id}, ship_id={self.ship_id}, ship_name={self.ship_name}, status={self.status})>"
    
class BattleHistory(Base):
    """
    Class representing the 'battle_history' table in the database.
    Stores information about each battle, including participants, ship stats, and battle details.
    """
    __tablename__ = 'battle_history'

    battle_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=utc_now, nullable=False)
    winner_user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    participants = Column(JSON, nullable=False)  # List of participants and their ships (as dict)
    battle_log = Column(JSON, nullable=True)     # List of battle events/texts
    extra = Column(JSON, nullable=True)          # Flexible field for other data (e.g. total damage, rounds, etc.)

    # Índices para melhorar performance de consultas
    __table_args__ = (
        Index('idx_battle_timestamp', 'timestamp'),
        Index('idx_battle_winner', 'winner_user_id'),
        Index('idx_battle_winner_timestamp', 'winner_user_id', 'timestamp'),
    )

    def __repr__(self) -> str:
        return f"<BattleHistory(battle_id={self.battle_id}, timestamp={self.timestamp}, winner_user_id={self.winner_user_id})>"

class SystemLogs(Base):
    """
    Class representing the 'system_logs' table in the database.
    Stores comprehensive logs for user activities, system events, and debugging.
    
    Attributes:
    log_id (int): Unique identifier for the log entry. Primary key.
    timestamp (datetime): When the event occurred. Default: current UTC time.
    user_id (int): ID of the user who performed the action (nullable for system events).
    log_level (str): Log level - 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
    log_category (str): Category of the log - 'USER_ACTION', 'SYSTEM', 'GAME_EVENT', 'SECURITY', 'PERFORMANCE'.
    action (str): Specific action performed (e.g., 'LOGIN', 'BUY_SHIP', 'BATTLE_START').
    details (JSON): Additional details about the event in JSON format.
    ip_address (str): IP address of the user (for security tracking).
    user_agent (str): User agent string (for security and analytics).
    session_id (str): Session identifier for tracking user sessions.
    resource_affected (str): Resource affected by the action (e.g., 'ship_id:123', 'user_id:456').
    old_value (JSON): Previous value before the change (for audit trails).
    new_value (JSON): New value after the change (for audit trails).
    error_message (str): Error message if the action failed.
    execution_time_ms (int): Time taken to execute the action in milliseconds.
    """

    __tablename__ = 'system_logs'

    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=utc_now, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    log_level = Column(String(10), nullable=False)
    log_category = Column(String(20), nullable=False)
    action = Column(String(50), nullable=False)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 can be up to 45 chars
    user_agent = Column(String(500), nullable=True)
    session_id = Column(String(255), nullable=True)
    resource_affected = Column(String(255), nullable=True)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    error_message = Column(String(1000), nullable=True)
    execution_time_ms = Column(Integer, nullable=True)

    # Constraints e índices para performance e integridade
    __table_args__ = (
        CheckConstraint("log_level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')", name='check_log_level_valid'),
        CheckConstraint("log_category IN ('USER_ACTION', 'SYSTEM', 'GAME_EVENT', 'SECURITY', 'PERFORMANCE', 'AUDIT')", name='check_log_category_valid'),
        CheckConstraint('execution_time_ms >= 0', name='check_execution_time_positive'),
        # Índices para consultas frequentes
        Index('idx_logs_timestamp', 'timestamp'),
        Index('idx_logs_user_id', 'user_id'),
        Index('idx_logs_level', 'log_level'),
        Index('idx_logs_category', 'log_category'),
        Index('idx_logs_action', 'action'),
        Index('idx_logs_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_logs_level_timestamp', 'log_level', 'timestamp'),
        Index('idx_logs_category_timestamp', 'log_category', 'timestamp'),
        # Índice composto para consultas de auditoria
        Index('idx_logs_audit', 'user_id', 'log_category', 'action', 'timestamp'),
    )

    def __repr__(self) -> str:
        return f"<SystemLogs(log_id={self.log_id}, timestamp={self.timestamp}, user_id={self.user_id}, level={self.log_level}, category={self.log_category}, action={self.action})>"