"""
api.py - FastAPI application exposing NL2SQL as a REST API.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.NL2sql import process_question
from app.database import execute_query, test_connection

app = FastAPI(
    title="NL2SQL API",
    description="Convert natural language questions to SQL and execute on PostgreSQL",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request / Response Models ---

class QuestionRequest(BaseModel):
    question: str

class NL2SQLResponse(BaseModel):
    question: str
    intent: dict | None
    sql: str | None
    validation: dict | None
    db_result: dict | None
    success: bool
    message: str
    attempts: int


# --- Routes ---

@app.get("/")
def root():
    return {"message": "NL2SQL API is running. Use POST /ask to query."}


@app.get("/health")
def health():
    """Check API and database connectivity."""
    db_ok = test_connection()
    return {
        "api": "ok",
        "database": "connected" if db_ok else "not connected"
    }


@app.post("/ask", response_model=NL2SQLResponse)
def ask(request: QuestionRequest):
    """
    Main endpoint: takes a natural language question,
    generates SQL, validates it, executes on PostgreSQL,
    and returns the result.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Step 1: Generate and validate SQL
    result = process_question(request.question)

    # Step 2: If SQL is valid, execute it on PostgreSQL
    db_result = None
    if result["success"] and result["sql"]:
        db_result = execute_query(result["sql"])
        if not db_result["success"]:
            result["message"] += f" | DB Error: {db_result['error']}"

    return NL2SQLResponse(
        question=result["question"],
        intent=result["intent"],
        sql=result["sql"],
        validation=result["validation"],
        db_result=db_result,
        success=result["success"],
        message=result["message"],
        attempts=result["attempts"]
    )


@app.post("/execute-sql")
def execute_raw_sql(payload: dict):
    """
    Directly execute a raw SQL query on PostgreSQL.
    Useful for testing.
    """
    sql = payload.get("sql", "").strip()
    if not sql:
        raise HTTPException(status_code=400, detail="SQL cannot be empty.")
    return execute_query(sql)