from typing import List, Dict, Any
from pydantic import BaseModel, Field
from uuid import uuid4
from broai.utils import get_timestamp
from datetime import datetime
class SessionRecord(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid4()))
    tone_of_voice:str = Field()
    outline:str = Field()
    retrieved:List[Dict[str, Any]] = Field(default=None)
    summarized:List[Dict[str, Any]] = Field(default=None)
    published:List[Dict[str, Any]] = Field(default=None)
    created_at:datetime = Field(default_factory=get_timestamp)