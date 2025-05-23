import streamlit as st


st.title("Account Info")

if st.session_state.user_info:
    username = st.session_state.user_info.get("username")
    user_id = st.session_state.user_info.get("user_id")
    st.write("username:", username)
    st.write("user_id:", user_id)


# st.radio("Test", ["all", "select"], key="all_or_select")
# if st.session_state.all_or_select=='select':
#     test = ["medium.com", "geeksforgeeks.org", "towardsdatascience.com"]
#     test_dict = {}
#     for t in test:
#         test_dict[t] = st.checkbox(t)
#     st.write(test_dict)