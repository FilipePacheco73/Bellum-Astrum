"""
Match Orchestrator - Coordinates matches between AI agents.
"""

import asyncio
import logging
import time
import httpx
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional
from AI_Agents.core.ai_agent import AIAgent
from AI_Agents.core.tool_caller import AICredentials, try_login
from AI_Agents.config.logging_config import log_ai_decision

logger = logging.getLogger(__name__)

class MatchType(Enum):
    """Available match types"""
    AI_VS_AI = "ai_vs_ai"
    AI_VS_HUMAN = "ai_vs_human"
    TOURNAMENT = "tournament"
    TRAINING = "training"
    CONTINUOUS = "continuous"

@dataclass
class AgentConfig:
    """Configuration for an AI agent"""
    agent_type: str  # 'aggressive', 'defensive', 'tactical'
    email: str
    password: str
    nickname: str
    
@dataclass
class MatchConfig:
    """Match configuration"""
    match_type: MatchType
    agents: List[AgentConfig] = None
    max_rounds: int = 100
    round_delay: float = 2.0
    max_concurrent_agents: int = 3
    enable_learning: bool = True
    save_logs: bool = True
    
    def __post_init__(self):
        if self.agents is None:
            self.agents = []
            
class MatchOrchestrator:
    """Orchestrates matches between AI agents"""
    
    def __init__(self, config: MatchConfig):
        self.config = config
        self.agents: List[AIAgent] = []
        self.match_history: List[Dict[str, Any]] = []
        self.current_round = 0
        self.is_running = False
        self.ai_logger = None  # Will be set by the runner
        
        # Event callbacks
        self.on_round_complete = None
        self.on_match_complete = None
        
    async def initialize_agents(self) -> bool:
        """Initializes all match agents"""
        try:
            for agent_config in self.config.agents:
                # First authenticate the agent
                credentials = await self._authenticate_agent(agent_config)
                if not credentials:
                    logger.error(f"Failed to authenticate {agent_config.nickname}")
                    return False
                
                # Create agent (LLM is loaded automatically in constructor)
                agent = AIAgent(agent_config.agent_type, credentials)
                self.agents.append(agent)
                logger.info(f"Agent {agent_config.nickname} ({agent_config.agent_type}) initialized")
                
            return True
            
        except Exception as e:
            logger.error(f"Error initializing agents: {e}")
            return False
    
    async def _authenticate_agent(self, agent_config: AgentConfig) -> Optional[AICredentials]:
        """Authenticates an agent using email/password"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                credentials = await try_login(client, agent_config.email, agent_config.password)
                if credentials:
                    logger.info(f"Agent {agent_config.nickname} authenticated successfully")
                    return credentials
                else:
                    logger.error(f"Authentication failed for agent {agent_config.nickname}")
                    return None
        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            return None
    
    async def run_match(self) -> Dict[str, Any]:
        """Executes a complete match"""
        logger.info("Starting match...")
        
        if not await self.initialize_agents():
            raise RuntimeError("Failed to initialize agents")
        
        match_start_time = time.time()
        
        try:
            for round_num in range(1, self.config.max_rounds + 1):
                self.current_round = round_num
                logger.info(f"--- Round {round_num} ---")
                
                round_results = await self._execute_round()
                self.match_history.append({
                    "round": round_num,
                    "timestamp": time.time(),
                    "results": round_results
                })
                
                # Call round complete callback
                if self.on_round_complete:
                    await self.on_round_complete(round_num, round_results)
                
                # Delay between rounds
                if round_num < self.config.max_rounds:
                    await asyncio.sleep(self.config.round_delay)
                    
        except Exception as e:
            logger.error(f"Error during match: {e}")
            
        match_duration = time.time() - match_start_time
        
        match_summary = {
            "match_type": self.config.match_type.value,
            "total_rounds": self.current_round,
            "duration_seconds": match_duration,
            "agents": [{"nickname": config.nickname, "type": config.agent_type} 
                      for config in self.config.agents],
            "history": self.match_history
        }
        
        logger.info(f"Match completed after {self.current_round} rounds")
        return match_summary
    
    async def _execute_round(self) -> Dict[str, Any]:
        """Executes a match round"""
        round_results = {}
        
        for i, agent in enumerate(self.agents):
            agent_config = self.config.agents[i]
            
            try:
                logger.info(f"Turn for agent {agent_config.nickname}")
                
                # Agent makes a decision
                decision = await agent.make_decision()
                
                # Detailed decision log in ai_decisions.log
                if self.ai_logger and decision:
                    action = decision.get('action', 'UNKNOWN')
                    reason = decision.get('reason', 'No reason provided')
                    parameters = decision.get('parameters', {})
                    
                    # Create context for log
                    log_context = {
                        'action': action,
                        'agent_type': agent_config.agent_type,
                        'reason': reason
                    }
                    
                    # Add parameters if they exist
                    if parameters:
                        for key, value in parameters.items():
                            log_context[f'param_{key}'] = value
                    
                    log_ai_decision(
                        self.ai_logger,
                        agent_config.nickname,
                        self.current_round,
                        f"DECISION: {action}",
                        log_context
                    )
                elif self.ai_logger:
                    # Log when there's no decision
                    log_ai_decision(
                        self.ai_logger,
                        agent_config.nickname,
                        self.current_round,
                        "DECISION: NO_ACTION",
                        {'agent_type': agent_config.agent_type, 'reason': 'Failed to make decision'}
                    )
                
                round_results[agent_config.nickname] = {
                    "agent_type": agent_config.agent_type,
                    "decision": decision,
                    "success": decision is not None
                }
                
                # Simplified log in debug (without prompt details)
                if decision:
                    logger.info(f"{agent_config.nickname} -> {decision.get('action', 'NO_ACTION')}")
                else:
                    logger.info(f"{agent_config.nickname} -> NO_ACTION (failed)")
                
            except Exception as e:
                logger.error(f"Error in turn for {agent_config.nickname}: {e}")
                
                # Log error in ai_decisions.log
                if self.ai_logger:
                    log_ai_decision(
                        self.ai_logger,
                        agent_config.nickname,
                        self.current_round,
                        "DECISION: ERROR",
                        {'agent_type': agent_config.agent_type, 'error': str(e)}
                    )
                
                round_results[agent_config.nickname] = {
                    "agent_type": agent_config.agent_type,
                    "decision": None,
                    "success": False,
                    "error": str(e)
                }
        
        return round_results
    
    def get_match_stats(self) -> Dict[str, Any]:
        """Returns match statistics"""
        if not self.match_history:
            return {"error": "No match executed"}
        
        stats = {
            "total_rounds": len(self.match_history),
            "agents": {}
        }
        
        for agent_config in self.config.agents:
            agent_name = agent_config.nickname
            successful_decisions = sum(1 for round_data in self.match_history 
                                     if round_data["results"].get(agent_name, {}).get("success", False))
            
            stats["agents"][agent_name] = {
                "type": agent_config.agent_type,
                "successful_decisions": successful_decisions,
                "success_rate": successful_decisions / len(self.match_history) if self.match_history else 0
            }
        
        return stats
    
    async def add_agent(self, agent_config: AgentConfig) -> bool:
        """Adds an agent to the match"""
        try:
            self.config.agents.append(agent_config)
            logger.info(f"Agent {agent_config.nickname} added to match")
            return True
        except Exception as e:
            logger.error(f"Error adding agent: {e}")
            return False
    
    async def start_match(self) -> bool:
        """Starts the match"""
        try:
            self.is_running = True
            result = await self.run_match()
            
            if self.on_match_complete:
                await self.on_match_complete(result)
            
            return True
        except Exception as e:
            logger.error(f"Error starting match: {e}")
            return False
    
    def stop_match(self):
        """Stops the match"""
        self.is_running = False
        logger.info("Match interrupted")
    
    def get_live_stats(self) -> Dict[str, Any]:
        """Returns live match statistics"""
        return {
            "current_round": self.current_round,
            "total_agents": len(self.config.agents),
            "is_running": self.is_running,
            "match_type": self.config.match_type.value
        }
    
    def get_agent_rankings(self) -> List[Dict[str, Any]]:
        """Returns agent rankings"""
        rankings = []
        stats = self.get_match_stats()
        
        if "agents" in stats:
            for agent_name, agent_stats in stats["agents"].items():
                rankings.append({
                    "name": agent_name,
                    "type": agent_stats.get("type", "unknown"),
                    "success_rate": agent_stats.get("success_rate", 0),
                    "successful_decisions": agent_stats.get("successful_decisions", 0)
                })
        
        # Sort by success rate
        rankings.sort(key=lambda x: x["success_rate"], reverse=True)
        return rankings
