import streamlit as st
import time
st.title("Account Info")

# @st.dialog("Test Dialog")
# def test_dialog():
    
#     with st.status("STEPS..."):
#         for i in range(5):
#             st.write(f"step{i+1}...")
#             time.sleep(1)
#     st.rerun()

# if st.button("Test "):
#     test_dialog()

if st.session_state.user_info:
    username = st.session_state.user_info.get("username")
    user_id = st.session_state.user_info.get("user_id")
    st.write(username)
    st.write(user_id)