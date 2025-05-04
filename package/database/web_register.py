from typing import List
from pydantic import BaseModel, Field, model_validator
from uuid import uuid4
from enum import StrEnum
from . import base

class WebStatus(StrEnum):
    PENDING="pending"
    DONE="done"
    ERROR="error"

class UrlRecord(BaseModel):
    id:str = Field(default_factory=lambda: str(uuid4()))
    url:str
    status:WebStatus = Field(default=WebStatus.PENDING.value)

    @model_validator(mode="after")
    def set_status(self):
        if isinstance(self.status, WebStatus):
            self.status = self.status.value
        return self

class WebRegister(base.BaseDuck):
    def __init__(self, db_name):
        super().__init__(db_name=db_name, table="urls")

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            id VARCHAR,
            url VARCHAR,
            status VARCHAR
        );
        """
        self.execute(query)

    def register(self, urls:List[UrlRecord]):
        query = f"INSERT INTO {self.table} (id, url, status) VALUES (?, ?, ?)"
        rows = [(u.id, u.url, u.status) for u in urls]
        self.executemany(query, rows)

    def read_all(self, ):
        query = f"SELECT * FROM {self.table};"
        return self.execute(query)

    def check_urls(self, urls:List[UrlRecord]):
        url_list = [u.url for u in urls]
        place_holder = ", ".join(["?"] * len(url_list))
        query = f"SELECT * FROM {self.table} WHERE url in ({place_holder});"
        return self.execute(query, param=url_list)

    def update_status(self, urls: List[UrlRecord]):
        query = f"UPDATE {self.table} SET status = ? WHERE url = ?;"
        values = [(u.status, u.url) for u in urls]
        with duckdb.connect(self.db_name) as conn:
            conn.executemany(query, values)