"""
LLM Manager - Handles loading and running of HuggingFace models for AI agents.
"""

import torch
import asyncio
import functools
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    BitsAndBytesConfig,
    pipeline
)
from typing import Dict, Any, Optional, NamedTuple
import logging
from pathlib import Path

from AI_Agents.config.llm_config import LLMConfig, get_llm_config, GLOBAL_CONFIG

logger = logging.getLogger(__name__)

class LLMResponse(NamedTuple):
    """Structure for LLM response with token information"""
    text: str
    input_tokens: int
    output_tokens: int
    reasoning: str = ""

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
            
            # Check if we already have this exact model loaded
            for existing_type, existing_config in [(t, get_llm_config(t)) for t in self.models.keys()]:
                if (existing_config.model_name == config.model_name and 
                    existing_config.load_in_4bit == config.load_in_4bit):
                    
                    logger.info(f"Reusing existing model for {agent_type} (same as {existing_type})")
                    # Share the same model, tokenizer, and pipeline
                    self.models[agent_type] = self.models[existing_type]
                    self.tokenizers[agent_type] = self.tokenizers[existing_type]
                    self.pipelines[agent_type] = self.pipelines[existing_type]
                    return True
            
            # If we reach here, we need to load a new model
            logger.info(f"Loading new model instance for {agent_type}")
            
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
    
    def generate_response(self, agent_type: str, prompt: str, **kwargs) -> Optional[LLMResponse]:
        """Generate response using the specified agent type's model with token tracking"""
        if agent_type not in self.pipelines:
            logger.error(f"Model for {agent_type} not loaded")
            return None
            
        try:
            # Get model configuration
            config = get_llm_config(agent_type)
            logger.debug(f"Generating response for {agent_type} with prompt length: {len(prompt)}")
            
            # Tokenize input to count input tokens
            tokenizer = self.tokenizers[agent_type]
            input_tokens = tokenizer.encode(prompt)
            input_token_count = len(input_tokens)
            
            # Truncate prompt if it's too long for small models
            max_prompt_length = 1800  # TinyLlama supports 2048, leave room for response
            if len(prompt) > max_prompt_length:
                logger.warning(f"Truncating long prompt for {agent_type}: {len(prompt)} -> {max_prompt_length}")
                prompt = prompt[-max_prompt_length:]  # Keep the end of the prompt (most recent context)
                # Recalculate input tokens after truncation
                input_tokens = tokenizer.encode(prompt)
                input_token_count = len(input_tokens)
            
            # Override default parameters with any provided kwargs - use more conservative settings
            generation_params = {
                "max_new_tokens": config.max_tokens,  # Allow full token limit for detailed reasoning
                "temperature": config.temperature,
                "do_sample": config.do_sample,
                "pad_token_id": tokenizer.pad_token_id,
                "eos_token_id": config.eos_token_id or tokenizer.eos_token_id,
                "return_full_text": False,  # Only return the generated text
                "repetition_penalty": 1.1,  # Prevent repetitive responses
                "no_repeat_ngram_size": 3,  # Prevent repetition
                **kwargs
            }
            
            logger.debug(f"Starting generation for {agent_type} with {input_token_count} input tokens...")
            
            # Generate response with timeout protection
            try:
                outputs = self.pipelines[agent_type](prompt, **generation_params)
            except Exception as gen_error:
                logger.error(f"Generation failed for {agent_type}: {str(gen_error)}")
                # Return LLMResponse with input_tokens but failed output
                return LLMResponse(
                    text="",
                    input_tokens=input_token_count,
                    output_tokens=0,
                    reasoning=f"Generation error: {str(gen_error)}"
                )
            
            logger.debug(f"Generation completed for {agent_type}")
            
            if outputs and len(outputs) > 0:
                generated_text = outputs[0]["generated_text"].strip()
                
                # Count output tokens
                output_tokens = tokenizer.encode(generated_text)
                output_token_count = len(output_tokens)
                
                # Validate response length
                if len(generated_text) < 2:
                    logger.warning(f"Generated response for {agent_type} too short: '{generated_text}'")
                    # Return LLMResponse with input_tokens but failed output
                    return LLMResponse(
                        text="",
                        input_tokens=input_token_count,
                        output_tokens=0,
                        reasoning="Response too short"
                    )
                
                logger.debug(f"Generated response for {agent_type}: {generated_text[:100]}... ({output_token_count} output tokens)")
                
                # For now, use the generated text as reasoning
                # In future, we could extract reasoning from a more complex prompt
                reasoning = generated_text
                
                return LLMResponse(
                    text=generated_text,
                    input_tokens=input_token_count,
                    output_tokens=output_token_count,
                    reasoning=reasoning
                )
            else:
                logger.warning(f"No output generated for {agent_type}")
                # Return LLMResponse with input_tokens but failed output
                return LLMResponse(
                    text="",
                    input_tokens=input_token_count,
                    output_tokens=0,
                    reasoning="No output generated"
                )
                
        except Exception as e:
            logger.error(f"Error generating response for {agent_type}: {str(e)}")
            # Try to return input_tokens if we calculated them before the error
            try:
                # If we at least got the tokenizer working, return the input tokens
                tokenizer = self.tokenizers.get(agent_type)
                if tokenizer:
                    input_tokens = tokenizer.encode(prompt)
                    input_token_count = len(input_tokens)
                    return LLMResponse(
                        text="",
                        input_tokens=input_token_count,
                        output_tokens=0,
                        reasoning=f"Error: {str(e)}"
                    )
            except:
                pass
            
            return LLMResponse(
                text="",
                input_tokens=0,
                output_tokens=0,
                reasoning=f"Fatal error: {str(e)}"
            )
    
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

def preload_shared_models():
    """Preload shared models to avoid multiple loading"""
    manager = get_llm_manager()
    
    # Since all agent types use the same TinyLlama model, load it once for 'aggressive'
    # and the other types will reuse it
    logger.info("Preloading shared models...")
    success = manager.load_model('aggressive')
    
    if success:
        logger.info("Shared model preloaded successfully")
        # The other types will automatically share this model when they try to load
        return True
    else:
        logger.error("Failed to preload shared model")
        return False
