from google.cloud import bigquery
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

load_dotenv()

KEY_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "bigquery-key.json")
PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID", "")


def get_client():
    credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE,
        scopes=["https://www.googleapis.com/auth/bigquery"]
    )
    return bigquery.Client(credentials=credentials, project=PROJECT_ID)

def execute_bigquery(sql: str) -> dict:
    """
    Execute SQL on BigQuery and return results.
    """
    try:
        client = get_client()
        query_job = client.query(sql)
        results = query_job.result()

        rows = [dict(row) for row in results]
        columns = list(rows[0].keys()) if rows else []

        return {
            "success": True,
            "columns": columns,
            "rows": rows,
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
