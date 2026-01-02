from pathlib import Path
from psycopg.sql import SQL

from backend.database import get_database_connection


def init_db() -> None:
    # root del projecte: .../localbet-backend/
    root_dir = Path(__file__).resolve().parent.parent
    schema_path = root_dir / "schema.sql"

    sql_text = schema_path.read_text(encoding="utf-8")

    # Divideix per ";" i executa cada sentència per separat
    statements = [stmt.strip() for stmt in sql_text.split(";") if stmt.strip()]

    with get_database_connection() as conn:
        for stmt in statements:
            conn.execute(query=SQL(stmt), parameters={})
