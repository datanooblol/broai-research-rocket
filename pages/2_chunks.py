import streamlit as st
from package.lib.searxng import SearxngSearchOptions, search_searxng
from broai.experiments.web_scraping import scrape_by_jina_ai
from broai.experiments.cleanup_markdown import clean_up_markdown_link
from broai.experiments.vector_store import DuckVectorStore
from broai.experiments.chunk import split_overlap
from broai.interface import Context
from package.lib.web_register import WebRegister, UrlRecord, WebStatus
from typing import List

from broai.experiments.cross_encoder import ReRanker
rr = ReRanker()

from broai.experiments.huggingface_embedding import BAAIEmbedding, EmbeddingDimension
baai_em = BAAIEmbedding()


def get_vectorstore(db_name, table):
    return DuckVectorStore(db_name, table, embedding=baai_em)

def get_webstore():
    return WebRegister(db_name="./web_list.db")

st.set_page_config(
    page_title="Chunks",
)

opts = SearxngSearchOptions(
    engines=["google", "bing", "DuckDuckGo"],
    language="en",
    pageno=1
)

def search_engine(questions, opts)->List[str]:
    urls = []
    for question in questions:
        # st.write(f"{question}")
        results = search_searxng(question, opts)
        urls.extend([result.url for result in results.results[:5]])
    urls = list(set(urls))
    return urls

def url_register(wr, urls:List[UrlRecord]):
    found = wr.check_urls(urls=urls)['url'].tolist()
    registered = [url for url in urls if url.url not in found]
    if len(registered)>0:
        wr.register(urls=registered)
    return registered

def scrape_and_save(wr, vs, registered_urls):
    size = len(registered_urls)
    progress_text = f"scraping 1/{size} urls"
    my_bar = st.progress(0, text=progress_text)
    for enum, registered_url in enumerate(registered_urls):
        my_bar.progress(int(((enum+1)/size)*100), text=f"scraping {enum+1}/{size} urls")
        try:
            text = scrape_by_jina_ai(registered_url.url)
            cleaned_text = clean_up_markdown_link(text)
            context = Context(context=cleaned_text, metadata={"source":registered_url.url})
            vs.add_contexts(split_overlap([context]))
            wr.update_status(urls=[UrlRecord(id=registered_url.id, url=registered_url.url, status=WebStatus.DONE)])
            st.toast(f"{registered_url.url} scraped and stored successfully!", icon="✅")
        except Exception as e:
            wr.update_status(urls=[UrlRecord(id=registered_url.id, url=registered_url.url, status=WebStatus.ERROR)])
            st.toast(f"{registered_url.url} scraped and stored unsuccessfully!", icon="❌")
    my_bar.empty()

@st.dialog("Contexts")
def question_contexts(short_q, context):
    with st.expander(context[:50]):
        st.write(context)

st.title("Chunks")
if st.session_state['sections']:
    st.session_state['contexts'] = []
    sections = st.session_state['sections']
    urls = []
    vs = get_vectorstore(db_name="./rocket.db", table="knowledge")
    wr = get_webstore()
    for section in sections.sections:
        st.write(f"## {section.section}")
        urls = search_engine(section.questions, opts)
        registered_urls = url_register(wr, urls=[UrlRecord(url=url) for url in urls])
        scrape_and_save(wr, vs, registered_urls)
        for question in section.questions:
            st.write(f"### - {question}")
            ret_contexts = vs.vector_search(search_query=question, )
            reranked_contexts, scores = rr.run(question, ret_contexts, top_n=5)
            st.session_state['contexts'].append({
                "section": section.section,
                "question": question,
                "contexts": reranked_contexts
            })
            url_dict = {}
            for reranked_context in reranked_contexts:
                source = reranked_context.metadata["source"]
                context = reranked_context.context
                if source not in url_dict.keys():
                    url_dict[source] = [context]
                else:
                    url_dict[source].append(context)
            for u, contexts in url_dict.items():
                st.write(f"🔗 [{u}]({u})")
                for context in contexts:
                    with st.expander(f"{context[:150]}"):
                        st.write(context)
    st.toast("Retrieved successfully!", icon="✅")
