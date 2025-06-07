from app.database.create_database import engine, Base

"""
This script initializes the database schema for the Space Battle Game API.
It creates the necessary tables if they do not already exist.
"""

def create_db():
    Base.metadata.create_all(bind=engine)
    print("Database schema created (if not already existing).")

if __name__ == "__main__":
    create_db()
    print("Database setup script finished. Data should be added via API endpoints.")