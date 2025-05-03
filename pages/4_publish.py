import streamlit as st

st.set_page_config(
    page_title="Publish",
)

st.title("Publish")

progress_text = "test"
my_bar1 = st.progress(0, text=progress_text)
my_bar2 = st.progress(0, text=progress_text)
array = [i for i in range(100)]
size = len(array)
for enum, u in enumerate(array):
    my_bar1.progress(int((enum/size)*100)+1, text=progress_text)
for enum in range(100):
    my_bar2.progress(enum+1, text=progress_text)