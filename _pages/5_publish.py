import streamlit as st
from agents.blog_writer import BlogWriter


st.set_page_config(
    page_title="Publish",
)

@st.dialog("Name your file")
def download_file(publish):
    filename = st.text_input("Filename", value=None)
    if filename is None:
        filename = "document.md"
    else:
        filename = f"{filename}.md"
    st.download_button(
        label="📄 Download Markdown",
        data=publish,
        file_name=filename,
        mime="text/markdown"
    )

st.title("Publish")
if st.session_state["answers"]:
    message = st.session_state['tone_of_voice']
    outline = st.session_state['outline']
    answers = st.session_state["answers"]
    draft = []
    section_list = []
    for _answer in answers:
        section = _answer["section"]
        question = _answer["question"]
        answer = _answer["answer"]
        urls = _answer["urls"]
        if section not in section_list:
            section_list.append(section)
            draft.append(f"## {section}")
        draft.append(f"### {question}")
        draft.append(f"{answer}")
        for u in urls:
            draft.append(f"[{u}]({u})")

    draft = "\n\n".join(draft)
    # st.write(draft)
    bw = BlogWriter()
    request = {
        "draft": draft,
        "outline": outline,
        "message": message
    }
    _ = bw.run(request)
    publish = bw.output_text
    
    if st.button("download"):
        download_file(publish)
    # filename = st.text_input("Filename: ", value="document")
    # st.download_button(
    #     label="📄 download",
    #     data=publish,
    #     file_name=f"{filename}.md",
    #     mime="text/markdown"
    # )
    st.write(publish)
        