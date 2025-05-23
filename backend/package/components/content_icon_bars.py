import streamlit as st
from package.services.utils import set_state
from package.services.research import ResearchService
from typing import Literal


def refresh_icon(col, method: Literal["knowledge", "enrich", "publish"]):
    if col.button("🔄"):
        st.switch_page(f"package/pages/{method}.py")


def generate_icon(col, method: Literal["enrich", "publish"]):
    if col.button("🤖"):
        service = ResearchService()
        session_id = st.session_state.session_id
        user_id = st.session_state.user_info.get("user_id")
        func = {
            "enrich": service.enrich,
            "publish": service.publish
        }[method]
        set_state(method, None)
        with st.spinner(f"{method.capitalize()}ing...", show_time=True):
            func(session_id, user_id)
        st.switch_page(f"package/pages/{method}.py")


def download_icon(col, method: Literal["knowledge", "enrich", "publish"]):
    if col.button("⬇️"):
        st.toast(f"{method} downloaded successfully")