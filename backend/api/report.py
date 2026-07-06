"""
Report APIs
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.schemas.report import ReportCreate
from backend.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post("/")
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):

    return ReportService.create_report(
        db,
        report
    )


@router.get("/")
def get_reports(
    db: Session = Depends(get_db)
):

    return ReportService.get_reports(db)

# ==========================================================
# Generate AI Report
# ==========================================================

@router.post("/generate/{document_id}")
def generate_ai_report(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Generate an AI report from a processed document.
    """

    return ReportService.generate_report(
        db,
        document_id
    )

# ==========================================================
# Generate & Export AI Report
# ==========================================================

@router.post("/generate-export/{document_id}")
def generate_and_export_report(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Generate an AI report, export it to Markdown,
    and save the report record.
    """

    return ReportService.generate_and_export(
        db=db,
        document_id=document_id
    )