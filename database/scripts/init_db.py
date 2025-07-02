#!/usr/bin/env python3
"""
Quick database initialization script.
"""

import sys
import os

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import initialize_database

if __name__ == "__main__":
    print("🚀 Initializing database with seed data...")
    initialize_database(with_seed=True)
    print("✅ Database ready!")
