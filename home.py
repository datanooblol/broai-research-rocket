import streamlit as st
from package.lib.parse_outline import parse_outline
from package.interfaces.sections import Sections

st.set_page_config(
    page_title="Home",
    # page_icon="👋",
)

st.title("Home")

def set_session_variable(key):
    try:
        _ = st.session_state[key]
    except:
        st.session_state[key] = None

set_session_variable("sections")

# Initialize default values in session state if not present
if 'tone_of_voice' not in st.session_state:
    st.session_state['tone_of_voice'] = "Set how BroAI writes your research"

if 'outline' not in st.session_state:
    st.session_state['outline'] = """\
## Overview of Insurance Fraud  
- what is insurance fraud look like  
- what is the impact on insurance fraud in USA  
- how many types of insurance frauds are  
- how to detect insurance fraud  
""".strip()