"""
AI Match Runner - Script to run AI vs AI matches in Bellum Astrum.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to Python path so AI_Agents module can be found
sys.path.append(str(Path(__file__).parent.parent))

from AI_Agents.core.match_orchestrator import MatchOrchestrator, MatchConfig, AgentConfig, MatchType
from AI_Agents.core.llm_manager import get_llm_manager
from AI_Agents.config.env_config import get_config
from AI_Agents.core.tool_caller import AICredentials
from AI_Agents.config.logging_config import setup_logging, log_match_event, log_ai_tool_usage

# Ensure required directories exist
logs_dir = Path(__file__).parent / "logs"
logs_dir.mkdir(exist_ok=True)

# Setup dual logging system
debug_logger, ai_logger = setup_logging(logs_dir)

# Use debug logger for this module
logger = debug_logger

class AIMatchRunner:
    """Manages and runs AI vs AI matches"""
    
    def __init__(self):
        self.orchestrator = None
        
    async def setup_test_agents(self):
        """Setup AI agents from environment configuration"""
        logger.info("Setting up AI agents from environment configuration...")
        log_match_event(ai_logger, "AGENT_SETUP_STARTED")
        
        # Load configuration
        config = get_config()
        
        if not config.ai_agents:
            logger.error("No AI agent credentials found in environment configuration!")
            logger.info("Please configure AI agents in your .env file based on .env.example")
            log_match_event(ai_logger, "AGENT_SETUP_FAILED", {"reason": "No AI credentials found"})
            return []
        
        # Map personalities based on agent nicknames or use defaults
        personality_mapping = {
            "warrior": ["warrior", "ai_warrior", "berserker"],
            "guardian": ["guardian", "ai_guardian", "defensive"],
            "tactician": ["tactician", "ai_tactician", "tactical"],
            "berserker": ["berserker", "ai_berserker", "aggressive"], 
            "economist": ["economist", "ai_economist", "economic"]
        }
        
        test_agents = []
        for i, agent_creds in enumerate(config.ai_agents):
            # Determine personality based on nickname
            personality = "warrior"  # default
            nickname_lower = agent_creds.nickname.lower()
            
            for pers_name, keywords in personality_mapping.items():
                if any(keyword in nickname_lower for keyword in keywords):
                    personality = pers_name
                    break
            
            # Create agent config
            agent_config = AgentConfig(
                personality_name=personality,
                email=agent_creds.email,
                password=agent_creds.password,
                nickname=agent_creds.nickname
            )
            
            test_agents.append(agent_config)
            logger.info(f"Configured agent: {agent_creds.nickname} (personality: {personality})")
        
        log_match_event(ai_logger, "AGENT_SETUP_COMPLETED", {
            "total_agents": len(test_agents), 
            "personalities": [agent.personality_name for agent in test_agents]
        })
        
        return test_agents
    
    async def run_training_match(self, rounds: int = 30):
        """Run a training match between AI agents"""
        logger.info("=== STARTING AI TRAINING MATCH ===")
        log_match_event(ai_logger, "TRAINING_MATCH_STARTED", {
            "max_rounds": rounds,
            "match_type": "TRAINING"
        })
        
        # Configure match
        config = MatchConfig(
            match_type=MatchType.TRAINING,
            max_rounds=rounds,
            round_delay=2.0,  # 2 seconds between rounds
            max_concurrent_agents=5,
            enable_learning=True,
            save_logs=True,
            auto_restart=False
        )
        
        # Create orchestrator
        self.orchestrator = MatchOrchestrator(config)
        
        # Setup event callbacks
        self.orchestrator.on_round_complete = self._on_round_complete
        self.orchestrator.on_match_complete = self._on_match_complete
        
        # Add AI agents
        test_agents = await self.setup_test_agents()
        
        for agent_config in test_agents[:3]:  # Start with 3 agents
            logger.info(f"Adding agent: {agent_config.nickname} ({agent_config.personality_name})")
            success = await self.orchestrator.add_agent(agent_config)
            if not success:
                logger.error(f"Failed to add agent {agent_config.nickname}")
                return False
        
        # Start the match
        logger.info("Starting match...")
        success = await self.orchestrator.start_match()
        
        if success:
            logger.info("=== MATCH COMPLETED SUCCESSFULLY ===")
            self._print_final_results()
        else:
            logger.error("=== MATCH FAILED ===")
        
        return success
    
    async def run_continuous_match(self):
        """Run a continuous match that goes on indefinitely"""
        logger.info("=== STARTING CONTINUOUS AI MATCH ===")
        
        config = MatchConfig(
            match_type=MatchType.CONTINUOUS,
            max_rounds=200,  # Very high number
            round_delay=1.0,   # Faster pace
            enable_learning=True,
            save_logs=True,
            auto_restart=True
        )
        
        self.orchestrator = MatchOrchestrator(config)
        self.orchestrator.on_round_complete = self._on_round_complete
        
        # Add all available AI personalities
        test_agents = await self.setup_test_agents()
        for agent_config in test_agents:
            await self.orchestrator.add_agent(agent_config)
        
        logger.info("Starting continuous match (Ctrl+C to stop)...")
        
        try:
            await self.orchestrator.start_match()
        except KeyboardInterrupt:
            logger.info("Match interrupted by user")
            self.orchestrator.stop_match()
    
    async def _on_round_complete(self, round_number: int, stats):
        """Callback when a round completes"""
        if round_number % 2 == 0:  # Log every 2 rounds
            logger.info(f"Round {round_number} completed")
            
            # Get live stats
            live_stats = self.orchestrator.get_live_stats()
            logger.info(f"Active agents: {live_stats['active_agents']}")
            logger.info(f"Total battles: {live_stats['total_battles']}")
            
            # Show top performer
            rankings = self.orchestrator.get_agent_rankings()
            if rankings:
                top_agent = rankings[0]
                logger.info(f"Top performer: {top_agent[0]} (Score: {top_agent[1]['performance_score']:.1f})")
    
    async def _on_match_complete(self, stats):
        """Callback when match completes"""
        logger.info("=== MATCH COMPLETED ===")
        duration = (stats.end_time - stats.start_time).total_seconds()
        logger.info(f"Duration: {duration:.1f} seconds")
        logger.info(f"Total rounds: {stats.total_rounds}")
        
    def _print_final_results(self):
        """Print final match results"""
        if not self.orchestrator:
            return
            
        rankings = self.orchestrator.get_agent_rankings()
        
        print("\n" + "="*50)
        print("FINAL RESULTS")
        print("="*50)
        
        for i, (nickname, stats) in enumerate(rankings, 1):
            print(f"{i}. {nickname} ({stats['personality']})")
            print(f"   Rounds: {stats['rounds_played']}")
            print(f"   Battles: {stats['battles_won']}W/{stats['battles_lost']}L")
            print(f"   Win Rate: {stats['win_rate']*20:.1f}%")
            print(f"   Credits: {stats['total_credits_earned']}")
            print(f"   Performance Score: {stats['performance_score']:.1f}")
            print()

async def main():
    """Main entry point"""
    runner = AIMatchRunner()
    
    print("Bellum Astrum AI Match Runner")
    print("1. Training Match (30 rounds)")
    print("2. Continuous Match (until stopped)")
    print("3. Quick Test (2 rounds)")
    
    choice = input("Choose option (1-3): ").strip()
    
    try:
        if choice == "1":
            await runner.run_training_match(30)
        elif choice == "2":
            await runner.run_continuous_match()
        elif choice == "3":
            await runner.run_training_match(2)
        else:
            print("Invalid choice")
            
    except Exception as e:
        logger.error(f"Match failed: {str(e)}")
        print(f"Error: {str(e)}")

# Convenience functions for direct usage
async def quick_test():
    """Run a quick 2-round test"""
    runner = AIMatchRunner()
    await runner.run_training_match(2)

async def training_session():
    """Run a standard 50-round training session"""
    runner = AIMatchRunner()
    await runner.run_training_match(50)

if __name__ == "__main__":
    # Run the main interface
    asyncio.run(main())
