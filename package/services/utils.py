import streamlit as st

def set_state(state, value):
    st.session_state[state]=value

def get_session_info():
    return {
        "user_id": st.session_state.user_info.get("user_id"),
        "session_id": st.session_state.session_id
    }