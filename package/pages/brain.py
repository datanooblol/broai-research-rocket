import streamlit as st
from package.services.brain import BrainService
from datetime import datetime


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
    st.write(f"👤 {username}")
    st.write(f"Updated: {last_update}")
    st.write(content['content'])
else:
    st.warning("No session ID in URL.")
