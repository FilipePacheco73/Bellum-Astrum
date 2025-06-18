from backend.app.database.create_database import engine, Base

"""
This script initializes the database schema for the Space Battle Game API.
It creates the necessary tables if they do not already exist.
"""

def create_db():
    """
    Create the database schema if it does not already exist.
    This function uses SQLAlchemy to create all tables defined in the Base metadata.
    """
    Base.metadata.create_all(bind=engine)
    print("Database schema created (if not already existing).")

if __name__ == "__main__":
    """
    Main entry point for the script.
    This will create the database schema when the script is run directly.
    """
    create_db()
    print("Database setup script finished. Data should be added via API endpoints.")