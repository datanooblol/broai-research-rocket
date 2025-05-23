from package.database.base import BaseDuck
from package.database.user.model import UserRegister, UserLogin


class UserDB(BaseDuck):
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

    def register(self, user: UserRegister):
        query = f"INSERT INTO {self.table} (user_id, username, password, created_at, updated_at) VALUES (?, ?, ? ,?, ?)"
        rows = [user.user_id, user.username, user.password, user.created_at, user.created_at]
        self.execute(query, param=rows)
        records = self.execute(f"SELECT * FROM {self.table} WHERE user_id = ?;", [user.user_id])
        return records

    def login(self, user: UserLogin):
        query = f"SELECT * FROM {self.table} WHERE username = ?"
        rows = [user.username]
        records = self.execute(query, rows)
        return records