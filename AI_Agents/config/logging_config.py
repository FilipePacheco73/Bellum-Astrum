"""
Logging Configuration for AI Agents
Sets up structured logging with separate files for debug and AI decisions
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from typing import Optional

class AIDecisionFormatter(logging.Formatter):
    """Custom formatter for AI decision logs"""
    
    def format(self, record):
        # Add timestamp and format specifically for AI decisions
        formatted_time = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        if hasattr(record, 'agent_name'):
            agent_prefix = f"[{record.agent_name}]"
        else:
            agent_prefix = "[SYSTEM]"
        
        if hasattr(record, 'round_number'):
            round_prefix = f"Round {record.round_number:03d}"
        else:
            round_prefix = "---"
        
        return f"{formatted_time} | {round_prefix} | {agent_prefix} | {record.getMessage()}"

class DebugFormatter(logging.Formatter):
    """Standard formatter for debug/system logs"""
    
    def __init__(self):
        super().__init__(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

def setup_logging(logs_dir: Path) -> tuple[logging.Logger, logging.Logger]:
    """
    Set up dual logging system:
    - debug_logger: For system debug, connections, errors
    - ai_logger: For AI decisions, actions, and results
    
    Returns:
        tuple: (debug_logger, ai_logger)
    """
    
    # Ensure logs directory exists
    logs_dir.mkdir(exist_ok=True)
    
    # Debug log file (system, connections, errors)
    debug_log_file = logs_dir / "debug.log"
    
    # AI decisions log file (decisions, actions, results)
    ai_decisions_log_file = logs_dir / "ai_decisions.log"
    
    # Configure debug logger
    debug_logger = logging.getLogger('bellum.debug')
    debug_logger.setLevel(logging.DEBUG)
    debug_logger.handlers.clear()  # Clear any existing handlers
    
    # Debug file handler
    debug_file_handler = logging.handlers.RotatingFileHandler(
        debug_log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(DebugFormatter())
    
    # Console handler for debug (only warnings and above)
    debug_console_handler = logging.StreamHandler()
    debug_console_handler.setLevel(logging.WARNING)
    debug_console_handler.setFormatter(DebugFormatter())
    
    debug_logger.addHandler(debug_file_handler)
    debug_logger.addHandler(debug_console_handler)
    
    # Configure AI decisions logger
    ai_logger = logging.getLogger('bellum.ai_decisions')
    ai_logger.setLevel(logging.INFO)
    ai_logger.handlers.clear()  # Clear any existing handlers
    ai_logger.propagate = False  # Don't propagate to root logger
    
    # AI decisions file handler
    ai_file_handler = logging.handlers.RotatingFileHandler(
        ai_decisions_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    ai_file_handler.setLevel(logging.INFO)
    ai_file_handler.setFormatter(AIDecisionFormatter())
    
    # Console handler for AI decisions (optional, for real-time monitoring)
    ai_console_handler = logging.StreamHandler()
    ai_console_handler.setLevel(logging.INFO)
    ai_console_handler.setFormatter(AIDecisionFormatter())
    
    ai_logger.addHandler(ai_file_handler)
    # ai_logger.addHandler(ai_console_handler)  # Uncomment for console output
    
    return debug_logger, ai_logger

def log_ai_decision(ai_logger: logging.Logger, agent_name: str, round_number: int, 
                   decision: str, context: Optional[dict] = None):
    """
    Log an AI decision with structured format
    """
    
    # Create log record with extra attributes
    record = ai_logger.makeRecord(
        ai_logger.name, logging.INFO, "", 0, decision, (), None
    )
    record.agent_name = agent_name
    record.round_number = round_number
    
    if context:
        # Add context to the message
        context_str = " | ".join([f"{k}: {v}" for k, v in context.items() if v is not None])
        if context_str:
            record.msg = f"{decision} | {context_str}"
    
    ai_logger.handle(record)
