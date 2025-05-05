import streamlit as st
from package.services import session as sessionAPI
from package.services.utils import set_state

st.title("Enrich")

if "enrich" not in st.session_state:
    set_state("enrich", None)
if st.session_state.session_id:
    # if st.session_state.enrich is None:
    if True:
        response = sessionAPI.enrich(
            session_id=st.session_state.session_id,
            user_id=st.session_state.user_info.get("user_id")
        )
        set_state("enrich", response)
    if st.button("🔄"):
        response = sessionAPI.enrich(
            session_id=st.session_state.session_id,
            user_id=st.session_state.user_info.get("user_id")
        )
        set_state("enrich", response)
    for section in st.session_state.enrich.get("sections"):
        _section = section.get("section")
        _questions = section.get("questions")
        st.write(f"## {_section}")
        for _question in _questions:
            question = _question.get("question")
            answer = _question.get("answer")
            st.write(f"### {question}")
            st.write(f"{answer}")
    # st.write(st.session_state.enrich)