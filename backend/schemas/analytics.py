"""
Analytics Schemas
"""

from pydantic import BaseModel


class DashboardAnalytics(BaseModel):

    total_documents: int

    processed_documents: int

    pending_documents: int

    total_pages: int

    total_words: int

    total_storage_bytes: int

    average_document_size: float

    pdf_documents: int

    docx_documents: int

    txt_documents: int

    csv_documents: int

    english_documents: int

    other_language_documents: int