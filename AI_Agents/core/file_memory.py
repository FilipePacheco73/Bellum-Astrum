"""
File-based Memory System for AI Agents
Replaces SQLite with simple log files for each agent's memory
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

logger = logging.getLogger('bellum.debug')

@dataclass
class AgentAction:
    """Represents a single action taken by an agent"""
    timestamp: str
    round_number: int
    tool_name: str
    tool_params: Dict[str, Any]
    game_state_before: Dict[str, Any]
    game_state_after: Dict[str, Any]
    success: bool
    result_data: Dict[str, Any]
    reasoning: str = ""

class FileBasedMemory:
    """File-based memory system for AI agents"""
    
    def __init__(self, agent_name: str, memories_dir: Path):
        self.agent_name = agent_name
        self.memories_dir = Path(memories_dir)
        self.memories_dir.mkdir(parents=True, exist_ok=True)
        
        # Create memory file for this agent
        self.memory_file = self.memories_dir / f"{agent_name}_memory.jsonl"
        
        # Ensure file exists
        if not self.memory_file.exists():
            self.memory_file.touch()
    
    def store_action(self, action: AgentAction):
        """Store an action in the agent's memory file"""
        try:
            with open(self.memory_file, 'a', encoding='utf-8') as f:
                json_line = json.dumps(asdict(action))
                f.write(json_line + '\n')
                
            logger.debug(f"Stored action for {self.agent_name}: {action.tool_name}")
            
        except Exception as e:
            logger.error(f"Failed to store action for {self.agent_name}: {str(e)}")
    
    def get_recent_actions(self, hours: int = 24, limit: int = 50) -> List[AgentAction]:
        """Get recent actions from memory"""
        try:
            actions = []
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            if not self.memory_file.exists():
                return actions
            
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                # Get last N lines for efficiency
                recent_lines = lines[-limit*2:] if len(lines) > limit*2 else lines
                
                for line in recent_lines:
                    if line.strip():
                        try:
                            action_data = json.loads(line.strip())
                            action_time = datetime.fromisoformat(action_data['timestamp'])
                            
                            if action_time >= cutoff_time:
                                action = AgentAction(**action_data)
                                actions.append(action)
                                
                        except (json.JSONDecodeError, KeyError, ValueError) as e:
                            logger.warning(f"Corrupted memory line for {self.agent_name}: {str(e)}")
                            continue
            
            # Sort by timestamp (most recent first)
            actions.sort(key=lambda x: x.timestamp, reverse=True)
            return actions[:limit]
            
        except Exception as e:
            logger.error(f"Failed to read recent actions for {self.agent_name}: {str(e)}")
            return []
    
    def get_tool_success_rate(self, tool_name: str, recent_hours: int = 24) -> float:
        """Get success rate for a specific tool"""
        try:
            recent_actions = self.get_recent_actions(hours=recent_hours)
            tool_actions = [a for a in recent_actions if a.tool_name == tool_name]
            
            if not tool_actions:
                return 0.5  # Default neutral success rate
            
            successful = sum(1 for a in tool_actions if a.success)
            return successful / len(tool_actions)
            
        except Exception as e:
            logger.error(f"Failed to calculate success rate for {tool_name}: {str(e)}")
            return 0.5
    
    def get_average_credits_per_work(self, recent_hours: int = 24) -> float:
        """Get average credits earned per work action"""
        try:
            recent_actions = self.get_recent_actions(hours=recent_hours)
            work_actions = [a for a in recent_actions if a.tool_name == "work" and a.success]
            
            if not work_actions:
                return 200.0  # Default expected work income
            
            total_credits = 0
            count = 0
            
            for action in work_actions:
                credits_earned = action.result_data.get('credits_earned', 0)
                if credits_earned > 0:
                    total_credits += credits_earned
                    count += 1
            
            return total_credits / count if count > 0 else 200.0
            
        except Exception as e:
            logger.error(f"Failed to calculate average credits per work: {str(e)}")
            return 200.0
    
    def get_battle_performance(self, recent_hours: int = 24) -> Dict[str, Any]:
        """Get battle performance statistics"""
        try:
            recent_actions = self.get_recent_actions(hours=recent_hours)
            battle_actions = [a for a in recent_actions if a.tool_name == "battle"]
            
            if not battle_actions:
                return {
                    "success_rate": 0.5,
                    "avg_credits_per_win": 500.0,
                    "total_battles": 0,
                    "wins": 0,
                    "losses": 0
                }
            
            wins = sum(1 for a in battle_actions if a.success)
            losses = len(battle_actions) - wins
            
            # Calculate average credits per win
            win_actions = [a for a in battle_actions if a.success]
            total_win_credits = sum(a.result_data.get('credits_earned', 0) for a in win_actions)
            avg_credits_per_win = total_win_credits / wins if wins > 0 else 500.0
            
            return {
                "success_rate": wins / len(battle_actions),
                "avg_credits_per_win": avg_credits_per_win,
                "total_battles": len(battle_actions),
                "wins": wins,
                "losses": losses
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate battle performance: {str(e)}")
            return {
                "success_rate": 0.5,
                "avg_credits_per_win": 500.0,
                "total_battles": 0,
                "wins": 0,
                "losses": 0
            }
    
    def get_memory_summary(self, recent_hours: int = 4) -> Dict[str, Any]:
        """Get a summary of recent memory for decision making"""
        try:
            recent_actions = self.get_recent_actions(hours=recent_hours)
            
            # Group actions by tool
            tool_usage = {}
            for action in recent_actions:
                if action.tool_name not in tool_usage:
                    tool_usage[action.tool_name] = {"count": 0, "successes": 0}
                
                tool_usage[action.tool_name]["count"] += 1
                if action.success:
                    tool_usage[action.tool_name]["successes"] += 1
            
            # Calculate success rates
            for tool_name, stats in tool_usage.items():
                stats["success_rate"] = stats["successes"] / stats["count"] if stats["count"] > 0 else 0
            
            return {
                "recent_actions_count": len(recent_actions),
                "tool_usage": tool_usage,
                "work_success_rate": self.get_tool_success_rate("work", recent_hours),
                "battle_performance": self.get_battle_performance(recent_hours),
                "avg_credits_per_work": self.get_average_credits_per_work(recent_hours),
                "last_actions": [
                    {
                        "tool": a.tool_name,
                        "success": a.success,
                        "round": a.round_number,
                        "reasoning": a.reasoning
                    }
                    for a in recent_actions[:5]  # Last 5 actions
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to generate memory summary: {str(e)}")
            return {
                "recent_actions_count": 0,
                "tool_usage": {},
                "work_success_rate": 0.5,
                "battle_performance": {"success_rate": 0.5},
                "avg_credits_per_work": 200.0,
                "last_actions": []
            }
    
    def cleanup_old_entries(self, days_to_keep: int = 7):
        """Remove entries older than specified days"""
        try:
            if not self.memory_file.exists():
                return
            
            cutoff_time = datetime.now() - timedelta(days=days_to_keep)
            temp_file = self.memory_file.with_suffix('.tmp')
            
            kept_count = 0
            removed_count = 0
            
            with open(self.memory_file, 'r', encoding='utf-8') as infile, \
                 open(temp_file, 'w', encoding='utf-8') as outfile:
                
                for line in infile:
                    if line.strip():
                        try:
                            action_data = json.loads(line.strip())
                            action_time = datetime.fromisoformat(action_data['timestamp'])
                            
                            if action_time >= cutoff_time:
                                outfile.write(line)
                                kept_count += 1
                            else:
                                removed_count += 1
                                
                        except (json.JSONDecodeError, KeyError, ValueError):
                            # Keep corrupted lines for manual inspection
                            outfile.write(line)
                            kept_count += 1
            
            # Replace original file with cleaned version
            temp_file.replace(self.memory_file)
            
            logger.info(f"Cleaned memory for {self.agent_name}: kept {kept_count}, removed {removed_count} entries")
            
        except Exception as e:
            logger.error(f"Failed to cleanup memory for {self.agent_name}: {str(e)}")
