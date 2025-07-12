"""
SQLAlchemy database models for the Bellum Astrum space battle game.

This module contains all database model definitions including:
- User: Game user accounts and statistics
- Ship: Ship templates with base characteristics  
- OwnedShips: User-owned ships with individual stats
- BattleHistory: Records of battles between users
- SystemLogs: Comprehensive logging for audit and debugging

All models use the declarative base and include proper constraints,
indexes, and relationships for optimal database performance.
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, JSON, ForeignKey, Index, CheckConstraint
from .config import Base
from datetime import datetime, UTC
from typing import Dict, Any

def utc_now() -> datetime:
    """Helper function to return current UTC datetime for SQLAlchemy defaults"""
    return datetime.now(UTC)

class Ship(Base):
    """
    Ship template model representing available ship types in the game.

    This model stores the base characteristics of ship types that can be
    purchased or used in the game. Individual owned ships reference this
    template but may have modified stats.

    Attributes:
        ship_id: Unique identifier for the ship type
        ship_name: Display name of the ship type
        attack: Base attack power (damage per hit)
        shield: Base defensive capability  
        evasion: Base chance to avoid attacks (0.0-1.0)
        fire_rate: Base firing speed multiplier
        hp: Base hit points (health)
        value: Base purchase/sell price
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

    # Database constraints to ensure valid values
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
        return f"<Ship(ship_id={self.ship_id}, name={self.ship_name}, attack={self.attack}, shield={self.shield}, evasion={self.evasion}, fire_rate={self.fire_rate}, hp={self.hp}, value={self.value})>"
    
class User(Base):
    """
    User account model for game players.

    Stores user account information, game statistics, and progression data.
    Includes authentication data, ELO ranking, currency, and battle statistics.

    Attributes:
        user_id: Unique identifier for the user
        nickname: Unique display name
        email: Unique email address for authentication
        password_hash: Hashed password for security
        elo_rank: Skill rating based on battle performance
        currency_value: In-game currency amount
        victories: Total number of battle wins
        defeats: Total number of battle losses
        damage_dealt: Cumulative damage dealt to enemies
        damage_taken: Cumulative damage received from enemies
        ships_destroyed_by_user: Total enemy ships destroyed
        ships_lost_by_user: Total own ships lost in battle
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

    # Database constraints to ensure valid values
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
        return f"<User(user_id={self.user_id}, nickname={self.nickname}, elo_rank={self.elo_rank}, currency_value={self.currency_value}, victories={self.victories}, defeats={self.defeats})>"
        
class OwnedShips(Base):
    """
    Individual ship instances owned by users.

    Represents specific ships owned by users, with individual stats that may
    differ from the base ship template due to upgrades, damage, or modifications.
    
    Attributes:
        ship_number: Unique identifier for this owned ship instance
        user_id: Owner of this ship (foreign key to users)
        ship_id: Ship template this is based on (foreign key to ships)
        status: Current status ('owned', 'active', 'destroyed', 'upgrading', 'sold')
        ship_name: Name of the ship (copied from template)
        base_*: Original stats when purchased
        actual_*: Current stats (may be modified by upgrades/damage)
    """

    __tablename__ = 'owned_ships'

    ship_number = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    ship_id = Column(Integer, ForeignKey('ships.ship_id'), nullable=False)
    status = Column(String(20), default='owned', nullable=False)
    ship_name = Column(String(100), nullable=False)
    
    # Base stats (original values when purchased)
    base_attack = Column(Float, default=10, nullable=False)
    base_shield = Column(Float, default=5, nullable=False)
    base_evasion = Column(Float, default=0, nullable=False)
    base_fire_rate = Column(Float, default=1, nullable=False)
    base_hp = Column(Float, default=100, nullable=False)
    base_value = Column(Integer, default=1000, nullable=False)
    
    # Actual stats (current values, may be modified)
    actual_attack = Column(Float, default=10, nullable=False)
    actual_shield = Column(Float, default=5, nullable=False)
    actual_evasion = Column(Float, default=0, nullable=False)
    actual_fire_rate = Column(Float, default=1, nullable=False)
    actual_hp = Column(Float, default=100, nullable=False)
    actual_value = Column(Integer, default=1000, nullable=False)
    
    # Database constraints and indexes
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
        return f"<OwnedShips(ship_number={self.ship_number}, user_id={self.user_id}, ship_id={self.ship_id}, ship_name={self.ship_name}, status={self.status})>"


# ShipyardLog: registra o último uso do shipyard por usuário
class ShipyardLog(Base):
    """
    Records the last use of the shipyard by user and ship.

    Attributes:
        id: Unique log identifier
        user_id: User ID (FK to users)
        ship_number: Ship instance number (FK to owned_ships)
        ship_id: Ship type (FK to ships)
        last_used_at: Datetime of last use
    """
    __tablename__ = 'shipyard_log'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    ship_number = Column(Integer, ForeignKey('owned_ships.ship_number'), nullable=False, index=True)
    ship_id = Column(Integer, ForeignKey('ships.ship_id'), nullable=False, index=True)
    last_used_at = Column(DateTime, nullable=False, default=utc_now)

    __table_args__ = (
        Index('idx_shipyardlog_user', 'user_id'),
        Index('idx_shipyardlog_ship', 'ship_number'),
        Index('idx_shipyardlog_shipid', 'ship_id'),
    )

    def __repr__(self) -> str:
        return f"<ShipyardLog(id={self.id}, user_id={self.user_id}, ship_number={self.ship_number}, ship_id={self.ship_id}, last_used_at={self.last_used_at})>"
    
class BattleHistory(Base):
    """
    Battle records between users.

    Stores detailed information about battles including participants,
    their ships, battle events, and outcomes for historical tracking
    and statistical analysis.
    
    Attributes:
        battle_id: Unique identifier for the battle
        timestamp: When the battle occurred
        winner_user_id: ID of the winning user (null for draws)
        participants: JSON data about all participants and their ships
        battle_log: JSON array of battle events/actions
        extra: Additional flexible data (damage totals, rounds, etc.)
    """
    
    __tablename__ = 'battle_history'

    battle_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=utc_now, nullable=False)
    winner_user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    participants = Column(JSON, nullable=False)  # List of participants and their ships
    battle_log = Column(JSON, nullable=True)     # List of battle events/actions
    extra = Column(JSON, nullable=True)          # Additional flexible data

    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_battle_timestamp', 'timestamp'),
        Index('idx_battle_winner', 'winner_user_id'),
        Index('idx_battle_winner_timestamp', 'winner_user_id', 'timestamp'),
    )

    def __repr__(self) -> str:
        return f"<BattleHistory(battle_id={self.battle_id}, timestamp={self.timestamp}, winner_user_id={self.winner_user_id})>"

class SystemLogs(Base):
    """
    Comprehensive system logging for audit trails and debugging.

    Captures all significant system events, user actions, security events,
    and performance metrics for monitoring, debugging, and compliance.
    
    Attributes:
        log_id: Unique identifier for the log entry
        timestamp: When the event occurred
        user_id: User who performed the action (null for system events)
        log_level: Severity level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_category: Type of event (USER_ACTION, SYSTEM, GAME_EVENT, SECURITY, PERFORMANCE)
        action: Specific action performed (LOGIN, BUY_SHIP, BATTLE_START, etc.)
        details: Additional event details in JSON format
        ip_address: Client IP address for security tracking
        user_agent: Client user agent string
        session_id: Session identifier for tracking user sessions
        resource_affected: What resource was affected (e.g., 'ship_id:123')
        old_value: Previous value before change (for audit trails)
        new_value: New value after change (for audit trails)
        error_message: Error details if action failed
        execution_time_ms: Action execution time in milliseconds
    """

    __tablename__ = 'system_logs'

    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=utc_now, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    log_level = Column(String(10), nullable=False)
    log_category = Column(String(20), nullable=False)
    action = Column(String(50), nullable=False)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(String(500), nullable=True)
    session_id = Column(String(255), nullable=True)
    resource_affected = Column(String(255), nullable=True)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    error_message = Column(String(1000), nullable=True)
    execution_time_ms = Column(Integer, nullable=True)

    # Constraints and indexes for performance and data integrity
    __table_args__ = (
        CheckConstraint("log_level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')", name='check_log_level_valid'),
        CheckConstraint("log_category IN ('USER_ACTION', 'SYSTEM', 'GAME_EVENT', 'SECURITY', 'PERFORMANCE', 'AUDIT')", name='check_log_category_valid'),
        CheckConstraint('execution_time_ms >= 0', name='check_execution_time_positive'),
        # Indexes for frequent queries
        Index('idx_logs_timestamp', 'timestamp'),
        Index('idx_logs_user_id', 'user_id'),
        Index('idx_logs_level', 'log_level'),
        Index('idx_logs_category', 'log_category'),
        Index('idx_logs_action', 'action'),
        Index('idx_logs_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_logs_level_timestamp', 'log_level', 'timestamp'),
        Index('idx_logs_category_timestamp', 'log_category', 'timestamp'),
        # Composite index for audit queries
        Index('idx_logs_audit', 'user_id', 'log_category', 'action', 'timestamp'),
    )

    def __repr__(self) -> str:
        return f"<SystemLogs(log_id={self.log_id}, timestamp={self.timestamp}, user_id={self.user_id}, level={self.log_level}, category={self.log_category}, action={self.action})>"
