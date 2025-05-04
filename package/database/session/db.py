from package.database.base import BaseDuck
from package.database.session.model import SessionInfo, SessionToneOut, SessionParsedOutline, SessionKnowledge, SessionEnrich, SessionPublish

class SessionDB(BaseDuck):
    def __init__(self, db_name):
        super().__init__(db_name=db_name, table="session")

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            session_id VARCHAR PRIMARY KEY,
            user_id VARCHAR,
            tone_of_voice VARCHAR,
            outline VARCHAR,
            parsed_outline JSON,
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

    def get_session(self, session_id:str):
        query = f"SELECT * FROM {self.table} WHERE session_id = ?;"
        rows = [session_id]
        return self.execute(query, rows)
    
    def list_sessions(self, session:SessionInfo):
        query = f"SELECT * FROM {self.table} WHERE user_id = ?;"
        rows = [session.user_id]
        return self.execute(query, rows)

    def update_outline(self, session:SessionToneOut):
        query = f"""
        UPDATE {self.table}
        SET tone_of_voice = ?, outline = ?, updated_at = ?
        WHERE session_id = ?;
        """
        rows = [session.tone_of_voice, session.outline, session.created_at, session.session_id]
        return self.execute(query, rows)

    def update_parsed_outline(self, session:SessionParsedOutline):
        query = f"""
        UPDATE {self.table}
        SET parsed_outline = ?, updated_at = ?
        WHERE session_id = ?;
        """
        rows = [session.parsed_outline, session.created_at, session.session_id]
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