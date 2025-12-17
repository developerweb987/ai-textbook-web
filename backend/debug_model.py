#!/usr/bin/env python3
"""
Debug script to check the ChatSession model
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Import the models to inspect
from db.models import ChatSession as DbChatSession
from sqlalchemy import inspect

# Check the model's table structure
print("ChatSession model columns:")
for column in DbChatSession.__table__.columns:
    print(f"  - {column.name}: {column.type}")

# Check if title column exists
column_names = [column.name for column in DbChatSession.__table__.columns]
print(f"\nColumn names: {column_names}")
print(f"Has 'title' column: {'title' in column_names}")

# Test creating an instance
try:
    session = DbChatSession(session_id="test", title="Test Title")
    print("\nSuccessfully created ChatSession instance with session_id and title")
    print(f"Session ID: {session.session_id}")
    print(f"Title: {session.title}")
except Exception as e:
    print(f"\nError creating ChatSession instance: {e}")