from typing import List
from package.database.base import BaseDuck
import duckdb
from package.database.web_register.model import UrlRecords, UrlRecord

class WebDB(BaseDuck):
    def __init__(self, db_name):
        super().__init__(db_name=db_name, table="urls")

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            url_id VARCHAR PRIMARY KEY,
            session_id VARCHAR,
            url VARCHAR UNIQUE,
            content VARCHAR,
            status VARCHAR,
            remark VARCHAR,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """
        self.execute(query)

    def register(self, urls:UrlRecords):
        query = f"INSERT INTO {self.table} (url_id, session_id, url, content, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
        rows = [(u.url_id, urls.session_id, u.url, u.content, u.status, u.created_at, u.created_at) for u in urls.urls]
        self.executemany(query, rows)

    def check_urls(self, urls:List[UrlRecord]):
        url_list = [u.url for u in urls]
        place_holder = ", ".join(["?"] * len(url_list))
        query = f"SELECT * FROM {self.table} WHERE url in ({place_holder});"
        return self.execute(query, param=url_list)

    def update_status(self, urls: List[UrlRecord]):
        query = f"UPDATE {self.table} SET status = ?, remark = ?, updated_at = ? WHERE url_id = ? AND url = ?;"
        values = [(u.status, u.remark, u.created_at, u.url_id, u.url) for u in urls]
        return self.executemany(query, values)