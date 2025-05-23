import streamlit as st
from package.services.brain import BrainService
from datetime import datetime
import math


def estimate_read_time(text: str, wpm: int = 200) -> int:
    word_count = len(text.split())
    minutes = math.ceil(word_count / wpm)
    return minutes


style = """
<style>
    .user-meta {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 14px;
        color: #555;
        margin-bottom: 12px;
    }
    .user-avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        margin-right: 4px;
    }
    .username {
        font-weight: 500;
        color: #000;
    }
    .meta-dot {
        margin: 0 4px;
        color: #aaa;
    }
    .read-time, .publish-date {
        color: #777;
    }
</style>
""".strip()


def get_href(username, last_update, read_time):
    href = f"""
    <div class="user-meta">
        <span class="username">👤 {username}</span>
        <span class="meta-dot">·</span>
        <span class="read-time">{read_time} min read</span>
        <span class="meta-dot">·</span>
        <span class="publish-date">{last_update}</span>
    </div>
    """.strip()
    return href


st.title("Brain")

query_params = st.query_params  # works in Streamlit v1.32+
session_id = query_params.get("session_id")

if session_id:
    service = BrainService()
    response = service.get_content(session_id)
    content = response[0]
    username = content['username']
    last_update = content["updated_at"]
    last_update = datetime.fromisoformat(last_update)
    last_update = last_update.strftime("%Y-%m-%d %H:%M:%S")
    read_time = estimate_read_time(content['content'])
    # st.write(f"👤 {username}")
    # st.write(f"Updated: {last_update}")
    # st.write(f"{estimate_read_time(content['content'])} min read")
    st.html(style+get_href(username, last_update, read_time))
    st.write(content['content'])
else:
    st.warning("No session ID in URL.")
