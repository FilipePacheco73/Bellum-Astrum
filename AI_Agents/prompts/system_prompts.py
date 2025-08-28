"""
System prompts for AI agents in Bellum Astrum.
"""

"""
System prompts for AI agents in Bellum Astrum.
"""

# Simplified system prompt for small models
BASE_SYSTEM_PROMPT = """You are {agent_type}, an AI commander in Bellum Astrum.

GAME: Turn-based strategy with ships, credits, and battles.

MECHANICS:
- Work → earn credits
- Buy/activate ships (limited slots by rank)  
- Battle NPCs (safe) or players (risky)
- Repair damaged ships
- Progress ranks for more ship slots

RESPONSE FORMAT (MANDATORY):
ACTION: [action_name]
EXPLANATION: [reasoning]

Be tactical and decisive!"""

def get_system_prompt(agent_type="AI_Warrior"):
    """
    Get the system prompt for a specific agent type.
    
    Args:
        agent_type: Type of AI agent (AI_Warrior, AI_Guardian, AI_Tactician)
    
    Returns:
        str: The system prompt for the agent
    """
    return BASE_SYSTEM_PROMPT.format(agent_type=agent_type)


