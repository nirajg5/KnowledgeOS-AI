"""
Analytics APIs
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db

from backend.schemas.analytics import DashboardAnalytics

from backend.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# ==========================================================
# Dashboard Analytics
# ==========================================================

@router.get(
    "/dashboard",
    response_model=DashboardAnalytics
)
def get_dashboard(
    db: Session = Depends(get_db)
):
    """
    Return enterprise analytics dashboard.
    """

    return AnalyticsService.get_dashboard(
        db
    )