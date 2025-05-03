import streamlit as st
from package.lib.searxng import SearxngSearchOptions, search_searxng
from broai.experiments.web_scraping import scrape_by_jina_ai
from broai.experiments.cleanup_markdown import clean_up_markdown_link
from broai.experiments.vector_store import DuckVectorStore
from broai.experiments.chunk import split_overlap
import json
from broai.interface import Context
from broai.experiments.huggingface_embedding import BAAIEmbedding, EmbeddingDimension
baai_em = BAAIEmbedding()


def get_vectorstore(db_name, table):
    return DuckVectorStore(db_name, table, embedding=baai_em)

st.set_page_config(
    page_title="Chunks",
)

st.title("Chunks")

opts = SearxngSearchOptions(
    engines=["google", "bing", "DuckDuckGo"],
    language="en",
    pageno=1
)

if st.session_state['sections']:
    sections = st.session_state['sections']
    urls = []
    vs = get_vectorstore(db_name="./rocket.db", table="knowledge")
    for section in sections.sections:
        with st.expander(section.section):
            # st.header(section.section)
            for question in section.questions:
                # st.write(f"{question}")
                results = search_searxng(question, opts)
                urls.extend([result.url for result in results.results[:]])
            _urls = list(set(urls))
            size = len(_urls)
            contexts = []
            progress_text = f"scraping {len(_urls)} urls"
            my_bar = st.progress(0, text=progress_text)
            for enum, url in enumerate(_urls):
                text = scrape_by_jina_ai(url)
                my_bar.progress(int(((enum+1)/size)*100), text=progress_text)
                cleaned_text = clean_up_markdown_link(text)
                context = Context(context=text, metadata={"source":url})
                contexts.extend(split_overlap([context]))
            vs.add_contexts(contexts)
            for question in section.questions:
                st.subheader(question)
                ret_contexts = vs.vector_search(search_query=question)
                for rc in ret_contexts[:1]:
                    st.write(rc.context[0:150], "...")
