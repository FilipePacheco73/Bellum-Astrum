"""
Environment configuration loader for AI Agents
"""

import os
from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class AIAgentCredentials:
    """Credentials for an AI agent"""
    email: str
    password: str
    nickname: str

@dataclass
class EnvironmentConfig:
    """Environment configuration for AI Agents"""
    environment: str
    api_base_url: str
    
    # LLM Configuration
    llm_cache_dir: str
    llm_use_quantization: bool
    llm_device: str
    
    # Logging Configuration
    log_level: str
    log_file: str
    
    # Match Configuration
    default_match_duration_minutes: int
    default_round_interval_seconds: int
    enable_memory_learning: bool
    
    # Database Configuration
    ai_memory_db_path: str
    
    # AI Agents
    ai_agents: List[AIAgentCredentials]

def load_env_file(env_path: Optional[str] = None) -> None:
    """Load environment variables from .env file"""
    if env_path is None:
        env_path = Path(__file__).parent.parent / ".env"
    
    if not os.path.exists(env_path):
        logger.warning(f"Environment file not found: {env_path}")
        logger.info("Please create .env file based on .env.example")
        return
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    except Exception as e:
        logger.error(f"Error loading environment file: {e}")

def get_api_base_url() -> str:
    """Get API base URL based on environment"""
    environment = os.getenv('ENVIRONMENT', 'development').lower()
    
    if environment == 'production':
        return os.getenv('API_BASE_URL_PROD')
    elif environment == 'development':
        return os.getenv('API_BASE_URL_DEV')
    else:  # local
        return os.getenv('API_BASE_URL_LOCAL')

def load_ai_agent_credentials() -> List[AIAgentCredentials]:
    """Load all configured AI agent credentials"""
    agents = []
    
    # Try to load up to 10 agents (AI_AGENT_1 through AI_AGENT_10)
    for i in range(1, 11):
        email_key = f'AI_AGENT_{i}_EMAIL'
        password_key = f'AI_AGENT_{i}_PASSWORD'
        nickname_key = f'AI_AGENT_{i}_NICKNAME'
        
        email = os.getenv(email_key)
        password = os.getenv(password_key)
        nickname = os.getenv(nickname_key)
        
        if email and password and nickname:
            agents.append(AIAgentCredentials(
                email=email,
                password=password,
                nickname=nickname
            ))
        elif email or password or nickname:
            # Partial configuration warning
            logger.warning(f"Partial configuration for AI_AGENT_{i}: missing some credentials")
    
    if not agents:
        logger.error("No AI agent credentials found in environment variables")
        logger.info("Please configure at least one AI agent in your .env file")
    
    return agents

def get_environment_config() -> EnvironmentConfig:
    """Get complete environment configuration"""
    # Load .env file first
    load_env_file()
    
    # Load AI agent credentials
    ai_agents = load_ai_agent_credentials()
    
    return EnvironmentConfig(
        environment=os.getenv('ENVIRONMENT', 'development'),
        api_base_url=get_api_base_url(),
        
        # LLM Configuration
        llm_cache_dir=os.getenv('LLM_CACHE_DIR', './models_cache'),
        llm_use_quantization=os.getenv('LLM_USE_QUANTIZATION', 'true').lower() == 'true',
        llm_device=os.getenv('LLM_DEVICE', 'auto'),
        
        # Logging Configuration
        log_level=os.getenv('LOG_LEVEL', 'INFO'),
        log_file=os.getenv('LOG_FILE', 'ai_agents.log'),
        
        # Match Configuration
        default_match_duration_minutes=int(os.getenv('DEFAULT_MATCH_DURATION_MINUTES', '30')),
        default_round_interval_seconds=int(os.getenv('DEFAULT_ROUND_INTERVAL_SECONDS', '10')),
        enable_memory_learning=os.getenv('ENABLE_MEMORY_LEARNING', 'true').lower() == 'true',
        
        # Database Configuration
        ai_memory_db_path=os.getenv('AI_MEMORY_DB_PATH', './memory/ai_memory.db'),
        
        # AI Agents
        ai_agents=ai_agents
    )

# Global configuration instance
_config: Optional[EnvironmentConfig] = None

def get_config() -> EnvironmentConfig:
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = get_environment_config()
    return _config
