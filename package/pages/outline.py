import streamlit as st
from package.services import session as sessionAPI
from package.services.utils import set_state
from package.services.research import ResearchService
import time

st.title("Outline")

if "selected_whitelist" not in st.session_state:
    st.session_state["selected_whitelist"] = None


system_whitelist = ["medium.com", "geeksforgeeks.org", "towardsdatascience.com"]


@st.dialog("White List")
def whitelist():
    """whitelist should connect to db.session.whitelist, so it will be used in later stages"""
    session_whitelist = sessionAPI.get_whitelist(
        st.session_state.user_info.get("user_id"), 
        st.session_state.session_id
    ).get("whitelist", [])
    default_whitelist = session_whitelist if len(session_whitelist)>0 else ["all"]
    selected_whitelist = st.multiselect(
        "White List URLs", 
        list(set(["all"]+session_whitelist+system_whitelist)), 
        default=default_whitelist, 
        accept_new_options=True
    )
    if st.button("Save/Update Whitelist"):
        set_state("selected_whitelist", selected_whitelist)
        sessionAPI.update_whitelist(
            st.session_state.session_id,
            st.session_state.selected_whitelist
        )
        st.rerun()


if st.button("White List", key="button_white_list"):
    whitelist()

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

# if st.session_state.selected_whitelist:
#     st.write(st.session_state.selected_whitelist)

_, save_btn_col, research_btn_col = st.columns([10,3,3])

if save_btn_col.button("Save/Update"):
    sessionAPI.update_outline(
        session_id=st.session_state.session_id, 
        tone_of_voice=st.session_state.tone_of_voice,
        outline=st.session_state.outline,
    )
    st.toast("Outline saved/updated successfully")

def quick_time_log(start, message):
    duration = time.perf_counter() - start
    st.success(f"{message}: {duration:.0f} seconds")

@st.dialog("Research...")
def research_dialog():
    service = ResearchService()
    session_id = st.session_state.session_id
    user_id = st.session_state.user_info.get("user_id")
    start_research = time.perf_counter()
    with st.spinner("Searching...", show_time=True):
        start_search = time.perf_counter()
        response = service.search(session_id, user_id)
        quick_time_log(start_search, response["response"])
    with st.spinner("Retrieving...", show_time=True):
        start_retrieve = time.perf_counter()
        response = service.retrieve(
            session_id,
            user_id,
            st.session_state.n_retrieve,
            st.session_state.n_rerank
        )
        quick_time_log(start_retrieve, response["response"])
    with st.spinner("Enriching...", show_time=True):
        start_enrich = time.perf_counter()
        response = service.enrich(session_id, user_id)
        quick_time_log(start_enrich, response["response"])
    with st.spinner("Revising...", show_time=True):
        start_revise = time.perf_counter()
        response = service.publish(session_id, user_id)
        quick_time_log(start_revise, response["response"])

    quick_time_log(start_research, "Researched successfully")
    if st.button("Go to Publish"):
        st.switch_page("package/pages/publish.py")

if research_btn_col.button("Research"):
    research_dialog()