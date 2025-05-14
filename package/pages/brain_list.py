import streamlit as st
from package.services.brain import BrainService

# session_id = st.session_state.session_id

style = """
<style>
.card {
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 16px;
    margin: 12px 0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    text-decoration: none;
    color: inherit;
    display: block;
}
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}
</style>
""".strip()

def get_href(session_id, title):
    href = f"""
    <a href="./brain?session_id={session_id}" target="_blank" class="card">
        <h4>{title}</h4>
        <p>Click to view this published article.</p>
    </a>
    """.strip()
    return href
# st.html(style+href)
st.title("Brain Bro")

# st.write(BrainService().list_contents())

for content in BrainService().list_contents():
    c = content['content']
    session_id = content['session_id']
    title = c.split("##")[1]
    st.html(style+get_href(session_id, title))
    # st.write(f"{content['content'][:150].replace('#', '')}...")