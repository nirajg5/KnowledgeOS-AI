"""
Report Service
"""

from sqlalchemy.orm import Session

from backend.models.report import Report
from backend.schemas.report import ReportCreate
from datetime import datetime

from backend.models.document import Document

from backend.prompts.report import REPORT_PROMPT
from backend.utils.report_export import ReportExporter

from backend.services.llm_service import LLMService

from backend.prompts.report import (
    REPORT_PROMPT,
    REPORT_SYSTEM_PROMPT
)

class ReportService:

    @staticmethod
    def create_report(
        db: Session,
        report: ReportCreate
    ):

        db_report = Report(

            document_id=report.document_id,

            report_name=report.report_name,

            report_type=report.report_type

        )

        db.add(db_report)

        db.commit()

        db.refresh(db_report)

        return db_report

    @staticmethod
    def get_reports(
        db: Session
    ):

        return db.query(Report).all()
    

    # =====================================================
# Generate AI Report
# =====================================================

    @staticmethod
    def generate_report(
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
        raise Exception(
            "Document not found."
        )

     if not document.content:
        raise Exception(
            "Document has not been processed."
        )

     prompt = REPORT_PROMPT.format(
        document=document.content
    )

     report_text = LLMService.generate(

    prompt=prompt,

    system_prompt=REPORT_SYSTEM_PROMPT

)

     return {

        "document_id": document.id,

        "title": document.title or "Executive Report",

        "report_type": "executive",

        "summary": document.summary,

        "report": report_text,

        "generated_at": datetime.utcnow()

    }

    # ======================================================
# Generate & Export AI Report
# ======================================================

    @staticmethod
    def generate_and_export(
    db: Session,
    document_id: str
):

     from backend.models.document import Document
     from backend.services.llm_service import LLMService
     from backend.prompts.report import REPORT_PROMPT

     document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.is_deleted == False
        )
        .first()
    )

     if not document:
        raise Exception("Document not found.")

     if not document.content:
        raise Exception("Document is not processed.")

    # ---------------------------------------
    # Generate Report
    # ---------------------------------------

     prompt = REPORT_PROMPT.format(
        document=document.content
    )

     report_text = LLMService.generate(
        prompt=prompt,
        system_prompt="You are an Enterprise AI Report Generator."
    )

    # ---------------------------------------
    # Export Markdown
    # ---------------------------------------

     filename = (
        document.title
        or document.original_filename
        or document.filename
    )

     filename = filename.replace(" ", "_")

     report_path = ReportExporter.export_markdown(
        report_text,
        filename
    )

    # ---------------------------------------
    # Save Report
    # ---------------------------------------

     report = Report(

        document_id=document.id,

        report_name=filename,

        report_type="Executive",

        summary=document.summary,

        key_insights="",

        action_items="",

        report_path=str(report_path),

        generated_by="KnowledgeOS AI",

        is_generated=True

    )

     db.add(report)

     db.commit()

     db.refresh(report)

     return report


    