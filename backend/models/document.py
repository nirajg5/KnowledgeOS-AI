"""
Document Model

Stores uploaded enterprise documents.
"""

import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.sql import func



from backend.database.database import Base


class Document(Base):
    """
    Enterprise Document
    """

    __tablename__ = "documents"

    # ======================================================
    # Primary Key
    # ======================================================

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # ======================================================
    # Basic Information
    # ======================================================

    title = Column(
    String(300),
    nullable=True
    )

    category = Column(
    String(100),
    nullable=True
    )
    filename = Column(
        String(255),
        nullable=False
     )

    original_filename = Column(
        String(255),
        nullable=False
    )

    file_type = Column(
        String(20),
        nullable=False
    )
    mime_type = Column(
    String(100),
    nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )
    file_hash = Column(
    String(64),
    unique=True,
    nullable=False
)

    file_size = Column(
        Integer,
        nullable=False
    )

    total_pages = Column(
        Integer,
        default=0
    )
    word_count = Column(
    Integer,
    default=0,
    nullable=False
    )

    
    # ======================================================
    # Processing Information
    # ======================================================

    processing_status = Column(
        String(30),
        default="Pending"
    )


    # ======================================================
    # AI Information
    # ======================================================

    summary = Column(
        Text,
        nullable=True
    )
    content = Column(
    Text,
    nullable=True
   )

    keywords = Column(
        Text,
        nullable=True
    )

    language = Column(
        String(50),
        default="English"
    )

    # ======================================================
    # Status
    # ======================================================

    is_processed = Column(
        Boolean,
        default=False
    )

    is_deleted = Column(
        Boolean,
        default=False
    )
     
    pageindex_doc_id = Column(
    String(255),
    nullable=True,
    unique=True
    )

    # ======================================================
    # Timestamp
    # ======================================================

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    def __repr__(self):

        return (
            f"<Document("
            f"filename='{self.filename}', "
            f"status='{self.processing_status}')>"
        )