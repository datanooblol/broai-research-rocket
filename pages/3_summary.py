import streamlit as st
from agents.context_compressor import ContextCompressor

st.set_page_config(
    page_title="Summary",
)

st.title("Summary")

if st.session_state:
    st.session_state["answers"] = None
    context_compressor = ContextCompressor()
    section_contexts = st.session_state["contexts"]
    # st.write(section_contexts)
    answers = []
    for sqc in section_contexts:
        section, question, contexts = sqc["section"], sqc["question"], sqc["contexts"]
        urls = set([c.metadata["source"] for c in contexts])
        request = {
            "context": "\n\n".join([c.context for c in contexts]),
            "message": question
        }
        answer = context_compressor.run(request=request)
        st.toast(f"{question}: answered successfully!", icon="✅")
        answers.append({"section":section, "question": question, "answer": answer, "urls": list(urls)})
    st.session_state["answers"] = answers
    section_list = []
    for _answer in answers:
        section = _answer["section"]
        question = _answer["question"]
        answer = _answer["answer"]
        urls = _answer["urls"]
        
        if section not in section_list:
            section_list.append(section)
            st.write(f"## {section}")
        st.write(f"### {question}")
        for u in urls:
            st.write(f"🔗 [{u}]({u})")
        with st.expander(f"{answer[:150]}"):
            st.write(answer)
