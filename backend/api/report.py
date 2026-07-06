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