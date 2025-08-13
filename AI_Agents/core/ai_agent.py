"""
AI Agent - Base class for autonomous AI players in Bellum Astrum.
"""

import asyncio
import logging
import json
import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass

from AI_Agents.core.llm_manager import get_llm_manager
from AI_Agents.core.tool_caller import GameToolCaller, GameTool, ToolResult, AICredentials
from AI_Agents.core.memory_manager import AIMemoryManager, ActionMemory, BattleMemory, ActionType
from AI_Agents.config.ai_personalities import get_personality, AIPersonality
from AI_Agents.prompts.system_prompts import get_system_prompt
from AI_Agents.prompts.aggressive_prompts import get_aggressive_prompt
from AI_Agents.prompts.defensive_prompts import get_defensive_prompt  
from AI_Agents.prompts.tactical_prompts import get_tactical_prompt

logger = logging.getLogger(__name__)

@dataclass
class GameState:
    """Current game state for an AI agent"""
    credits: int = 0
    level: int = 1
    rank: str = "Recruit"
    elo: float = 1000.0
    active_ships: List[Dict] = None
    work_cooldown: Optional[datetime] = None
    ship_limits: Dict = None
    available_opponents: List[Dict] = None
    
    def __post_init__(self):
        if self.active_ships is None:
            self.active_ships = []

class AIAgent:
    """Base AI agent that can play Bellum Astrum autonomously"""
    
    def __init__(self, personality_name: str, credentials: AICredentials):
        self.personality_name = personality_name
        self.personality = get_personality(personality_name)
        self.credentials = credentials
        self.tool_caller = GameToolCaller()
        self.llm_manager = get_llm_manager()
        self.game_state = GameState()
        
        # Decision tracking
        self.decision_history: List[Dict] = []
        self.round_count = 0
        self.last_action_time = None
        
        # Load the appropriate LLM model
        self._load_model()
    
    def _load_model(self):
        """Load the LLM model for this agent's personality"""
        if not self.llm_manager.is_model_loaded(self.personality.llm_type):
            success = self.llm_manager.load_model(self.personality.llm_type)
            if not success:
                logger.error(f"Failed to load model for {self.personality_name}")
                raise RuntimeError(f"Could not load LLM model for {self.personality.llm_type}")
    
    async def update_game_state(self) -> bool:
        """Update the current game state by calling various APIs"""
        try:
            # Get user status
            user_result = await self.tool_caller.execute_tool(
                GameTool.GET_MY_STATUS, self.credentials
            )
            if user_result.success:
                user_data = user_result.data
                self.game_state.credits = user_data.get('currency_value', 0)
                self.game_state.level = user_data.get('level', 1)
                self.game_state.rank = user_data.get('rank', 'Recruit')
                self.game_state.elo = user_data.get('elo', 1000.0)
            
            # Get fleet status
            fleet_result = await self.tool_caller.execute_tool(
                GameTool.GET_FLEET_STATUS, self.credentials
            )
            if fleet_result.success:
                self.game_state.active_ships = fleet_result.data or []
            
            # Get work status
            work_result = await self.tool_caller.execute_tool(
                GameTool.GET_WORK_STATUS, self.credentials
            )
            if work_result.success:
                work_data = work_result.data
                # Parse cooldown if exists
                cooldown_str = work_data.get('cooldown_until')
                if cooldown_str:
                    try:
                        self.game_state.work_cooldown = datetime.fromisoformat(cooldown_str.replace('Z', '+00:00'))
                    except:
                        self.game_state.work_cooldown = None
                else:
                    self.game_state.work_cooldown = None
            
            # Get ship limits
            limits_result = await self.tool_caller.execute_tool(
                GameTool.GET_SHIP_LIMITS, self.credentials
            )
            if limits_result.success:
                self.game_state.ship_limits = limits_result.data
            
            # Get available opponents
            opponents_result = await self.tool_caller.execute_tool(
                GameTool.LIST_OPPONENTS, self.credentials
            )
            if opponents_result.success:
                self.game_state.available_opponents = opponents_result.data or []
            
            logger.info(f"{self.credentials.nickname} updated game state - Credits: {self.game_state.credits}, Level: {self.game_state.level}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update game state for {self.credentials.nickname}: {str(e)}")
            return False
    
    def _build_context_prompt(self) -> str:
        """Build context prompt with current game state"""
        context = f"""
=== CURRENT GAME STATE ===
Your Name: {self.credentials.nickname}
Credits: {self.game_state.credits}
Level: {self.game_state.level}
Rank: {self.game_state.rank}
ELO: {self.game_state.elo:.1f}

Active Ships: {len(self.game_state.active_ships)}
"""
        
        # Add ship details
        if self.game_state.active_ships:
            context += "\nShip Details:\n"
            for ship in self.game_state.active_ships:
                hp_percent = (ship.get('actual_hp', 0) / ship.get('base_hp', 1)) * 100
                context += f"- Ship #{ship.get('ship_number')}: {ship.get('ship_name')} (HP: {hp_percent:.1f}%)\n"
        
        # Add work cooldown
        if self.game_state.work_cooldown:
            if self.game_state.work_cooldown > datetime.now():
                remaining = self.game_state.work_cooldown - datetime.now()
                context += f"\nWork Cooldown: {remaining.total_seconds()/60:.1f} minutes remaining"
            else:
                context += f"\nWork: Available"
        else:
            context += f"\nWork: Available"
        
        # Add opponents
        if self.game_state.available_opponents:
            context += f"\n\nAvailable Opponents: {len(self.game_state.available_opponents)}"
            # Show top 3 opponents for context
            for i, opp in enumerate(self.game_state.available_opponents[:3]):
                context += f"\n- {opp.get('nickname', 'Unknown')} (Level {opp.get('level', 1)}, ELO {opp.get('elo', 1000):.1f})"
        
        return context
    
    def _build_simplified_context(self) -> str:
        """Build a simplified context prompt for small models"""
        context = f"Credits: {self.game_state.credits}, Level: {self.game_state.level}"
        
        if self.game_state.active_ships:
            context += f", Ships: {len(self.game_state.active_ships)}"
        
        if self.game_state.available_opponents:
            context += f", Opponents: {len(self.game_state.available_opponents)}"
        
        return context
    
    def _get_personality_prompt(self) -> str:
        """Get personality-specific prompt"""
        if self.personality.llm_type == "aggressive":
            return get_aggressive_prompt("personality")
        elif self.personality.llm_type == "defensive":
            return get_defensive_prompt("personality")
        elif self.personality.llm_type == "tactical":
            return get_tactical_prompt("personality")
        else:
            return ""
    
    async def make_decision(self) -> Optional[Dict[str, Any]]:
        """Make a decision using the LLM"""
        try:
            # Build a simplified prompt for small models
            context_prompt = self._build_simplified_context()
            
            # Simple game flow explanation
            game_flow = """
GAME FLOW:
1. Work to earn credits (perform_work)
2. Buy a ship (buy_ship)
3. Activate ship (activate_ship) 
4. Battle other players (engage_battle)
"""
            
            # Determine best action based on current state
            if self.game_state.credits < 1000 and len(self.game_state.active_ships) == 0:
                suggestion = "You need credits to buy a ship. Try: perform_work"
            elif len(self.game_state.active_ships) == 0:
                suggestion = "You need a ship to battle. Try: buy_ship"
            elif self.game_state.available_opponents and len(self.game_state.available_opponents) > 0:
                suggestion = "You have ships and opponents available. Try: engage_battle"
            else:
                suggestion = "Check your status. Try: get_my_status"
            
            decision_prompt = f"""
{game_flow}

Current state: {context_prompt}

{suggestion}

Choose ONE action:
- get_my_status
- perform_work  
- buy_ship
- activate_ship
- engage_battle

Answer with just the action name:
"""
            
            full_prompt = decision_prompt
            
            # Generate response
            response = self.llm_manager.generate_response(
                self.personality.llm_type, 
                full_prompt,
                temperature=self.personality.risk_tolerance * 0.5 + 0.3  # Dynamic temperature
            )
            
            if not response:
                logger.error(f"No response from LLM for {self.credentials.nickname}")
                # Use fallback decision making
                fallback_decision = self._make_fallback_decision()
                if fallback_decision:
                    logger.info(f"Using fallback decision for {self.credentials.nickname}")
                    return fallback_decision
                return None
            
            # Parse the response
            decision = self._parse_decision(response)
            
            if decision:
                # Add to history
                self.decision_history.append({
                    "round": self.round_count,
                    "timestamp": datetime.now().isoformat(),
                    "decision": decision,
                    "llm_response": response[:200] + "..." if len(response) > 200 else response
                })
                
                logger.info(f"{self.credentials.nickname} decided: {decision['action']} - {decision['reason']}")
            
            return decision
            
        except Exception as e:
            logger.error(f"Decision making failed for {self.credentials.nickname}: {str(e)}")
            return None
    
    def _parse_decision(self, llm_response: str) -> Optional[Dict[str, Any]]:
        """Parse LLM response to extract decision"""
        try:
            # Simple parsing - just look for the action name
            response = llm_response.strip().lower()
            
            # Map common responses to actions
            action_map = {
                'get_my_status': 'get_my_status',
                'status': 'get_my_status',
                'check': 'get_my_status',
                'perform_work': 'perform_work', 
                'work': 'perform_work',
                'buy_ship': 'buy_ship',
                'buy': 'buy_ship',
                'ship': 'buy_ship',
                'activate_ship': 'activate_ship',
                'activate': 'activate_ship',
                'engage_battle': 'engage_battle',
                'battle': 'engage_battle',
                'fight': 'engage_battle'
            }
            
            # Find matching action
            action = None
            for keyword, mapped_action in action_map.items():
                if keyword in response:
                    action = mapped_action
                    break
            
            if not action:
                logger.warning(f"No action found in LLM response: {llm_response}")
                return None
            
            decision = {
                'action': action,
                'parameters': {},
                'reason': 'AI decision'
            }
            
            # Auto-add parameters for specific actions
            decision = self._add_default_parameters(decision)
            
            return decision
            
        except Exception as e:
            logger.error(f"Failed to parse decision from response '{llm_response}': {str(e)}")
            return None
    
    def _extract_action_from_text(self, text: str) -> Optional[str]:
        """Try to extract action from free-form text"""
        text_lower = text.lower()
        
        # Look for action keywords
        if 'status' in text_lower or 'check' in text_lower:
            return 'get_my_status'
        elif 'work' in text_lower:
            return 'perform_work'
        elif 'buy' in text_lower or 'ship' in text_lower:
            return 'buy_ship'
        elif 'battle' in text_lower or 'fight' in text_lower:
            return 'engage_battle'
        
        return None
    
    def _add_default_parameters(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Add default parameters for actions that need them"""
        action = decision.get('action', '')
        
        if action == 'buy_ship' and not decision['parameters']:
            decision['parameters'] = {'ship_id': 1}  # Buy cheapest ship
        elif action == 'activate_ship' and not decision['parameters']:
            # Find first owned inactive ship to activate
            owned_ships = [ship for ship in self.game_state.fleet if ship.get('status') == 'owned']
            if owned_ships:
                decision['parameters'] = {'ship_number': owned_ships[0].get('ship_number')}
            else:
                # No ships to activate, fallback to buying
                decision['action'] = 'buy_ship'
                decision['parameters'] = {'ship_id': 1}
        elif action == 'engage_battle' and not decision['parameters']:
            if self.game_state.available_opponents and self.game_state.active_ships:
                opponent = self.game_state.available_opponents[0]
                formations = ["AGGRESSIVE", "DEFENSIVE", "TACTICAL"]
                formation = formations[hash(self.personality_name) % len(formations)]
                
                decision['parameters'] = {
                    'opponent_id': opponent.get('user_id'),
                    'formation': formation,
                    'ship_numbers': [ship.get('ship_number') for ship in self.game_state.active_ships[:3]]
                }
        
        return decision
    
    def _parse_simple_params(self, params_str: str) -> Dict[str, Any]:
        """Parse simple parameter format"""
        params = {}
        if not params_str or params_str.lower() in ['none', 'null', '{}']:
            return params
        
        # Look for common patterns
        if 'ship_id=' in params_str:
            match = re.search(r'ship_id=(\d+)', params_str)
            if match:
                params['ship_id'] = int(match.group(1))
        
        if 'ship_number=' in params_str:
            match = re.search(r'ship_number=(\d+)', params_str)
            if match:
                params['ship_number'] = int(match.group(1))
        
        if 'opponent_id=' in params_str:
            match = re.search(r'opponent_id=(\d+)', params_str)
            if match:
                params['opponent_user_id'] = int(match.group(1))
        
        return params
    
    async def execute_decision(self, decision: Dict[str, Any]) -> ToolResult:
        """Execute a decision using the game tools"""
        try:
            action = decision['action']
            parameters = decision.get('parameters', {})
            
            # Map action names to GameTool enums
            tool_mapping = {
                'get_my_status': GameTool.GET_MY_STATUS,
                'get_fleet_status': GameTool.GET_FLEET_STATUS,
                'list_opponents': GameTool.LIST_OPPONENTS,
                'get_work_status': GameTool.GET_WORK_STATUS,
                'get_ship_limits': GameTool.GET_SHIP_LIMITS,
                'perform_work': GameTool.PERFORM_WORK,
                'buy_ship': GameTool.BUY_SHIP,
                'repair_ship': GameTool.REPAIR_SHIP,
                'activate_ship': GameTool.ACTIVATE_SHIP,
                'deactivate_ship': GameTool.DEACTIVATE_SHIP,
                'engage_battle': GameTool.ENGAGE_BATTLE
            }
            
            if action not in tool_mapping:
                return ToolResult(success=False, error=f"Unknown action: {action}")
            
            tool = tool_mapping[action]
            
            # Execute the tool
            result = await self.tool_caller.execute_tool(tool, self.credentials, **parameters)
            
            self.last_action_time = datetime.now()
            
            logger.info(f"{self.credentials.nickname} executed {action} - Success: {result.success}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to execute decision: {str(e)}"
            logger.error(error_msg)
            return ToolResult(success=False, error=error_msg)
    
    async def play_round(self) -> bool:
        """Play one round of the game"""
        try:
            self.round_count += 1
            logger.info(f"{self.credentials.nickname} starting round {self.round_count}")
            
            # Update game state
            if not await self.update_game_state():
                logger.error(f"Failed to update game state for {self.credentials.nickname}")
                return False
            
            # Make decision
            decision = await self.make_decision()
            if not decision:
                logger.error(f"Failed to make decision for {self.credentials.nickname}")
                return False
            
            # Execute decision
            result = await self.execute_decision(decision)
            
            # Log result
            if result.success:
                logger.info(f"{self.credentials.nickname} round {self.round_count} completed successfully")
            else:
                logger.warning(f"{self.credentials.nickname} round {self.round_count} failed: {result.error}")
            
            return result.success
            
        except Exception as e:
            logger.error(f"Round failed for {self.credentials.nickname}: {str(e)}")
            return False
    
    def _make_fallback_decision(self) -> Optional[Dict[str, Any]]:
        """Make a simple fallback decision when LLM fails"""
        import random
        
        try:
            # Simple decision logic based on game state
            if self.game_state.credits < 100:
                # Low credits - try to work
                return {
                    "action": "perform_work",
                    "parameters": {},
                    "reason": "Fallback: Need credits"
                }
            elif len(self.game_state.active_ships) == 0:
                # No ships - try to get status or buy ship
                if self.game_state.credits >= 500:
                    return {
                        "action": "buy_ship",
                        "parameters": {"ship_id": 1},  # Buy cheapest ship
                        "reason": "Fallback: Need ships"
                    }
                else:
                    return {
                        "action": "get_my_status",
                        "parameters": {},
                        "reason": "Fallback: Check status"
                    }
            elif self.game_state.available_opponents:
                # Have ships and opponents - try to battle
                opponent = random.choice(self.game_state.available_opponents)
                formations = ["AGGRESSIVE", "DEFENSIVE", "TACTICAL"]
                formation = formations[hash(self.personality_name) % len(formations)]
                
                return {
                    "action": "engage_battle",
                    "parameters": {
                        "opponent_id": opponent.get('user_id'),
                        "formation": formation,
                        "ship_numbers": [ship.get('ship_number') for ship in self.game_state.active_ships[:3]]
                    },
                    "reason": "Fallback: Battle available opponent"
                }
            else:
                # Default to getting status
                return {
                    "action": "get_my_status",
                    "parameters": {},
                    "reason": "Fallback: Refresh status"
                }
                
        except Exception as e:
            logger.error(f"Fallback decision failed for {self.credentials.nickname}: {str(e)}")
            # Ultimate fallback
            return {
                "action": "get_my_status",
                "parameters": {},
                "reason": "Ultimate fallback: Check status"
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            "nickname": self.credentials.nickname,
            "personality": self.personality_name,
            "round_count": self.round_count,
            "level": self.game_state.level,
            "rank": self.game_state.rank,
            "credits": self.game_state.credits,
            "elo": self.game_state.elo,
            "active_ships": len(self.game_state.active_ships),
            "decisions_made": len(self.decision_history),
            "last_action": self.last_action_time.isoformat() if self.last_action_time else None
        }
