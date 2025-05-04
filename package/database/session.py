from . import base
from pydantic import BaseModel, Field, model_validator
from uuid import uuid4
from broai.utils import get_timestamp
from datetime import datetime
from enum import StrEnum
from typing import List, Dict, Any

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

class SessionDB(base.BaseDuck):
    def __init__(self, db_name):
        super().__init__(db_name=db_name, table="session")

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            session_id VARCHAR PRIMARY KEY,
            user_id VARCHAR,
            tone_of_voice VARCHAR,
            outline VARCHAR,
            step VARCHAR,
            step_remark VARCHAR,
            knowledge JSON,
            enrich JSON,
            publish VARCHAR,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """
        self.execute(query)

    def add_session(self, session:SessionInfo):
        query = f"""INSERT INTO {self.table} (session_id, user_id, step, created_at, updated_at) VALUES (?, ?, ?, ?, ?);"""
        rows = [session.session_id, session.user_id, session.step, session.created_at, session.created_at]
        return self.execute(query, rows)

    def get_sessions(self, session:SessionInfo):
        query = f"SELECT * FROM {self.table} WHERE user_id = ?;"
        rows = [session.user_id]
        return self.execute(query, rows)

    def update_tone_outline(self, session:SessionToneOut):
        query = f"""
        UPDATE {self.table}
        SET tone_of_voice = ?, outline = ?, updated_at = ?
        WHERE session_id = ?;
        """
        rows = [session.tone_of_voice, session.outline, session.created_at, session.session_id]
        return self.execute(query, rows)

    def update_knowledge(self, session:SessionKnowledge):
        query = f"""
        UPDATE {self.table}
        SET knowledge = ?, step = ?, updated_at = ?
        WHERE session_id = ?;
        """
        rows = [session.knowledge.model_dump(), session.step, session.created_at, session.session_id]
        return self.execute(query, rows)

    def update_enrich(self, session:SessionEnrich):
        query = f"""
        UPDATE {self.table}
        SET enrich = ?, step = ?, updated_at = ?
        WHERE session_id = ?;
        """
        rows = [session.enrich.model_dump(), session.step, session.created_at, session.session_id]
        return self.execute(query, rows)

    def update_publish(self, session:SessionPublish):
        query = f"""
        UPDATE {self.table}
        SET publish = ?, step = ?, updated_at = ?
        WHERE session_id = ?;
        """
        rows = [session.publish, session.step, session.created_at, session.session_id]
        return self.execute(query, rows)