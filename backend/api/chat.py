"""
Chat APIs
"""

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.schemas.chat import ChatCreate
from backend.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

# ==========================================================
# Normal Chat
# ==========================================================

@router.post("/")
def ask_ai(
    chat: ChatCreate,
    db: Session = Depends(get_db)
):
    """
    Ask a question to an uploaded document.
    """

    return ChatService.ask_document(
        db=db,
        chat=chat
    )


# ==========================================================
# Streaming Chat
# ==========================================================

@router.post("/stream")
def stream_ai(
    chat: ChatCreate,
    db: Session = Depends(get_db)
):
    """
    Stream AI response token by token.
    """

    generator = ChatService.stream_document(
        db=db,
        chat=chat
    )

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )


# ==========================================================
# Chat History
# ==========================================================

@router.get("/{session_id}")
def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db)
):

    return ChatService.get_session(
        db,
        session_id
    )