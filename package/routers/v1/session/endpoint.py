from fastapi import APIRouter, Depends
from package.database.session.model import (
    SessionInfo, SessionToneOut, SessionParsedOutline
)
from package.lib.parse_outline import parse_outline
import json
from package.routers.v1.session.services.web_search import WebSearchService
from package.routers.v1.session.services.retrieve import RetrieveService
from package.routers.v1.session.services.enrich import EnrichService
from package.routers.v1.session.services.publish import PublishService
from package.database.utils import (
    get_SessionDB, get_WebDB, get_KnowledgeDB, get_ReRanker
)

router = APIRouter(prefix="/v1/session", tags=["session"])


@router.post("/create")
async def create_session(
    session: SessionInfo,
    sessionDB=Depends(get_SessionDB)
):
    """use with button create in workspace page and move to outline page"""
    try:
        session_id = sessionDB.add_session(session)
        return {"session_id": session_id}
    except Exception as e:
        return {"response": str(e)}


@router.post("/select-session")
async def get_session(
    session: SessionInfo,
    sessionDB=Depends(get_SessionDB)
):
    records = sessionDB.get_session(session.session_id)
    records = records.to_dict(orient="records")
    return {"response": records}


@router.post("/list")
async def list_session(
    session: SessionInfo,
    sessionDB=Depends(get_SessionDB)
):
    """use with button refresh in workspace page or entering workspace page"""
    records = sessionDB.list_sessions(session)
    if records.shape[0] == 0:
        return {"response": []}
    return {"response": records.to_dict(orient="records")}


@router.put("/update-outline")
async def update_outline(
    session: SessionToneOut,
    sessionDB=Depends(get_SessionDB)
):
    """use with button save/update in outline page"""
    _ = sessionDB.update_outline(session)
    parsed_outline = parse_outline(outline=session.outline)
    _ = sessionDB.update_parsed_outline(
        SessionParsedOutline(
            session_id=session.session_id, parsed_outline=parsed_outline
        )
    )
    return {"response": parsed_outline}


@router.post("/research/search")
async def research_search(
    session: SessionInfo,
    webDB=Depends(get_WebDB),
    sessionDB=Depends(get_SessionDB),
    knowledgeDB=Depends(get_KnowledgeDB)
):
    service = WebSearchService(webDB, sessionDB, knowledgeDB)
    service.run(session.session_id)
    return {"response": "searched successfully"}


@router.post("/research/retrieve")
async def research_retrieve(
    session: SessionInfo,
    sessionDB=Depends(get_SessionDB),
    knowledgeDB=Depends(get_KnowledgeDB),
    reranker=Depends(get_ReRanker)
):
    service = RetrieveService(sessionDB, knowledgeDB, reranker)
    service.retrieve(session.session_id)
    return {"response": "retrieved successfully"}


@router.post("/research/enrich")
async def research_enrich(
    session: SessionInfo,
    sessionDB=Depends(get_SessionDB),
    knowledgeDB=Depends(get_KnowledgeDB)
):
    service = EnrichService(sessionDB, knowledgeDB)
    service.enrich(session.session_id)
    return {"response": "enriched successfully"}


@router.post("/research/publish")
async def research_publish(
    session: SessionInfo,
    sessionDB=Depends(get_SessionDB)
):
    service = PublishService(sessionDB)
    service.publish(session.session_id)
    return {"response": "publishedsuccessfully"}


@router.post("/outline")
async def retrieve_outline(
    session: SessionInfo,
    sessionDB=Depends(get_SessionDB)
):
    record = sessionDB.get_session(session.session_id).to_dict(orient="records")[0]
    tone_of_voice = record.get("tone_of_voice")
    outline = record.get("outline")
    return {"tone_of_voice": tone_of_voice, "outline": outline}


@router.post("/knowledge")
async def retrieve_knowledge(
    session: SessionInfo, 
    sessionDB=Depends(get_SessionDB),
    knowledgeDB=Depends(get_KnowledgeDB),
    reranker=Depends(get_ReRanker)
):
    service = RetrieveService(sessionDB, knowledgeDB, reranker)
    return service.get_knowledge(session.session_id)


@router.post("/enrich")
async def retrieve_enrich(
    session: SessionInfo,
    sessionDB=Depends(get_SessionDB)
):
    record = sessionDB.get_session(session.session_id).to_dict(orient="records")[0].get("enrich")
    return json.loads(record)


@router.post("/publish")
async def retrieve_publish(
    session: SessionInfo,
    sessionDB=Depends(get_SessionDB)
):
    record = sessionDB.get_session(session.session_id).to_dict(orient="records")[0].get("publish")
    return {"publish": record}