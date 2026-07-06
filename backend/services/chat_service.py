"""
Chat Service
"""

from sqlalchemy.orm import Session

from backend.models.chat_history import ChatHistory
from backend.models.document import Document

from backend.schemas.chat import ChatCreate

from backend.retrival.pageindex_client import KnowledgePageIndex


class ChatService:

    # =====================================================
    # Save Chat
    # =====================================================

    @staticmethod
    def create_chat(
        db: Session,
        chat: ChatCreate,
        ai_response: str,
        citations: str = ""
    ):

        db_chat = ChatHistory(

            session_id=chat.session_id,

            document_id=chat.document_id,

            user_question=chat.user_question,

            ai_response=ai_response,

            citations=citations,

            model_used="PageIndex",

            response_time="0 sec"

        )

        db.add(db_chat)

        db.commit()

        db.refresh(db_chat)

        return db_chat

    # =====================================================
    # Get Session
    # =====================================================

    @staticmethod
    def get_session(
        db: Session,
        session_id: str
    ):

        return (
            db.query(ChatHistory)
            .filter(
                ChatHistory.session_id == session_id
            )
            .all()
        )

    # =====================================================
    # Normal Chat
    # =====================================================

    @staticmethod
    def ask_document(
        db: Session,
        chat: ChatCreate
    ):

        document = (
            db.query(Document)
            .filter(
                Document.id == chat.document_id,
                Document.is_deleted == False
            )
            .first()
        )

        if not document:
            raise Exception("Document not found.")

        if not document.pageindex_doc_id:
            raise Exception(
                "Document is not indexed in PageIndex."
            )

        client = KnowledgePageIndex()

        response = client.chat(

            doc_id=document.pageindex_doc_id,

            question=chat.user_question

        )

        tree = client.get_citations(
            document.pageindex_doc_id
        )

        ai_response = response["choices"][0]["message"]["content"]

        citations = str(tree)

        return ChatService.create_chat(

            db=db,

            chat=chat,

            ai_response=ai_response,

            citations=citations

        )

    # =====================================================
# Stream Chat
# =====================================================

 
    @staticmethod
    def stream_document(
    db: Session,
    chat: ChatCreate
):

     document = (
        db.query(Document)
        .filter(
            Document.id == chat.document_id,
            Document.is_deleted == False
        )
        .first()
    )

     if not document:
        raise Exception("Document not found.")

     if not document.pageindex_doc_id:
        raise Exception(
            "Document is not indexed in PageIndex."
        )

     client = KnowledgePageIndex()

     stream = client.stream_chat(

        doc_id=document.pageindex_doc_id,

        question=chat.user_question

    )

     return stream

    def chat(
    self,
    doc_id: str,
    question: str,
    stream: bool = False
):

     return self.client.chat_completions(

        messages=[
            {
                "role": "user",
                "content": question
            }
        ],

        doc_id=doc_id,

        stream=stream
    )