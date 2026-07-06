"""
Small, dependency-free helper functions shared across pages/components.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import streamlit as st

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def load_css() -> None:
    """Inject the global stylesheet plus a small runtime style patch."""
    css_path = ASSETS_DIR / "style.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def human_size(num_bytes: float) -> str:
    """Convert a byte count into a human readable string (KB / MB / GB)."""
    if num_bytes is None:
        return "0 B"
    step = 1024.0
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_bytes < step:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= step
    return f"{num_bytes:.1f} PB"


def human_time_ago(timestamp: datetime) -> str:
    """Return a friendly 'x minutes ago' style string."""
    if timestamp is None:
        return "—"
    delta = datetime.now() - timestamp
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} min ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hr ago"
    days = hours // 24
    return f"{days} day{'s' if days != 1 else ''} ago"


def status_badge(status: str) -> str:
    """Return an HTML badge span for a given document/report status."""
    mapping = {
        "processed": ("status-success", "✅ Processed"),
        "processing": ("status-warning", "⏳ Processing"),
        "queued": ("status-info", "🕓 Queued"),
        "failed": ("status-danger", "⚠️ Failed"),
        "uploaded": ("status-info", "📥 Uploaded"),
        "online": ("status-success", "● Online"),
        "offline": ("status-danger", "● Offline"),
        "degraded": ("status-warning", "● Degraded"),
        "unknown": ("status-warning", "● Checking"),
    }
    cls, label = mapping.get(str(status).lower(), ("status-info", status))
    return f'<span class="badge {cls}">{label}</span>'


def file_type_icon(file_type: str) -> str:
    icons = {
        "pdf": "📕",
        "docx": "📘",
        "doc": "📘",
        "txt": "📄",
        "csv": "📊",
    }
    return icons.get(str(file_type).lower(), "📁")


def truncate(text: str, length: int = 60) -> str:
    if text is None:
        return ""
    return text if len(text) <= length else text[: length - 1] + "…"
