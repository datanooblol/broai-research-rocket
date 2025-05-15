import streamlit as st
from package.services.brain import BrainService

style = """
<style>
    .blog-card {
        font-family: Arial, sans-serif;
        max-width: 600px;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        text-decoration: none;
        color: black;
        display: block;
        transition: box-shadow 0.3s ease;
    }
    .blog-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .user-info {
        font-weight: bold;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
    }
    .user-info img {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .blog-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .blog-summary {
        font-size: 14px;
        color: #555;
    }
</style>
"""


def get_href(session_id, username, title, content):
    href = f"""
    <a href="./brain?session_id={session_id}" target="_blank" class="blog-card">
        <div class="user-info">
        <span style="font-size: 20px; margin-right: 8px;">👤</span>
            {username}
        </div>
        <div class="blog-title">
            {title}
        </div>
        <div class="blog-summary">
            {content}
        </div>
    </a>
    """.strip()
    return href


st.title("Brain Bro")

# st.write(BrainService().list_contents())

for content in BrainService().list_contents():
    c = content['content']
    session_id = content['session_id']
    username = content["username"]
    # chunks = c.split("##")
    chunks = c.replace("#", "").split("\n")
    title = f"{chunks[0][:150]}..." if len(chunks[0]) > 150 else chunks[0]
    content = f"{chunks[2][:150]}..."
    st.html(style+get_href(session_id, username, title, content))
