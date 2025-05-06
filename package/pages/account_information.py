import streamlit as st


st.title("Account Info")

if st.session_state.user_info:
    username = st.session_state.user_info.get("username")
    user_id = st.session_state.user_info.get("user_id")
    st.write("username:", username)
    st.write("user_id:", user_id)