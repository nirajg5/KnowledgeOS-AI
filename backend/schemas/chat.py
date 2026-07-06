"""
Chat Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# ======================================================
# Chat Request
# ======================================================

class ChatCreate(BaseModel):

    session_id: str

    document_id: Optional[str] = None

    user_question: str


# ======================================================
# Chat Response
# ======================================================

class ChatResponse(BaseModel):

    id: str

    session_id: str

    document_id: Optional[str] = None

    user_question: str

    ai_response: str

    citations: Optional[str] = None

    model_used: Optional[str] = None

    response_time: Optional[str] = None

    is_success: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )