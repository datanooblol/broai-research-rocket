from pydantic import BaseModel, Field
from uuid import uuid4
from broai.utils import get_timestamp
from datetime import datetime


class UserInfo(BaseModel):
    user_id: str = Field(default_factory=lambda x: str(uuid4()))
    username: str


class UserLogin(UserInfo):
    password: str


class UserRegister(UserLogin):
    created_at: datetime = Field(default_factory=get_timestamp)