from package.database.session.db import SessionDB, SessionParsedOutline
from package.database.session.model import SessionKnowledge, Knowledge, KnowledgeSection, KnowledgeQuestion
from package.database.session.model import EnrichQuestion, EnrichSection, Enrich, SessionEnrich
from package.database.session.model import SessionStep, SessionPublish
from package.database.web_register.db import WebDB
from package.database.web_register.model import UrlRecords, UrlRecord, WebStatus
from package.lib.searxng import SearxngSearchOptions, search_searxng
from broai.experiments.web_scraping import scrape_by_jina_ai
from broai.experiments.cleanup_markdown import clean_up_markdown_link
from broai.experiments.chunk import split_overlap
from broai.interface import Context
from broai.experiments.vector_store import DuckVectorStore
import json
from agents.context_compressor import ContextCompressor
from agents.blog_writer import BlogWriter

from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables

from broai.experiments.cross_encoder import ReRanker
rr = ReRanker()

from broai.experiments.huggingface_embedding import BAAIEmbedding, EmbeddingDimension
baai_em = BAAIEmbedding()

sessionDB = SessionDB(db_name=os.getenv("DB_NAME"))
webDB = WebDB(db_name=os.getenv("DB_NAME"))
knowledgeDB = DuckVectorStore(db_name=os.getenv("DB_NAME"), table="knowledge", embedding=baai_em)

def web_search(session_id:str) -> UrlRecords:
    """get parsed_outline, search, return urls"""
    opts = SearxngSearchOptions(
        engines=["google", "bing", "DuckDuckGo"],
        language="en",
        pageno=1
    )
    records = sessionDB.get_session(session_id)
    record = records.to_dict(orient="records")[0]
    parsed_outline = record.get("parsed_outline")
    parsed_outline = json.loads(parsed_outline)
    results = []
    for section in parsed_outline:
        print(section.get("section"))
        questions = section.get("questions", [])
        for question in questions:
            print(question)
            results.append(search_searxng(query=question, opts=opts))
    urls_obj = []
    url_list = []
    for urls in results:
        for url in urls.results:
            if url.url not in url_list:
                url_list.append(url.url)
                urls_obj.append(UrlRecord(url=url.url, content=url.content))
    
    return UrlRecords(session_id=session_id, urls=urls_obj)

def web_register(session:UrlRecords)->UrlRecords:
    """get urls, register, return working urls"""
    urls = [UrlRecord(url=url.url, content=url.content) for url in session.urls]
    found_df = webDB.check_urls(urls)
    found_ids = found_df['url_id'].tolist()
    found_urls = found_df['url'].tolist()
    selected_urls = UrlRecords(session_id=session.session_id, urls=[
        UrlRecord(url=url.url, content=url.content)
        for url in urls
        if url.url not in found_urls
    ])
    if len(selected_urls.urls) > 0:
        webDB.register(selected_urls)
    return selected_urls

def web_scrape(session:UrlRecords):
    """get working urls, loop each url, scrape, chunk, vectordb"""
    for uc in session.urls:
        url = uc.url
        webDB.update_status([UrlRecord(url_id=uc.url_id, url=url, content="", remark="", status=WebStatus.DOING)])
        try:
            text = scrape_by_jina_ai(url)
            text = clean_up_markdown_link(text)
            context = Context(context=text, metadata={"source":url})
            contexts = split_overlap([context])
            knowledgeDB.add_contexts(contexts)
            webDB.update_status([UrlRecord(url_id=uc.url_id, url=url, content="", remark="", status=WebStatus.DONE)])
        except Exception as e:
            webDB.update_status([UrlRecord(url_id=uc.url_id, url=url, content="", remark=f"{e}", status=WebStatus.ERROR)])

def retrieve(session_id:str):
    """get parsed_outline, vectorsearch, rerank, update knowledge, return retrieved_contexts"""
    records = sessionDB.get_session(session_id)
    record = records.to_dict(orient="records")[0]
    parsed_outline = record.get("parsed_outline")
    parsed_outline = json.loads(parsed_outline)
    # retrieved_contexts = []
    section_list = []
    for section in parsed_outline:
        _section = section.get("section")
        knowledge_list = []
        for _question in section.get("questions"):
            ret_contexts = knowledgeDB.vector_search(search_query=_question, )
            reranked_contexts, scores = rr.run(_question, ret_contexts, top_n=5)
            knowledge_list.append(KnowledgeQuestion(question=_question, retrieved_ids=[c.id for c in reranked_contexts]))
        section_list.append(KnowledgeSection(section=_section, questions=knowledge_list))
    
    sk = SessionKnowledge(session_id=session_id, step=SessionStep.ENRICH, knowledge=Knowledge(sections=section_list))
    sessionDB.update_knowledge(sk)
    return sk

def _pack_context(contexts):
    source_list = []
    context_dict = {}
    for c in contexts:
        source = c.metadata.copy().get("source", "")
        context = c.context
        if source not in source_list:
            context_dict[source] = [context]
            source_list.append(source)
        else:
            context_dict[source].append(context)
    prompt = []
    for s, c in context_dict.items():
        # print(s)
        context_str = "\n".join(c)
        prompt.append(
            f"SOURCE: {s}\n{context_str}"
        )
    return "\n\n".join(prompt)

def enrich(session_id:str):
    context_compressor = ContextCompressor()
    """get parsed_outline and retrieved_contexts, enrich, update enrich, return enriched_contexts"""
    # sections = session.knowledge.sections
    sections = Knowledge(**json.loads(sessionDB.get_session(session_id).to_dict(orient="records")[0].get("knowledge")))
    section_list = []
    for section in sections.sections:
        _section = section.section
        _questions = section.questions
        enriched_question_list = []
        for _question in _questions:
            question = _question.question
            retrieved_ids = _question.retrieved_ids
            ret_contexts = knowledgeDB.search_by_ids(retrieved_ids)
            request = {
                "context": _pack_context(ret_contexts),
                "message": question
            }
            answer = context_compressor.run(request)
            enriched_question_list.append(EnrichQuestion(question=question, answer=answer))
        section_list.append(EnrichSection(section=_section, questions=enriched_question_list))
    se = SessionEnrich(session_id=session_id, step=SessionStep.REVISE, enrich=Enrich(sections=section_list))
    sessionDB.update_enrich(se)
    return se

def publish(session_id):
    """get tone_of_voice, parsed_outline, enriched_contexts, revise, update publish, return publish"""
    blog_writer = BlogWriter()
    record = sessionDB.get_session(session_id).to_dict(orient="records")[0]
    tone_of_voice = record.get("tone_of_voice")
    outline = record.get("outline")
    session_enrichs = SessionEnrich(session_id=record.get("session_id"), enrich=json.loads(record.get("enrich")))
    draft = []
    for section in session_enrichs.enrich.sections:
        _section = section.section
        _questions = section.questions
        draft.append(f"## {_section}")
        for question in _questions:
            _question = question.question
            _answer = question.answer
            draft.append(f"### {_question}")
            draft.append(f"{_answer}")
    draft = "\n\n".join(draft)
    request = {
        "draft": draft,
        "outline": outline,
        "message": tone_of_voice
    }
    blog_writer.run(request)
    _publish = blog_writer.output_text
    sp = SessionPublish(session_id=session_id, publish=_publish, step=SessionStep.PUBLISH)
    sessionDB.update_publish(sp)
    return sp