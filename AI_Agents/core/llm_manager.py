"""
LLM Manager - Handles loading and running of HuggingFace models for AI agents.
"""

import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    BitsAndBytesConfig,
    pipeline
)
from typing import Dict, Any, Optional
import logging
from pathlib import Path

from AI_Agents.config.llm_config import LLMConfig, get_llm_config, GLOBAL_CONFIG

logger = logging.getLogger(__name__)

class LLMManager:
    """Manages LLM models for different AI agent types"""
    
    def __init__(self):
        self.models: Dict[str, AutoModelForCausalLM] = {}
        self.tokenizers: Dict[str, AutoTokenizer] = {}
        self.pipelines: Dict[str, pipeline] = {}
        
        # Setup device
        self.device = GLOBAL_CONFIG["device"]
        logger.info(f"Device set to use {self.device}")
        
        # Create cache directory
        self.cache_dir = Path(GLOBAL_CONFIG["cache_dir"])
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def load_model(self, agent_type: str) -> bool:
        """Load a model for a specific agent type"""
        try:
            config = get_llm_config(agent_type)
            logger.info(f"Loading model for {agent_type}: {config.model_name}")
            
            # Setup quantization config if enabled
            quantization_config = None
            if config.load_in_4bit:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True,
                )
                logger.info(f"Using 4-bit quantization for {agent_type}")
            
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                config.model_name,
                cache_dir=str(self.cache_dir),
                trust_remote_code=config.trust_remote_code
            )
            
            # Set pad token if not present
            if tokenizer.pad_token is None:
                if config.pad_token_id is not None:
                    tokenizer.pad_token_id = config.pad_token_id
                else:
                    tokenizer.pad_token = tokenizer.eos_token
            
            # Load model
            model = AutoModelForCausalLM.from_pretrained(
                config.model_name,
                cache_dir=str(self.cache_dir),
                device_map=config.device_map,
                torch_dtype=torch.float16 if config.torch_dtype == "auto" else config.torch_dtype,
                quantization_config=quantization_config,
                trust_remote_code=config.trust_remote_code
            )
            
            # Create text generation pipeline
            text_pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device_map=config.device_map,
                torch_dtype=torch.float16
            )
            
            # Store everything
            self.models[agent_type] = model
            self.tokenizers[agent_type] = tokenizer
            self.pipelines[agent_type] = text_pipeline
            
            logger.info(f"Successfully loaded model for {agent_type}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model for {agent_type}: {str(e)}")
            return False
    
    def generate_response(self, agent_type: str, prompt: str, **kwargs) -> Optional[str]:
        """Generate response using the specified agent type's model"""
        if agent_type not in self.pipelines:
            logger.error(f"Model for {agent_type} not loaded")
            return None
            
        try:
            # Get model configuration
            config = get_llm_config(agent_type)
            
            # Truncate prompt if it's too long for small models
            max_prompt_length = 1500  # TinyLlama supports 2048, leave room for response
            if len(prompt) > max_prompt_length:
                logger.warning(f"Truncating long prompt for {agent_type}: {len(prompt)} -> {max_prompt_length}")
                prompt = prompt[-max_prompt_length:]  # Keep the end of the prompt (most recent context)
            
            # Override default parameters with any provided kwargs
            generation_params = {
                "max_new_tokens": config.max_tokens,
                "temperature": config.temperature,
                "do_sample": config.do_sample,
                "pad_token_id": self.tokenizers[agent_type].pad_token_id,
                "eos_token_id": config.eos_token_id or self.tokenizers[agent_type].eos_token_id,
                "return_full_text": False,  # Only return the generated text
                **kwargs
            }
            
            # Generate response
            outputs = self.pipelines[agent_type](prompt, **generation_params)
            
            if outputs and len(outputs) > 0:
                generated_text = outputs[0]["generated_text"].strip()
                
                # Validate response length
                if len(generated_text) < 5:
                    logger.warning(f"Generated response for {agent_type} too short: '{generated_text}'")
                    return None
                
                logger.debug(f"Generated response for {agent_type}: {generated_text[:100]}...")
                return generated_text
            else:
                logger.warning(f"No output generated for {agent_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating response for {agent_type}: {str(e)}")
            return None
    
    def unload_model(self, agent_type: str):
        """Unload a model to free memory"""
        if agent_type in self.models:
            del self.models[agent_type]
        if agent_type in self.tokenizers:
            del self.tokenizers[agent_type]
        if agent_type in self.pipelines:
            del self.pipelines[agent_type]
        
        # Force garbage collection
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        logger.info(f"Unloaded model for {agent_type}")
    
    def get_loaded_models(self) -> list:
        """Get list of currently loaded models"""
        return list(self.models.keys())
    
    def is_model_loaded(self, agent_type: str) -> bool:
        """Check if a model is loaded for the given agent type"""
        return agent_type in self.models and agent_type in self.pipelines
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage information"""
        info = {
            "loaded_models": len(self.models),
            "device": self.device
        }
        
        if torch.cuda.is_available():
            info.update({
                "gpu_memory_allocated": f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB",
                "gpu_memory_reserved": f"{torch.cuda.memory_reserved() / 1024**3:.2f} GB",
                "gpu_memory_cached": f"{torch.cuda.memory_cached() / 1024**3:.2f} GB"
            })
        
        return info

# Global instance
_llm_manager = None

def get_llm_manager() -> LLMManager:
    """Get the global LLM manager instance"""
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager
