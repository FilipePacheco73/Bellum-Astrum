"""
AI User Manager - Handles automatic creation and management of AI user accounts
"""

import asyncio
import logging
import httpx
from typing import List, Dict, Optional
from dataclasses import dataclass

from AI_Agents.config.env_config import get_config, AIAgentCredentials

logger = logging.getLogger(__name__)

@dataclass
class AIUserCredentials:
    """AI User credentials"""
    email: str
    password: str
    nickname: str
    agent_type: str

class AIUserManager:
    """Manages AI user accounts automatically"""
    
    def __init__(self, api_base_url: str = None):
        # Load configuration
        self.config = get_config()
        self.api_base_url = api_base_url or self.config.api_base_url
        
        # Map agent types based on agent nicknames
        self.agent_type_mapping = {
            "warrior": "aggressive",
            "berserker": "aggressive", 
            "guardian": "defensive",
            "economist": "defensive",
            "tactician": "tactical",
            "strategist": "tactical"
        }
    
    def _determine_agent_type(self, nickname: str) -> str:
        """Determine agent type based on nickname"""
        nickname_lower = nickname.lower()
        
        for keyword, mapped_type in self.agent_type_mapping.items():
            if keyword in nickname_lower:
                return mapped_type
        
        # Default to aggressive if no match
        return "aggressive"
    
    def get_ai_users_from_config(self) -> List[AIUserCredentials]:
        """
        Get AI user credentials from environment configuration
        
        Returns:
            List of AI user credentials from .env file
        """
        ai_users = []
        
        for agent_creds in self.config.ai_agents:
            agent_type = self._determine_agent_type(agent_creds.nickname)
            
            ai_user = AIUserCredentials(
                email=agent_creds.email,
                password=agent_creds.password,
                nickname=agent_creds.nickname,
                agent_type=agent_type
            )
            
            ai_users.append(ai_user)
            logger.debug(f"Loaded AI user config: {agent_creds.nickname} ({agent_type})")
        
        return ai_users
    
    async def ensure_ai_users_exist(self) -> List[AIUserCredentials]:
        """
        Ensure all AI users exist, creating them if necessary
        
        Returns:
            List of AI user credentials that are ready to use
        """
        # Get AI users from configuration
        configured_users = self.get_ai_users_from_config()
        
        if not configured_users:
            logger.error("No AI users configured in .env file!")
            logger.info("Please configure AI agents in your .env file based on .env.example")
            return []
        
        logger.info(f"Found {len(configured_users)} AI users in configuration")
        ready_users = []
        
        async with httpx.AsyncClient(timeout=30) as client:
            for user_creds in configured_users:
                try:
                    # Try to create the user
                    is_ready = await self._ensure_user_exists(client, user_creds)
                    if is_ready:
                        ready_users.append(user_creds)
                        logger.info(f"AI user ready: {user_creds.nickname}")
                    else:
                        logger.error(f"Failed to prepare AI user: {user_creds.nickname}")
                        
                except Exception as e:
                    logger.error(f"Error preparing AI user {user_creds.nickname}: {e}")
        
        logger.info(f"AI Users ready: {len(ready_users)}/{len(configured_users)}")
        return ready_users
    
    async def _ensure_user_exists(self, client: httpx.AsyncClient, user_creds: AIUserCredentials) -> bool:
        """
        Ensure a single user exists (create if needed, verify login)
        
        Args:
            client: HTTP client
            user_creds: User credentials to check/create
            
        Returns:
            True if user is ready to use
        """
        try:
            # First try to login (check if user exists and password is correct)
            login_result = await self._try_login(client, user_creds)
            if login_result:
                logger.debug(f"User {user_creds.nickname} already exists and login works")
                return True
            
            # User doesn't exist or login failed, try to create
            logger.info(f"Creating AI user: {user_creds.nickname}")
            create_result = await self._create_user(client, user_creds)
            
            if create_result:
                # Verify login after creation
                login_result = await self._try_login(client, user_creds)
                if login_result:
                    logger.info(f"Successfully created and verified AI user: {user_creds.nickname}")
                    return True
                else:
                    logger.error(f"Created user {user_creds.nickname} but login verification failed")
                    return False
            else:
                logger.error(f"Failed to create AI user: {user_creds.nickname}")
                return False
                
        except Exception as e:
            logger.error(f"Error ensuring user {user_creds.nickname} exists: {e}")
            return False
    
    async def _try_login(self, client: httpx.AsyncClient, user_creds: AIUserCredentials) -> bool:
        """
        Try to login with user credentials
        
        Returns:
            True if login successful
        """
        try:
            login_data = {
                "email": user_creds.email,
                "password": user_creds.password
            }
            
            response = await client.post(
                f"{self.api_base_url}/api/v1/users/login",
                json=login_data
            )
            
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                logger.debug(f"Login failed for {user_creds.nickname}: Invalid credentials")
                return False
            else:
                logger.warning(f"Unexpected login response for {user_creds.nickname}: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Login attempt failed for {user_creds.nickname}: {e}")
            return False
    
    async def _create_user(self, client: httpx.AsyncClient, user_creds: AIUserCredentials) -> bool:
        """
        Create a new user account
        
        Returns:
            True if creation successful or user already exists
        """
        try:
            user_data = {
                "email": user_creds.email,
                "password": user_creds.password,
                "nickname": user_creds.nickname
            }
            
            response = await client.post(
                f"{self.api_base_url}/api/v1/users/register",
                json=user_data
            )
            
            if response.status_code in [200, 201]:
                return True
            elif response.status_code == 400:
                # Check if it's because user already exists
                response_text = response.text.lower()
                if "nickname already registered" in response_text or "email already registered" in response_text:
                    return True
                else:
                    logger.error(f"Failed to create user {user_creds.nickname}: {response.status_code} - {response.text}")
                    return False
            elif response.status_code == 409:
                return True  # User exists, that's fine
            else:
                logger.error(f"Failed to create user {user_creds.nickname}: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"User creation failed for {user_creds.nickname}: {e}")
            return False
    
    def get_env_config_format(self, ready_users: List[AIUserCredentials]) -> str:
        """
        Generate .env file format for the ready AI users
        
        Args:
            ready_users: List of ready AI user credentials
            
        Returns:
            String in .env format
        """
        env_lines = [
            "# Auto-generated AI Agent Credentials",
            f"API_BASE_URL_LOCAL=http://localhost:8000",
            ""
        ]
        
        for i, user in enumerate(ready_users, 1):
            env_lines.extend([
                f"# AI Agent {i} ({user.agent_type})",
                f"AI_AGENT_{i}_EMAIL={user.email}",
                f"AI_AGENT_{i}_PASSWORD={user.password}",
                f"AI_AGENT_{i}_NICKNAME={user.nickname}",
                ""
            ])
        
        return "\n".join(env_lines)
    
    async def initialize_ai_system(self) -> bool:
        """
        Complete AI system initialization
        
        Returns:
            True if initialization successful
        """
        try:
            logger.info("=== INITIALIZING AI SYSTEM ===")
            
            # Ensure AI users exist
            ready_users = await self.ensure_ai_users_exist()
            
            if not ready_users:
                logger.error("No AI users are ready - cannot start AI system")
                return False
            
            logger.info(f"AI System initialized with {len(ready_users)} users")
            return True
            
        except Exception as e:
            logger.error(f"AI system initialization failed: {e}")
            return False
