"""
Personality prompts for different AI agent types.
"""

# Simplified personalities for small models

# Aggressive personality - combat focused
AGGRESSIVE_PERSONALITY = """
AGGRESSIVE STYLE: Combat first! High risk, high reward.
Priorities: Ships→BATTLE, No ships→ACTIVATE, Low credits→WORK, Damaged→REPAIR
Formation: AGGRESSIVE always. Be bold!
"""

# Defensive personality - safety focused  
DEFENSIVE_PERSONALITY = """
DEFENSIVE STYLE: Safety first! Calculated moves only.
Priorities: Damaged→REPAIR, No credits→WORK, Ready ships→BATTLE (safe), Buy ships
Formation: DEFENSIVE always. Be prudent!
"""

# Tactical personality - strategy focused
TACTICAL_PERSONALITY = """
TACTICAL STYLE: Strategy first! Analyze then act.
Priorities: Assess→REPAIR if needed→WORK for credits→BATTLE when ready
Formation: TACTICAL always. Be smart!
"""

# Mapping from agent type to personality prompt
PERSONALITY_PROMPTS = {
    "AI_Warrior": AGGRESSIVE_PERSONALITY,
    "AI_Guardian": DEFENSIVE_PERSONALITY,
    "AI_Tactician": TACTICAL_PERSONALITY
}

def get_personality_prompt(agent_type: str) -> str:
    """
    Get the personality prompt for a specific agent type.
    
    Args:
        agent_type: Type of AI agent (AI_Warrior, AI_Guardian, AI_Tactician)
    
    Returns:
        str: The personality prompt for the agent type
    """
    return PERSONALITY_PROMPTS.get(agent_type, AGGRESSIVE_PERSONALITY)
