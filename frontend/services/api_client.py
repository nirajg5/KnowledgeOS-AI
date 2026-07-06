"""
Thin HTTP client around the KnowledgeOS AI FastAPI backend.

Design goals
------------
1. Every page talks to *this* module only — never to `requests` directly.
2. If the backend is unreachable (e.g. during a demo, or local dev without
   the API running) every method transparently falls back to realistic
   demo data so the UI never breaks and never shows a raw traceback.
3. Results are cached in Streamlit's session/cache layers by the caller,
   not here, so pages stay in control of freshness.
"""

from __future__ import annotations

from typing import Any, Optional

import requests
import streamlit as st

from services import demo_data


class APIClientError(Exception):
    """Raised for real (non-connectivity) backend errors."""


class KnowledgeOSClient:
    def __init__(self, base_url: str, timeout: float = 6.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    # ------------------------------------------------------------------ #
    # low level
    # ------------------------------------------------------------------ #
    def _request(self, method: str, path: str, **kwargs) -> Optional[dict]:
        url = f"{self.base_url}{path}"
        try:
            resp = requests.request(method, url, timeout=self.timeout, **kwargs)
            if resp.status_code >= 400:
                raise APIClientError(f"{resp.status_code}: {resp.text[:200]}")
            if resp.content:
                return resp.json()
            return {}
        except requests.exceptions.RequestException:
            # Backend unreachable — signal caller to use demo fallback.
            return None

    def is_online(self) -> bool:
        result = self._request("GET", "/health")
        return result is not None

    # ------------------------------------------------------------------ #
    # Documents
    # ------------------------------------------------------------------ #
    def list_documents(self):
        result = self._request("GET", "/documents/")
        if result is not None:
            return result
        return demo_data.generate_documents()

    def get_document(self, doc_id: str):
        result = self._request("GET", f"/documents/{doc_id}")
        if result is not None:
            return result
        docs = st.session_state.get("documents") or []
        return next((d for d in docs if d["id"] == doc_id), None)

    def upload_document(self, file_bytes: bytes, filename: str):
        result = self._request(
            "POST", "/documents/upload",
            files={"file": (filename, file_bytes)},
        )
        if result is not None:
            return result
        # Demo fallback: synthesize a plausible response
        ext = filename.split(".")[-1].lower()
        return {
            "id": f"doc_demo_{filename}",
            "filename": filename,
            "type": ext,
            "status": "uploaded",
            "pages": max(1, len(file_bytes) // 2000),
            "words": max(1, len(file_bytes) // 6),
            "language": "English",
            "size_bytes": len(file_bytes),
        }

    def process_document(self, doc_id: str):
        result = self._request("POST", f"/documents/{doc_id}/process")
        if result is not None:
            return result
        return {"id": doc_id, "status": "processed"}

    def delete_document(self, doc_id: str):
        result = self._request("DELETE", f"/documents/{doc_id}")
        return result if result is not None else {"deleted": True, "id": doc_id}

    def update_document(self, doc_id: str, payload: dict):
        result = self._request("PUT", f"/documents/{doc_id}", json=payload)
        return result if result is not None else {**payload, "id": doc_id}

    def document_stats(self, documents):
        result = self._request("GET", "/documents/stats")
        if result is not None:
            return result
        return demo_data.dashboard_stats(documents)

    def search_documents(self, query: str, documents):
        result = self._request("GET", "/documents/search", params={"q": query})
        if result is not None:
            return result
        q = query.lower().strip()
        if not q:
            return documents
        return [d for d in documents if q in d["filename"].lower()]

    # ------------------------------------------------------------------ #
    # Chat
    # ------------------------------------------------------------------ #
    def send_chat_message(self, message: str, session_id: str, doc_scope: str):
        result = self._request(
            "POST", "/chat",
            json={"message": message, "session_id": session_id, "scope": doc_scope},
        )
        if result is not None:
            return result
        return {
            "reply": demo_data.ai_reply(message, doc_scope),
            "citations": demo_data.citations_for(message),
            "session_id": session_id,
        }

    def get_chat_history(self, session_id: str):
        result = self._request("GET", f"/chat/{session_id}")
        if result is not None:
            return result
        return {"session_id": session_id, "messages": []}

    # ------------------------------------------------------------------ #
    # Reports
    # ------------------------------------------------------------------ #
    def list_reports(self):
        result = self._request("GET", "/reports")
        if result is not None:
            return result
        return demo_data.generate_reports()

    def generate_report(self, document_id: str):
        result = self._request("POST", f"/reports/generate/{document_id}")
        if result is not None:
            return result
        return {
            "document_id": document_id,
            "markdown": (
                f"# AI Report\n\n"
                f"**Document:** `{document_id}`\n\n"
                "## Executive Summary\n"
                "This document presents a coherent narrative with well-structured "
                "sections. Key themes include operational performance, risk factors, "
                "and forward-looking guidance.\n\n"
                "## Key Findings\n"
                "- Strong alignment between stated objectives and outcomes\n"
                "- Several action items require follow-up ownership\n"
                "- Language and tone remain consistent throughout\n\n"
                "## Recommendations\n"
                "1. Assign owners to open action items\n"
                "2. Schedule a follow-up review in 30 days\n"
                "3. Archive alongside related documents for traceability\n"
            ),
        }

    def generate_export(self, document_id: str, fmt: str = "markdown"):
        result = self._request(
            "POST", f"/reports/generate-export/{document_id}", params={"format": fmt}
        )
        return result if result is not None else {"document_id": document_id, "format": fmt}

    # ------------------------------------------------------------------ #
    # Analytics
    # ------------------------------------------------------------------ #
    def analytics_dashboard(self):
        result = self._request("GET", "/analytics/dashboard")
        if result is not None:
            return result
        return None  # pages compute demo analytics locally from documents

    # ------------------------------------------------------------------ #
    # System status
    # ------------------------------------------------------------------ #
    def system_status(self):
        result = self._request("GET", "/health")
        if result is not None:
            return {
                "backend": "online",
                "database": result.get("database", "online"),
                "pageindex": result.get("pageindex", "online"),
                "llm": result.get("llm", "online"),
            }
        return demo_data.system_status_check()


@st.cache_resource(show_spinner=False)
def get_client(base_url: str) -> KnowledgeOSClient:
    return KnowledgeOSClient(base_url)
