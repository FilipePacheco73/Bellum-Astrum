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
from AI_Agents.core.llm_manager import get_llm_manager, preload_shared_models
from AI_Agents.core.ai_user_manager import AIUserManager
from AI_Agents.config.env_config import get_config
from AI_Agents.core.tool_caller import AICredentials
from AI_Agents.config.logging_config import setup_logging

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
        """Setup AI agents using automatic user management"""
        logger.info("Setting up AI agents with automatic user management...")
        
        try:
            # Preload shared models to avoid multiple loading
            logger.info("Preloading shared LLM models...")
            if not preload_shared_models():
                logger.error("Failed to preload shared models")
                return []
            
            # Initialize AI user manager
            user_manager = AIUserManager()
            
            # Ensure AI users exist and are ready
            ready_users = await user_manager.ensure_ai_users_exist()
            
            if not ready_users:
                logger.error("No AI users are ready!")
                return []
            
            # Convert to AgentConfig format
            test_agents = []
            for user_creds in ready_users:
                agent_config = AgentConfig(
                    agent_type=user_creds.agent_type,
                    email=user_creds.email,
                    password=user_creds.password,
                    nickname=user_creds.nickname
                )
                
                test_agents.append(agent_config)
            
            logger.info(f"Configured {len(test_agents)} agents for match")
            
            return test_agents
            
        except Exception as e:
            logger.error(f"Failed to setup AI agents: {e}")
            return []
    
    async def run_training_match(self, rounds: int = 30):
        """Run a training match between AI agents"""
        logger.info("=== STARTING AI TRAINING MATCH ===")
        
        # Configure match for lightweight LLMs
        config = MatchConfig(
            match_type=MatchType.TRAINING,
            max_rounds=rounds,
            round_delay=3.0,  # Slower pace for lightweight LLMs
            max_concurrent_agents=3,  # Fewer concurrent agents
            enable_learning=True,
            save_logs=True
        )
        
        # Create orchestrator
        self.orchestrator = MatchOrchestrator(config)
        
        # Set the AI logger for detailed decision logging
        self.orchestrator.ai_logger = ai_logger
        
        # Setup event callbacks
        self.orchestrator.on_round_complete = self._on_round_complete
        self.orchestrator.on_match_complete = self._on_match_complete
        
        # Add AI agents
        test_agents = await self.setup_test_agents()
        
        for agent_config in test_agents[:3]:  # Start with 3 agents
            logger.info(f"Adding agent: {agent_config.nickname} ({agent_config.agent_type})")
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
            logger.info(f"Total agents: {live_stats['total_agents']}")
            logger.info(f"Current round: {live_stats['current_round']}")
            
            # Show top performer
            rankings = self.orchestrator.get_agent_rankings()
            if rankings:
                top_agent = rankings[0]
                logger.info(f"Top performer: {top_agent['name']} (Success rate: {top_agent['success_rate']:.1%})")
    
    async def _on_match_complete(self, stats):
        """Callback when match completes"""
        logger.info("=== MATCH COMPLETED ===")
        duration = stats.get("duration_seconds", 0)
        logger.info(f"Duration: {duration:.1f} seconds")
        logger.info(f"Total rounds: {stats.get('total_rounds', 0)}")
        
        # Cleanup empty memory files
        await self._cleanup_empty_memory_files()
    
    async def _cleanup_empty_memory_files(self):
        """Clean up empty memory files created during the match"""
        try:
            from pathlib import Path
            memories_dir = Path(__file__).parent / "memories"
            
            if not memories_dir.exists():
                return
                
            # Remove empty files
            for file_path in memories_dir.glob("*.json"):
                if file_path.stat().st_size == 0:
                    file_path.unlink()
                    logger.info(f"Removed empty memory file: {file_path.name}")
                    
        except Exception as e:
            logger.error(f"Failed to cleanup empty memory files: {str(e)}")
        
    def _print_final_results(self):
        """Print final match results"""
        if not self.orchestrator:
            return
            
        rankings = self.orchestrator.get_agent_rankings()
        
        print("\n" + "="*50)
        print("FINAL RESULTS")
        print("="*50)
        
        for i, agent_stats in enumerate(rankings, 1):
            print(f"{i}. {agent_stats['name']} ({agent_stats['type']})")
            print(f"   Successful decisions: {agent_stats['successful_decisions']}")
            print(f"   Success rate: {agent_stats['success_rate']:.1%}")
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
