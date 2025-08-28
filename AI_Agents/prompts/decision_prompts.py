"""
Decision-making prompts for AI agents.
These prompts guide the AI in making strategic decisions during gameplay.
"""

import re
import logging
from AI_Agents.prompts.system_prompts import get_system_prompt
from AI_Agents.prompts.personality_prompts import get_personality_prompt

logger = logging.getLogger(__name__)

# Base decision template for all agent types
DECISION_TEMPLATE = """
=== MEMORY & CONTEXT ===
{memory_summary}

=== CURRENT SITUATION ===
{context_prompt}

=== INSTRUCTIONS ===
1. Analyze the situation and your memories
2. Choose ONE action from the options below
3. Provide your response in the exact format specified

AVAILABLE ACTIONS:
- status (check your current situation and resources)
- fleet (check your fleet status and ship details)
- opponents (list available opponents for battle)
- work (earn credits through work)
- buy (purchase a new ship)
- activate (activate an inactive ship)
- deactivate (deactivate an active ship) 
- repair (repair a damaged ship)
- battle (engage in combat with an opponent)

=== MANDATORY RESPONSE FORMAT ===
You MUST respond using this EXACT format:

ACTION: [action_name]
EXPLANATION: [brief explanation in English]

EXAMPLES:
ACTION: status
EXPLANATION: Need to check current resources and ship status before making decisions.

ACTION: fleet
EXPLANATION: Want to review my ships' health and active status before planning.

ACTION: battle
EXPLANATION: Have strong active ships and found suitable opponent for combat.

ACTION: work
EXPLANATION: Low credits, need to earn money for ship repairs and purchases.

ACTION: repair
EXPLANATION: My ships are damaged and need fixing before combat.

IMPORTANT: Use only English in your response. Be concise but clear. The explanation will be saved for future reference.
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
