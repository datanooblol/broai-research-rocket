from package.database.base import BaseDuck
from package.database.brain.model import BrainRecord

class BrainDB(BaseDuck):
    def __init__(self, db_name):
        super().__init__(db_name=db_name, table="brain")

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            brain_id VARCHAR PRIMARY KEY,
            user_id VARCHAR,
            session_id VARCHAR,
            content VARCHAR,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """
        self.execute(query)

    def get_content(self, session_id: str):
        query = f"SELECT * FROM {self.table} WHERE session_id = ?;"
        rows = [session_id]
        return self.execute(query, rows)

    def insert_content(self, brain: BrainRecord):
        query = f"INSERT INTO {self.table} (brain_id, user_id, session_id, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)"
        rows = [brain.brain_id, brain.user_id, brain.session_id, brain.content, brain.created_at, brain.created_at]
        self.execute(query, param=rows)
    
    def publish_content(self, brain: BrainRecord):
        record = self.get_content(brain.session_id)
        if record.shape[0]==0:
            self.insert_content(brain)
        else:
            self.update_content(brain)
        records = self.execute(f"SELECT * FROM {self.table} WHERE session_id = ?;", [brain.session_id])
        return records

    def update_content(self, brain: BrainRecord):
        query = f"""
        UPDATE {self.table}
        SET content = ?, updated_at = ?
        WHERE session_id = ?;
        """
        rows = [brain.content, brain.created_at, brain.session_id]
        return self.execute(query, rows)

    def retract_content(self, brain: BrainRecord):
        query = f"""
        DELETE FROM {self.table}
        WHERE session_id = ?;
        """
        rows = [brain.session_id]
        return self.execute(query, rows)