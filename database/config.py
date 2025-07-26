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
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
DATABASE_URL = os.getenv(f"DATABASE_URL_{ENVIRONMENT.upper()}")
if not DATABASE_URL:
    raise RuntimeError(f"DATABASE_URL_{ENVIRONMENT.upper()} environment variable must be set.")

# Database settings
DB_ECHO = os.getenv("DB_ECHO", "False").lower() == "true"

# User seeding configuration
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
NPC_PASSWORD = os.getenv('NPC_PASSWORD')
NPC_ASTRO_EMAIL = os.getenv('NPC_ASTRO_EMAIL')
NPC_CYBER_EMAIL = os.getenv('NPC_CYBER_EMAIL')
NPC_ORION_EMAIL = os.getenv('NPC_ORION_EMAIL')
NPC_VEGA_EMAIL = os.getenv('NPC_VEGA_EMAIL')
NPC_NEBULA_EMAIL = os.getenv('NPC_NEBULA_EMAIL')
NPC_PULSAR_EMAIL = os.getenv('NPC_PULSAR_EMAIL')
NPC_QUASAR_EMAIL = os.getenv('NPC_QUASAR_EMAIL')
NPC_TITAN_EMAIL = os.getenv('NPC_TITAN_EMAIL')
NPC_SOLARIS_EMAIL = os.getenv('NPC_SOLARIS_EMAIL')
NPC_ANDROMEDA_EMAIL = os.getenv('NPC_ANDROMEDA_EMAIL')
NPC_CENTAURI_EMAIL = os.getenv('NPC_CENTAURI_EMAIL')

# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=DB_ECHO
)

# Declarative base for SQLAlchemy models
Base = declarative_base()

if ENVIRONMENT == "local":
    from database.lifecycle import initialize_database
    initialize_database(with_seed=True)