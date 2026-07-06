"""
Database Session

Dependency for FastAPI.
"""

from backend.database.database import SessionLocal


def get_db():
    """
    Creates a new database session.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()