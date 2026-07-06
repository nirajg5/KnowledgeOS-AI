"""
PageIndex Client

Wrapper around the official PageIndex SDK.
"""

import time

from pageindex import PageIndexClient

from backend.core.config import settings


class KnowledgePageIndex:
    """
    Wrapper around the PageIndex SDK.
    """

    def __init__(self):

        self.client = PageIndexClient(
            api_key=settings.PAGEINDEX_API_KEY
        )

    # =====================================================
    # Upload Document
    # =====================================================

    def upload_document(
        self,
        file_path: str
    ):

        return self.client.submit_document(
            file_path
        )

    # =====================================================
    # Get Document Status
    # =====================================================

    def get_status(
        self,
        doc_id: str
    ):

        return self.client.get_document(
            doc_id
        )

    # =====================================================
    # AI Chat
    # =====================================================

    def chat(
        self,
        doc_id: str,
        question: str
    ):

        return self.client.chat_completions(

            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],

            doc_id=doc_id,

            enable_citations=True

        )

    # =====================================================
    # Streaming Chat
    # =====================================================

    def stream_chat(
        self,
        doc_id: str,
        question: str
    ):

        return self.client.chat_completions(

            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],

            doc_id=doc_id,

            stream=True,

            enable_citations=True

        )

    # =====================================================
    # Get Document Tree
    # =====================================================

    def get_tree(
        self,
        doc_id: str
    ):

        return self.client.get_tree(
            doc_id
        )

    # =====================================================
    # Get Citations
    # =====================================================

    def get_citations(
        self,
        doc_id: str
    ):

        tree = self.get_tree(doc_id)

        return tree.get(
            "result",
            {}
        )

    # =====================================================
    # Wait Until Document Processing Completes
    # =====================================================

    def wait_until_ready(
        self,
        doc_id: str,
        interval: int = 3,
        timeout: int = 300
    ):

        start = time.time()

        while time.time() - start < timeout:

            result = self.get_status(
                doc_id
            )

            status = result["status"]

            if status == "completed":
                return result

            if status == "failed":
                raise Exception(
                    "PageIndex processing failed."
                )

            time.sleep(interval)

        raise TimeoutError(
            "PageIndex processing timed out."
        )