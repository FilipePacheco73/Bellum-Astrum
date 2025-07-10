"""
Database configuration and engine setup.

This module contains all database configuration settings, including
database URL construction and engine initialization.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env
env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), env_file))

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable must be set.")

# Create database engine
echo_flag = os.getenv("DB_ECHO", "False").lower() == "true"

engine = create_engine(
    DATABASE_URL,
    echo=echo_flag
)

# Declarative base for SQLAlchemy models
Base = declarative_base()
