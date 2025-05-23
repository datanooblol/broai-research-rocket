from pydantic import BaseModel, Field
from uuid import uuid4
from broai.utils import get_timestamp
from datetime import datetime


class BrainBase(BaseModel):
    created_at:datetime = Field(default_factory=get_timestamp)


class BrainRecord(BrainBase):
    brain_id:str = Field(default_factory=lambda: str(uuid4()))
    user_id:str = Field(default=None)
    username:str = Field(default=None)
    session_id:str = Field(default=None)
    content:str = Field(default=None)