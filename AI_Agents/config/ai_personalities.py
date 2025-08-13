"""
Definição das personalidades dos agentes de IA.
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class AIPersonality:
    """Definição de uma personalidade de IA"""
    name: str
    description: str
    llm_type: str
    preferred_formation: str
    risk_tolerance: float  # 0.0 (muito conservador) a 1.0 (muito arriscado)
    work_frequency: float  # 0.0 (nunca trabalha) a 1.0 (sempre trabalha)
    battle_frequency: float  # 0.0 (nunca batalha) a 1.0 (sempre batalha)
    economic_focus: float  # 0.0 (ignora economia) a 1.0 (foca só na economia)
    target_selection_priority: List[str]  # Critérios para escolher oponentes
    ship_buying_strategy: str  # "cheapest", "balanced", "premium"
    repair_threshold: float  # % de HP para considerar reparo (0.0-1.0)

# Definições das personalidades
AI_PERSONALITIES: Dict[str, AIPersonality] = {
    "warrior": AIPersonality(
        name="AI_Warrior",
        description="Combatente agressivo que busca domínio através da força bruta",
        llm_type="aggressive",
        preferred_formation="AGGRESSIVE",
        risk_tolerance=0.9,
        work_frequency=0.2,
        battle_frequency=0.8,
        economic_focus=0.3,
        target_selection_priority=["higher_level", "equal_level", "lower_level"],
        ship_buying_strategy="premium",
        repair_threshold=0.6
    ),
    
    "guardian": AIPersonality(
        name="AI_Guardian", 
        description="Defensor cauteloso que prioriza sobrevivência e crescimento sustentável",
        llm_type="defensive",
        preferred_formation="DEFENSIVE",
        risk_tolerance=0.2,
        work_frequency=0.7,
        battle_frequency=0.3,
        economic_focus=0.8,
        target_selection_priority=["lower_level", "equal_level", "npcs_only"],
        ship_buying_strategy="balanced",
        repair_threshold=0.8
    ),
    
    "tactician": AIPersonality(
        name="AI_Tactician",
        description="Estrategista calculista que adapta suas táticas ao oponente",
        llm_type="tactical", 
        preferred_formation="TACTICAL",
        risk_tolerance=0.5,
        work_frequency=0.5,
        battle_frequency=0.5,
        economic_focus=0.6,
        target_selection_priority=["analyze_opponent", "favorable_matchup", "strategic_target"],
        ship_buying_strategy="balanced",
        repair_threshold=0.7
    ),
    
    "berserker": AIPersonality(
        name="AI_Berserker",
        description="Lutador imprudente que ataca sem pensar nas consequências",
        llm_type="aggressive",
        preferred_formation="AGGRESSIVE", 
        risk_tolerance=1.0,
        work_frequency=0.1,
        battle_frequency=0.9,
        economic_focus=0.1,
        target_selection_priority=["random", "highest_elo", "strongest_opponent"],
        ship_buying_strategy="cheapest",
        repair_threshold=0.4
    ),
    
    "economist": AIPersonality(
        name="AI_Economist",
        description="Focado em acúmulo de riqueza e crescimento econômico",
        llm_type="defensive",
        preferred_formation="DEFENSIVE",
        risk_tolerance=0.1,
        work_frequency=0.9,
        battle_frequency=0.1,
        economic_focus=1.0,
        target_selection_priority=["guaranteed_win", "npcs_only", "much_lower_level"],
        ship_buying_strategy="cheapest",
        repair_threshold=0.9
    )
}

def get_personality(name: str) -> AIPersonality:
    """Retorna a personalidade especificada"""
    if name not in AI_PERSONALITIES:
        available = list(AI_PERSONALITIES.keys())
        raise ValueError(f"Personalidade '{name}' não encontrada. Disponíveis: {available}")
    return AI_PERSONALITIES[name]

def list_personalities() -> List[str]:
    """Lista todas as personalidades disponíveis"""
    return list(AI_PERSONALITIES.keys())

def get_personality_summary(name: str) -> Dict[str, any]:
    """Retorna um resumo da personalidade para logging/debug"""
    personality = get_personality(name)
    return {
        "name": personality.name,
        "description": personality.description,
        "risk_profile": "Alto" if personality.risk_tolerance > 0.7 else "Médio" if personality.risk_tolerance > 0.3 else "Baixo",
        "focus": "Batalha" if personality.battle_frequency > personality.work_frequency else "Economia" if personality.work_frequency > personality.battle_frequency else "Balanceado",
        "formation": personality.preferred_formation,
        "llm": personality.llm_type
    }

# Mapeamento de estratégias para facilitar decisões
STRATEGY_MAPPINGS = {
    "target_selection": {
        "higher_level": "Prefere oponentes de nível superior para maior XP",
        "equal_level": "Ataca oponentes de nível similar", 
        "lower_level": "Foca em oponentes mais fracos para vitórias garantidas",
        "npcs_only": "Só ataca NPCs, evita jogadores reais",
        "random": "Escolhe aleatoriamente qualquer oponente",
        "highest_elo": "Mira nos oponentes com maior ELO",
        "analyze_opponent": "Analisa estatísticas antes de decidir",
        "favorable_matchup": "Só ataca quando tem vantagem estatística",
        "strategic_target": "Escolhe baseado em objetivos de longo prazo"
    },
    
    "ship_buying": {
        "cheapest": "Sempre compra as naves mais baratas disponíveis",
        "balanced": "Balanceia custo-benefício das naves",
        "premium": "Prefere naves caras e poderosas"
    }
}
