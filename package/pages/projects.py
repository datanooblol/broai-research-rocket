import streamlit as st
from package.services import session as sessionAPI
from package.services.utils import set_state

st.title("Projects")

_, c, r = st.columns([14,1,1])

def main():
    sessions = sessionAPI.list_sessions(st.session_state.user_info.get("user_id"))
    set_state("sessions", sessions)

    if "session_id" not in st.session_state:
        set_state("session_id", None)

    if st.session_state.sessions:
        session = st.radio(
            "Select Session",
            [f"""{session.get("session_id")}<|split|>{session.get("tone_of_voice")}""" for session in st.session_state.sessions],
            format_func=lambda x: x.split("<|split|>")[-1],
            index=None,
        )
        if session:
            session_id = session.split("<|split|>")[0]
            st.write("You selected:", session_id)
            set_state("session_id", session_id)
            st.switch_page("package/pages/outline.py")

    if c.button("➕"):
        session_id = sessionAPI.create_session(
            user_id=st.session_state.user_info.get("user_id")
        )
        set_state("session_id", session_id)
        st.toast("Project created successfully")
        st.switch_page("package/pages/outline.py")
        # st.write(session_id)

    if r.button("🔄"):
        _sessions = sessionAPI.list_sessions(st.session_state.user_info.get("user_id"))
        set_state("sessions", _sessions)
        st.toast("Refresh project page")


if st.session_state.user_info:
    main()