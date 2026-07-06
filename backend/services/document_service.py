"""
Document Service
"""

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from pathlib import Path

from backend.models.document import Document
from backend.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
)
from backend.utils.file_handler import (
    calculate_file_hash,
    delete_file,
    extract_metadata,
    get_extension,
    get_file_size,
    get_mime_type,
    save_file,
)
from backend.services.processing_service import (
    ProcessingService
)
from backend.retrival.processor import DocumentProcessor

from backend.retrival.ai_metadata import AIMetadataGenerator


class DocumentService:

    # ======================================================
    # Create Document
    # ======================================================

    @staticmethod
    def create_document(
        db: Session,
        document: DocumentCreate
    ):

        db_document = Document(**document.model_dump())

        db.add(db_document)

        db.commit()

        db.refresh(db_document)

        return db_document

    # ======================================================
    # Upload Document
    # ======================================================

    @staticmethod
    def upload_document(
        db: Session,
        file: UploadFile
    ):
        """
        Upload document and save metadata.
        """

        # Save file
        file_path = save_file(file)

        # Metadata
        extension = get_extension(file.filename)

        mime_type = get_mime_type(file.filename)

        file_size = get_file_size(file_path)

        file_hash = calculate_file_hash(file_path)

        total_pages, word_count = extract_metadata(file_path)

        # Duplicate Detection
        existing = (
            db.query(Document)
            .filter(Document.file_hash == file_hash)
            .first()
        )

        if existing:

            delete_file(str(file_path))

            raise HTTPException(
                status_code=409,
                detail="Duplicate document already exists."
            )

        document = DocumentCreate(

            filename=file_path.name,

            original_filename=file.filename,

            file_type=extension,

            mime_type=mime_type,

            file_hash=file_hash,

            file_path=str(file_path),

            file_size=file_size,

            total_pages=total_pages,

            word_count=word_count
        )

        return DocumentService.create_document(
            db,
            document
        )

    # ======================================================
    # Get Single Document
    # ======================================================

    @staticmethod
    def get_document(
        db: Session,
        document_id: str
    ):

        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    # ======================================================
    # Get All Documents
    # ======================================================

    @staticmethod
    def get_all_documents(
        db: Session
    ):

        return (
            db.query(Document)
            .filter(Document.is_deleted == False)
            .all()
        )

    # ======================================================
    # Search Documents
    # ======================================================

    @staticmethod
    def search_documents(
        db: Session,
        keyword: str
    ):

        return (
            db.query(Document)
            .filter(
                Document.filename.ilike(f"%{keyword}%"),
                Document.is_deleted == False
            )
            .all()
        )

    # ======================================================
    # Filter by File Type
    # ======================================================

    @staticmethod
    def filter_by_type(
        db: Session,
        file_type: str
    ):

        return (
            db.query(Document)
            .filter(
                Document.file_type == file_type,
                Document.is_deleted == False
            )
            .all()
        )

    # ======================================================
    # Pagination
    # ======================================================

    @staticmethod
    def get_documents_paginated(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        offset = (page - 1) * limit

        return (
            db.query(Document)
            .filter(Document.is_deleted == False)
            .offset(offset)
            .limit(limit)
            .all()
        )

    # ======================================================
    # Statistics
    # ======================================================

    @staticmethod
    def get_document_stats(
        db: Session
    ):

        documents = (
            db.query(Document)
            .filter(Document.is_deleted == False)
            .all()
        )

        total_documents = len(documents)

        total_size = sum(
            doc.file_size for doc in documents
        )

        processed = sum(
            1 for doc in documents
            if doc.is_processed
        )

        return {

            "total_documents": total_documents,

            "processed_documents": processed,

            "pending_documents": total_documents - processed,

            "total_size_bytes": total_size
        }

    # ======================================================
    # Update Document
    # ======================================================

    @staticmethod
    def update_document(
        db: Session,
        document_id: str,
        document: DocumentUpdate
    ):

        db_document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not db_document:

            return None

        update_data = document.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():

            setattr(db_document, key, value)

        db.commit()

        db.refresh(db_document)

        return db_document

    # ======================================================
    # Delete Document (Soft Delete)
    # ======================================================

    @staticmethod
    def delete_document(
        db: Session,
        document_id: str
    ):

        db_document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not db_document:

            return None

        db_document.is_deleted = True

        db.commit()

        db.refresh(db_document)

        return db_document

    @staticmethod
    def preview_document(
    db: Session,
    document_id: str
    ):

     document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.is_deleted == False
        )
        .first()
    )

     if not document:
        return None

     return {
        "id": document.id,
        "filename": document.original_filename,
        "file_type": document.file_type,
        "file_size": document.file_size,
        "total_pages": document.total_pages,
        "word_count": document.word_count,
        "processing_status": document.processing_status,
        "uploaded_at": document.uploaded_at
    }

    # ======================================================
# Download Document
# ======================================================

    @staticmethod
    def download_document(
      db: Session,
     document_id: str
    ):

     document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.is_deleted == False
        )
        .first()
    )

     if not document:
        return None

     path = Path(document.file_path)

     if not path.exists():
        return None

     return path
    

# ======================================================
# Process Document
# ======================================================

    @staticmethod
    def process_document(
    db: Session,
    document_id: str
):

     document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.is_deleted == False
        )
        .first()
    )

     if not document:
        return None

     return ProcessingService.process_document(
        db,
        document
    )