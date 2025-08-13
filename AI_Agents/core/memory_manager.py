"""
AI Memory Manager - Comprehensive memory system for AI agents to track and learn from their actions.
"""

import json
import sqlite3
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)

class ActionType(Enum):
    """Types of actions an AI can take"""
    WORK = "work"
    BATTLE = "battle"
    BUY_SHIP = "buy_ship"
    REPAIR_SHIP = "repair_ship"
    ACTIVATE_SHIP = "activate_ship"
    DEACTIVATE_SHIP = "deactivate_ship"
    QUERY = "query"  # Information gathering actions

class MemoryType(Enum):
    """Types of memories to store"""
    ACTION_RESULT = "action_result"
    BATTLE_OUTCOME = "battle_outcome"
    OPPONENT_PROFILE = "opponent_profile"
    PATTERN_RECOGNITION = "pattern_recognition"
    STRATEGY_EVALUATION = "strategy_evaluation"

@dataclass
class ActionMemory:
    """Memory of a single action and its outcome"""
    timestamp: datetime
    round_number: int
    action_type: ActionType
    action_parameters: Dict[str, Any]
    game_state_before: Dict[str, Any]
    game_state_after: Dict[str, Any]
    result_success: bool
    result_data: Dict[str, Any]
    credits_change: int = 0
    xp_change: int = 0
    elo_change: float = 0.0
    ships_lost: int = 0
    ships_gained: int = 0

@dataclass
class BattleMemory:
    """Detailed memory of a battle"""
    timestamp: datetime
    opponent_id: int
    opponent_nickname: str
    opponent_level: int
    opponent_elo: float
    my_level_at_time: int
    my_elo_at_time: float
    my_formation: str
    opponent_formation: str = "UNKNOWN"
    my_ships_count: int = 0
    opponent_ships_count: int = 0
    victory: bool = False
    credits_gained: int = 0
    xp_gained: int = 0
    elo_change: float = 0.0
    ships_lost: int = 0
    battle_duration: float = 0.0
    battle_log: str = ""

@dataclass
class OpponentProfile:
    """Profile of an opponent built over time"""
    user_id: int
    nickname: str
    battles_fought: int = 0
    victories_against: int = 0
    defeats_against: int = 0
    win_rate_vs_me: float = 0.0
    average_level: float = 0.0
    average_elo: float = 0.0
    preferred_formation: str = "UNKNOWN"
    typical_ship_count: int = 1
    last_seen: Optional[datetime] = None
    threat_level: str = "UNKNOWN"  # LOW, MEDIUM, HIGH, EXTREME

class AIMemoryManager:
    """Manages all memory operations for an AI agent"""
    
    def __init__(self, agent_nickname: str, memory_dir: str = "./AI_Agents/memories"):
        self.agent_nickname = agent_nickname
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.memory_dir / f"{agent_nickname}_memory.db"
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for persistent memory"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Actions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    round_number INTEGER NOT NULL,
                    action_type TEXT NOT NULL,
                    action_parameters TEXT,
                    game_state_before TEXT,
                    game_state_after TEXT,
                    result_success BOOLEAN,
                    result_data TEXT,
                    credits_change INTEGER DEFAULT 0,
                    xp_change INTEGER DEFAULT 0,
                    elo_change REAL DEFAULT 0,
                    ships_lost INTEGER DEFAULT 0,
                    ships_gained INTEGER DEFAULT 0
                )
            ''')
            
            # Battles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS battles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    opponent_id INTEGER NOT NULL,
                    opponent_nickname TEXT NOT NULL,
                    opponent_level INTEGER,
                    opponent_elo REAL,
                    my_level_at_time INTEGER,
                    my_elo_at_time REAL,
                    my_formation TEXT,
                    opponent_formation TEXT DEFAULT 'UNKNOWN',
                    my_ships_count INTEGER DEFAULT 0,
                    opponent_ships_count INTEGER DEFAULT 0,
                    victory BOOLEAN NOT NULL,
                    credits_gained INTEGER DEFAULT 0,
                    xp_gained INTEGER DEFAULT 0,
                    elo_change REAL DEFAULT 0,
                    ships_lost INTEGER DEFAULT 0,
                    battle_duration REAL DEFAULT 0,
                    battle_log TEXT
                )
            ''')
            
            # Opponent profiles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS opponent_profiles (
                    user_id INTEGER PRIMARY KEY,
                    nickname TEXT NOT NULL,
                    battles_fought INTEGER DEFAULT 0,
                    victories_against INTEGER DEFAULT 0,
                    defeats_against INTEGER DEFAULT 0,
                    win_rate_vs_me REAL DEFAULT 0,
                    average_level REAL DEFAULT 0,
                    average_elo REAL DEFAULT 0,
                    preferred_formation TEXT DEFAULT 'UNKNOWN',
                    typical_ship_count INTEGER DEFAULT 1,
                    last_seen TEXT,
                    threat_level TEXT DEFAULT 'UNKNOWN',
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Patterns and insights table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    insight_type TEXT NOT NULL,
                    insight_data TEXT NOT NULL,
                    confidence REAL DEFAULT 0.5,
                    created_at TEXT NOT NULL,
                    last_validated TEXT
                )
            ''')
            
            conn.commit()
    
    def store_action_memory(self, memory: ActionMemory):
        """Store memory of an action"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO actions (
                        timestamp, round_number, action_type, action_parameters,
                        game_state_before, game_state_after, result_success, result_data,
                        credits_change, xp_change, elo_change, ships_lost, ships_gained
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    memory.timestamp.isoformat(),
                    memory.round_number,
                    memory.action_type.value,
                    json.dumps(memory.action_parameters),
                    json.dumps(memory.game_state_before),
                    json.dumps(memory.game_state_after),
                    memory.result_success,
                    json.dumps(memory.result_data),
                    memory.credits_change,
                    memory.xp_change,
                    memory.elo_change,
                    memory.ships_lost,
                    memory.ships_gained
                ))
                conn.commit()
                logger.debug(f"Stored action memory: {memory.action_type.value}")
        except Exception as e:
            logger.error(f"Failed to store action memory: {str(e)}")
    
    def store_battle_memory(self, memory: BattleMemory):
        """Store memory of a battle"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO battles (
                        timestamp, opponent_id, opponent_nickname, opponent_level, opponent_elo,
                        my_level_at_time, my_elo_at_time, my_formation, opponent_formation,
                        my_ships_count, opponent_ships_count, victory, credits_gained,
                        xp_gained, elo_change, ships_lost, battle_duration, battle_log
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    memory.timestamp.isoformat(),
                    memory.opponent_id,
                    memory.opponent_nickname,
                    memory.opponent_level,
                    memory.opponent_elo,
                    memory.my_level_at_time,
                    memory.my_elo_at_time,
                    memory.my_formation,
                    memory.opponent_formation,
                    memory.my_ships_count,
                    memory.opponent_ships_count,
                    memory.victory,
                    memory.credits_gained,
                    memory.xp_gained,
                    memory.elo_change,
                    memory.ships_lost,
                    memory.battle_duration,
                    memory.battle_log
                ))
                conn.commit()
                
                # Update opponent profile
                self._update_opponent_profile(memory)
                
                logger.info(f"Stored battle memory vs {memory.opponent_nickname}: {'Victory' if memory.victory else 'Defeat'}")
        except Exception as e:
            logger.error(f"Failed to store battle memory: {str(e)}")
    
    def _update_opponent_profile(self, battle: BattleMemory):
        """Update opponent profile based on battle result"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if profile exists
                cursor.execute('SELECT * FROM opponent_profiles WHERE user_id = ?', (battle.opponent_id,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing profile
                    new_battles = existing[3] + 1
                    new_victories = existing[4] + (1 if battle.victory else 0)
                    new_defeats = existing[5] + (0 if battle.victory else 1)
                    new_win_rate = new_victories / new_battles if new_battles > 0 else 0
                    
                    # Update averages
                    new_avg_level = (existing[7] * existing[3] + battle.opponent_level) / new_battles
                    new_avg_elo = (existing[8] * existing[3] + battle.opponent_elo) / new_battles
                    
                    # Determine threat level
                    threat_level = self._calculate_threat_level(new_win_rate, new_avg_level, battle.my_level_at_time)
                    
                    cursor.execute('''
                        UPDATE opponent_profiles SET
                            battles_fought = ?, victories_against = ?, defeats_against = ?,
                            win_rate_vs_me = ?, average_level = ?, average_elo = ?,
                            last_seen = ?, threat_level = ?, updated_at = ?
                        WHERE user_id = ?
                    ''', (
                        new_battles, new_victories, new_defeats, new_win_rate,
                        new_avg_level, new_avg_elo, battle.timestamp.isoformat(),
                        threat_level, datetime.now().isoformat(), battle.opponent_id
                    ))
                else:
                    # Create new profile
                    threat_level = self._calculate_threat_level(
                        1.0 if not battle.victory else 0.0,
                        battle.opponent_level,
                        battle.my_level_at_time
                    )
                    
                    cursor.execute('''
                        INSERT INTO opponent_profiles (
                            user_id, nickname, battles_fought, victories_against, defeats_against,
                            win_rate_vs_me, average_level, average_elo, last_seen,
                            threat_level, updated_at
                        ) VALUES (?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        battle.opponent_id, battle.opponent_nickname,
                        1 if battle.victory else 0,
                        0 if battle.victory else 1,
                        1.0 if not battle.victory else 0.0,
                        battle.opponent_level,
                        battle.opponent_elo,
                        battle.timestamp.isoformat(),
                        threat_level,
                        datetime.now().isoformat()
                    ))
                
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to update opponent profile: {str(e)}")
    
    def _calculate_threat_level(self, win_rate_against_me: float, their_level: float, my_level: float) -> str:
        """Calculate threat level of an opponent"""
        level_diff = their_level - my_level
        
        if win_rate_against_me >= 0.8 or level_diff > 5:
            return "EXTREME"
        elif win_rate_against_me >= 0.6 or level_diff > 2:
            return "HIGH"
        elif win_rate_against_me >= 0.4 or level_diff > -2:
            return "MEDIUM"
        else:
            return "LOW"
    
    # Query methods for AI decision making
    def get_recent_actions(self, hours: int = 24, action_type: ActionType = None) -> List[Dict[str, Any]]:
        """Get recent actions within specified timeframe"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                since = datetime.now() - timedelta(hours=hours)
                
                if action_type:
                    cursor.execute('''
                        SELECT * FROM actions 
                        WHERE timestamp > ? AND action_type = ?
                        ORDER BY timestamp DESC
                    ''', (since.isoformat(), action_type.value))
                else:
                    cursor.execute('''
                        SELECT * FROM actions 
                        WHERE timestamp > ?
                        ORDER BY timestamp DESC
                    ''', (since.isoformat(),))
                
                return [self._row_to_dict(row, 'action') for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get recent actions: {str(e)}")
            return []
    
    def get_opponent_profile(self, opponent_id: int) -> Optional[OpponentProfile]:
        """Get detailed profile of a specific opponent"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM opponent_profiles WHERE user_id = ?', (opponent_id,))
                row = cursor.fetchone()
                
                if row:
                    return OpponentProfile(
                        user_id=row[0],
                        nickname=row[1],
                        battles_fought=row[2],
                        victories_against=row[3],
                        defeats_against=row[4],
                        win_rate_vs_me=row[5],
                        average_level=row[6],
                        average_elo=row[7],
                        preferred_formation=row[8],
                        typical_ship_count=row[9],
                        last_seen=datetime.fromisoformat(row[10]) if row[10] else None,
                        threat_level=row[11]
                    )
                return None
        except Exception as e:
            logger.error(f"Failed to get opponent profile: {str(e)}")
            return None
    
    def get_winnable_opponents(self, available_opponents: List[Dict]) -> List[Tuple[int, float]]:
        """Get opponents ranked by probability of victory"""
        try:
            winnable = []
            
            for opponent in available_opponents:
                opponent_id = opponent.get('user_id')
                profile = self.get_opponent_profile(opponent_id)
                
                if profile:
                    # Use historical data
                    win_probability = 1.0 - profile.win_rate_vs_me
                else:
                    # Estimate based on level/ELO difference
                    level_diff = opponent.get('level', 1) - opponent.get('my_level', 1)
                    elo_diff = opponent.get('elo', 1000) - opponent.get('my_elo', 1000)
                    
                    # Simple heuristic
                    win_probability = 0.5 - (level_diff * 0.1) - (elo_diff * 0.0001)
                    win_probability = max(0.1, min(0.9, win_probability))  # Clamp between 10-90%
                
                winnable.append((opponent_id, win_probability))
            
            # Sort by win probability (highest first)
            winnable.sort(key=lambda x: x[1], reverse=True)
            return winnable
            
        except Exception as e:
            logger.error(f"Failed to analyze winnable opponents: {str(e)}")
            return []
    
    def get_action_success_rate(self, action_type: ActionType, days: int = 7) -> float:
        """Get success rate for a specific action type"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                since = datetime.now() - timedelta(days=days)
                
                cursor.execute('''
                    SELECT COUNT(*) as total, 
                           SUM(CASE WHEN result_success THEN 1 ELSE 0 END) as successful
                    FROM actions 
                    WHERE action_type = ? AND timestamp > ?
                ''', (action_type.value, since.isoformat()))
                
                row = cursor.fetchone()
                if row and row[0] > 0:
                    return row[1] / row[0]
                return 0.5  # Default if no data
                
        except Exception as e:
            logger.error(f"Failed to get action success rate: {str(e)}")
            return 0.5
    
    def get_average_credits_per_work(self, days: int = 7) -> float:
        """Get average credits earned per work session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                since = datetime.now() - timedelta(days=days)
                
                cursor.execute('''
                    SELECT AVG(credits_change) FROM actions 
                    WHERE action_type = ? AND result_success = 1 AND timestamp > ?
                ''', (ActionType.WORK.value, since.isoformat()))
                
                result = cursor.fetchone()
                return result[0] if result[0] else 0.0
                
        except Exception as e:
            logger.error(f"Failed to get average credits per work: {str(e)}")
            return 0.0
    
    def _row_to_dict(self, row: tuple, table_type: str) -> Dict[str, Any]:
        """Convert database row to dictionary"""
        if table_type == 'action':
            return {
                'id': row[0],
                'timestamp': row[1],
                'round_number': row[2],
                'action_type': row[3],
                'action_parameters': json.loads(row[4]) if row[4] else {},
                'result_success': row[6],
                'credits_change': row[9],
                'xp_change': row[10],
                'elo_change': row[11]
            }
        return {}
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get summary of stored memories"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count actions
                cursor.execute('SELECT COUNT(*) FROM actions')
                action_count = cursor.fetchone()[0]
                
                # Count battles
                cursor.execute('SELECT COUNT(*) FROM battles')
                battle_count = cursor.fetchone()[0]
                
                # Count opponent profiles
                cursor.execute('SELECT COUNT(*) FROM opponent_profiles')
                opponent_count = cursor.fetchone()[0]
                
                # Recent activity
                since_24h = datetime.now() - timedelta(hours=24)
                cursor.execute('SELECT COUNT(*) FROM actions WHERE timestamp > ?', (since_24h.isoformat(),))
                recent_actions = cursor.fetchone()[0]
                
                return {
                    'total_actions': action_count,
                    'total_battles': battle_count,
                    'known_opponents': opponent_count,
                    'actions_last_24h': recent_actions,
                    'database_path': str(self.db_path)
                }
                
        except Exception as e:
            logger.error(f"Failed to get memory summary: {str(e)}")
            return {}
    
    def cleanup_old_memories(self, days: int = 30):
        """Clean up old memories to manage database size"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cutoff = datetime.now() - timedelta(days=days)
                
                # Keep battles and opponent profiles, only clean up routine actions
                cursor.execute('''
                    DELETE FROM actions 
                    WHERE timestamp < ? AND action_type NOT IN (?, ?)
                ''', (cutoff.isoformat(), ActionType.BATTLE.value, ActionType.BUY_SHIP.value))
                
                deleted = cursor.rowcount
                conn.commit()
                
                logger.info(f"Cleaned up {deleted} old action memories (older than {days} days)")
                
        except Exception as e:
            logger.error(f"Failed to cleanup old memories: {str(e)}")
