"""
Backend configuration module.

This module handles backend-specific configuration including
database connections and other environment settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from backend .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

# Database configuration
DATABASE_URL = os.getenv(f"DATABASE_URL_{ENVIRONMENT.upper()}")
if not DATABASE_URL:
    raise RuntimeError(f"DATABASE_URL_{ENVIRONMENT.upper()} environment variable must be set in backend/.env")

# Database settings
DB_ECHO = os.getenv("DB_ECHO", "False").lower() == "true"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# JWT Configuration - Environment-based
JWT_SECRET_KEY = os.getenv(f"JWT_SECRET_KEY_{ENVIRONMENT.upper()}")
if not JWT_SECRET_KEY:
    raise RuntimeError(f"JWT_SECRET_KEY_{ENVIRONMENT.upper()} environment variable must be set in backend/.env")

# Python path configuration
PYTHONPATH = os.getenv("PYTHONPATH", ".")