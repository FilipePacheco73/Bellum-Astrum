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

@dataclass
class SimpleDecision:
    """Simple decision entry for memory"""
    timestamp: str
    round_number: int
    action: str
    reason: str  # Will be replaced by AI reasoning/thinking
    success: bool = True
    input_tokens: int = 0
    output_tokens: int = 0
    ai_reasoning: str = ""

class FileBasedMemory:
    """File-based memory system for AI agents"""
    
    def __init__(self, agent_name: str, memories_dir: Path):
        self.agent_name = agent_name
        self.memories_dir = Path(memories_dir)
        self.memories_dir.mkdir(parents=True, exist_ok=True)
        
        # Create memory file for this agent
        self.memory_file = self.memories_dir / f"{agent_name}_memory.json"
        
        # Simple decisions file (for new system)
        self.decisions_file = self.memories_dir / f"{agent_name}_decisions.json"
        
        # Only create files when there's actual content to write
        # Don't create empty files unnecessarily
    
    def store_decision(self, round_number: int, action: str, reason: str, success: bool = True, 
                      input_tokens: int = 0, output_tokens: int = 0, ai_reasoning: str = ""):
        """Store a simple decision in memory with token information and AI reasoning"""
        try:
            decision = SimpleDecision(
                timestamp=datetime.now().isoformat(),
                round_number=round_number,
                action=action,
                reason=reason,
                success=success,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                ai_reasoning=ai_reasoning or reason  # Use AI reasoning if provided, otherwise fallback to reason
            )
            
            # Load existing decisions or create empty list
            decisions = []
            if self.decisions_file.exists():
                try:
                    with open(self.decisions_file, 'r', encoding='utf-8') as f:
                        decisions = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    decisions = []
            
            # Add new decision
            decisions.append(asdict(decision))
            
            # Write back to file with proper JSON formatting
            with open(self.decisions_file, 'w', encoding='utf-8') as f:
                json.dump(decisions, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Failed to store decision for {self.agent_name}: {str(e)}")
    
    def get_recent_decisions(self, max_rounds: int = 3) -> List[SimpleDecision]:
        """Get recent decisions (last N rounds)"""
        try:
            decisions = []
            
            if not self.decisions_file.exists():
                return decisions
            
            # Load decisions from JSON file
            try:
                with open(self.decisions_file, 'r', encoding='utf-8') as f:
                    decisions_data = json.load(f)
                    
                for decision_data in decisions_data:
                    try:
                        decision = SimpleDecision(**decision_data)
                        decisions.append(decision)
                    except (KeyError, ValueError):
                        continue  # Skip corrupted entries silently
                        
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.error(f"Failed to read decisions file for {self.agent_name}: {str(e)}")
                return []
            
            # Sort by round number and get the last max_rounds
            decisions.sort(key=lambda x: x.round_number)
            recent_decisions = decisions[-max_rounds:] if decisions else []
            
            return recent_decisions
            
        except Exception as e:
            logger.error(f"Failed to read recent decisions for {self.agent_name}: {str(e)}")
            return []
    
    def get_memory_summary(self, max_rounds: int = 3) -> str:
        """Get a formatted summary of recent decisions for prompt inclusion"""
        recent_decisions = self.get_recent_decisions(max_rounds)
        
        if not recent_decisions:
            return "No previous decision memories available."
        
        summary_lines = ["=== RECENT ROUNDS MEMORIES ==="]
        
        for decision in recent_decisions:
            round_num = decision.round_number
            action = decision.action
            reasoning = decision.ai_reasoning or decision.reason
            
            # Simplify the reasoning if it's too long
            if len(reasoning) > 100:
                reasoning = reasoning[:97] + "..."
            
            success_indicator = "✓" if decision.success else "✗"
            tokens_info = f"({decision.input_tokens}→{decision.output_tokens}t)" if decision.input_tokens > 0 else ""
            
            summary_lines.append(f"Round {round_num}: {action} {success_indicator} {tokens_info}")
            if reasoning and reasoning != action:
                summary_lines.append(f"  Thinking: {reasoning}")
        
        summary_lines.append("=== END OF MEMORIES ===")
        return "\n".join(summary_lines)
    
    def store_action(self, action: AgentAction):
        """Store an action in the agent's memory file"""
        try:
            # Load existing actions or create empty list
            actions = []
            if self.memory_file.exists():
                try:
                    with open(self.memory_file, 'r', encoding='utf-8') as f:
                        actions = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    actions = []
            
            # Add new action
            actions.append(asdict(action))
            
            # Write back to file with proper JSON formatting
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(actions, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Failed to store action for {self.agent_name}: {str(e)}")
    
    def get_recent_actions(self, hours: int = 24, limit: int = 50) -> List[AgentAction]:
        """Get recent actions from memory"""
        try:
            actions = []
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            if not self.memory_file.exists():
                return actions
            
            # Load actions from JSON file
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    actions_data = json.load(f)
                    
                for action_data in actions_data:
                    try:
                        action_time = datetime.fromisoformat(action_data['timestamp'])
                        
                        if action_time >= cutoff_time:
                            action = AgentAction(**action_data)
                            actions.append(action)
                            
                    except (KeyError, ValueError):
                        continue  # Skip corrupted entries silently
                        
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.error(f"Failed to read memory file for {self.agent_name}: {str(e)}")
                return []
            
            # Sort by timestamp (most recent first) and limit results
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
    
    def cleanup_old_entries(self, days_to_keep: int = 7):
        """Remove entries older than specified days"""
        try:
            if not self.memory_file.exists():
                return
            
            cutoff_time = datetime.now() - timedelta(days=days_to_keep)
            
            # Load existing actions
            actions_data = []
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    actions_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return
            
            # Filter actions to keep only recent ones
            kept_actions = []
            removed_count = 0
            
            for action_data in actions_data:
                try:
                    action_time = datetime.fromisoformat(action_data['timestamp'])
                    
                    if action_time >= cutoff_time:
                        kept_actions.append(action_data)
                    else:
                        removed_count += 1
                        
                except (KeyError, ValueError):
                    # Keep corrupted entries for manual inspection
                    kept_actions.append(action_data)
            
            # Write back the cleaned data
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(kept_actions, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Cleaned memory for {self.agent_name}: kept {len(kept_actions)}, removed {removed_count} entries")
            
        except Exception as e:
            logger.error(f"Failed to cleanup memory for {self.agent_name}: {str(e)}")
    
    def cleanup_empty_files(self):
        """Remove empty memory files"""
        try:
            # Check and remove empty memory file
            if self.memory_file.exists() and self.memory_file.stat().st_size == 0:
                self.memory_file.unlink()
                logger.info(f"Removed empty memory file for {self.agent_name}")
            
            # Check and remove empty decisions file
            if self.decisions_file.exists() and self.decisions_file.stat().st_size == 0:
                self.decisions_file.unlink()
                logger.info(f"Removed empty decisions file for {self.agent_name}")
                
        except Exception as e:
            logger.error(f"Failed to cleanup empty files for {self.agent_name}: {str(e)}")
