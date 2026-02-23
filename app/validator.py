"""
validator.py - Validates generated SQL against the schema using regex and Python logic.
NO LLM used here. Pure rule-based validation.
"""
import re
from app.schema import VALID_TABLES, VALID_COLUMNS

# SQL keywords and functions that look like table aliases but aren't
SQL_KEYWORDS = {
    'extract', 'year', 'month', 'day', 'hour', 'minute', 'second',
    'date_part', 'date_trunc', 'now', 'current_date', 'current_timestamp',
    'coalesce', 'nullif', 'cast', 'case', 'when', 'then', 'else', 'end',
    'count', 'sum', 'avg', 'max', 'min', 'upper', 'lower', 'trim',
    'substring', 'length', 'concat', 'round', 'floor', 'ceil',
    'interval', 'timestamp', 'date', 'time', 'epoch', 'timezone'
}


class ValidationResult:
    def __init__(self, is_valid: bool, errors: list):
        self.is_valid = is_valid
        self.errors = errors

    def __repr__(self):
        status = "✅ VALID" if self.is_valid else "❌ INVALID"
        if self.errors:
            return f"{status}\nErrors:\n" + "\n".join(f"  - {e}" for e in self.errors)
        return status


def _extract_tables_from_sql(sql: str):
    """
    Extract table names and aliases from FROM and JOIN clauses.
    Returns (set of real table names, dict of alias -> real table name).
    """

    sql_no_parens = re.sub(r'\([^)]*\)', ' ', sql)
    pattern = r'\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\s+(?:AS\s+)?([a-zA-Z_][a-zA-Z0-9_]*))?'
    matches = re.findall(pattern, sql_no_parens, re.IGNORECASE)

    tables = set()
    alias_map = {}

    for table_name, alias in matches:
        table_lower = table_name.lower()
        if table_lower in SQL_KEYWORDS:
            continue
        tables.add(table_lower)
        if alias and alias.lower() not in SQL_KEYWORDS:
            alias_map[alias.lower()] = table_lower

    return tables, alias_map


def _extract_column_references(sql: str, alias_map: dict):
    """
    Extract table.column references from SQL.
    Resolves aliases to real table names.
    Skips SQL function keywords.
    """
    pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\b'
    matches = re.findall(pattern, sql)

    resolved = []
    for tbl_or_alias, col in matches:
        tbl_lower = tbl_or_alias.lower()
        col_lower = col.lower()

        # Skip SQL keywords that look like table references
        if tbl_lower in SQL_KEYWORDS:
            continue

        # Resolve alias to real table name
        real_table = alias_map.get(tbl_lower, tbl_lower)
        resolved.append((real_table, col_lower))

    return resolved


def validate_sql(sql: str, intent: dict) -> ValidationResult:
    """
    Validate the generated SQL query against the schema.
    Checks:
      1. All tables referenced exist in schema
      2. All table.column references are valid
      3. Tables in intent are actually used in query
      4. Basic SQL structure
      5. GROUP BY completeness
    """
    errors = []
    sql_clean = sql.strip().rstrip(";")

    # --- Step 1: Extract tables and aliases ---
    tables_used, alias_map = _extract_tables_from_sql(sql_clean)

    for tbl in tables_used:
        if tbl not in VALID_TABLES:
            errors.append(f"Table '{tbl}' does not exist in schema.")

    # --- Step 2: Validate table.column references ---
    col_refs = _extract_column_references(sql_clean, alias_map)
    for tbl, col in col_refs:
        if tbl not in VALID_TABLES:
            errors.append(f"Unknown table '{tbl}' in column reference '{tbl}.{col}'.")
        elif col not in VALID_COLUMNS.get(tbl, set()):
            errors.append(f"Column '{col}' does not exist in table '{tbl}'.")

    # --- Step 3: Check intent tables are present ---
    intent_tables = set(t.lower() for t in intent.get("target_tables", []))
    for tbl in intent_tables:
        if tbl not in tables_used:
            errors.append(f"Intent specified table '{tbl}' but it is missing from the SQL.")

    # --- Step 4: Basic SQL structure check ---
    if not re.search(r'\bSELECT\b', sql_clean, re.IGNORECASE):
        errors.append("SQL does not contain a SELECT statement.")
    if not re.search(r'\bFROM\b', sql_clean, re.IGNORECASE):
        errors.append("SQL does not contain a FROM clause.")

    # --- Step 5: GROUP BY completeness check ---
    select_match = re.search(r'SELECT\s+(.*?)\s+FROM', sql_clean, re.IGNORECASE | re.DOTALL)
    if select_match:
        select_part = select_match.group(1)
        groupby_match = re.search(r'GROUP\s+BY\s+(.*?)(?:ORDER|LIMIT|HAVING|$)', sql_clean, re.IGNORECASE | re.DOTALL)
        if groupby_match:
            groupby_cols = groupby_match.group(1).strip()
            # Remove aggregate functions from SELECT before checking
            select_no_agg = re.sub(
                r'\b(COUNT|SUM|AVG|MAX|MIN)\s*\(.*?\)', '', select_part, flags=re.IGNORECASE
            )
            select_cols = re.findall(r'\b([a-zA-Z_]+)\.([a-zA-Z_]+)\b', select_no_agg)
            groupby_col_refs = re.findall(r'\b([a-zA-Z_]+)\.([a-zA-Z_]+)\b', groupby_cols)
            groupby_plain = re.findall(r'\b([a-zA-Z_]+)\b', groupby_cols)

            for tbl, col in select_cols:
                if tbl.lower() in SQL_KEYWORDS:
                    continue
                # Resolve alias for comparison
                real_tbl = alias_map.get(tbl.lower(), tbl.lower())
                real_grp = [(alias_map.get(t.lower(), t.lower()), c.lower()) for t, c in groupby_col_refs]
                in_groupby = (real_tbl, col.lower()) in real_grp or col.lower() in groupby_plain
                if not in_groupby:
                    errors.append(
                        f"Column '{tbl}.{col}' in SELECT must appear in GROUP BY or inside an aggregate function."
                    )

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)


def build_retry_hint(validation_result: ValidationResult, intent: dict) -> str:
    """Build a hint string to feed back to LLM when validation fails."""
    hint_lines = ["The previously generated SQL failed validation. Please fix these issues:"]
    for err in validation_result.errors:
        hint_lines.append(f"  - {err}")
    hint_lines.append("\nOnly use tables and columns that exist in the provided schema.")
    hint_lines.append(f"Valid tables: {', '.join(sorted(VALID_TABLES))}")
    for tbl in VALID_TABLES:
        hint_lines.append(f"  {tbl}: {', '.join(sorted(VALID_COLUMNS[tbl]))}")
    return "\n".join(hint_lines)