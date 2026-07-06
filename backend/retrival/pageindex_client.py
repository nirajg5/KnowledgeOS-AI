"""
PageIndex Client

Wrapper around the official PageIndex SDK.
"""

from pageindex import PageIndexClient

import time

from backend.core.config import settings


class KnowledgePageIndex:

    def __init__(self):

        self.client = PageIndexClient(
            api_key=settings.PAGEINDEX_API_KEY
        )

    # ============================================
    # Upload Document
    # ============================================

    def upload_document(
        self,
        file_path: str
    ):

        response = self.client.submit_document(
            file_path
        )

        return response

    # ============================================
    # Document Status
    # ============================================

    def get_status(
        self,
        doc_id: str
    ):

        return self.client.get_document(
            doc_id
        )

    # ============================================
    # Chat
    # ============================================

    def chat(
        self,
        doc_id,
        question: str
    ):

        return self.client.chat_completions(

            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],

            doc_id=doc_id

        )


# ============================================
# Streaming Chat
# ============================================

    def stream_chat(
    self,
    doc_id,
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
    # ============================================
    # Tree
    # ============================================

    def get_tree(
        self,
        doc_id: str
    ):

        return self.client.get_tree(
            doc_id
        )
    
    # ============================================
# Get Citations
# ============================================

    def get_citations(
    self,
    doc_id: str
   ):

     tree = self.get_tree(doc_id)

     return tree.get("result", {})
    

    # ==========================================
# Wait Until Processing Completes
# ==========================================


    def wait_until_ready(
      self,
       doc_id: str,
     interval: int = 3,
     timeout: int = 300  
    ):

     start = time.time()

     while time.time() - start < timeout:

        result = self.get_status(doc_id)

        status = result["status"]

        if status == "completed":
            return result

        elif status == "failed":
            raise Exception("PageIndex processing failed.")

        time.sleep(interval)

     raise TimeoutError(
        "PageIndex processing timed out."
    )
    

    