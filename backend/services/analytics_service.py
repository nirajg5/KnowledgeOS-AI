"""
Analytics Service
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models.document import Document


class AnalyticsService:

    # ======================================================
    # Dashboard Analytics
    # ======================================================

    @staticmethod
    def get_dashboard(
        db: Session
    ):

        documents = (
            db.query(Document)
            .filter(Document.is_deleted == False)
            .all()
        )

        total_documents = len(documents)

        processed_documents = sum(
            1 for doc in documents
            if doc.is_processed
        )

        pending_documents = (
            total_documents - processed_documents
        )

        total_pages = sum(
            doc.total_pages or 0
            for doc in documents
        )

        total_words = sum(
            doc.word_count or 0
            for doc in documents
        )

        total_storage_bytes = sum(
            doc.file_size or 0
            for doc in documents
        )

        average_document_size = 0.0

        if total_documents > 0:

            average_document_size = (
                total_storage_bytes / total_documents
            )

        # ==================================================
        # File Types
        # ==================================================

        pdf_documents = sum(
            1 for doc in documents
            if doc.file_type.lower() == ".pdf"
        )

        docx_documents = sum(
            1 for doc in documents
            if doc.file_type.lower() == ".docx"
        )

        txt_documents = sum(
            1 for doc in documents
            if doc.file_type.lower() == ".txt"
        )

        csv_documents = sum(
            1 for doc in documents
            if doc.file_type.lower() == ".csv"
        )

        # ==================================================
        # Languages
        # ==================================================

        english_documents = sum(
            1 for doc in documents
            if (
                doc.language
                and doc.language.lower() == "english"
            )
        )

        other_language_documents = (
            total_documents - english_documents
        )

        return {

            "total_documents": total_documents,

            "processed_documents": processed_documents,

            "pending_documents": pending_documents,

            "total_pages": total_pages,

            "total_words": total_words,

            "total_storage_bytes": total_storage_bytes,

            "average_document_size": round(
                average_document_size,
                2
            ),

            "pdf_documents": pdf_documents,

            "docx_documents": docx_documents,

            "txt_documents": txt_documents,

            "csv_documents": csv_documents,

            "english_documents": english_documents,

            "other_language_documents": other_language_documents

        }