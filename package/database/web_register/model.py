from pydantic import BaseModel, Field, model_validator
from uuid import uuid4
from broai.utils import get_timestamp
from datetime import datetime
from enum import StrEnum
from typing import List, Any

class WebStatus(StrEnum):
    TO_DO="to do"
    DOING="doing"
    DONE="done"
    ERROR="error"

class UrlBase(BaseModel):
    url_id:str = Field(default_factory=lambda: str(uuid4()))
    created_at:datetime = Field(default_factory=get_timestamp)
    status:WebStatus = Field(default=WebStatus.TO_DO.value)
    remark:str = Field(default=None)

    @model_validator(mode="after")
    def set_status(self):
        if isinstance(self.status, WebStatus):
            self.status = self.status.value
        return self

class UrlRecord(UrlBase):
    url:str
    content:str

class UrlRecords(BaseModel):
    session_id:str
    urls:List[UrlRecord]