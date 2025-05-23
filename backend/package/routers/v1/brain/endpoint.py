from fastapi import APIRouter, Depends
from package.database.utils import (
    get_SessionDB, get_WebDB, get_KnowledgeDB, get_BrainDB, get_ReRanker
)
from pydantic import BaseModel


router = APIRouter(prefix="/v1/brain", tags=["brain"])


@router.get("/")
async def list_contents(brainDB=Depends(get_BrainDB)):
    records = brainDB.read_all()
    records = records.to_dict(orient="records")
    return {"contents": records}


class ContentInfo(BaseModel):
    session_id: str

@router.post("/get-content")
async def get_content(content: ContentInfo, brainDB=Depends(get_BrainDB)):
    records = brainDB.get_content(content.session_id)
    records = records.to_dict(orient="records")
    return {"contents": records}


