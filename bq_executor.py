"""
bq_query_executor.py
Script 2 — Execute SQL queries on BigQuery and display results.
Uses bq_connection.py to get the client.
"""
from bq_connection import get_bigquery_connection


def execute_query(sql: str) -> dict:
    
    try:
        client = get_bigquery_connection()
        query_job = client.query(sql)
        results   = query_job.result()

        rows    = [dict(row) for row in results]
        columns = list(rows[0].keys()) if rows else []

       
        for row in rows:
            print(row)

        return {
            "success":   True,
            "columns":   columns,
            "rows":      rows,
            "row_count": len(rows),
            "error":     None
        }

    except Exception as e:
        print(f"\n Query failed: {e}")
        return {
            "success":   False,
            "columns":   [],
            "rows":      [],
            "row_count": 0,
            "error":     str(e)
        }


