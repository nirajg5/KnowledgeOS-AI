"""
Document Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# ===========================================
# Create
# ===========================================

class DocumentCreate(BaseModel):

    filename: str

    original_filename: str

    file_type: str

    mime_type: str

    file_hash: str

    file_path: str

    file_size: int

    total_pages: int

    word_count: int


# ===========================================
# Update
# ===========================================

class DocumentUpdate(BaseModel):

    summary: Optional[str] = None
    keywords: Optional[str] = None
    processing_status: Optional[str] = None
    is_processed: Optional[bool] = None


# ===========================================
# Response
# ===========================================

class DocumentResponse(BaseModel):

    id: str

    filename: str

    original_filename: str

    file_type: str

    mime_type: str

    file_hash: str

    file_path: str

    file_size: int

    total_pages: int

    pageindex_doc_id: str | None = None

    word_count: int

    processing_status: str

    summary: str | None

    keywords: str | None

    language: Optional[str] = None

    title: str | None = None

    category: str | None = None

    is_processed: bool

    uploaded_at: datetime

    content: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )