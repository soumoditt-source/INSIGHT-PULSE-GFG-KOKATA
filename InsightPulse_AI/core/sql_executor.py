"""
InsightPulse AI - SQL Executor v5.0 (DuckDB)
=====================================================================
Safely executes generated SQL against the loaded DataFrame.
Table is ALWAYS registered as 'sales' for consistency across all datasets.
"""
import duckdb
import pandas as pd
from typing import Optional, Tuple

# ── Module-level DuckDB connection (in-memory, reinitialized on upload)
_conn: Optional[duckdb.DuckDBPyConnection] = None
_registered_df: Optional[pd.DataFrame] = None

# Blocked SQL keywords (security + data integrity)
_BLOCKED_KEYWORDS = frozenset([
    "DROP", "DELETE", "INSERT", "UPDATE", "CREATE", "ALTER",
    "TRUNCATE", "EXEC", "EXECUTE", "MERGE", "REPLACE"
])


def init_connection(df: pd.DataFrame) -> None:
    """
    Initialize DuckDB in-memory connection.
    Registers DataFrame as table 'sales' (universal name across all datasets).
    Old connection is closed and replaced on re-upload.
    """
    global _conn, _registered_df
    if _conn is not None:
        try:
            _conn.close()
        except Exception:
            pass

    _conn = duckdb.connect(database=":memory:")
    _registered_df = df.copy()

    # Register as 'sales' - every dataset uses this name
    _conn.register("sales", _registered_df)

    # Verify registration
    count = _conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    print(f"[DuckDB] [OK] Table 'sales' registered: {count:,} rows * {len(df.columns)} columns")


def get_conn() -> Optional[duckdb.DuckDBPyConnection]:
    """Return the current DuckDB connection (may be None if not initialized)."""
    return _conn


def validate_sql(sql: str) -> Tuple[bool, str]:
    """
    Validate SQL before execution.
    Returns (is_valid: bool, reason: str).
    """
    if not sql or not sql.strip():
        return False, "SQL is empty."

    sql_clean = sql.strip()
    sql_upper = sql_clean.upper()

    # Must be a SELECT statement
    if not sql_upper.lstrip().startswith("SELECT"):
        return False, "Only SELECT statements are allowed. Non-SELECT SQL rejected."

    # Block destructive keywords
    for kw in _BLOCKED_KEYWORDS:
        # Word-boundary check to avoid false positives (e.g., "CREATED_AT")
        import re
        if re.search(rf'\b{kw}\b', sql_upper):
            return False, f"Blocked keyword '{kw}' found in SQL."

    # Must reference 'sales' table
    if "SALES" not in sql_upper and "FROM" in sql_upper:
        return False, "SQL must query the 'sales' table. Use: FROM sales"

    return True, "OK"


def execute_sql(sql: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Execute validated SQL against the registered 'sales' table.
    Returns (DataFrame, None) on success, or (None, error_message) on failure.
    """
    global _conn

    if _conn is None:
        return None, "Database not initialized. Please upload a dataset first."

    is_valid, reason = validate_sql(sql)
    if not is_valid:
        return None, f"SQL validation failed: {reason}"

    try:
        result_df = _conn.execute(sql).df()
        return result_df, None

    except duckdb.CatalogException as e:
        # Column or table not found
        err = str(e)
        return None, (
            f"Column or table not found: {err}. "
            "Make sure column names exactly match the schema. "
            "Table must be 'sales'."
        )
    except duckdb.ParserException as e:
        return None, f"SQL syntax error: {str(e)}. Try rephrasing your query."
    except duckdb.ConversionException as e:
        return None, f"Data type error: {str(e)}. Check date formats or numeric casts."
    except Exception as e:
        return None, f"Query execution error: {str(e)}"


def get_schema_json(df: pd.DataFrame) -> dict:
    """Generate lightweight schema JSON from a DataFrame."""
    columns = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        if dtype.startswith(("float", "int")):
            col_type = "numeric"
            try:
                sample_vals = df[col].dropna().round(4).head(3).tolist()
                stats = {
                    "min": round(float(df[col].min()), 4),
                    "max": round(float(df[col].max()), 4),
                    "mean": round(float(df[col].mean()), 4)
                }
            except Exception:
                sample_vals, stats = [], {}
        else:
            col_type = "categorical"
            sample_vals = [str(v) for v in df[col].dropna().unique()[:5]]
            stats = {"unique_count": int(df[col].nunique())}

        columns.append({
            "name": col,
            "type": col_type,
            "sample_values": sample_vals,
            "stats": stats
        })

    return {
        "table_name": "sales",
        "total_rows": len(df),
        "columns": columns
    }


def get_sample_rows(df: pd.DataFrame, n: int = 5) -> list:
    """Return n sample rows as JSON-serializable list of dicts."""
    return df.head(n).fillna("").to_dict(orient="records")


def dataframe_to_records(df: pd.DataFrame) -> list:
    """
    Convert DataFrame to JSON-serializable list of records.
    Rounds floats, converts datetimes, fills NaN with null.
    """
    if df is None:
        return []
    # Round floats for clean display
    for col in df.select_dtypes(include=["float64", "float32"]).columns:
        df[col] = df[col].round(4)
    # Convert any datetime columns to string
    for col in df.select_dtypes(include=["datetime64"]).columns:
        df[col] = df[col].astype(str)
    return df.where(pd.notnull(df), None).to_dict(orient="records")
