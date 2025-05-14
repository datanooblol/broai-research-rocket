import streamlit as st
from package.services.session import DisplayService
from package.services.utils import set_state
# from package.components.content_icon_bars import refresh_icon, generate_icon
from package.services.research import ResearchService


st.title("Knowledge")


def re_retrieve(col):
    if col.button("🔄", key="re_retrieve"):
        service = ResearchService()
        service.retrieve(
            st.session_state.session_id,
            st.session_state.user_info.get("user_id"),
            st.session_state.n_retrieve,
            st.session_state.n_rerank,
        )
        st.switch_page("package/pages/knowledge.py")


if "knowledge" not in st.session_state:
    set_state("knowledge", None)
if st.session_state.session_id:
    service = DisplayService()
    response = service.knowledge(
        session_id=st.session_state.session_id,
        user_id=st.session_state.user_info.get("user_id")
    )
    set_state("knowledge", response)
    eb1, eb2, eb3, eb4 = st.columns([1, 1, 1, 13])
    # refresh_icon(eb1, method="knowledge")
    re_retrieve(eb1)
    contents = []
    if st.session_state.knowledge:
        for section in st.session_state.knowledge.get("sections"):
            _section = section.get("section")
            _questions = section.get("questions")
            st.write(f"## {_section}")
    
            for _question in _questions:
                question = _question.get("question")
                retrieved_contexts = _question.get("retrieved_ids")
                st.write(f"### {question}")
                context_dict = {}
                for _context in retrieved_contexts:
                    source = _context.get("metadata").get("source")
                    context = _context.get("context")
                    if source not in context_dict:
                        context_dict[source] = [context]
                    else:
                        context_dict[source].append(context)
                for s, _cs in context_dict.items():
                    st.write(f"🔗 [{s}]({s})")
                    for c in _cs:
                        with st.expander(f"{c[:150]}"):
                            st.write(c)