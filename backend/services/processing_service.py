"""
Processing Service

Coordinates the document processing pipeline.
"""

from sqlalchemy.orm import Session

from backend.models.document import Document

from backend.retrival.processor import DocumentProcessor
from backend.services.metadata_service import MetadataService
from backend.retrival.pageindex_client import (
    KnowledgePageIndex
)
from backend.retrival.pageindex_client import KnowledgePageIndex


class ProcessingService:

    @staticmethod
    def process_document(
        db: Session,
        document: Document
    ):

        # ----------------------------------
        # Extract Text
        # ----------------------------------

        extracted_text = DocumentProcessor.extract_text(
            document.file_path
        )

        document.content = extracted_text

        # ----------------------------------
        # Generate AI Metadata
        # ----------------------------------

        metadata = MetadataService.generate_metadata(
            extracted_text
        )

        document.title = metadata.get("title")

        document.summary = metadata.get("summary")

        document.category = metadata.get("category")

        document.language = metadata.get("language")

        document.keywords = ",".join(
            metadata.get("keywords", [])
        )


       # ==========================================
# Upload to PageIndex
# ==========================================

        print("=" * 60)
        print("START PAGEINDEX UPLOAD")
        print("File:", document.file_path)
        print("=" * 60)

        pageindex = KnowledgePageIndex()

        response = pageindex.upload_document(
    document.file_path
)

        print("UPLOAD RESPONSE:", response)

        document.pageindex_doc_id = response.get("doc_id")
        print("PageIndex Response:", response)
        print("Saved Doc ID:", document.pageindex_doc_id)

        pageindex.wait_until_ready(
    document.pageindex_doc_id
)

        print("PAGEINDEX PROCESSING COMPLETED")
        if isinstance(response, dict):
         document.pageindex_doc_id = response.get("doc_id")
        else:
         print("Unexpected response type:", type(response))

        pageindex.wait_until_ready(
    document.pageindex_doc_id
      )
        # ----------------------------------
        # Processing Status
        # ----------------------------------

        document.processing_status = "Completed"

        document.is_processed = True

        db.commit()

        db.refresh(document)
        print("Database Doc ID:", document.pageindex_doc_id)

        return document
    

    