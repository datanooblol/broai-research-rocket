import streamlit as st
# from package.services import session as sessionAPI
from package.services.session import DisplayService
from package.services.utils import set_state
from package.components.content_icon_bars import refresh_icon, generate_icon, download_icon


st.title("Enrich")

if "enrich" not in st.session_state:
    set_state("enrich", None)
if st.session_state.session_id:
    service = DisplayService()
    response = service.enrich(
        session_id=st.session_state.session_id,
        user_id=st.session_state.user_info.get("user_id")
    )
    set_state("enrich", response)
    eb1, eb2, eb3, eb4 = st.columns([1, 1, 1, 13])
    refresh_icon(eb1, method="enrich")
    generate_icon(eb2, method="enrich")
    download_icon(eb3, method="enrich")
    if st.session_state.enrich:
        contents = []
        for section in st.session_state.enrich.get("sections"):
            _section = section.get("section")
            _questions = section.get("questions")
            contents.append(f"## {_section}")
            for _question in _questions:
                question = _question.get("question")
                answer = _question.get("answer")
                contents.append(f"### {question}")
                contents.append(f"{answer}")
        contents = "\n".join(contents)
        st.write(contents)