import streamlit as st
from package.services import user as userAPI
from package.services.utils import set_state

if "user_info" not in st.session_state:
    set_state("user_info", None)

@st.dialog("Log In")
def login():
    username = st.text_input("username")
    password = st.text_input("password")
    if st.button("Log In", key="dialog_login"):
        status_code, user_info = userAPI.login(username, password)
        if status_code == 200:
            set_state("user_info", user_info)
            st.switch_page("package/pages/projects.py")
        if user_info:
            st.error(user_info.get("detail"))

def logout():
    set_state("user_info", None)
    st.switch_page("package/pages/account_information.py")

def sign_in_off():
    s, si, so = st.columns([10,3,3])
    if st.session_state.user_info is None:
        if si.button("↪ Log in"):
            login()
    if so.button("↩ Log out"):
        logout()

    if st.session_state.user_info:
        username = st.session_state.user_info.get("username")
        s.write(f"Hello {username}")

sign_in_off()

pages = {
    "Your Account": [
        st.Page("package/pages/account_information.py", title="Account Info"),
    ],
    "Workspace": [
        st.Page("package/pages/projects.py", title="Projects"),
        st.Page("package/pages/outline.py", title="Outline"),
        st.Page("package/pages/knowledge.py", title="Knowledge"),
        st.Page("package/pages/enrich.py", title="Enrich"),
        st.Page("package/pages/publish.py", title="Publish"),
    ],
}

with st.sidebar:
    st.slider("Url Limit", 0, 5, 3, key="n_url")
    st.slider("Retrieve Limit", 5, 10, 7, key="n_retrieve")
    st.slider("Rerank Limit", 3, 7, 5, key="n_rerank")

pg = st.navigation(pages)
pg.run()