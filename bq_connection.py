"""
bq_connection.py
Connects to BigQuery and fetches all tables from thelook_ecommerce dataset.
"""
from google.cloud import bigquery
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

load_dotenv()

KEY_FILE   = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "bigquery-key.json")
PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID", "")
DATASET    = "bigquery-public-data.thelook_ecommerce"


def get_bigquery_connection():
    """Connect to BigQuery and return client."""
    credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE,
        scopes=["https://www.googleapis.com/auth/bigquery"]
    )
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    print(f"Connected to BigQuery | Project: {PROJECT_ID}")
    return client


def fetch_all_tables():
    """Fetch all table names from thelook_ecommerce dataset."""
    client = get_bigquery_connection()

    dataset_ref = client.dataset(
        dataset_id="thelook_ecommerce",
        project="bigquery-public-data"
    )

    tables = list(client.list_tables(dataset_ref))

    print(f"\nDataset: {DATASET}")
    print(f"Total tables found: {len(tables)}")
    print("-" * 40)

    table_names = []
    for table in tables:
        print(f"  → {table.table_id}")
        table_names.append(table.table_id)

    return table_names


if __name__ == "__main__":

    # Step 1 — fetch all tables
    tables = fetch_all_tables()
    print(f"\nDone. {len(tables)} tables fetched.")

   
    from bq_executor import execute_query

   
    query_1 = """
    SELECT status, COUNT(order_id) AS order_count 
    FROM `bigquery-public-data.thelook_ecommerce.orders` 
    GROUP BY status
    """

    query_2 = """
    SELECT 
        u.id, 
        COUNT(o.order_id) AS total_orders
    FROM 
        `bigquery-public-data.thelook_ecommerce.orders` o
    INNER JOIN 
        `bigquery-public-data.thelook_ecommerce.users` u
    ON 
        o.user_id = u.id
    GROUP BY 
        u.id
    ORDER BY 
        total_orders DESC
    LIMIT 5
    """

    # Step 4 — run queries
    print("\n" + "=" * 40)
    print("Query 1: Orders by status")
    print("=" * 40)
    result1 = execute_query(query_1)

    print("\n" + "=" * 40)
    print("Query 2: Top 5 users by total orders")
    print("=" * 40)
    result2 = execute_query(query_2)