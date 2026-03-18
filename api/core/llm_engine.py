"""
InsightPulse AI - LLM Engine v5.0
=====================================================================
Gemini 2.0 Flash powered Text-to-SQL-to-Dashboard pipeline.
Fully generalized for ANY uploaded dataset + pre-tuned for Amazon Sales.
"""
import json
import re
import os
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

from openai import OpenAI
from google import genai

# ── Load API key securely from .env
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass  # dotenv optional - key can be set via OS environment

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Initialize Google SDK (Modern v1.0+ Client)
genai_client = None
if GEMINI_API_KEY:
    try:
        genai_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"[LLM] Error initializing Google GenAI client: {e}")

# Initialize OpenRouter Client
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

# ── System prompt - fully dynamic, injected with real schema at runtime
SYSTEM_PROMPT_TEMPLATE = """
You are INSIGHTPULSE ORACLE v6.0 (Super Intelligence Edition) - a world-class AI 
architecture powered by Gemini 1.5 Pro. You utilize "Transformer Pathways" for 
recursive reasoning and 100% accuracy in data-to-dashboard transformation.

You transform plain-English business questions into interactive Plotly dashboards 
using a strictly verified SQL-based reasoning pipeline.

----------------------- LOADED DATASET SCHEMA (RAG-INDEXED) -----------------------
{schema_json}

----------------------- SAMPLE DATA ROWS -----------------------
{sample_rows}

----------------------- PREVIOUS CONVERSATION -----------------------
{chat_history}

----------------------- LIVE WEB CONTEXT -----------------------
{live_context}

----------------------- USER QUERY -----------------------
"{user_query}"

----------------------- YOUR 5-STEP PIPELINE -----------------------

STEP 1 - INTENT CLASSIFY:
  Operations: ranking | trend | comparison | distribution | heatmap | correlation | anomaly | forecast | raw_table
  Group-by candidates from schema columns
  Metric candidates from numeric columns
  Filters from string/date columns

STEP 2 - GENERATE DUCKDB SQL:
  - Table name: `sales` (always - this is how it's registered)
  - Only SELECT statements (no INSERT/UPDATE/DELETE/DROP)
  - Use exact column names from the schema above
  - For date/time columns use: STRPTIME or CAST as DATE
  - Always LIMIT 50 unless user specifies or ranking (then LIMIT 10-20)
  - Order by primary metric DESC for rankings
  - For time series: ORDER BY date_column ASC
  - NEVER invent column names not in the schema

STEP 3 - VALIDATE:
  - Confirm every column in SELECT exists in schema
  - String filters must be exact values from the sample_values list
  - If invalid: set error field with clear explanation

STEP 4 - SELECT VISUALIZATION:
  - `bar`    -> categorical comparisons (e.g., revenue by category)
  - `hbar`   -> rankings (top N, sorted descending by value)
  - `line`   -> time series (monthly trend, daily revenue)
  - `pie`    -> part-of-whole (payment method share, category split)
  - `donut`  -> same as pie but with hole=0.45
  - `heatmap` -> 2D matrix (category * region, colored by metric)
  - `scatter` -> correlation between 2 numeric columns
  - `treemap` -> hierarchical breakdown
  - `radar`  -> multi-metric comparison of 2-5 entities
  - `table`  -> raw data view, top rows
  - MULTI-CHART: if query has 2+ logical views, output up to 4 chart objects

STEP 5 - GENERATE 3 INSIGHTS:
  1. Key finding (best/worst performer, highest value)
  2. Anomaly (anything > avg + 1.5 std, or < avg - 1.5 std)
  3. Business recommendation (actionable, data-driven)

═══════════════════════ TRANSFORMER REASONING PATHWAY (CoT) ═══════════════════════
1. BREAKDOWN: Deconstruct the user query into atomic data requirements.
2. SCHEMATIC MAPPING: Map every requirement to a SPECIFIC column in the schema.
3. CONVERSATIONAL SYNERGY: Leverage chat history to maintain context of filters.
4. PREDICATE VERIFICATION: Double-check all WHEWE clauses against sample_values.
5. VISUAL OPTIMIZATION: Choose charts that minimize cognitive load for CXOs.

═══════════════════════ ABSOLUTE RULES (100% ACCURACY) ═══════════════════════
1. Output ONLY raw JSON - no markdown fences, no explanation, no extra keys.
2. If a column doesn't exist in schema -> set "error": "Column 'X' not found."
3. If query is unanswerable -> set "error" with helpful explanation.
4. NEVER hallucinate - if data isn't in schema, say so.
5. Use STRPTIME or CAST for all Date operations in DuckDB.
6. Target model: Gemini 1.5 Pro / Transformer Logic.

═══════════════════════ OUTPUT FORMAT (STRICT JSON) ═══════════════════════
{{
  "intent": "ranking|trend|comparison|distribution|heatmap|correlation|anomaly|table",
  "sql": "SELECT ... FROM sales ... LIMIT 20",
  "charts": [
    {{
      "type": "bar|hbar|line|pie|donut|heatmap|scatter|treemap|radar|table",
      "title": "Descriptive Chart Title with Units",
      "x_col": "column_name",
      "y_col": "column_name",
      "color_col": null,
      "orientation": "v",
      "layout": {{
        "height": 450,
        "showlegend": true,
        "colorscale": "Viridis"
      }},
      "annotations": []
    }}
  ],
  "insights": [
    "Key finding: ...",
    "Anomaly: ...",
    "Recommendation: ..."
  ],
  "followup_suggestions": [
    "Suggestion 1?",
    "Suggestion 2?",
    "Suggestion 3?"
  ],
  "error": null
}}
"""


def build_prompt(
    user_query: str,
    schema_json: dict,
    sample_rows: List[Dict[str, Any]],
    chat_history: List[Dict[str, Any]],
    live_context: str = ""
) -> str:
    """Build the full LLM prompt with live schema + history + web context injected."""
    history_text = ""
    if chat_history:
        for msg in chat_history[-6:]:  # last 3 exchanges (6 messages)
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if isinstance(content, dict):
                content = content.get("sql", "") or str(content)[:200]
            history_text += f"{role.upper()}: {str(content)[:300]}\n"

    return SYSTEM_PROMPT_TEMPLATE.format(
        schema_json=json.dumps(schema_json, indent=2),
        sample_rows=json.dumps(sample_rows[:5], indent=2, default=str),
        user_query=user_query,
        chat_history=history_text or "No prior conversation.",
        live_context=live_context or "No live context required."
    )
def call_llm(prompt: str) -> str:
    """Multi-stage fallback: Native Google SDK -> OpenRouter Gemini -> OpenRouter Claude -> Free."""
    # -- 1. Native Google Flash (Fast & Cost-Effective)
    if genai_client:
        for model_id in ["gemini-2.0-flash", "gemini-1.5-flash"]:
            try:
                print(f"[LLM] Attempting Native Google {model_id}...")
                response = genai_client.models.generate_content(
                    model=model_id,
                    config={
                        "temperature": 0.0,
                        "system_instruction": """
    1.  **Professionalism**: Always use sophisticated, business-ready language.
    2.  **Accuracy**: Only refer to data present in the schema or document context.
    3.  **Proactivity**: If a trend is found, suggest a strategic optimization.
    4.  **Visuals**: Recommend specific chart types (bar, line, pie, etc.) in your JSON response.
    5.  **Humanized Response**: Acknowledge the user as 'Operator' or 'Lead Architect'.
                    """},
                    contents=prompt
                )
                if response and response.text:
                    print(f"[LLM SUCCESS] Received response using Native {model_id}.")
                    return response.text
                else:
                    print(f"[LLM WARNING] {model_id} returned empty text or blocked content.")
            except Exception as e:
                print(f"[LLM ERROR] {model_id} failed: {e}")
                # We specifically check for 429 to continue silently, or just try all.
                continue

    # ── 2. Dual-Channel: Try OpenRouter (Gemini 1.5 Pro)
    if OPENROUTER_API_KEY:
        try:
            print(f"[LLM] Falling back to OpenRouter Gemini 1.5 Pro...")
            completion = client.chat.completions.create(
              model="google/gemini-pro-1.5",
              messages=[{"role": "user", "content": prompt}],
              temperature=0.0,
              max_tokens=2048,
              timeout=10,
            )
            content = completion.choices[0].message.content
            if content:
                print(f"[LLM SUCCESS] Received response using OpenRouter Gemini.")
                return content
            else:
                print(f"[LLM WARNING] OpenRouter Gemini returned empty content.")
        except Exception as e:
            print(f"[LLM ERROR] OpenRouter Gemini fallback failed: {e}")

    # ── 3. Final Fail-Safe: OpenRouter (Claude 3.5 Sonnet)
    if OPENROUTER_API_KEY:
        try:
            print(f"[LLM] Final fail-safe: OpenRouter Claude 3.5 Sonnet...")
            completion = client.chat.completions.create(
              model="anthropic/claude-3.5-sonnet",
              messages=[{"role": "user", "content": prompt}],
              temperature=0.0,
              max_tokens=2048,
              timeout=10,
            )
            content = completion.choices[0].message.content
            if content:
                print(f"[LLM SUCCESS] Received response using Claude 3.5 Sonnet.")
                return content
        except Exception as e:
            print(f"[LLM ERROR] Claude 3.5 fallback failed: {e}")

    # ── 4. EMERGENCY FREE BACKUP: Verified OpenRouter Free Models
    if OPENROUTER_API_KEY:
        # Using specific models verified via diagnostic list_models run
        free_models = [
            "google/gemini-2.0-flash-lite-preview-02-05:free",
            "nvidia/nemotron-3-super-120b-a12b:free",
            "minimax/minimax-m2.5:free",
            "google/gemini-2.0-flash-exp:free"
        ]
        for model_id in free_models:
            try:
                print(f"[LLM] EMERGENCY: Attempting Verified Free Model ({model_id})...")
                completion = client.chat.completions.create(
                  model=model_id,
                  messages=[{"role": "user", "content": prompt}],
                  temperature=0.0,
                  max_tokens=2048,
                  timeout=8,
                )
                content = completion.choices[0].message.content
                if content:
                    print(f"[LLM SUCCESS] Received response using FREE {model_id}.")
                    return content
            except Exception as e:
                print(f"[LLM ERROR] Free model {model_id} failed: {e}")
    
    return None


def parse_llm_response(raw: str) -> dict:
    """Parse and validate the LLM JSON response with robust fallback."""
    EMPTY = {
        "intent": "unknown",
        "sql": None,
        "charts": [],
        "insights": [],
        "followup_suggestions": [],
        "error": None
    }

    if not raw:
        return {**EMPTY, "error": "LLM returned empty response. Please retry."}

    raw = raw.strip()
    # Strip markdown code fences if Gemini adds them despite instruction
    raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'\s*```\s*$', '', raw, flags=re.MULTILINE)
    raw = raw.strip()

    try:
        result = json.loads(raw)
        # Ensure all required fields exist
        for key, default in EMPTY.items():
            result.setdefault(key, default)
        return result
    except json.JSONDecodeError:
        # Attempt to extract largest JSON object from messy output
        match = re.search(r'\{[\s\S]*\}', raw)
        if match:
            try:
                result = json.loads(match.group())
                for key, default in EMPTY.items():
                    result.setdefault(key, default)
                return result
            except Exception:
                pass

        return {
            **EMPTY,
            "error": "LLM produced invalid JSON. Try rephrasing your query.",
            "followup_suggestions": [
                "Try: 'Show top 10 products by revenue'",
                "Try: 'Monthly sales trend'",
                "Try: 'Revenue by customer region'"
            ]
        }


def get_live_context(user_query: str) -> str:
    """Uses DuckDuckGo to pull live news or web context if requested."""
    keywords = ["news", "live", "today", "current", "latest", "search", "internet"]
    if any(k in user_query.lower() for k in keywords):
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                if "news" in user_query.lower():
                    results = list(ddgs.news(user_query, max_results=3))
                    return "LIVE NEWS:\n" + "\n".join([f"- {r.get('title','')}: {r.get('body','')} ({r.get('date','')})" for r in results])
                else:
                    results = list(ddgs.text(user_query, max_results=3))
                    return "LIVE WEB:\n" + "\n".join([f"- {r.get('title','')}: {r.get('body','')}" for r in results])
        except Exception as e:
            print(f"[DDG ERROR] Web search failed: {e}")
            return ""
    return ""

def generate_dashboard(
    user_query: str,
    schema_json: dict,
    sample_rows: List[Dict[str, Any]],
    chat_history: List[Dict[str, Any]]
) -> dict:
    """
    Main entry point: NL query -> structured dashboard JSON.
    """
    # 1. Fetch live web context if needed
    live_context = get_live_context(user_query)

    # 2. Build Prompt
    prompt = build_prompt(user_query, schema_json, sample_rows, chat_history, live_context)
    
    # 3. Call Claude 3.5 Sonnet
    raw_response = call_llm(prompt)
    
    # 4. Parse
    return parse_llm_response(raw_response)
