import streamlit as st
from package.services.session import DisplayService
from package.services.utils import set_state
from package.components.content_icon_bars import refresh_icon, generate_icon, download_icon


st.title("Publish")

if "publish" not in st.session_state:
    set_state("publish", None)
if st.session_state.session_id:
    service = DisplayService()
    response = service.publish(
        session_id=st.session_state.session_id,
        user_id=st.session_state.user_info.get("user_id")
    )
    set_state("publish", response.get("publish"))
    eb1, eb2, eb3, eb4 = st.columns([1, 1, 1, 13])
    refresh_icon(eb1, method="publish")
    generate_icon(eb2, method="publish")
    download_icon(eb3, method="publish")
    st.write(st.session_state.publish)