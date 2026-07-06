"""Chat-specific rendering helpers: message bubbles, citations, typing indicator."""

from __future__ import annotations

import streamlit as st


def render_message(role: str, content: str):
    css_class = "user" if role == "user" else "ai"
    st.markdown(
        f'<div class="chat-bubble {css_class}">{content}</div>',
        unsafe_allow_html=True,
    )


def render_citations(citations: list[dict]):
    if not citations:
        return
    for c in citations:
        st.markdown(
            f"""
            <div class="citation-card">
                📎 <b>{c['source']}</b> · page {c['page']}<br>
                <span style="opacity:0.85;">{c['snippet']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_typing_indicator():
    st.markdown(
        """
        <div class="chat-bubble ai">
            <span class="typing-dots"><span></span><span></span><span></span></span>
        </div>
        """,
        unsafe_allow_html=True,
    )
