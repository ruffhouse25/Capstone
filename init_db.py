#!/usr/bin/env python3
"""
Database initialization script for Heroku deployment
This script creates all database tables
"""

import os
from app import APP
from models import db, setup_db

def init_database():
    """Initialize database tables"""
    print("Initializing database...")
    
    # Setup database with app context
    with APP.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Verify tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Created tables: {tables}")

if __name__ == '__main__':
    init_database()
