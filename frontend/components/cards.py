"""Reusable visual building blocks: KPI cards, empty states, section headers."""

from __future__ import annotations

import streamlit as st


def kpi_card(icon: str, value: str, label: str, delta: str | None = None, delta_up: bool = True):
    delta_html = ""
    if delta:
        cls = "delta-up" if delta_up else "delta-down"
        arrow = "▲" if delta_up else "▼"
        delta_html = f'<div class="delta {cls}">{arrow} {delta}</div>'
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="icon">{icon}</div>
            <div class="value">{value}</div>
            <div class="label">{label}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = ""):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def empty_state(icon: str, title: str, desc: str):
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="icon">{icon}</div>
            <div class="title">{title}</div>
            <div class="desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def glass_card_start():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


def glass_card_end():
    st.markdown("</div>", unsafe_allow_html=True)
