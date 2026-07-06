"""Sticky sidebar: brand, navigation, live system status."""

from __future__ import annotations

import streamlit as st

from utils.helpers import status_badge


NAV_ITEMS = [
    ("app.py", "🏠", "Dashboard"),
    ("pages/2_📁_Documents.py", "📁", "Documents"),
    ("pages/3_⬆️_Upload.py", "⬆️", "Upload"),
    ("pages/4_💬_AI_Chat.py", "💬", "AI Chat"),
    ("pages/5_📄_Reports.py", "📄", "Reports"),
    ("pages/6_📈_Analytics.py", "📈", "Analytics"),
    ("pages/7_⚙️_Settings.py", "⚙️", "Settings"),
]


def render_sidebar(active: str, client) -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-logo">
                <div class="mark">🧠</div>
                <div>
                    <div class="name">KnowledgeOS AI</div>
                    <div class="tag">Enterprise Intelligence</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="nav-section-label">Navigation</div>', unsafe_allow_html=True)
        for path, icon, label in NAV_ITEMS:
            is_active = label == active
            if st.button(
                f"{icon}  {label}",
                key=f"nav_{label}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.switch_page(path)

        st.markdown('<div class="nav-section-label">System Status</div>', unsafe_allow_html=True)

        status = st.session_state.system_status
        rows = [
            ("Backend", status.get("backend", "unknown")),
            ("Database", status.get("database", "unknown")),
            ("PageIndex", status.get("pageindex", "unknown")),
            ("LLM", status.get("llm", "unknown")),
        ]
        for name, state in rows:
            st.markdown(
                f'<div class="status-row"><span>{name}</span>{status_badge(state)}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("v1.4.0 · © 2026 KnowledgeOS AI")
