"""DATABASE INITIALIZATION - Run this to create tables"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db

def init_database():
    """Initialize the SQLite database by creating all tables"""
    print("\n🔧 Initializing database...")
    
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
        print("\n📊 Created tables:")
        print("   - users")
        print("   - conversations")
        print("   - messages")
        print("   - notes")
        print("   - pdf_summaries")
        print("   - quizzes")
        print("   - quiz_attempts")
        print("   - flashcards")
        print("   - study_plans")
        print("\n📝 Database path: database/database.db")
        print("\n✨ Database initialization complete!\n")

if __name__ == '__main__':
    init_database()
