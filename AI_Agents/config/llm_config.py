"""
Configuração dos modelos LLM para os agentes de IA.
"""

from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuração de um modelo LLM"""
    model_name: str
    max_tokens: int
    temperature: float
    do_sample: bool
    pad_token_id: int = None
    eos_token_id: int = None
    device_map: str = "auto"
    torch_dtype: str = "auto"
    load_in_4bit: bool = False  # Para reduzir uso de memória
    trust_remote_code: bool = False

# Configurações específicas para cada personalidade de IA
LLM_CONFIGS: Dict[str, LLMConfig] = {
    # IA Agressiva - Usando GPT2 que funcionou melhor
    "aggressive": LLMConfig(
        model_name="gpt2",  # Mudando para gpt2
        max_tokens=60,
        temperature=0.8,
        do_sample=True,
        load_in_4bit=True,
        pad_token_id=50256,
        eos_token_id=50256
    ),
    
    # IA Defensiva - Usando GPT2 
    "defensive": LLMConfig(
        model_name="gpt2",  # Mudando para gpt2
        max_tokens=60,
        temperature=0.4,
        do_sample=True,
        load_in_4bit=True,
        pad_token_id=50256,
        eos_token_id=50256
    ),
    
    # IA Tática - Mantendo GPT2 que já funcionava
    "tactical": LLMConfig(
        model_name="gpt2",
        max_tokens=80,
        temperature=0.6,
        do_sample=True,
        load_in_4bit=True,
        pad_token_id=50256,
        eos_token_id=50256
    )
}

# Configurações globais
GLOBAL_CONFIG = {
    "device": "auto",  # "cuda" se disponível, senão "cpu"
    "cache_dir": "./AI_Agents/models_cache",  # Cache local dos modelos
    "max_memory_per_gpu": "4GB",
    "offload_folder": "./AI_Agents/offload_cache"
}

# Prompts de sistema base (será expandido nos arquivos de prompts específicos)
BASE_SYSTEM_PROMPT = """
Você é um jogador AI no jogo espacial Bellum Astrum. Este é um jogo de batalha espacial onde você:

MECÂNICAS BÁSICAS:
- Possui naves com estatísticas (ataque, escudo, HP, evasão, taxa de tiro)
- Ganha créditos trabalhando (/work/perform) 
- Compra naves no mercado (/market/buy)
- Ativa naves para batalha (/battle/activate-ship)
- Batalha contra outros jogadores (/battle/battle)
- Repara naves danificadas (/shipyard/repair)

FORMAÇÕES DE BATALHA:
- AGGRESSIVE: Sem modificadores, ataque direto
- DEFENSIVE: +20% evasão, foca em sobrevivência  
- TACTICAL: -10% evasão, mas mira nos alvos mais ameaçadores

OBJETIVOS:
- Subir de nível e rank através de batalhas
- Gerenciar recursos (créditos) eficientemente
- Manter frota de naves ativa e saudável
- Dominar outros jogadores em combate

Você deve tomar decisões estratégicas baseadas na situação atual e sua personalidade.
"""

def get_llm_config(personality: str) -> LLMConfig:
    """Retorna a configuração LLM para uma personalidade específica"""
    if personality not in LLM_CONFIGS:
        raise ValueError(f"Personalidade '{personality}' não encontrada. Disponíveis: {list(LLM_CONFIGS.keys())}")
    return LLM_CONFIGS[personality]

def get_model_info(personality: str) -> Dict[str, Any]:
    """Retorna informações sobre o modelo para uma personalidade"""
    config = get_llm_config(personality)
    return {
        "model_name": config.model_name,
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "estimated_size": _get_model_size(config.model_name)
    }

def _get_model_size(model_name: str) -> str:
    """Estima o tamanho do modelo baseado no nome"""
    size_mapping = {
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0": "~1.1B parâmetros (~2.2GB)",
        "microsoft/DialoGPT-medium": "~345M parâmetros (~1.4GB)",
        "mistralai/Mistral-7B-Instruct-v0.1": "~7B parâmetros (~14GB)"
    }
    return size_mapping.get(model_name, "Tamanho desconhecido")
