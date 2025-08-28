"""
LLM models configuration for AI agents.
"""

import torch
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuration for an LLM model"""
    model_name: str
    max_tokens: int
    temperature: float
    do_sample: bool
    pad_token_id: int = None
    eos_token_id: int = None
    device_map: str = "auto"
    torch_dtype: str = "auto"
    load_in_4bit: bool = False  # To reduce memory usage
    trust_remote_code: bool = False

# Configurations for different agent types
LLM_CONFIGS: Dict[str, LLMConfig] = {
    # Aggressive Agent - Using TinyLlama (lightweight and free)
    "aggressive": LLMConfig(
        model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        max_tokens=300,  # Increased for more complete responses
        temperature=0.8,
        do_sample=True,
        load_in_4bit=True,  # Use quantization to save VRAM
        device_map="cuda:0",  # Specify GPU explicitly
        torch_dtype="float16",  # Half precision for memory economy
        pad_token_id=2,
        eos_token_id=2
    ),
    
    # Defensive Agent - Using TinyLlama
    "defensive": LLMConfig(
        model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        max_tokens=300,
        temperature=0.4,
        do_sample=True,
        load_in_4bit=True,
        device_map="cuda:0",
        torch_dtype="float16",
        pad_token_id=2,
        eos_token_id=2
    ),
    
    # Tactical Agent - Using TinyLlama
    "tactical": LLMConfig(
        model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        max_tokens=300,
        temperature=0.6,
        do_sample=True,
        load_in_4bit=True,
        device_map="cuda:0",
        torch_dtype="float16",
        pad_token_id=2,
        eos_token_id=2
    )
}

# Global configurations
GLOBAL_CONFIG = {
    "device": "cuda" if torch.cuda.is_available() else "cpu",  # Auto-detect GPU
    "cache_dir": "./AI_Agents/models_cache",  # Local model cache
    "max_memory_per_gpu": "5GB",  # Optimized for RTX 4050 (6GB total)
    "offload_folder": "./AI_Agents/offload_cache",
    "torch_dtype": torch.float16,  # Use half precision for memory economy
    "attn_implementation": "flash_attention_2"  # Use flash attention if available
}

def get_llm_config(agent_type: str) -> LLMConfig:
    """Returns LLM configuration for a specific agent type"""
    if agent_type not in LLM_CONFIGS:
        raise ValueError(f"Agent type '{agent_type}' not found. Available: {list(LLM_CONFIGS.keys())}")
    return LLM_CONFIGS[agent_type]

def get_model_info(agent_type: str) -> Dict[str, Any]:
    """Returns model information for an agent type"""
    config = get_llm_config(agent_type)
    return {
        "model_name": config.model_name,
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "estimated_size": _get_model_size(config.model_name)
    }

def _get_model_size(model_name: str) -> str:
    """Estimates model size based on name"""
    size_mapping = {
        "microsoft/DialoGPT-medium": "~345M parameters (~690MB)",
        "gpt2": "~124M parameters (~500MB)",
        "gpt2-medium": "~345M parameters (~1.4GB)",
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0": "~1.1B parameters (~2.2GB, ~550MB with 4bit)",
        "mistralai/Mistral-7B-Instruct-v0.1": "~7B parameters (~14GB, ~3.5GB with 4bit)"
    }
    return size_mapping.get(model_name, "Unknown size")
