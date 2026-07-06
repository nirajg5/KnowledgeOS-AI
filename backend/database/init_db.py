"""
Database Initialization

Creates all database tables.
"""

from backend.database.database import Base
from backend.database.database import engine

# Import all models here
from backend.models.document import Document
from backend.models.chat_history import ChatHistory
from backend.models.report import Report


def init_database():
    """
    Create all database tables.
    """

    Base.metadata.create_all(bind=engine)

    print("=" * 60)
    print("KnowledgeOS AI")
    print("Database Initialized Successfully")
    print("=" * 60)


if __name__ == "__main__":
    init_database()