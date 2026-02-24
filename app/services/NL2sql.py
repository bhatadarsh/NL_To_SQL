"""
nl2sql.py - Core pipeline: NL → Intent JSON → SQL → Validate → Return
"""
import json
from app.schemas.schema import TABLES, VALID_TABLES
from app.llm.prompts import build_schema_summary, INTENT_EXTRACTION_PROMPT, SQL_GENERATION_PROMPT
from app.llm.gemini_client import call_gemini, call_gemini_for_json
from app.validation.validator import validate_sql, build_retry_hint
from app.configuration.config import MAX_RETRIES


def extract_intent(question: str, schema_text: str) -> dict:
    """Stage 1: Use Gemini to extract structured intent JSON from the question."""
    prompt = INTENT_EXTRACTION_PROMPT.format(schema=schema_text, question=question)
    return call_gemini_for_json(prompt)


def generate_sql(question: str, intent: dict, schema_text: str, retry_hint: str = "") -> str:
    """Stage 2: Use Gemini to generate SQL from the intent JSON."""
    intent_json_str = json.dumps(intent, indent=2)
    prompt = SQL_GENERATION_PROMPT.format(
        schema=schema_text,
        intent_json=intent_json_str,
        question=question,
    )
    if retry_hint:
        prompt += f"\n\n=== PREVIOUS ATTEMPT FAILED ===\n{retry_hint}"

    return call_gemini(prompt)


def process_question(question: str) -> dict:
    """
    Full pipeline:
      1. Build schema summary
      2. Extract intent via Gemini
      3. Check relevance
      4. Generate SQL via Gemini
      5. Validate SQL (no LLM)
      6. Retry up to MAX_RETRIES if validation fails
    Returns a result dict with all intermediate outputs.
    """
    schema_text = build_schema_summary(TABLES)
    result = {
        "question": question,
        "intent": None,
        "sql": None,
        "validation": None,
        "success": False,
        "message": "",
        "attempts": 0,
    }

    # --- Stage 1: Intent Extraction ---
    print(f"\n{'='*60}")
    print(f" Question: {question}")
    print(f"{'='*60}")
    print(" Stage 1: Extracting intent...")

    try:
        intent = extract_intent(question, schema_text)
    except Exception as e:
        result["message"] = f"Intent extraction failed: {e}"
        print(f" {result['message']}")
        return result

    result["intent"] = intent
    print(f"   is_relevant: {intent.get('is_relevant')}")
    print(f"   summary: {intent.get('query_intent_summary', 'N/A')}")

    # --- Relevance Check ---
    if not intent.get("is_relevant", False):
        table_names = ", ".join(sorted(VALID_TABLES))
        reason = intent.get("irrelevance_reason", "The question doesn't relate to available tables.")
        result["message"] = (
            f"Your question doesn't seem to be related to the available data. {reason} "
            f"Please ask questions about: {table_names}."
        )
        print(f"  Irrelevant question: {result['message']}")
        return result

    # --- Stage 2: SQL Generation with Retry Loop ---
    print("\n Stage 2: Generating SQL...")
    retry_hint = ""

    for attempt in range(1, MAX_RETRIES + 1):
        result["attempts"] = attempt
        print(f"   Attempt {attempt}/{MAX_RETRIES}...")

        try:
            sql = generate_sql(question, intent, schema_text, retry_hint)
        except Exception as e:
            result["message"] = f"SQL generation failed: {e}"
            print(f" {result['message']}")
            return result

        result["sql"] = sql

        # --- Stage 3: Validation (no LLM) ---
        validation = validate_sql(sql, intent)
        result["validation"] = {
            "is_valid": validation.is_valid,
            "errors": validation.errors,
        }

        if validation.is_valid:
            result["success"] = True
            result["message"] = "SQL generated and validated successfully."
            print(f"    Validation passed on attempt {attempt}")
            break
        else:
            print(f"    Validation failed:")
            for err in validation.errors:
                print(f"      - {err}")
            retry_hint = build_retry_hint(validation, intent)
            if attempt == MAX_RETRIES:
                result["message"] = f"SQL validation failed after {MAX_RETRIES} attempts."
                print(f"    Max retries reached.")

    return result