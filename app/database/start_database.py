'''
Code to create the Database
'''

# Ensure create_database is correctly imported.
# If it's in the same directory, it might be:
# from .create_database import engine, Base
# If create_database.py is directly in app/database/ then:
from app.database.create_database import engine, Base

# The add_initial_data.py file might become unused after this,
# consider if it should be deleted or kept if it has other utilities.
# For now, just remove the import of its functions here.

def create_db():
    Base.metadata.create_all(bind=engine)
    print("Database schema created (if not already existing).")

if __name__ == "__main__":
    create_db()
    print("Database setup script finished. Data should be added via API endpoints.")