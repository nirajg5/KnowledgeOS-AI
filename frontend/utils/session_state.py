"""
Centralized Streamlit session-state initialization for KnowledgeOS AI.

Every mutable piece of client-side state lives here so that pages never
have to guess whether a key exists before reading it.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

import streamlit as st


DEFAULT_SETTINGS = {
    "backend_url": "http://localhost:8000",
    "theme": "Dark",
    "llm_model": "openrouter/anthropic/claude-3.5-sonnet",
    "temperature": 0.4,
    "max_tokens": 2048,
    "use_demo_data": True,
}


def _set_default(key: str, value: Any) -> None:
    if key not in st.session_state:
        st.session_state[key] = value


def init_session_state() -> None:
    """Populate st.session_state with every key the app relies on."""

    _set_default("settings", DEFAULT_SETTINGS.copy())

    # Navigation / UI chrome
    _set_default("theme_mode", "dark")
    _set_default("notifications", [
        {
            "id": str(uuid.uuid4()),
            "title": "Welcome to KnowledgeOS AI",
            "message": "Your enterprise knowledge base is ready.",
            "time": datetime.now().strftime("%H:%M"),
            "read": False,
        }
    ])
    _set_default("search_query", "")
    _set_default("last_refresh", datetime.now())

    # Documents
    _set_default("documents", None)  # populated lazily by services layer
    _set_default("selected_document_id", None)
    _set_default("document_filter_status", "All")
    _set_default("document_filter_type", "All")
    _set_default("document_search", "")
    _set_default("document_page", 1)
    _set_default("document_page_size", 8)
    _set_default("confirm_delete_id", None)

    # Upload
    _set_default("upload_history", [])
    _set_default("auto_process_on_upload", True)

    # Chat
    _set_default("chat_sessions", {})  # session_id -> list[dict]
    _set_default("active_chat_session", None)
    _set_default("chat_document_scope", "All Documents")
    _set_default("chat_input_key", 0)

    # Reports
    _set_default("reports", None)
    _set_default("report_preview", None)
    _set_default("report_generating", False)

    # Analytics
    _set_default("analytics_range", "Last 30 Days")

    # System status cache
    _set_default("system_status", {
        "backend": "unknown",
        "database": "unknown",
        "pageindex": "unknown",
        "llm": "unknown",
    })


def new_chat_session() -> str:
    """Create a fresh chat session and make it active. Returns its id."""
    session_id = str(uuid.uuid4())[:8]
    st.session_state.chat_sessions[session_id] = {
        "id": session_id,
        "title": "New Conversation",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "messages": [],
    }
    st.session_state.active_chat_session = session_id
    return session_id


def get_active_chat():
    if not st.session_state.active_chat_session:
        new_chat_session()
    return st.session_state.chat_sessions[st.session_state.active_chat_session]
