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
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Database configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.getenv("DB_NAME", "Bellum_Astrum.db")
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, DATABASE_NAME)}"

# SQLite specific configuration for FastAPI
SQLITE_CONNECT_ARGS = {"check_same_thread": False}

# Create database engine
echo_flag = os.getenv("DB_ECHO", "False").lower() == "true"
engine = create_engine(
    DATABASE_URL, 
    connect_args=SQLITE_CONNECT_ARGS,
    echo=echo_flag  # Set to True for SQL query logging in development
)

# Declarative base for SQLAlchemy models
Base = declarative_base()
