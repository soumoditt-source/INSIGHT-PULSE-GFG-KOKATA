"""
InsightPulse AI - Neural Agentic Core
=====================================================================
Developed by Soumoditya Das | Advised by Sounak Mondal

This module orchestrates the 'Super Intelligence' feedback loop.
It uses 'Transformer Pathways' to deconstruct user intent, 
generate DuckDB SQL, and reflect on its own logic before execution.
This ensures a professional, high-accuracy experience for data analysis.
"""
import time
import json
from typing import Optional, Tuple, List, Dict, Any

import pandas as pd

from core.llm_engine import generate_dashboard, call_llm, parse_llm_response, build_prompt
from core.sql_executor import execute_sql, validate_sql, init_connection


# -----------------------------------------------------------------
# SELF-CORRECTION PROMPT
# When SQL fails, we send the error back to Gemini with context
# -----------------------------------------------------------------

CORRECTION_PROMPT = """
You are INSIGHTPULSE ORACLE - fixing a SQL error.

## SCHEMA
{schema_json}

## ORIGINAL USER QUERY
"{user_query}"

## YOUR PREVIOUS (FAILED) SQL
```sql
{failed_sql}
```

## ERROR MESSAGE
{error_msg}

## TASK
Generate a CORRECTED DuckDB SQL query using Chain-of-Thought reasoning.
1. Table name MUST be: `sales`
2. Fix the specific error shown above.
3. Use exact column names from schema.

Output ONLY valid JSON:
{{
  "sql": "SELECT ... FROM sales ... LIMIT 20",
  "charts": [...],
  "insights": [...],
  "followup_suggestions": [...],
  "error": null
}}
"""

REFLECTION_PROMPT = """
You are INSIGHTPULSE ORACLE - performing a PRE-FLIGHT REFLECTION.

## SCHEMA
{schema_json}

## YOUR GENERATED PLAN
SQL: {sql}
INTENT: {intent}

## TASK
Critique this plan. Does it use valid columns? Does it follow DuckDB syntax? 
If perfect, return "READY". 
If flawed, return a JSON with a corrected "sql" and "error" explanation.

Output ONLY "READY" or the JSON object.
"""


def _build_correction_prompt(
    user_query: str,
    failed_sql: str,
    error_msg: str,
    schema_json: dict,
    document_context: str = ""
) -> str:
    """Build the self-correction prompt for failed SQL."""
    return CORRECTION_PROMPT.format(
        schema_json=json.dumps(schema_json, indent=2),
        document_context=document_context[:10000] if document_context else "No external documents loaded.",
        user_query=user_query,
        failed_sql=failed_sql,
        error_msg=error_msg
    )

def _process_intent(user_query: str, schema_json: dict, sample_rows: List[Dict[str, Any]], chat_history: List[Dict[str, Any]], document_context: str) -> Dict[str, Any]:
    """Helper to handle first LLM reasoning step."""
    enriched_query = f"DOCUMENT CONTEXT:\n{document_context[:10000]}\n\nUSER QUERY: {user_query}" if document_context else user_query
    return generate_dashboard(enriched_query, schema_json, sample_rows, chat_history)

def _handle_sql_loop(user_query: str, schema_json: dict, initial_result: dict, max_retries: int, pathway: List[str], document_context: str) -> Tuple[Optional[pd.DataFrame], Dict[str, Any], str]:
    """Handles the SQL execution and self-correction loop."""
    current_sql = initial_result.get("sql")
    current_charts = initial_result.get("charts", [])
    current_insights = initial_result.get("insights", [])
    
    last_error = None
    result_df = None

    for attempt in range(max_retries):
        pathway.append(f"📡 Executing SQL (Attempt {attempt+1})...")
        result_df, exec_error = execute_sql(current_sql)

        if exec_error is None and result_df is not None:
            return result_df, {"sql": current_sql, "charts": current_charts, "insights": current_insights}, ""

        last_error = exec_error or "Unknown execution error"
        pathway.append(f"🔄 Auto-Correction required: {last_error[:50]}...")
        
        if attempt < max_retries - 1:
            correction_prompt = _build_correction_prompt(user_query, current_sql, last_error, schema_json, document_context)
            correction_raw = call_llm(correction_prompt)
            correction_result = parse_llm_response(correction_raw)
            if correction_result.get("sql"):
                current_sql = correction_result["sql"]
                if correction_result.get("charts"): current_charts = correction_result["charts"]
                if correction_result.get("insights"): current_insights = correction_result["insights"]
            else:
                break
    return None, {"sql": current_sql, "charts": current_charts, "insights": current_insights}, last_error

def run_agentic_pipeline(
    user_query: str,
    schema_json: dict,
    sample_rows: List[Dict[str, Any]],
    chat_history: List[Dict[str, Any]],
    document_context: str = "",
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Full agentic SQL pipeline with self-correction loop + Document RAG context.
    """
    agent_meta = {"retries": 0, "total_ms": 0, "success": False, "pathway": []}
    pathway = agent_meta["pathway"]
    t_start = time.time()

    # Step 1: Intent
    pathway.append("🧠 Thinking with Gemini 1.5 Pro core (RAG mode)...")
    llm_result = _process_intent(user_query, schema_json, sample_rows, chat_history, document_context)
    
    if llm_result.get("error") and not llm_result.get("sql"):
        agent_meta["total_ms"] = int((time.time() - t_start) * 1000)
        return {**llm_result, "agent_metadata": agent_meta, "pathway": pathway}

    intent = llm_result.get("intent", "")
    if intent in ("general_ai", "document_qa") or not llm_result.get("sql"):
        agent_meta["total_ms"] = int((time.time() - t_start) * 1000)
        agent_meta["success"] = True
        pathway.append("🗣️ Native Conversational / Document Engine engaged. Bypassing SQL.")
        return {
            "intent": intent,
            "sql": None,
            "result_df": None,
            "charts": [],
            "insights": llm_result.get("insights", []),
            "followup_suggestions": llm_result.get("followup_suggestions", []),
            "error": None,
            "agent_metadata": agent_meta,
            "pathway": pathway
        }

    # Step 2: SQL Loop
    result_df, final_state, error = _handle_sql_loop(user_query, schema_json, llm_result, max_retries, pathway, document_context)
    
    agent_meta["total_ms"] = int((time.time() - t_start) * 1000)
    agent_meta["success"] = result_df is not None

    if result_df is None:
        return {**final_state, "data": [], "error": error, "agent_metadata": agent_meta, "pathway": pathway}

    return {
        "intent": llm_result.get("intent"),
        "sql": final_state["sql"],
        "result_df": result_df,
        "charts": final_state["charts"],
        "insights": final_state["insights"],
        "followup_suggestions": llm_result.get("followup_suggestions", []),
        "error": None,
        "agent_metadata": agent_meta,
        "pathway": pathway
    }
