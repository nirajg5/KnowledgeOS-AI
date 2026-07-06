"""
KnowledgeOS AI

Streamlit Frontend
"""

import requests
import streamlit as st


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="KnowledgeOS AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# Backend URL
# ==========================================================

BACKEND_URL = "http://127.0.0.1:8000"


# ==========================================================
# Backend Status
# ==========================================================

def backend_status():
    """
    Check whether FastAPI backend is running.
    """

    try:

        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=3
        )

        if response.status_code == 200:
            return True

    except Exception:
        pass

    return False


# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("🧠 KnowledgeOS AI")

st.sidebar.markdown("---")

st.sidebar.success("Enterprise Knowledge Operating System")

st.sidebar.markdown("---")

st.sidebar.write("### Navigation")

st.sidebar.info("Dashboard")

st.sidebar.info("Upload")

st.sidebar.info("Documents")

st.sidebar.info("Chat")

st.sidebar.info("Reports")

st.sidebar.markdown("---")

st.sidebar.caption("Version 1.0.0")


# ==========================================================
# Main Title
# ==========================================================

st.title("🧠 KnowledgeOS AI")

st.subheader(
    "Enterprise Knowledge Operating System powered by Vectorless RAG & Multi-Agent AI"
)

st.markdown("---")


# ==========================================================
# Backend Status
# ==========================================================

if backend_status():

    st.success("✅ Backend Connected")

else:

    st.error("❌ Backend Not Running")


# ==========================================================
# Dashboard Cards
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Documents",
        "0"
    )

with col2:
    st.metric(
        "Questions",
        "0"
    )

with col3:
    st.metric(
        "Reports",
        "0"
    )

with col4:
    st.metric(
        "Agents",
        "4"
    )


st.markdown("---")


# ==========================================================
# Project Overview
# ==========================================================

st.header("Project Overview")

st.write(
    """
KnowledgeOS AI is an Enterprise Knowledge Operating System that combines

- Vectorless Retrieval (PageIndex)
- LangGraph Multi-Agent AI
- FastAPI Backend
- PostgreSQL
- Streamlit Dashboard

to provide intelligent document understanding and enterprise knowledge management.
"""
)


# ==========================================================
# Core Features
# ==========================================================

st.header("Core Features")

features = [

    "📄 Multi-format Document Upload",

    "🧠 Vectorless RAG",

    "🤖 Multi-Agent AI",

    "💬 AI Chat",

    "📚 Citation-based Answers",

    "📄 Executive Summaries",

    "📊 Enterprise Dashboard",

    "📂 Document Management"

]

for feature in features:
    st.write(feature)


st.markdown("---")


# ==========================================================
# Footer
# ==========================================================

st.caption("KnowledgeOS AI • Version 1.0.0")