"""
Match Orchestrator - Manages AI vs AI matches and tournaments in Bellum Astrum.
"""

import asyncio
import logging
import random
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json

from AI_Agents.core.ai_agent import AIAgent, AICredentials
from AI_Agents.core.tool_caller import authenticate_ai_agent
from AI_Agents.core.file_memory import FileBasedMemory, AgentAction
from AI_Agents.config.ai_personalities import get_personality, list_personalities
from AI_Agents.config.logging_config import log_ai_decision, log_ai_tool_usage, log_match_event

logger = logging.getLogger('bellum.debug')

class MatchType(Enum):
    """Types of matches"""
    FREE_FOR_ALL = "free_for_all"
    ROUND_ROBIN = "round_robin" 
    TOURNAMENT = "tournament"
    CONTINUOUS = "continuous"
    TRAINING = "training"

class MatchStatus(Enum):
    """Status of a match"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class MatchConfig:
    """Configuration for a match"""
    match_type: MatchType
    max_rounds: int = 100
    round_delay: float = 2.0  # Seconds between rounds
    max_concurrent_agents: int = 5
    allow_same_personality: bool = False
    enable_learning: bool = True
    save_logs: bool = True
    auto_restart: bool = False

@dataclass 
class AgentConfig:
    """Configuration for an AI agent in a match"""
    personality_name: str
    email: str
    password: str
    nickname: str = ""
    enabled: bool = True

@dataclass
class MatchStats:
    """Statistics for a match"""
    start_time: datetime
    end_time: Optional[datetime] = None
    total_rounds: int = 0
    total_battles: int = 0
    agent_stats: Dict[str, Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.agent_stats is None:
            self.agent_stats = {}

class MatchOrchestrator:
    """Orchestrates AI vs AI matches"""
    
    def __init__(self, config: MatchConfig):
        self.config = config
        self.agents: Dict[str, AIAgent] = {}
        self.credentials: Dict[str, AICredentials] = {}
        self.memories: Dict[str, FileBasedMemory] = {}
        self.status = MatchStatus.PENDING
        self.stats = MatchStats(start_time=datetime.now())
        self.current_round = 0
        self.running = False
        
        # Get AI decisions logger
        self.ai_logger = logging.getLogger('bellum.ai_decisions')
        
        # Event hooks
        self.on_round_complete = None
        self.on_battle_complete = None
        self.on_match_complete = None
        
    async def add_agent(self, agent_config: AgentConfig) -> bool:
        """Add an AI agent to the match"""
        try:
            # Authenticate the agent
            credentials = await authenticate_ai_agent(agent_config.email, agent_config.password)
            if not credentials:
                logger.error(f"Failed to authenticate agent {agent_config.email}")
                return False
            
            # Use provided nickname or fallback to credentials nickname
            nickname = agent_config.nickname or credentials.nickname
            
            # Create AI agent
            agent = AIAgent(agent_config.personality_name, credentials)
            
            # Create file-based memory manager
            from pathlib import Path
            memories_dir = Path(__file__).parent.parent / "memories"
            memory = FileBasedMemory(nickname, memories_dir)
            
            # Store references
            self.agents[nickname] = agent
            self.credentials[nickname] = credentials  
            self.memories[nickname] = memory
            
            # Initialize stats
            self.stats.agent_stats[nickname] = {
                "personality": agent_config.personality_name,
                "rounds_played": 0,
                "battles_won": 0,
                "battles_lost": 0,
                "total_credits_earned": 0,
                "total_xp_gained": 0,
                "elo_change": 0.0,
                "ships_purchased": 0,
                "ships_lost": 0,
                "work_sessions": 0,
                "avg_credits_per_round": 0.0,
                "win_rate": 0.0
            }
            
            logger.info(f"Added AI agent {nickname} ({agent_config.personality_name})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add agent {agent_config.email}: {str(e)}")
            return False
    
    async def start_match(self) -> bool:
        """Start the AI vs AI match"""
        try:
            if len(self.agents) < 2:
                logger.error("Need at least 2 agents to start a match")
                log_match_event(self.ai_logger, "MATCH_START_FAILED", {"reason": "Insufficient agents"})
                return False
            
            self.status = MatchStatus.RUNNING
            self.running = True
            self.stats.start_time = datetime.now()
            
            # Log match start
            agent_list = list(self.agents.keys())
            log_match_event(self.ai_logger, "MATCH_STARTED", {
                "match_type": self.config.match_type.value,
                "max_rounds": self.config.max_rounds,
                "agents": agent_list,
                "agent_count": len(agent_list)
            })
            
            logger.info(f"Starting {self.config.match_type.value} match with {len(self.agents)} agents")
            
            # Start the main match loop
            await self._run_match_loop()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start match: {str(e)}")
            self.status = MatchStatus.ERROR
            return False
    
    async def _run_match_loop(self):
        """Main match execution loop"""
        try:
            while self.running and self.current_round < self.config.max_rounds:
                self.current_round += 1
                logger.info(f"=== ROUND {self.current_round} ===")
                
                # Play one round for all agents
                await self._play_round()
                
                # Update statistics
                await self._update_stats()
                
                # Check for match completion conditions
                if await self._check_completion_conditions():
                    break
                
                # Call round complete hook
                if self.on_round_complete:
                    await self.on_round_complete(self.current_round, self.stats)
                
                # Delay between rounds
                await asyncio.sleep(self.config.round_delay)
            
            # Match completed
            await self._finish_match()
            
        except Exception as e:
            logger.error(f"Match loop error: {str(e)}")
            self.status = MatchStatus.ERROR
    
    async def _play_round(self):
        """Play one round where each agent takes one action"""
        # Create tasks for all agents to play simultaneously
        tasks = []
        
        for nickname, agent in self.agents.items():
            if self.stats.agent_stats[nickname].get("enabled", True):
                task = asyncio.create_task(self._play_agent_round(nickname, agent))
                tasks.append(task)
        
        # Wait for all agents to complete their round
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Log any exceptions
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    agent_name = list(self.agents.keys())[i]
                    logger.error(f"Agent {agent_name} failed in round {self.current_round}: {str(result)}")
    
    async def _play_agent_round(self, nickname: str, agent: AIAgent) -> bool:
        """Play one round for a specific agent"""
        try:
            # Log round start for agent
            log_ai_decision(
                self.ai_logger, nickname, self.current_round,
                "ROUND_START", 
                {"action": "Updating game state"}
            )
            
            # Update agent's game state first
            if not await agent.update_game_state():
                logger.warning(f"Failed to update game state for {nickname}")
                log_ai_tool_usage(
                    self.ai_logger, nickname, self.current_round,
                    "UPDATE_GAME_STATE", {}, False, {"reason": "Game state update failed"}
                )
                return False
            
            # Get memory-enhanced context
            memory = self.memories[nickname]
            context = await self._build_enhanced_context(agent, memory)
            
            # Log game state before decision
            game_state = {
                "credits": getattr(agent.game_state, 'credits', 'unknown'),
                "level": getattr(agent.game_state, 'level', 'unknown'),
                "health": getattr(agent.game_state, 'health', 'unknown'),
                "energy": getattr(agent.game_state, 'energy', 'unknown')
            }
            
            log_ai_decision(
                self.ai_logger, nickname, self.current_round,
                "DECISION_MAKING", game_state
            )
            
            # Agent makes decision based on enhanced context
            success = await agent.play_round()
            
            # Log the action result
            action_taken = getattr(agent, 'last_action', 'unknown_action')
            log_ai_tool_usage(
                self.ai_logger, nickname, self.current_round,
                action_taken, {}, success, game_state
            )
            
            # Store action in memory if enabled
            if self.config.enable_learning and hasattr(agent, 'last_decision'):
                await self._store_action_memory(nickname, agent, success)
            
            # Update agent stats
            self._update_agent_round_stats(nickname, agent, success)
            
            return success
            
        except Exception as e:
            logger.error(f"Error in agent round for {nickname}: {str(e)}")
            return False
    
    async def _build_enhanced_context(self, agent: AIAgent, memory: FileBasedMemory) -> Dict[str, Any]:
        """Build enhanced context with memory data for better decision making"""
        memory_summary = memory.get_memory_summary(hours=4)
        
        context = {
            "recent_actions": memory_summary.get("last_actions", []),
            "work_success_rate": memory.get_tool_success_rate("work"),
            "battle_success_rate": memory.get_tool_success_rate("battle"),
            "avg_work_income": memory.get_average_credits_per_work(),
            "battle_performance": memory_summary.get("battle_performance", {}),
            "tool_usage": memory_summary.get("tool_usage", {})
        }
        
        return context
    
    async def _store_action_memory(self, nickname: str, agent: AIAgent, success: bool):
        """Store the agent's action in memory for learning"""
        try:
            memory = self.memories[nickname]
            
            # Get the last decision (this would need to be stored in AIAgent)
            if hasattr(agent, 'last_decision') and agent.last_decision:
                decision = agent.last_decision
                
                # Get tool name from decision
                tool_name = decision.get('action', 'unknown')
                tool_params = decision.get('parameters', {})
                
                # Get game state before and after
                game_state_before = getattr(agent, 'game_state_before', {})
                game_state_after = agent.game_state.__dict__.copy() if hasattr(agent, 'game_state') else {}
                
                # Create action record
                action = AgentAction(
                    timestamp=datetime.now().isoformat(),
                    round_number=self.current_round,
                    tool_name=tool_name,
                    tool_params=tool_params,
                    game_state_before=game_state_before,
                    game_state_after=game_state_after,
                    success=success,
                    result_data={"round": self.current_round},
                    reasoning=decision.get('reasoning', '')
                )
                
                memory.store_action(action)
                
        except Exception as e:
            logger.error(f"Failed to store action memory for {nickname}: {str(e)}")
    
    def _update_agent_round_stats(self, nickname: str, agent: AIAgent, success: bool):
        """Update statistics for an agent after a round"""
        stats = self.stats.agent_stats[nickname]
        stats["rounds_played"] += 1
        
        # Update based on agent's current state
        if hasattr(agent.game_state, 'credits'):
            stats["total_credits_earned"] = agent.game_state.credits
        
        if hasattr(agent.game_state, 'level'):
            current_level = agent.game_state.level
            # XP change would need to be calculated
            
        if hasattr(agent.game_state, 'elo'):
            current_elo = agent.game_state.elo
            # ELO change would need to be calculated
    
    async def _update_stats(self):
        """Update match-level statistics"""
        self.stats.total_rounds = self.current_round
        
        # Calculate derived stats for each agent
        for nickname, stats in self.stats.agent_stats.items():
            if stats["rounds_played"] > 0:
                stats["avg_credits_per_round"] = stats["total_credits_earned"] / stats["rounds_played"]
                
            total_battles = stats["battles_won"] + stats["battles_lost"]
            if total_battles > 0:
                stats["win_rate"] = stats["battles_won"] / total_battles
    
    async def _check_completion_conditions(self) -> bool:
        """Check if the match should end"""
        # Basic completion: max rounds reached
        if self.current_round >= self.config.max_rounds:
            logger.info("Match completed: Maximum rounds reached")
            return True
        
        # Check if all agents are inactive (could add more sophisticated conditions)
        active_agents = sum(1 for stats in self.stats.agent_stats.values() 
                          if stats.get("enabled", True))
        
        if active_agents < 2:
            logger.info("Match completed: Insufficient active agents")
            return True
        
        return False
    
    async def _finish_match(self):
        """Finalize the match"""
        self.running = False
        self.status = MatchStatus.COMPLETED
        self.stats.end_time = datetime.now()
        
        duration = self.stats.end_time - self.stats.start_time
        logger.info(f"Match completed after {duration.total_seconds():.1f} seconds")
        
        # Log match completion with statistics
        log_match_event(self.ai_logger, "MATCH_COMPLETED", {
            "duration_seconds": duration.total_seconds(),
            "total_rounds": self.stats.total_rounds,
            "total_battles": self.stats.total_battles,
            "final_rankings": [name for name, _ in self.get_agent_rankings()[:3]]  # Top 3
        })
        
        # Call completion hook
        if self.on_match_complete:
            await self.on_match_complete(self.stats)
        
        # Save match results if enabled
        if self.config.save_logs:
            await self._save_match_results()
    
    async def _save_match_results(self):
        """Save match results to file"""
        try:
            results = {
                "match_config": {
                    "match_type": self.config.match_type.value,
                    "max_rounds": self.config.max_rounds,
                    "agents": len(self.agents)
                },
                "stats": {
                    "start_time": self.stats.start_time.isoformat(),
                    "end_time": self.stats.end_time.isoformat() if self.stats.end_time else None,
                    "total_rounds": self.stats.total_rounds,
                    "total_battles": self.stats.total_battles,
                    "agent_stats": self.stats.agent_stats
                }
            }
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/match_results_{timestamp}.json"
            
            # Ensure logs directory exists
            import os
            os.makedirs("logs", exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Match results saved to {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save match results: {str(e)}")
    
    def pause_match(self):
        """Pause the match"""
        if self.status == MatchStatus.RUNNING:
            self.status = MatchStatus.PAUSED
            logger.info("Match paused")
    
    def resume_match(self):
        """Resume a paused match"""
        if self.status == MatchStatus.PAUSED:
            self.status = MatchStatus.RUNNING
            logger.info("Match resumed")
    
    def stop_match(self):
        """Stop the match"""
        self.running = False
        self.status = MatchStatus.COMPLETED
        logger.info("Match stopped by user")
    
    def get_live_stats(self) -> Dict[str, Any]:
        """Get current match statistics"""
        return {
            "status": self.status.value,
            "current_round": self.current_round,
            "max_rounds": self.config.max_rounds,
            "agents": len(self.agents),
            "active_agents": sum(1 for stats in self.stats.agent_stats.values() 
                               if stats.get("enabled", True)),
            "total_battles": self.stats.total_battles,
            "agent_stats": self.stats.agent_stats,
            "elapsed_time": (datetime.now() - self.stats.start_time).total_seconds()
        }
    
    def get_agent_rankings(self) -> List[Tuple[str, Dict[str, Any]]]:
        """Get agents ranked by performance"""
        rankings = []
        
        for nickname, stats in self.stats.agent_stats.items():
            score = (
                stats.get("battles_won", 0) * 10 +
                stats.get("total_credits_earned", 0) * 0.01 +
                stats.get("total_xp_gained", 0) * 0.1 +
                stats.get("elo_change", 0) * 0.1
            )
            
            rankings.append((nickname, {
                **stats,
                "performance_score": score
            }))
        
        # Sort by performance score (descending)
        rankings.sort(key=lambda x: x[1]["performance_score"], reverse=True)
        return rankings

# Convenience functions for setting up matches
async def create_default_match() -> MatchOrchestrator:
    """Create a default match with basic AI agents"""
    config = MatchConfig(
        match_type=MatchType.CONTINUOUS,
        max_rounds=50,
        round_delay=3.0,
        enable_learning=True
    )
    
    orchestrator = MatchOrchestrator(config)
    
    # Example agent configurations (would need real credentials)
    agents = [
        AgentConfig("warrior", "ai_warrior@bellum.com", "password123", "AI_Warrior"),
        AgentConfig("guardian", "ai_guardian@bellum.com", "password123", "AI_Guardian"), 
        AgentConfig("tactician", "ai_tactician@bellum.com", "password123", "AI_Tactician")
    ]
    
    for agent_config in agents:
        await orchestrator.add_agent(agent_config)
    
    return orchestrator

async def run_quick_match(rounds: int = 20) -> MatchStats:
    """Run a quick match between AI agents"""
    orchestrator = await create_default_match()
    orchestrator.config.max_rounds = rounds
    
    await orchestrator.start_match()
    return orchestrator.stats
