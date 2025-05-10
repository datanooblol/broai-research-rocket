import streamlit as st
from package.services import session as sessionAPI
from package.services.utils import set_state
from package.services.research import ResearchService

st.title("Outline")

if st.session_state.session_id:
    response = sessionAPI.get_outline(
        session_id=st.session_state.session_id,
        user_id=st.session_state.user_info.get("user_id")
    )
    outline = response.get("outline", "")
    tone_of_voice = response.get("tone_of_voice", "")
    set_state("outline", outline)
    set_state("tone_of_voice", tone_of_voice)
    st.session_state.tone_of_voice = st.text_area(
        "Tone of Voice",
        st.session_state.tone_of_voice,
        height=120
    )
    st.session_state.outline = st.text_area(
        "Outline",
        st.session_state.outline,
        height=360
    )

_, save_btn_col, research_btn_col = st.columns([10,3,3])

if save_btn_col.button("Save/Update"):
    sessionAPI.update_outline(
        session_id=st.session_state.session_id, 
        tone_of_voice=st.session_state.tone_of_voice,
        outline=st.session_state.outline,
    )
    st.toast("Outline saved/updated successfully")


@st.dialog("Research...")
def research_dialog():
    service = ResearchService()
    session_id = st.session_state.session_id
    user_id = st.session_state.user_info.get("user_id")
    with st.spinner("Searching...", show_time=True):
        st.write(service.search(session_id, user_id))
    with st.spinner("Retrieving...", show_time=True):
        st.write(service.retrieve(
            session_id,
            user_id,
            st.session_state.n_retrieve,
            st.session_state.n_rerank
        ))
    with st.spinner("Enriching...", show_time=True):
        st.write(service.enrich(session_id, user_id))
    with st.spinner("Revising...", show_time=True):
        st.write(service.publish(session_id, user_id))
        st.switch_page("package/pages/publish.py")
    # st.rerun()


if research_btn_col.button("Research"):
    research_dialog()