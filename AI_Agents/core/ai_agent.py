"""
AI Agent - Base class for autonomous AI players in Bellum Astrum.
"""

import asyncio
import logging
import json
import re
import random
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from pathlib import Path

from AI_Agents.core.llm_manager import get_llm_manager
from AI_Agents.core.tool_caller import GameToolCaller, GameTool, ToolResult, AICredentials
from AI_Agents.core.file_memory import FileBasedMemory
from AI_Agents.prompts.decision_prompts import get_decision_prompt, parse_ai_decision

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
    
    def __init__(self, agent_type: str, credentials: AICredentials):
        """
        Initialize AI Agent
        agent_type: 'aggressive', 'defensive', or 'tactical'
        """
        self.agent_type = agent_type.lower()
        self.credentials = credentials
        self.tool_caller = GameToolCaller()
        self.llm_manager = get_llm_manager()
        self.game_state = GameState()
        
        # Initialize memory system
        memories_dir = Path("AI_Agents/memories")
        self.memory = FileBasedMemory(credentials.nickname, memories_dir)
        
        # Decision tracking
        self.decision_history: List[Dict] = []
        self.round_count = 0
        self.last_action_time = None
        self.last_action = None  # Track the type of action taken
        self.last_decision = None  # Track the decision made
        
        # Load the appropriate LLM model
        self._load_model()
    
    def _load_model(self):
        """Load the LLM model (or reuse shared model)"""
        # Use the personality type as the model type
        model_type = self.agent_type
        if not self.llm_manager.is_model_loaded(model_type):
            logger.info(f"Loading/sharing model for {self.agent_type}...")
            success = self.llm_manager.load_model(model_type)
            if not success:
                logger.error(f"Failed to load model for {self.agent_type}")
                raise RuntimeError(f"Could not load LLM model for {model_type}")
        else:
            logger.info(f"Model for {self.agent_type} already loaded/shared")
    
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
    
    async def make_decision(self) -> Optional[Dict[str, Any]]:
        """
        Make a decision using the LLM
        
        IMPORTANT: The first round (round_count == 1) ALWAYS forces a get_my_status() call
        to ensure the AI understands its current situation before making any other decisions.
        """
        try:
            # Increment round count
            self.round_count += 1
            
            # FORCE STATUS CHECK ON FIRST ROUND
            if self.round_count == 1:
                logger.info(f"{self.credentials.nickname} - First round: forcing status check")
                decision = {
                    'action': 'get_my_status',
                    'reason': 'First round mandatory status check',
                    'parameters': {}
                }
                
                # Save mandatory first decision to memory
                self.memory.store_decision(
                    self.round_count,
                    decision['action'],
                    decision['reason'],
                    success=True,
                    input_tokens=0,  # No LLM used for mandatory decision
                    output_tokens=0,
                    ai_reasoning="Mandatory first round status check"
                )
                
                # Add to history
                self.decision_history.append({
                    "round": self.round_count,
                    "timestamp": datetime.now().isoformat(),
                    "decision": decision,
                    "llm_response": "FORCED_FIRST_STATUS_CHECK"
                })
                
                return decision
            
            # Build current game state context
            context_prompt = self._build_simplified_context()
            
            # Get recent memories
            memory_summary = self.memory.get_memory_summary(max_rounds=3)
            
            # Generate decision prompt using centralized template (now includes personality automatically)
            decision_prompt = get_decision_prompt(
                memory_summary=memory_summary,
                context_prompt=context_prompt,
                agent_type=self.agent_type
            )
            
            logger.debug(f"Sending prompt to LLM for {self.credentials.nickname}")
            
            # Generate response with detailed reasoning
            llm_response = self.llm_manager.generate_response(
                self.agent_type, 
                decision_prompt,
                temperature=0.5  # Lower temperature for more consistent responses
            )
            
            # LLM manager now always returns an LLMResponse, even on failure
            response_text = llm_response.text if llm_response and llm_response.text else None
            input_tokens = llm_response.input_tokens if llm_response else 0
            output_tokens = llm_response.output_tokens if llm_response else 0
            ai_reasoning = llm_response.reasoning if llm_response else ""
            
            logger.debug(f"Received response from LLM for {self.credentials.nickname}: {response_text or 'EMPTY'} (tokens: {input_tokens}→{output_tokens})")
            
            if not response_text:
                logger.error(f"No response from LLM for {self.credentials.nickname}")
                # Save failed decision to memory
                self.memory.store_decision(
                    self.round_count, 
                    "NO_ACTION", 
                    "LLM failed to generate response",
                    success=False,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    ai_reasoning="LLM generation failed"
                )
                
                # Use fallback decision making
                fallback_decision = self._make_fallback_decision()
                if fallback_decision:
                    logger.info(f"Using fallback decision for {self.credentials.nickname}: {fallback_decision['action']}")
                    # Save fallback decision to memory
                    self.memory.store_decision(
                        self.round_count,
                        fallback_decision['action'],
                        f"Fallback: {fallback_decision['reason']}",
                        success=True,
                        input_tokens=0,
                        output_tokens=0,
                        ai_reasoning=f"Fallback reasoning: {fallback_decision['reason']}"
                    )
                    return fallback_decision
                return None
            
            # Parse the response
            decision = self._parse_decision(response_text)
            
            if decision:
                # Store the decision for tracking
                self.last_decision = decision
                
                # Save decision to memory with token information and AI reasoning
                self.memory.store_decision(
                    self.round_count,
                    decision['action'],
                    decision['reason'],
                    success=True,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    ai_reasoning=ai_reasoning
                )
                
                # Add to history
                self.decision_history.append({
                    "round": self.round_count,
                    "timestamp": datetime.now().isoformat(),
                    "decision": decision,
                    "llm_response": response_text[:200] + "..." if len(response_text) > 200 else response_text,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "ai_reasoning": ai_reasoning
                })
                
                # Log only the final decision with token info
                logger.debug(f"{self.credentials.nickname} -> {decision['action']}: {ai_reasoning[:100]} (tokens: {input_tokens}→{output_tokens})")
            else:
                # Save failed parsing to memory
                self.memory.store_decision(
                    self.round_count,
                    "PARSE_FAILED",
                    f"Could not understand LLM response: {response_text[:50]}...",
                    success=False,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    ai_reasoning=f"Parse failed for response: {response_text}"
                )
            
            return decision
            
        except Exception as e:
            logger.error(f"Decision making failed for {self.credentials.nickname}: {str(e)}")
            return None
    
    def _parse_decision(self, llm_response: str) -> Optional[Dict[str, Any]]:
        """Parse LLM response to extract decision and reasoning"""
        try:
            # Use the centralized parsing function
            decision = parse_ai_decision(llm_response)
            
            if decision:
                # Auto-add parameters for specific actions
                decision = self._add_default_parameters(decision)
                return decision
            else:
                logger.debug(f"No valid decision found in LLM response from {self.credentials.nickname}")
                return None
            
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
                formation = formations[hash(self.agent_type) % len(formations)]
                
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
            
            # Track the action taken
            self.last_action = action
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
            logger.info(f"{self.credentials.nickname} starting round {self.round_count + 1}")
            
            # Update game state
            if not await self.update_game_state():
                logger.error(f"Failed to update game state for {self.credentials.nickname}")
                return False
            
            # Make decision (this will increment round_count)
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
                formation = formations[hash(self.agent_type) % len(formations)]
                
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
            "personality": self.agent_type,
            "round_count": self.round_count,
            "level": self.game_state.level,
            "rank": self.game_state.rank,
            "credits": self.game_state.credits,
            "elo": self.game_state.elo,
            "active_ships": len(self.game_state.active_ships),
            "decisions_made": len(self.decision_history),
            "last_action": self.last_action_time.isoformat() if self.last_action_time else None
        }
