#!/usr/bin/env python3
"""
Script to recreate the database with the correct schema
"""
import asyncio
from db.database import engine, drop_tables, create_tables
from config import settings
import os

async def recreate_database():
    print("Dropping and recreating database tables...")

    # Drop all tables
    await drop_tables()
    print("All tables dropped.")

    # Create all tables with new schema
    await create_tables()
    print("All tables recreated with new schema.")

    print("Database has been reset with correct schema!")

if __name__ == "__main__":
    asyncio.run(recreate_database())