from fastapi import APIRouter
from package.database.session.db import SessionDB
from package.database.session.model import SessionInfo, SessionToneOut, SessionParsedOutline
from package.routers.v1.session.service import web_search, web_register, web_scrape, retrieve, enrich, publish
from package.lib.parse_outline import parse_outline
from typing import List
import json
# from broai.experiments.cross_encoder import ReRanker
# rr = ReRanker()

# from broai.experiments.huggingface_embedding import BAAIEmbedding, EmbeddingDimension
# baai_em = BAAIEmbedding()

from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables

sessionDB = SessionDB(db_name=os.getenv("DB_NAME"))
router = APIRouter(prefix="/v1/session", tags=["session"])

@router.post("/create")
async def create_session(session:SessionInfo):
    """use with button create in workspace page and move to outline page"""
    try:
        records = sessionDB.add_session(session)
        return {"response": "success"}
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

@router.post("/research/knowledge")
async def retrieve_knowledge(session:SessionInfo):
    record = sessionDB.get_session(session.session_id).to_dict(orient="records")[0].get("knowledge")
    return {"response": json.loads(record)}

@router.post("/research/enrich")
async def retrieve_enrich(session:SessionInfo):
    record = sessionDB.get_session(session.session_id).to_dict(orient="records")[0].get("enrich")
    return {"response": json.loads(record)}

@router.post("/research/publish")
async def retrieve_publish(session:SessionInfo):
    record = sessionDB.get_session(session.session_id).to_dict(orient="records")[0].get("publish")
    return {"response": record}