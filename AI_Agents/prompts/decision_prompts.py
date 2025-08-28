"""
Decision-making prompts for AI agents.
These prompts guide the AI in making strategic decisions during gameplay.
"""

import re
import logging
from AI_Agents.prompts.system_prompts import get_system_prompt
from AI_Agents.prompts.personality_prompts import get_personality_prompt

logger = logging.getLogger(__name__)

# Simplified decision template for small models
DECISION_TEMPLATE = """
=== CURRENT SITUATION ===
{context_prompt}

=== RECENT MEMORIES ===
{memory_summary}

ACTIONS: status, fleet, opponents, work, buy, activate, deactivate, repair, battle

MANDATORY FORMAT:
ACTION: [action_name]
EXPLANATION: [brief reasoning]

EXAMPLES:
ACTION: status
EXPLANATION: Check current resources and status.

ACTION: work  
EXPLANATION: Need credits for ships and repairs.

ACTION: battle
EXPLANATION: Have strong ships, engaging opponent.

Choose wisely and respond in the exact format above!
"""

def get_decision_prompt(memory_summary: str, context_prompt: str, agent_type: str = "AI_Warrior") -> str:
    """
    Generate a complete decision prompt combining system prompt, personality, and context.
    
    Args:
        memory_summary: Recent memory summary from previous rounds
        context_prompt: Current game state context
        agent_type: Type of AI agent (AI_Warrior, AI_Guardian, AI_Tactician)
        
    Returns:
        Complete prompt with system instructions, personality, and decision context
    """
    # Get the appropriate prompts for the agent type
    system_prompt = get_system_prompt(agent_type)
    personality_prompt = get_personality_prompt(agent_type)
    
    # Combine system prompt with the decision template
    decision_context = DECISION_TEMPLATE.format(
        memory_summary=memory_summary,
        context_prompt=context_prompt
    )
    
    # Return complete prompt: system + personality + decision context
    return f"{system_prompt}\n\n{personality_prompt}\n\n{decision_context}"

# Action mapping for parsing responses
ACTION_KEYWORDS = {
    # Information tools
    'status': 'get_my_status',
    'check': 'get_my_status',
    'fleet': 'get_fleet_status',
    'ships': 'get_fleet_status',
    'opponents': 'list_opponents',
    'list': 'list_opponents',
    
    # Economic tools
    'work': 'perform_work',
    'buy': 'buy_ship',
    'purchase': 'buy_ship',
    'repair': 'repair_ship',
    'fix': 'repair_ship',
    
    # Ship management
    'activate': 'activate_ship',
    'deactivate': 'deactivate_ship',
    
    # Battle
    'battle': 'engage_battle',
    'fight': 'engage_battle',
    'combat': 'engage_battle'
}

def parse_ai_decision(response_text: str) -> dict:
    """
    Parse AI response in the standardized format.
    Expected format: ACTION: [action] EXPLANATION: [text]
    """
    try:
        response = response_text.strip()
        
        # Look for the mandatory format: ACTION: ... EXPLANATION: ...
        action_match = re.search(r'ACTION:\s*(\w+)', response, re.IGNORECASE)
        explanation_match = re.search(r'EXPLANATION:\s*(.+?)(?:\n|$)', response, re.IGNORECASE | re.DOTALL)
        
        if action_match and explanation_match:
            action_word = action_match.group(1).lower()
            explanation = explanation_match.group(1).strip()
            
            # Map action word to actual function name
            mapped_action = ACTION_KEYWORDS.get(action_word)
            if mapped_action:
                return {
                    'action': mapped_action,
                    'reason': explanation,
                    'parameters': {}
                }
        
        # Fallback: try to find any action keyword in the response
        response_lower = response.lower()
        for keyword, mapped_action in ACTION_KEYWORDS.items():
            if keyword in response_lower:
                return {
                    'action': mapped_action,
                    'reason': f'Fallback parsing detected: {keyword}',
                    'parameters': {}
                }
        
        return None
        
    except Exception as e:
        logger.error(f"Failed to parse AI decision: {e}")
        return None
