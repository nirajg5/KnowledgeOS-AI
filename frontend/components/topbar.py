"""Sticky top bar: brand mark, global search, theme toggle, refresh, notifications, profile."""

from __future__ import annotations

from datetime import datetime

import streamlit as st


def render_topbar(page_title: str, client) -> None:
    st.markdown('<div class="topbar">', unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        st.markdown(
            f"""
            <div class="topbar-brand">
                <span class="dot"></span> KnowledgeOS AI
                <span style="color:var(--text-muted); font-weight:400; margin-left:8px;">/ {page_title}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
        with c1:
            st.text_input(
                "Search",
                placeholder="🔍  Search documents, chats, reports…",
                key="global_search_box",
                label_visibility="collapsed",
            )
        with c2:
            if st.button("🌗", key="theme_toggle_btn", help="Toggle theme"):
                st.session_state.theme_mode = (
                    "light" if st.session_state.theme_mode == "dark" else "dark"
                )
                st.toast("Theme preference saved (dark mode is optimized for this build).", icon="🌗")
        with c3:
            if st.button("🔄", key="refresh_btn", help="Refresh data"):
                st.cache_data.clear()
                st.session_state.last_refresh = datetime.now()
                st.session_state.system_status = client.system_status()
                st.toast("Data refreshed", icon="✅")
                st.rerun()
        with c4:
            unread = len([n for n in st.session_state.notifications if not n["read"]])
            label = f"🔔 {unread}" if unread else "🔔"
            if st.button(label, key="notif_btn", help="Notifications"):
                st.session_state["_show_notifs"] = not st.session_state.get("_show_notifs", False)
        with c5:
            st.button("👤", key="profile_btn", help="Ava Turner · Admin")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("_show_notifs"):
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**🔔 Notifications**")
            for n in st.session_state.notifications:
                st.markdown(
                    f"- **{n['title']}** — {n['message']} "
                    f"<span style='color:var(--text-muted); font-size:0.78rem;'>· {n['time']}</span>",
                    unsafe_allow_html=True,
                )
            for n in st.session_state.notifications:
                n["read"] = True
            st.markdown("</div>", unsafe_allow_html=True)
