import streamlit as st
from package.lib.parse_outline import parse_outline
from package.interfaces.sections import Sections

st.set_page_config(
    page_title="Outline",
)

st.title("Outline")

# Use text_area and update session state on change
st.session_state['tone_of_voice'] = st.text_area(
    "Tone of voice",
    st.session_state['tone_of_voice'],
    height=120,
)

st.session_state['outline'] = st.text_area(
    "Outline",
    st.session_state['outline'],
    height=360,
)

parsed_outline = parse_outline(st.session_state['outline'])
sections = Sections(sections=parsed_outline)
st.session_state['sections'] = sections
