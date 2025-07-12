#!/usr/bin/env python3
"""
Database setup and seeding script for Bellum Astrum.

This script provides commands to initialize, seed, reset, and manage
the database from the command line.

Database: Neon (PostgreSQL as a Service)

Usage:
    python setup.py init              # Initialize database (create tables)
    python setup.py init --seed       # Initialize database with sample data
    python setup.py seed              # Add sample data to existing database
    python setup.py reset             # Reset database (drop + recreate tables)
    python setup.py reset --seed      # Reset database and add sample data
    python setup.py clear             # Clear all data (keep tables)
    python setup.py health            # Check database health
"""

import argparse
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), env_file))

# Add the current directory to Python path so we can import the database module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

from database import (
    initialize_database,
    seed_initial_data,
    reset_database, 
    clear_all_data,
    check_database_health
)

def main():
    parser = argparse.ArgumentParser(description='Database setup and seeding for Bellum Astrum')
    parser.add_argument('command', choices=['init', 'seed', 'reset', 'clear', 'health'],
                       help='Command to execute')
    parser.add_argument('--seed', action='store_true',
                       help='Also seed data when initializing or resetting')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'init':
            print("🚀 Initializing database...")
            initialize_database(with_seed=args.seed)
            print("✅ Database initialized successfully!")
            
        elif args.command == 'seed':
            print("🌱 Seeding database with initial data...")
            seed_initial_data()
            print("✅ Database seeded successfully!")
            
        elif args.command == 'reset':
            print("🔄 Resetting database...")
            reset_database()
            if args.seed:
                print("🌱 Seeding with initial data...")
                seed_initial_data()
            print("✅ Database reset successfully!")
            
        elif args.command == 'clear':
            print("🧹 Clearing all database data...")
            clear_all_data()
            print("✅ Database data cleared successfully!")
            
        elif args.command == 'health':
            print("🩺 Checking database health...")
            if check_database_health():
                print("✅ Database is healthy and accessible!")
            else:
                print("❌ Database is not accessible!")
                sys.exit(1)
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()