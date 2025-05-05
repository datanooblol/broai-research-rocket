from fastapi import APIRouter
from package.database.session.db import SessionDB
from package.database.session.model import SessionInfo, SessionToneOut, SessionParsedOutline
from package.routers.v1.session.service import web_search, web_register, web_scrape, retrieve, enrich, publish, get_knowledge_by_ids
from package.lib.parse_outline import parse_outline
from typing import List
import json

from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables

sessionDB = SessionDB(db_name=os.getenv("DB_NAME"))
router = APIRouter(prefix="/v1/session", tags=["session"])

@router.post("/create")
async def create_session(session:SessionInfo):
    """use with button create in workspace page and move to outline page"""
    try:
        session_id = sessionDB.add_session(session)
        return {"session_id": session_id}
    except Exception as e:
        return {"response": str(e)}

@router.post("/select-session")
async def get_session(session:SessionInfo):
    records = sessionDB.get_session(session.session_id)
    records = records.to_dict(orient="records")
    return {"response": records}

@router.post("/list")
async def list_session(session:SessionInfo):
    """use with button refresh in workspace page or entering workspace page"""
    records = sessionDB.list_sessions(session)
    if records.shape[0]==0:
        return {"response": []}
    return {"response": records.to_dict(orient="records")}

@router.put("/update-outline")
async def update_outline(session:SessionToneOut):
    """use with button save/update in outline page"""
    records = sessionDB.update_outline(session)
    parsed_outline = parse_outline(outline=session.outline)
    records = sessionDB.update_parsed_outline(SessionParsedOutline(session_id=session.session_id, parsed_outline=parsed_outline))
    return {"response": parsed_outline}

@router.post("/research")
async def research(session:SessionInfo):
    """start research
    Steps:
        - web_search
        - web_register
        - web_scrape
        - retrieve
        - enrich
        - reviseabc
    """
    session_id = session.session_id
    results = web_search(session_id)
    scrap_urls = web_register(results)
    web_scrape(scrap_urls)
    retrieve(session_id)
    enrich(session_id)
    publish(session_id)
    return {"response": "success"}

@router.post("/outline")
async def retrieve_outline(session:SessionInfo):
    record = sessionDB.get_session(session.session_id).to_dict(orient="records")[0]
    tone_of_voice = record.get("tone_of_voice")
    outline = record.get("outline")
    return {"tone_of_voice": tone_of_voice, "outline": outline}

@router.post("/knowledge")
async def retrieve_knowledge(session:SessionInfo):
    record = sessionDB.get_session(session.session_id).to_dict(orient="records")[0].get("knowledge")
    record = json.loads(record)
    for section in record.get("sections"):
        _section = section.get("section")
        _questions = section.get("questions")
        for _question in _questions:
            question = _question.get("question")
            retrieved_ids = _question.get("retrieved_ids")
            ret_contexts = get_knowledge_by_ids(retrieved_ids)
            _question['retrieved_ids'] = ret_contexts
    return record

@router.post("/enrich")
async def retrieve_enrich(session:SessionInfo):
    record = sessionDB.get_session(session.session_id).to_dict(orient="records")[0].get("enrich")
    return json.loads(record)

@router.post("/publish")
async def retrieve_publish(session:SessionInfo):
    record = sessionDB.get_session(session.session_id).to_dict(orient="records")[0].get("publish")
    return {"publish": record}