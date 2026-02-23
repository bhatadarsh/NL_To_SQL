"""
prompts.py - All prompt templates used when calling Gemini.
"""

def build_schema_summary(tables: dict) -> str:
    """Convert schema dict into a readable string for the prompt."""
    lines = []
    for table_name, table_info in tables.items():
        lines.append(f"Table: {table_name} — {table_info['description']}")
        for col, meta in table_info["columns"].items():
            fk = f" [FK → {meta['foreign_key']}]" if meta.get("foreign_key") else ""
            pk = " [PK]" if meta.get("primary_key") else ""
            lines.append(f"  - {col} ({meta['type']}){pk}{fk}: {meta['description']}")
        lines.append("")
    return "\n".join(lines)


INTENT_EXTRACTION_PROMPT = """
You are a SQL intent extractor. Given a user's natural language question and the available database schema, extract the intent as structured JSON.

=== SCHEMA ===
{schema}

=== USER QUESTION ===
{question}

=== INSTRUCTIONS ===
Respond with ONLY a valid JSON object (no markdown, no explanation). Use this exact structure:

{{
  "is_relevant": true or false,           // Is the question answerable using the given tables?
  "irrelevance_reason": "..." or null,    // If not relevant, explain briefly
  "target_tables": ["table1", ...],       // List of tables needed
  "selected_columns": {{                  // Columns needed per table
    "table1": ["col1", "col2"],
    ...
  }},
  "conditions": [                         // WHERE clause conditions
    {{
      "table": "table_name",
      "column": "col_name",
      "operator": "=, >, <, LIKE, IN, etc.",
      "value": "the value or null if dynamic"
    }}
  ],
  "joins": [                              // JOIN relationships needed
    {{
      "left_table": "table1",
      "left_column": "col1",
      "right_table": "table2",
      "right_column": "col2",
      "join_type": "INNER, LEFT, RIGHT"
    }}
  ],
  "aggregations": [                       // Any GROUP BY / aggregation functions
    {{
      "function": "COUNT, SUM, AVG, MAX, MIN",
      "column": "col_name",
      "table": "table_name",
      "alias": "result_alias"
    }}
  ],
  "group_by": [                           // Columns to group by
    {{"table": "table_name", "column": "col_name"}}
  ],
  "order_by": [                           // ORDER BY clauses
    {{"table": "table_name", "column": "col_name", "direction": "ASC or DESC"}}
  ],
  "limit": null or integer,              // LIMIT clause
  "query_intent_summary": "..."          // One-line plain English summary of what query does
}}
"""


SQL_GENERATION_PROMPT = """
You are a SQL query generator. Given the structured intent JSON and the database schema, generate a clean, correct SQL query.

=== SCHEMA ===
{schema}

=== INTENT JSON ===
{intent_json}

=== ORIGINAL QUESTION ===
{question}

=== INSTRUCTIONS ===
- Use the intent JSON as your primary guide. Do NOT add tables or columns not present in the intent.
- Generate standard SQL (compatible with MySQL/PostgreSQL).
- Use table aliases where appropriate.
- If the intent has joins, use them exactly as specified.
- Return ONLY the SQL query. No explanation, no markdown, no code fences.

=== STRICT SQL RULES ===
- If using COUNT(*) or any aggregate function WITHOUT GROUP BY, do NOT select individual columns — only select the aggregate.
- If you need BOTH individual columns AND a count, use GROUP BY on ALL non-aggregated columns.
- NEVER mix individual columns and aggregate functions without a proper GROUP BY clause.
- For questions like "show details with count", either:
    Option A: SELECT all detail columns, GROUP BY all of them, COUNT(*)
    Option B: Run two separate ideas as one — but in PostgreSQL use a subquery or window function
- When asked for "details", prefer SELECT * or all columns WITHOUT aggregation unless count is specifically needed.
- NEVER use LIKE on DATE columns. For year filtering use: EXTRACT(YEAR FROM column) = 2024
- NEVER use LIKE on DATE columns. For month filtering use: EXTRACT(MONTH FROM column) = 1
- NEVER cast dates as strings. Always use EXTRACT or DATE_PART for date comparisons.
"""