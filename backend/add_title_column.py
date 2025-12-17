#!/usr/bin/env python3
"""
Script to add the missing 'title' column to the chat_sessions table
"""
import sqlite3
from config import settings

def add_title_column():
    # Connect to the database
    conn = sqlite3.connect(settings.DATABASE_URL.replace('sqlite+aiosqlite:///', '').replace('sqlite:///', ''))
    cursor = conn.cursor()

    try:
        # Check if the title column already exists
        cursor.execute("PRAGMA table_info(chat_sessions)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'title' not in columns:
            # Add the title column
            cursor.execute("ALTER TABLE chat_sessions ADD COLUMN title TEXT")
            print("Added 'title' column to chat_sessions table")
        else:
            print("'title' column already exists in chat_sessions table")

        conn.commit()
        print("Database updated successfully!")

    except Exception as e:
        print(f"Error updating database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_title_column()