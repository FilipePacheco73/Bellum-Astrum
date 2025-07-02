#!/usr/bin/env python3
"""
Database seeding script.
"""

import sys
import os

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import seed_initial_data

if __name__ == "__main__":
    print("🌱 Seeding database...")
    seed_initial_data()
    print("✅ Database seeded!")
