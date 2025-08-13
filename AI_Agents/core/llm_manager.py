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
    """Manages LLM models for different AI personalities"""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or GLOBAL_CONFIG["cache_dir"]
        self.models: Dict[str, Any] = {}
        self.tokenizers: Dict[str, Any] = {}
        self.pipelines: Dict[str, Any] = {}
        self._ensure_cache_dir()
        
    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        
    def load_model(self, personality: str) -> bool:
        """Load a model for a specific personality"""
        try:
            config = get_llm_config(personality)
            logger.info(f"Loading model for {personality}: {config.model_name}")
            
            # Configure quantization if needed
            quantization_config = None
            if config.load_in_4bit:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_compute_dtype=torch.float16
                )
            
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                config.model_name,
                cache_dir=self.cache_dir,
                trust_remote_code=config.trust_remote_code
            )
            
            # Handle missing pad token
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            # Load model
            model = AutoModelForCausalLM.from_pretrained(
                config.model_name,
                cache_dir=self.cache_dir,
                device_map=config.device_map,
                torch_dtype=getattr(torch, config.torch_dtype) if config.torch_dtype != "auto" else "auto",
                quantization_config=quantization_config,
                trust_remote_code=config.trust_remote_code
            )
            
            # Create pipeline
            text_pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=config.max_tokens,
                temperature=config.temperature,
                do_sample=config.do_sample,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
            
            # Store components
            self.models[personality] = model
            self.tokenizers[personality] = tokenizer
            self.pipelines[personality] = text_pipeline
            
            logger.info(f"Successfully loaded model for {personality}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model for {personality}: {str(e)}")
            return False
    
    def generate_response(self, personality: str, prompt: str, **kwargs) -> Optional[str]:
        """Generate response using the specified personality's model"""
        if personality not in self.pipelines:
            logger.error(f"Model for {personality} not loaded")
            return None
            
        try:
            # Get model configuration
            config = get_llm_config(personality)
            
            # Truncate prompt if it's too long for small models
            max_prompt_length = 512  # Conservative limit for small models
            if len(prompt) > max_prompt_length:
                logger.warning(f"Truncating long prompt for {personality}: {len(prompt)} -> {max_prompt_length}")
                prompt = prompt[-max_prompt_length:]  # Keep the end of the prompt (most recent context)
            
            # Override default parameters with any provided kwargs
            generation_params = {
                "max_new_tokens": kwargs.get("max_tokens", config.max_tokens),
                "temperature": kwargs.get("temperature", config.temperature),
                "do_sample": kwargs.get("do_sample", config.do_sample),
                "pad_token_id": self.tokenizers[personality].pad_token_id,
                "eos_token_id": self.tokenizers[personality].eos_token_id,
                "return_full_text": False  # Only return generated text
            }
            
            logger.debug(f"Generating response for {personality} with prompt length: {len(prompt)}")
            
            # Generate response
            pipeline_output = self.pipelines[personality](prompt, **generation_params)
            
            # Debug logging
            logger.debug(f"Pipeline output type: {type(pipeline_output)}")
            logger.debug(f"Pipeline output: {pipeline_output}")
            
            if pipeline_output and len(pipeline_output) > 0:
                try:
                    # Check if output has the expected structure
                    if isinstance(pipeline_output[0], dict) and "generated_text" in pipeline_output[0]:
                        response = pipeline_output[0]["generated_text"].strip()
                        
                        # Check if response is meaningful (not just whitespace or newlines)
                        if response and not response.replace('\n', '').replace(' ', '').replace('\t', ''):
                            logger.warning(f"Generated response for {personality} is only whitespace: '{response}'")
                            return None
                        
                        if len(response) < 3:
                            logger.warning(f"Generated response for {personality} too short: '{response}'")
                            return None
                            
                        logger.debug(f"Generated response for {personality}: {response[:100]}...")
                        return response
                    else:
                        logger.error(f"Unexpected pipeline output structure for {personality}: {pipeline_output[0]}")
                        return None
                except (IndexError, KeyError, TypeError) as e:
                    logger.error(f"Error accessing pipeline output for {personality}: {str(e)}")
                    logger.error(f"Pipeline output structure: {pipeline_output}")
                    return None
            else:
                logger.warning(f"Empty or None response from {personality} model")
                return None
                
        except Exception as e:
            logger.error(f"Error generating response for {personality}: {str(e)}")
            return None
    
    def is_model_loaded(self, personality: str) -> bool:
        """Check if a model is loaded for the personality"""
        return personality in self.pipelines
    
    def unload_model(self, personality: str) -> bool:
        """Unload a model to free memory"""
        try:
            if personality in self.models:
                del self.models[personality]
            if personality in self.tokenizers:
                del self.tokenizers[personality]
            if personality in self.pipelines:
                del self.pipelines[personality]
                
            # Force garbage collection
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
            logger.info(f"Unloaded model for {personality}")
            return True
            
        except Exception as e:
            logger.error(f"Error unloading model for {personality}: {str(e)}")
            return False
    
    def get_loaded_models(self) -> list:
        """Get list of loaded model personalities"""
        return list(self.pipelines.keys())
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage information"""
        usage = {
            "loaded_models": len(self.pipelines),
            "personalities": list(self.pipelines.keys())
        }
        
        if torch.cuda.is_available():
            usage.update({
                "gpu_memory_allocated": torch.cuda.memory_allocated(),
                "gpu_memory_reserved": torch.cuda.memory_reserved(),
                "gpu_memory_cached": torch.cuda.memory_cached()
            })
        
        return usage
    
    def cleanup(self):
        """Clean up all models and free memory"""
        personalities = list(self.pipelines.keys())
        for personality in personalities:
            self.unload_model(personality)
        
        logger.info("LLM Manager cleanup completed")


# Singleton instance for easy access
_llm_manager_instance = None

def get_llm_manager() -> LLMManager:
    """Get the global LLM manager instance"""
    global _llm_manager_instance
    if _llm_manager_instance is None:
        _llm_manager_instance = LLMManager()
    return _llm_manager_instance
