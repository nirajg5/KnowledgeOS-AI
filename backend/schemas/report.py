"""
Report Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class ReportCreate(BaseModel):

    document_id: Optional[str] = None

    report_name: str

    report_type: str


class ReportResponse(BaseModel):

    id: str

    document_id: Optional[str]

    report_name: str

    report_type: str

    summary: Optional[str]

    key_insights: Optional[str]

    action_items: Optional[str]

    report_path: Optional[str]

    generated_by: str

    is_generated: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )