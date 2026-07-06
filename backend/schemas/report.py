"""
Report Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# ======================================================
# Generate Report Request
# ======================================================

class ReportCreate(BaseModel):

    document_id: Optional[str] = None

    report_name: str

    report_type: str = "executive"


# ======================================================
# Report Response
# ======================================================

class ReportResponse(BaseModel):

    id: str

    document_id: Optional[str] = None

    report_name: str

    report_type: str

    summary: Optional[str] = None

    key_insights: Optional[str] = None

    action_items: Optional[str] = None

    report_path: Optional[str] = None

    generated_by: str

    is_generated: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ======================================================
# Report Preview
# ======================================================

class ReportPreview(BaseModel):

    report_name: str

    summary: Optional[str] = None

    key_insights: Optional[str] = None

    action_items: Optional[str] = None