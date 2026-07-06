"""
Report Model

Stores AI generated reports.
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


class Report(Base):

    __tablename__ = "reports"

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # ==================================================
    # Related Document
    # ==================================================

    document_id = Column(
        String(36),
        ForeignKey("documents.id"),
        nullable=True
    )

    # ==================================================
    # Report Information
    # ==================================================

    report_name = Column(
        String(255),
        nullable=False
    )

    report_type = Column(
        String(100),
        nullable=False
    )

    summary = Column(
        Text,
        nullable=True
    )

    key_insights = Column(
        Text,
        nullable=True
    )

    action_items = Column(
        Text,
        nullable=True
    )

    report_path = Column(
        String(500),
        nullable=True
    )

    generated_by = Column(
        String(100),
        default="KnowledgeOS AI"
    )

    # ==================================================
    # Status
    # ==================================================

    is_generated = Column(
        Boolean,
        default=False
    )

    # ==================================================
    # Timestamp
    # ==================================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    def __repr__(self):

        return (
            f"<Report(report='{self.report_name}')>"
        )