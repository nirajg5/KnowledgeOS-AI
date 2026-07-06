"""
Chat History Model

Stores AI conversations.
"""

import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.sql import func

from backend.database.database import Base


class ChatHistory(Base):

    __tablename__ = "chat_history"

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # ==================================================
    # Session
    # ==================================================

    session_id = Column(
        String(100),
        nullable=False,
        index=True
    )

    # ==================================================
    # Document
    # ==================================================

    document_id = Column(
        String(36),
        ForeignKey("documents.id"),
        nullable=True
    )

    # ==================================================
    # Conversation
    # ==================================================

    user_question = Column(
        Text,
        nullable=False
    )

    ai_response = Column(
        Text,
        nullable=False
    )

    citations = Column(
        Text,
        nullable=True
    )

    # ==================================================
    # Metadata
    # ==================================================

    model_used = Column(
        String(100),
        nullable=True
    )

    response_time = Column(
        String(20),
        nullable=True
    )

    is_success = Column(
        Boolean,
        default=True
    )

    # ==================================================
    # Timestamp
    # ==================================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    def __repr__(self):

        return (
            f"<ChatHistory(session='{self.session_id}')>"
        )