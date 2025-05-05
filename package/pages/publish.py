import streamlit as st
from package.services import session as sessionAPI
from package.services.utils import set_state

st.title("Publish")
# button("🔄")

if "publish" not in st.session_state:
    set_state("publish", None)
if st.session_state.session_id:
    # if st.session_state.publish is None:
    if True:
        response = sessionAPI.publish(
            session_id=st.session_state.session_id,
            user_id=st.session_state.user_info.get("user_id")
        )
        set_state("publish", response.get("publish"))
    if st.button("🔄"):
        response = sessionAPI.publish(
            session_id=st.session_state.session_id,
            user_id=st.session_state.user_info.get("user_id")
        )
        set_state("publish", response.get("publish"))
    st.write(st.session_state.publish)