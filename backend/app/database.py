"""
Backend database configuration and session management.

This module creates database connections using backend-specific
configuration and provides session management for the backend.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.config import DATABASE_URL, DB_ECHO
from database.models import Base
from typing import Generator

# Create database engine with backend configuration
engine = create_engine(
    DATABASE_URL,
    echo=DB_ECHO
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI.
    
    This function creates a database session using backend configuration
    and ensures it's properly closed after use.
    
    Yields:
        Session: A SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_session() -> Session:
    """
    Create a new database session.
    
    Returns:
        Session: A new SQLAlchemy session object.
    """
    return SessionLocal()

# Initialize database tables if needed
def init_database():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

def shutdown_database():
    """Shutdown database connections."""
    engine.dispose()

def check_database_health() -> dict:
    """
    Check database connection health.
    
    Returns:
        dict: Health status information.
    """
    try:
        with engine.connect() as connection:
            from sqlalchemy import text
            connection.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database_url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else "local",
            "engine_echo": DB_ECHO
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "database_url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else "local"
        }
