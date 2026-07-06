"""
Database Configuration

Creates:
- SQLAlchemy Engine
- Session Factory
- Declarative Base
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings


# ===========================================================
# Database Engine
# ===========================================================

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)


# ===========================================================
# Session Factory
# ===========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ===========================================================
# Base Class
# ===========================================================

Base = declarative_base()