import streamlit as st
from package.services.user import UserAPI
from package.services.utils import set_state

userAPI = UserAPI()

if "user_info" not in st.session_state:
    set_state("user_info", None)

@st.dialog("Register")
def register():
    username = st.text_input("username")
    password = st.text_input("password")
    if st.button("Register", key="dialog_register"):
        status_code, user_info = userAPI.register(username, password)
        if status_code == 200:
            set_state("user_info", user_info)
            st.switch_page("package/pages/projects.py")
        if user_info:
            st.error(user_info.get("detail"))

@st.dialog("Sign In")
def sign_in():
    username = st.text_input("username")
    password = st.text_input("password")
    if st.button("Sign In", key="dialog_sign_in"):
        status_code, user_info = userAPI.login(username, password)
        if status_code == 200:
            set_state("user_info", user_info)
            st.switch_page("package/pages/projects.py")
        if user_info:
            st.error(user_info.get("detail"))

def sign_out():
    set_state("user_info", None)
    st.switch_page("package/pages/account_information.py")

def sign_in_off():
    s, s1, s2 = st.columns([10,2,2])
    if st.session_state.user_info is None:
        if s1.button("Sign In"):
            sign_in()
        if s2.button("Register"):
            register()
    if st.session_state.user_info is not None:
        if s2.button("Sign Out"):
            sign_out()

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
    "Brain Bro": [
        st.Page("package/pages/brain_list.py", title="Brain List"),
        st.Page("package/pages/brain.py", title="Brain"),
    ]
}

with st.sidebar:
    # st.slider("Url Limit", 0, 5, 3, key="n_url")
    st.slider("Retrieve Limit", 5, 10, 7, key="n_retrieve")
    st.slider("Rerank Limit", 3, 7, 5, key="n_rerank")

pg = st.navigation(pages)
pg.run()