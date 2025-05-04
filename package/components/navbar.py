import streamlit as st

def navbar():
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    col1.page_link("./pages/1_workspace.py", label="Workspace", icon="🏠")
    col2.page_link("./pages/2_outline.py", label="Outline", icon="🏠")
    col3.page_link("./pages/3_chunks.py", label="Chunks", icon="🏠")
    col4.page_link("./pages/4_summary.py", label="Summary", icon="🏠")
    col5.page_link("./pages/5_publish.py", label="Publish", icon="🏠")