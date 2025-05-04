from . import base
from pydantic import BaseModel, Field
from uuid import uuid4
from broai.utils import get_timestamp
from datetime import datetime

class UserInfo(BaseModel):
    user_id:str = Field(default_factory=lambda x: str(uuid4()))
    username:str

class UserLogin(UserInfo):
    password:str

class UserRegister(UserLogin):
    created_at:datetime = Field(default_factory=get_timestamp)

class UserDB(base.BaseDuck):
    def __init__(self, db_name):
        super().__init__(db_name=db_name, table="user")

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            user_id VARCHAR PRIMARY KEY,
            username VARCHAR UNIQUE,
            password VARCHAR,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """
        self.execute(query)

    def register(self, user:UserRegister):
        query = f"INSERT INTO {self.table} (user_id, username, password, created_at, updated_at) VALUES (?, ?, ? ,?, ?)"
        rows = [user.user_id, user.username, user.password, user.created_at, user.created_at]
        records = self.execute(query, param=rows)
        return records

    def login(self, user:UserLogin):
        query = f"SELECT * FROM {self.table} WHERE username = ?"
        rows = [user.username]
        records = self.execute(query, rows)
        return records