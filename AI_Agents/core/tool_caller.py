"""
Tool Caller - Interface for calling Bellum Astrum game APIs from AI agents.
"""

import httpx
import asyncio
import json
import logging
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass
from enum import Enum

from AI_Agents.config.env_config import get_config

logger = logging.getLogger(__name__)

class ToolResult:
    """Result of a tool execution"""
    def __init__(self, success: bool, data: Any = None, error: str = None, status_code: int = None):
        self.success = success
        self.data = data
        self.error = error
        self.status_code = status_code
    
    def __repr__(self):
        return f"ToolResult(success={self.success}, data={self.data}, error={self.error})"

class GameTool(Enum):
    """Available game tools/APIs"""
    # Information tools
    GET_MY_STATUS = "get_my_status"
    GET_FLEET_STATUS = "get_fleet_status"
    LIST_OPPONENTS = "list_opponents"
    GET_WORK_STATUS = "get_work_status"
    GET_SHIP_LIMITS = "get_ship_limits"
    
    # Economic tools
    PERFORM_WORK = "perform_work"
    BUY_SHIP = "buy_ship"
    REPAIR_SHIP = "repair_ship"
    
    # Battle tools
    ACTIVATE_SHIP = "activate_ship"
    DEACTIVATE_SHIP = "deactivate_ship"
    ENGAGE_BATTLE = "engage_battle"

@dataclass
class AICredentials:
    """AI agent authentication credentials"""
    user_id: int
    access_token: str
    nickname: str

class GameAPIClient:
    """HTTP client for Bellum Astrum game APIs"""
    
    def __init__(self, base_url: str = None, timeout: int = 30):
        if base_url is None:
            config = get_config()
            base_url = config.api_base_url
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._client = None
    
    async def __aenter__(self):
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
    
    def _get_headers(self, credentials: AICredentials) -> Dict[str, str]:
        """Get HTTP headers with authentication"""
        return {
            "Authorization": f"Bearer {credentials.access_token}",
            "Content-Type": "application/json"
        }
    
    async def get(self, endpoint: str, credentials: AICredentials, params: Dict = None) -> ToolResult:
        """Make GET request to API"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = self._get_headers(credentials)
            
            response = await self._client.get(url, headers=headers, params=params or {})
            
            if response.status_code == 200:
                return ToolResult(success=True, data=response.json(), status_code=response.status_code)
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                return ToolResult(success=False, error=error_msg, status_code=response.status_code)
                
        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            return ToolResult(success=False, error=error_msg)
    
    async def post(self, endpoint: str, credentials: AICredentials, data: Dict = None, json_data: Dict = None) -> ToolResult:
        """Make POST request to API"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = self._get_headers(credentials)
            
            kwargs = {"headers": headers}
            if json_data:
                kwargs["json"] = json_data
            elif data:
                kwargs["data"] = data
            
            response = await self._client.post(url, **kwargs)
            
            if response.status_code in [200, 201]:
                return ToolResult(success=True, data=response.json(), status_code=response.status_code)
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                return ToolResult(success=False, error=error_msg, status_code=response.status_code)
                
        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            return ToolResult(success=False, error=error_msg)

class GameToolCaller:
    """Main tool calling interface for AI agents"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = GameAPIClient(base_url)
    
    async def execute_tool(self, tool: GameTool, credentials: AICredentials, **kwargs) -> ToolResult:
        """Execute a game tool with the provided parameters"""
        async with GameAPIClient(self.base_url) as client:
            self.client = client
            
            try:
                if tool == GameTool.GET_MY_STATUS:
                    return await self._get_my_status(credentials)
                elif tool == GameTool.GET_FLEET_STATUS:
                    return await self._get_fleet_status(credentials)
                elif tool == GameTool.LIST_OPPONENTS:
                    return await self._list_opponents(credentials)
                elif tool == GameTool.GET_WORK_STATUS:
                    return await self._get_work_status(credentials)
                elif tool == GameTool.GET_SHIP_LIMITS:
                    return await self._get_ship_limits(credentials)
                elif tool == GameTool.PERFORM_WORK:
                    return await self._perform_work(credentials)
                elif tool == GameTool.BUY_SHIP:
                    ship_id = kwargs.get('ship_id')
                    return await self._buy_ship(credentials, ship_id)
                elif tool == GameTool.REPAIR_SHIP:
                    ship_number = kwargs.get('ship_number')
                    return await self._repair_ship(credentials, ship_number)
                elif tool == GameTool.ACTIVATE_SHIP:
                    ship_number = kwargs.get('ship_number')
                    return await self._activate_ship(credentials, ship_number)
                elif tool == GameTool.DEACTIVATE_SHIP:
                    ship_number = kwargs.get('ship_number')
                    return await self._deactivate_ship(credentials, ship_number)
                elif tool == GameTool.ENGAGE_BATTLE:
                    return await self._engage_battle(credentials, **kwargs)
                else:
                    return ToolResult(success=False, error=f"Unknown tool: {tool}")
                    
            except Exception as e:
                error_msg = f"Tool execution failed for {tool}: {str(e)}"
                return ToolResult(success=False, error=error_msg)
    
    # Information tools
    async def _get_my_status(self, credentials: AICredentials) -> ToolResult:
        """Get user's current status"""
        result = await self.client.get(f"/api/v1/users/{credentials.user_id}", credentials)
        return result
    
    async def _get_fleet_status(self, credentials: AICredentials) -> ToolResult:
        """Get user's ship fleet status"""
        return await self.client.get(f"/api/v1/users/{credentials.user_id}/ships", credentials)
    
    async def _list_opponents(self, credentials: AICredentials) -> ToolResult:
        """List available opponents"""
        result = await self.client.get("/api/v1/users/", credentials, params={"limit": 100})
        if result.success and result.data:
            # Filter out self from opponents list
            opponents = [user for user in result.data if user.get('user_id') != credentials.user_id]
            result.data = opponents
        return result
    
    async def _get_work_status(self, credentials: AICredentials) -> ToolResult:
        """Get work cooldown and status"""
        return await self.client.get("/api/v1/work/status", credentials)
    
    async def _get_ship_limits(self, credentials: AICredentials) -> ToolResult:
        """Get ship activation limits info"""
        return await self.client.get("/api/v1/battle/ship-limits/", credentials)
    
    # Economic tools
    async def _perform_work(self, credentials: AICredentials) -> ToolResult:
        """Perform work to earn credits"""
        return await self.client.post("/api/v1/work/perform", credentials)
    
    async def _buy_ship(self, credentials: AICredentials, ship_id: int) -> ToolResult:
        """Buy a ship from the market"""
        if ship_id is None:
            return ToolResult(success=False, error="ship_id is required for buy_ship")
        return await self.client.post(f"/api/v1/market/buy/{ship_id}", credentials)
    
    async def _repair_ship(self, credentials: AICredentials, ship_number: int) -> ToolResult:
        """Repair a damaged ship"""
        if ship_number is None:
            return ToolResult(success=False, error="ship_number is required for repair_ship")
        return await self.client.post("/api/v1/shipyard/repair", credentials, 
                                    json_data={"ship_number": ship_number})
    
    # Battle tools
    async def _activate_ship(self, credentials: AICredentials, ship_number: int) -> ToolResult:
        """Activate a ship for battle"""
        if ship_number is None:
            return ToolResult(success=False, error="ship_number is required for activate_ship")
        return await self.client.post("/api/v1/battle/activate-ship/", credentials,
                                    params={"ship_number": ship_number})
    
    async def _deactivate_ship(self, credentials: AICredentials, ship_number: int) -> ToolResult:
        """Deactivate a ship to free up slot"""
        if ship_number is None:
            return ToolResult(success=False, error="ship_number is required for deactivate_ship")
        return await self.client.post("/api/v1/battle/deactivate-ship/", credentials,
                                    params={"ship_number": ship_number})
    
    async def _engage_battle(self, credentials: AICredentials, **kwargs) -> ToolResult:
        """Engage in battle with another player"""
        required_params = ['opponent_user_id', 'user_ship_numbers', 'opponent_ship_numbers']
        for param in required_params:
            if param not in kwargs:
                return ToolResult(success=False, error=f"{param} is required for engage_battle")
        
        battle_data = {
            "opponent_user_id": kwargs['opponent_user_id'],
            "user_ship_numbers": kwargs['user_ship_numbers'],
            "opponent_ship_numbers": kwargs['opponent_ship_numbers'],
            "user_formation": kwargs.get('user_formation', 'AGGRESSIVE'),
            "opponent_formation": kwargs.get('opponent_formation', 'AGGRESSIVE')
        }
        
        return await self.client.post("/api/v1/battle/battle", credentials, json_data=battle_data)

# Convenience functions for common operations
async def get_available_ships_for_purchase() -> List[Dict]:
    """Get list of ships available for purchase (no auth needed)"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/ships/")
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get available ships: {response.status_code}")
                return []
    except Exception as e:
        logger.error(f"Error getting available ships: {str(e)}")
        return []

async def try_login(client: httpx.AsyncClient, email: str, password: str) -> Optional[AICredentials]:
    """Try to login with existing credentials"""
    try:
        config = get_config()
        response = await client.post(
            f"{config.api_base_url}/api/v1/users/login",
            json={"email": email, "password": password}
        )
        
        if response.status_code == 200:
            auth_data = response.json()
            access_token = auth_data.get('access_token')
            
            if not access_token:
                logger.error("No access token received from login response")
                return None
            
            # Decode JWT token to extract user_id and other info
            try:
                from jose import jwt
                # We don't verify signature here since we just got the token from our own API
                # This is just to extract the payload for user_id
                decoded = jwt.decode(access_token, key="", options={"verify_signature": False})
                user_id = decoded.get('user_id')
                user_email = decoded.get('sub')  # 'sub' contains the email
                
                if not user_id:
                    logger.error("No user_id found in JWT token payload")
                    return None
                
                # Now get the user details using the user_id from the token
                headers = {"Authorization": f"Bearer {access_token}"}
                user_response = await client.get(
                    f"{config.api_base_url}/api/v1/users/{user_id}", 
                    headers=headers
                )
                
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    nickname = user_data.get('nickname')
                    
                    if not nickname:
                        logger.error(f"No nickname found for user_id {user_id}")
                        return None
                    
                    logger.info(f"Successfully authenticated user: {nickname} (ID: {user_id})")
                    return AICredentials(
                        user_id=user_id,
                        access_token=access_token,
                        nickname=nickname
                    )
                else:
                    logger.error(f"Failed to get user details for user_id {user_id}: {user_response.status_code}")
                    
            except Exception as jwt_error:
                logger.error(f"Failed to decode JWT token: {str(jwt_error)}")
                return None
            
        else:
            logger.debug(f"Login failed with status {response.status_code}: {response.text}")
        
        return None
    except Exception as e:
        logger.debug(f"Login attempt failed: {str(e)}")
        return None

async def try_register(client: httpx.AsyncClient, email: str, password: str, nickname: str) -> Optional[AICredentials]:
    """Try to register a new user"""
    try:
        config = get_config()
        response = await client.post(
            f"{config.api_base_url}/api/v1/users/register",
            json={
                "email": email,
                "password": password,
                "nickname": nickname
            }
        )
        
        if response.status_code in [200, 201]:
            logger.info(f"Successfully registered new AI agent: {nickname}")
            # After registration, try to login
            return await try_login(client, email, password)
        elif response.status_code == 400:
            response_data = response.json()
            if "already registered" in response_data.get('detail', '').lower():
                logger.info(f"User {email} already exists, will try login instead")
                return None  # Indicates we should try login
            else:
                logger.error(f"Registration failed: {response_data.get('detail', 'Unknown error')}")
                return None
        else:
            logger.error(f"Registration failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.debug(f"Registration attempt failed: {str(e)}")
        return None

async def authenticate_ai_agent(email: str, password: str) -> Optional[AICredentials]:
    """
    Authenticate an AI agent with robust user handling.
    
    Strategy:
    1. Try to login first (user might already exist)
    2. If login fails, try to register the user  
    3. If registration fails because user exists, try login again
    4. Handle all errors gracefully without crashing
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Extract nickname from email for registration
            nickname = email.split('@')[0]
            if not nickname.startswith('AI_'):
                nickname = f"AI_{nickname}"
            
            logger.info(f"Authenticating AI agent: {email}")
            
            # Step 1: Try login first (most common case for existing users)
            credentials = await try_login(client, email, password)
            if credentials:
                return credentials
            
            logger.info(f"Login failed for {email}, attempting registration...")
            
            # Step 2: Try to register new user
            credentials = await try_register(client, email, password, nickname)
            if credentials:
                return credentials
            
            # Step 3: Registration might have failed because user exists, try login again
            logger.info(f"Registration didn't succeed for {email}, trying login one more time...")
            credentials = await try_login(client, email, password)
            if credentials:
                return credentials
            
            # If all attempts failed
            logger.error(f"All authentication attempts failed for {email}")
            logger.error("Please verify:")
            logger.error("  1. Email and password are correct")
            logger.error("  2. Backend server is running")
            logger.error("  3. Network connectivity is working")
            return None
                
    except Exception as e:
        logger.error(f"Critical authentication error for {email}: {str(e)}")
        return None
