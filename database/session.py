"""
Database session management and dependency injection.

This module handles SQLAlchemy session creation and provides
dependency injection functions for FastAPI routes.
"""

from sqlalchemy.orm import sessionmaker, Session
from .config import engine
from typing import Generator

# Session factory
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI.
    
    This function creates a database session and ensures it's properly
    closed after use. Used as a dependency in FastAPI route handlers.
    
    Yields:
        Session: A SQLAlchemy session object.
        
    Example:
        @app.get("/users/")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_session() -> Session:
    """
    Create a new database session.
    
    Use this for manual session management outside of FastAPI routes.
    Remember to close the session when done.
    
    Returns:
        Session: A new SQLAlchemy session object.
        
    Example:
        session = create_session()
        try:
            # Do database operations
            session.commit()
        finally:
            session.close()
    """
    return SessionLocal()
