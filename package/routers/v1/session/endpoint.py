from fastapi import APIRouter
from package.database.session import SessionDB, SessionInfo, SessionToneOut

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

@router.post("/list")
async def get_session(session:SessionInfo):
    """use with button refresh in workspace page or entering workspace page"""
    records = sessionDB.get_sessions(session)
    if records.shape[0]==0:
        return {"response": []}
    return {"response": records.to_dict(orient="records")}

@router.put("/update-tone-of-voice-and-outline")
async def update_tone_outline(session:SessionToneOut):
    """use with button save/update in outline page"""
    records = sessionDB.update_tone_outline(session)
    return {"response": "success"}

@router.post("/research")
async def research():
    return {"response": "success"}