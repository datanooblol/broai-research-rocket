import streamlit as st
from package.services import session as sessionAPI
from package.services.utils import set_state

st.title("Knowledge")

if "knowledge" not in st.session_state:
    set_state("knowledge", None)
if st.session_state.session_id:
    # if st.session_state.knowledge is None:
    if True:
        response = sessionAPI.knowledge(
            session_id=st.session_state.session_id,
            user_id=st.session_state.user_info.get("user_id")
        )
        set_state("knowledge", response)
    if st.button("🔄"):
        response = sessionAPI.knowledge(
            session_id=st.session_state.session_id,
            user_id=st.session_state.user_info.get("user_id")
        )
        set_state("knowledge", response)

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
    # st.write(st.session_state.knowledge)