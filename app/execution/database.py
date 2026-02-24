"""
database.py - PostgreSQL connection and query execution.
"""
import psycopg2
import psycopg2.extras
from app.configuration.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    """Create and return a PostgreSQL connection."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def execute_query(sql: str) -> dict:
    """
    Execute a SQL query and return results.
    Returns a dict with columns, rows, and row count.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql)

        rows = cursor.fetchall()
        columns = list(rows[0].keys()) if rows else []

        return {
            "success": True,
            "columns": columns,
            "rows": [dict(row) for row in rows],
            "row_count": len(rows),
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "columns": [],
            "rows": [],
            "row_count": 0,
            "error": str(e)
        }
    finally:
        if conn:
            conn.close()


def test_connection() -> bool:
    """Test if database connection works."""
    try:
        conn = get_connection()
        conn.close()
        return True
    except Exception:
        return False