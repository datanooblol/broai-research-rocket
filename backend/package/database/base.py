from abc import ABC, abstractmethod
import duckdb

class BaseDuck(ABC):
    def __init__(self, db_name, table):
        self.db_name = db_name
        self.table = table
        self.create_table()

    def execute(self, query, param=None):
        with duckdb.connect(self.db_name) as conn:
            return conn.execute(query, param).df()

    def executemany(self, query, rows):
        with duckdb.connect(self.db_name) as conn:
            return conn.executemany(query, rows).df()

    @abstractmethod
    def create_table(self, ):
        pass

    def read_all(self, ):
        query = f"SELECT * FROM {self.table};"
        return self.execute(query)

    def delete_table(self):
        query = f"DELETE FROM {self.table};"
        return self.execute(query)

    def drop_table(self):
        query = f"DROP TABLE {self.table};"
        return self.execute(query)