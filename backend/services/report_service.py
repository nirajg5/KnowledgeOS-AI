"""
Report Service
"""

from sqlalchemy.orm import Session

from backend.models.report import Report
from backend.schemas.report import ReportCreate


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