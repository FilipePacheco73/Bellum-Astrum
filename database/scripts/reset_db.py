#!/usr/bin/env python3
"""
Database reset script.
"""

import sys
import os

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import reset_database, seed_initial_data

if __name__ == "__main__":
    print("🔄 Resetting database...")
    reset_database()
    print("🌱 Seeding with initial data...")
    seed_initial_data()
    print("✅ Database reset and seeded!")
