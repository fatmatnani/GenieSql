from langchain_community.utilities import SQLDatabase
from sqlalchemy import text

class CustomSQLDatabase(SQLDatabase):
    def _get_sample_rows(self, table: str) -> str:
        connection = self._engine.connect()
        command = text(f"SELECT * FROM {table} LIMIT 3;")
        sample_rows_result = connection.execute(command)
        sample_rows = sample_rows_result.fetchall()
        sample_rows_string = "\n".join([str(row) for row in sample_rows])
        connection.close()
        return sample_rows_string