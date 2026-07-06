"""
KnowledgeOS AI — Dashboard (entry point)

Run with:  streamlit run app.py
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.cards import kpi_card, section_header, glass_card_start, glass_card_end, empty_state
from components.sidebar import render_sidebar
from components.topbar import render_topbar
from services import demo_data
from services.api_client import get_client
from utils.helpers import human_size, human_time_ago, status_badge, file_type_icon, load_css
from utils.session_state import init_session_state

st.set_page_config(
    page_title="KnowledgeOS AI · Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
load_css()

client = get_client(st.session_state.settings["backend_url"])

if st.session_state.documents is None:
    st.session_state.documents = client.list_documents()
    st.session_state.system_status = client.system_status()

documents = st.session_state.documents

render_sidebar(active="Dashboard", client=client)
render_topbar(page_title="Dashboard", client=client)

section_header("Dashboard", "A real-time overview of your enterprise knowledge base.")

# ---------------------------------------------------------------- KPI row
stats = client.document_stats(documents)
k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("📚", f"{stats['total_documents']}", "Total Documents", "12.4%", True)
with k2:
    processed_pct = (
        round(100 * stats["processed_documents"] / stats["total_documents"], 1)
        if stats["total_documents"] else 0
    )
    kpi_card("✅", f"{stats['processed_documents']}", f"Processed ({processed_pct}%)", "8.1%", True)
with k3:
    kpi_card("📄", f"{stats['reports_generated']}", "Reports Generated", "4.7%", True)
with k4:
    kpi_card("💾", human_size(stats["storage_used_bytes"]), "Storage Used", "2.3%", False)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------- Charts row
col_left, col_right = st.columns([1, 1])

with col_left:
    glass_card_start()
    st.markdown("**📊 Document Types**")
    type_counts = demo_data.document_type_distribution(documents)
    if type_counts:
        fig = px.pie(
            names=[k.upper() for k in type_counts.keys()],
            values=list(type_counts.values()),
            hole=0.55,
            color_discrete_sequence=["#7c5cff", "#4f8cff", "#22d3ee", "#f5a623"],
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#97a3bf",
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=10, b=10, l=10, r=10),
            height=280,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        empty_state("📁", "No documents yet", "Upload your first document to see type distribution.")
    glass_card_end()

with col_right:
    glass_card_start()
    st.markdown("**⏳ Processing Status**")
    status_counts = demo_data.processing_status_distribution(documents)
    if status_counts:
        fig = go.Figure(
            data=[
                go.Bar(
                    x=list(status_counts.values()),
                    y=[s.title() for s in status_counts.keys()],
                    orientation="h",
                    marker=dict(
                        color=["#22c55e", "#f5a623", "#4f8cff", "#f04747"][: len(status_counts)]
                    ),
                )
            ]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#97a3bf",
            margin=dict(t=10, b=10, l=10, r=10),
            height=280,
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        empty_state("⏳", "Nothing processing", "Processed document status will appear here.")
    glass_card_end()

col_left2, col_right2 = st.columns([1, 1])

with col_left2:
    glass_card_start()
    st.markdown("**🌐 Language Distribution**")
    lang_counts = demo_data.language_distribution(documents)
    if lang_counts:
        fig = px.bar(
            x=list(lang_counts.keys()),
            y=list(lang_counts.values()),
            color_discrete_sequence=["#7c5cff"],
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#97a3bf",
            margin=dict(t=10, b=10, l=10, r=10),
            height=260,
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        empty_state("🌐", "No language data", "Language breakdown appears after processing.")
    glass_card_end()

with col_right2:
    glass_card_start()
    st.markdown("**🕒 Recent Activity Timeline**")
    timeline = demo_data.activity_timeline()
    df = pd.DataFrame(timeline)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["uploads"], name="Uploads",
                              line=dict(color="#7c5cff", width=3), mode="lines"))
    fig.add_trace(go.Scatter(x=df["date"], y=df["processed"], name="Processed",
                              line=dict(color="#22d3ee", width=3), mode="lines"))
    fig.add_trace(go.Scatter(x=df["date"], y=df["chats"], name="Chats",
                              line=dict(color="#4f8cff", width=3), mode="lines"))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#97a3bf",
        margin=dict(t=10, b=10, l=10, r=10),
        height=260,
        legend=dict(orientation="h", y=1.15),
        xaxis=dict(gridcolor="rgba(255,255,255,0.03)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
    )
    st.plotly_chart(fig, use_container_width=True)
    glass_card_end()

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------- Recent panels
r1, r2, r3 = st.columns(3)

with r1:
    glass_card_start()
    st.markdown("**📥 Recent Uploads**")
    recent_docs = sorted(documents, key=lambda d: d["uploaded_at"], reverse=True)[:5]
    if recent_docs:
        for d in recent_docs:
            st.markdown(
                f"{file_type_icon(d['type'])} **{d['filename']}**  \n"
                f"<span style='color:var(--text-muted); font-size:0.8rem;'>"
                f"{human_time_ago(d['uploaded_at'])} · {status_badge(d['status'])}</span>",
                unsafe_allow_html=True,
            )
            st.markdown("<hr style='margin:6px 0; opacity:0.15;'>", unsafe_allow_html=True)
    else:
        empty_state("📥", "No uploads yet", "Uploaded files will show up here.")
    glass_card_end()

with r2:
    glass_card_start()
    st.markdown("**💬 Recent Chats**")
    chats = demo_data.generate_chats()
    if chats:
        for c in chats[:5]:
            st.markdown(
                f"🗨️ **{c['title']}**  \n"
                f"<span style='color:var(--text-muted); font-size:0.8rem;'>"
                f"{human_time_ago(c['updated_at'])} · {c['message_count']} messages</span>",
                unsafe_allow_html=True,
            )
            st.markdown("<hr style='margin:6px 0; opacity:0.15;'>", unsafe_allow_html=True)
    else:
        empty_state("💬", "No chats yet", "Start a conversation from the AI Chat page.")
    glass_card_end()

with r3:
    glass_card_start()
    st.markdown("**📄 Recent Reports**")
    reports = demo_data.generate_reports()
    if reports:
        for rep in reports[:5]:
            st.markdown(
                f"📄 **{rep['title']}**  \n"
                f"<span style='color:var(--text-muted); font-size:0.8rem;'>"
                f"{human_time_ago(rep['created_at'])} · "
                f"{status_badge('processed' if rep['status']=='completed' else 'failed')}</span>",
                unsafe_allow_html=True,
            )
            st.markdown("<hr style='margin:6px 0; opacity:0.15;'>", unsafe_allow_html=True)
    else:
        empty_state("📄", "No reports yet", "Generate your first AI report from a document.")
    glass_card_end()
