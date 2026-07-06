"""
Document APIs
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from backend.database.session import get_db
from backend.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
)
from backend.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# ==========================================================
# Upload Document
# ==========================================================

@router.post(
    "/upload",
    response_model=DocumentResponse
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return DocumentService.upload_document(
        db,
        file
    )


# ==========================================================
# Create Document
# ==========================================================

@router.post(
    "/",
    response_model=DocumentResponse
)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):

    return DocumentService.create_document(
        db,
        document
    )


# ==========================================================
# Get All Documents
# ==========================================================

@router.get(
    "/",
    response_model=list[DocumentResponse]
)
def get_documents(
    db: Session = Depends(get_db)
):

    return DocumentService.get_all_documents(db)


# ==========================================================
# Search Documents
# ==========================================================

@router.get("/search")
def search_documents(
    keyword: str,
    db: Session = Depends(get_db)
):

    return DocumentService.search_documents(
        db,
        keyword
    )


# ==========================================================
# Filter Documents
# ==========================================================

@router.get("/filter")
def filter_documents(
    file_type: str,
    db: Session = Depends(get_db)
):

    return DocumentService.filter_by_type(
        db,
        file_type
    )


# ==========================================================
# Pagination
# ==========================================================

@router.get("/page")
def paginated_documents(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    return DocumentService.get_documents_paginated(
        db,
        page,
        limit
    )


# ==========================================================
# Statistics
# ==========================================================

@router.get("/stats")
def document_stats(
    db: Session = Depends(get_db)
):

    return DocumentService.get_document_stats(
        db
    )


# ==========================================================
# Preview Document
# ==========================================================

@router.get("/{document_id}/preview")
def preview_document(
    document_id: str,
    db: Session = Depends(get_db)
):

    document = DocumentService.preview_document(
        db,
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

# ==========================================================
# Process Document
# ==========================================================

# ==========================================================
# Process Document
# ==========================================================

@router.post("/{document_id}/process")
def process_document(
    document_id: str,
    db: Session = Depends(get_db)
):

    document = DocumentService.process_document(
        db,
        document_id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "message": "Document processed successfully.",
        "document_id": document.id,
        "status": document.processing_status,
        "content_length": len(document.content or "")
    }


# ==========================================================
# Get Document
# ==========================================================

@router.get(
    "/{document_id}",
    response_model=DocumentResponse
)
def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):

    document = DocumentService.get_document(
        db,
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document


# ==========================================================
# Update Document
# ==========================================================

@router.put(
    "/{document_id}",
    response_model=DocumentResponse
)
def update_document(
    document_id: str,
    document: DocumentUpdate,
    db: Session = Depends(get_db)
):

    updated = DocumentService.update_document(
        db,
        document_id,
        document
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return updated


# ==========================================================
# Delete Document
# ==========================================================

@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):

    deleted = DocumentService.delete_document(
        db,
        document_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "message": "Document deleted successfully"
    }

# ==========================================================
# Download Document
# ==========================================================

@router.get("/{document_id}/download")
def download_document(
    document_id: str,
    db: Session = Depends(get_db)
):

    file_path = DocumentService.download_document(
        db,
        document_id
    )

    if file_path is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/octet-stream"
    )