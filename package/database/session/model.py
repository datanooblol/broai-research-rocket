from pydantic import BaseModel, Field, model_validator
from uuid import uuid4
from broai.utils import get_timestamp
from datetime import datetime
from enum import StrEnum
from typing import List, Any

class SessionStep(StrEnum):
    NOT_START = "not start"
    SEARCH = "search"
    REGISTER = "register"
    SCRAPE = "scrape"
    STORE = "store"
    RETRIEVE = "retrieve"
    ENRICH = "enrich"
    REVISE = "revise"
    PUBLISH = "publish"
    DONE = "done"

class SessionBase(BaseModel):
    created_at:datetime = Field(default_factory=get_timestamp)
    step:SessionStep = Field(default=SessionStep.NOT_START.value)
    step_remark:str = Field(default=None)

    @model_validator(mode="after")
    def set_step(self):
        if isinstance(self.step, SessionStep):
            self.step = self.step.value
        return self

class SessionInfo(SessionBase):
    session_id:str = Field(default_factory=lambda x: str(uuid4()))
    user_id:str

class SessionToneOut(SessionBase):
    session_id:str
    tone_of_voice:str
    outline:str

class SessionParsedOutline(SessionBase):
    session_id:str
    parsed_outline:List[Any]

class KnowledgeQuestion(BaseModel):
    question:str
    retrieved_ids:List[str]

class KnowledgeSection(BaseModel):
    section:str
    questions:List[KnowledgeQuestion]

class Knowledge(BaseModel):
    sections:List[KnowledgeSection]

class SessionKnowledge(SessionBase):
    session_id:str
    knowledge:Knowledge

class EnrichQuestion(BaseModel):
    question:str
    answer:str

class EnrichSection(BaseModel):
    section:str
    questions:List[EnrichQuestion]

class Enrich(BaseModel):
    sections:List[EnrichSection]

class SessionEnrich(SessionBase):
    session_id:str
    enrich:Enrich

class SessionPublish(SessionBase):
    session_id:str
    publish:str