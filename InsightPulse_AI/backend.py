"""
InsightPulse AI - FastAPI Backend v5.1
=====================================================================
Emergency Restored Version for GFG Kolkata 2026 Showcase.
Includes: No-Fail 4-Stage Fallback, Robust File Loader, and Forecast Engine.
"""

import os, sys, json, time, io
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# ── Path setup
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

from core.rag_schema import build_schema_context
from core.ml_analyzer import profile_dataset, get_sample_rows, get_forensic_metrics
from core.document_engine import process_business_file
from core.presentation_engine import generate_presentation_json, export_to_pptx
from core.chart_builder import build_figures, serialize_figures
from core.ml_analyzer import (
    compute_classification_metrics, compute_regression_metrics,
    compute_clustering, profile_dataset, detect_task_type, compute_distributions
)
from core.sql_executor import init_connection, dataframe_to_records
from core.agent import run_agentic_pipeline
from crm.crm_db import log_query, init_db

# ── Default dataset paths
DATA_DIR = Path(__file__).parent / "data"
DEFAULT_CSVS = [
    DATA_DIR / "Amazon Sales.csv",
    DATA_DIR / "Copy of India Life Insurance Claims.csv",
]

# ═══════════════════════════════════════════════════════════════════
# App creation
# ═══════════════════════════════════════════════════════════════════
app = FastAPI(
    title="InsightPulse AI - BI Engine v5.1",
    description="Conversational BI Dashboard for GFG Kolkata 2026",
    version="5.1.0",
)

api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_state: dict = {
    "df": None,
    "schema_json": None,
    "sample_rows": None,
    "dataset_name": "Not loaded",
    "profile": None,
    "document_context": "",
    "geo_info": {},
}

# ═══════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════

def _load_dataframe_into_state(df: pd.DataFrame, name: str) -> None:
    df.columns = [c.strip() for c in df.columns]
    app_state["df"] = df
    app_state["dataset_name"] = name
    app_state["schema_json"] = build_schema_context(df, dataset_name=name)
    app_state["sample_rows"] = get_sample_rows(df, n=7)
    app_state["profile"] = profile_dataset(df)
    app_state["geo_info"] = app_state["profile"].get("geo_detected", {})
    init_connection(df)
    print(f"[OK] Dataset loaded: '{name}' - {len(df):,} rows")

def _read_csv_resilient(data: bytes, filename: str = "") -> pd.DataFrame:
    if data.startswith(b'bplist00'):
        raise ValueError(f"'{filename}' is a Binary Plist (Mac format), not a spreadsheet.")
    if data.startswith(b'PK') and filename.lower().endswith(('.xlsx', '.xlsm')):
        return pd.read_excel(io.BytesIO(data))
    for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            return pd.read_csv(io.BytesIO(data), encoding=enc)
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    raise ValueError(f"Cannot decode '{filename}'. Verify file encoding.")

def _load_default_dataset() -> bool:
    for csv_path in DEFAULT_CSVS:
        if csv_path.exists():
            try:
                df = _read_csv_resilient(csv_path.read_bytes(), csv_path.name)
                _load_dataframe_into_state(df, csv_path.name)
                return True
            except Exception as e:
                print(f"[WARN] {csv_path.name} load failed: {e}")
    return False

def _set_active_dataset(name: str, data: bytes = None):
    try:
        Path("/tmp/active_dataset.txt").write_text(name)
        if data:
            (Path("/tmp") / name).write_bytes(data)
    except:
        pass

def _ensure_dataset_loaded():
    if app_state["df"] is not None:
        return
    try:
        active_txt = Path("/tmp/active_dataset.txt")
        if active_txt.exists():
            active_name = active_txt.read_text().strip()
            # Check if it was a custom upload
            custom_path = Path("/tmp") / active_name
            if custom_path.exists():
                df = _read_csv_resilient(custom_path.read_bytes(), active_name)
                _load_dataframe_into_state(df, active_name)
                return
            
            # Check if it was a preset
            mapping = {
                "Amazon Sales.csv": "Amazon Sales.csv",
                "Insurance Claims.csv": "Copy of India Life Insurance Claims.csv"
            }
            target = mapping.get(active_name)
            if target and (DATA_DIR / target).exists():
                df = _read_csv_resilient((DATA_DIR / target).read_bytes(), target)
                _load_dataframe_into_state(df, active_name)
                return
    except Exception as e:
        print(f"[WARN] Failed to load from /tmp cache: {e}")
    # Fallback to default
    _load_default_dataset()

# ═══════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup():
    init_db()
    _load_default_dataset()

@app.get("/health")
@api_router.get("/health")
async def health():
    _ensure_dataset_loaded()
    df = app_state["df"]
    return {
        "status": "healthy",
        "dataset_loaded": df is not None,
        "rows": len(df) if df is not None else 0,
        "geo_detected": app_state["geo_info"]
    }

@app.get("/schema")
@api_router.get("/schema")
async def get_schema():
    _ensure_dataset_loaded()
    if not app_state["schema_json"]: raise HTTPException(404, "No dataset loaded.")
    return app_state["schema_json"]

@app.get("/profile")
@api_router.get("/profile")
async def get_profile():
    _ensure_dataset_loaded()
    if app_state["df"] is None: raise HTTPException(404, "No dataset.")
    return app_state["profile"] or profile_dataset(app_state["df"])

class GenerateRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"
    chat_history: Optional[List[dict]] = []

class GenerateResponse(BaseModel):
    intent: Optional[str] = None
    sql: Optional[str] = None
    data: Optional[List[dict]] = []
    charts: Optional[List[dict]] = []
    insights: Optional[List[str]] = []
    error: Optional[str] = None
    duration_ms: Optional[int] = 0

@app.post("/upload")
@api_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    contents = await file.read()
    try:
        if filename.endswith(".csv"): df = _read_csv_resilient(contents, file.filename)
        elif filename.endswith((".xlsx", ".xls")): df = pd.read_excel(io.BytesIO(contents))
        else: raise HTTPException(400, "Unsupported format.")
        _set_active_dataset(file.filename, contents)
        _load_dataframe_into_state(df, file.filename)
        return {"status": "success", "filename": file.filename, "rows": len(df)}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/load-preset")
@api_router.post("/load-preset")
async def load_preset(req: dict):
    dataset_name = req.get("name")
    if not dataset_name: raise HTTPException(400, "Dataset name required.")
    
    # Map friendly names to actual files
    mapping = {
        "Amazon Sales.csv": "Amazon Sales.csv",
        "Insurance Claims.csv": "Copy of India Life Insurance Claims.csv"
    }
    target = mapping.get(dataset_name)
    if not target: raise HTTPException(404, "Preset not found.")
    
    path = DATA_DIR / target
    if not path.exists(): raise HTTPException(404, f"File {target} missing from server data folder.")
    
    try:
        _set_active_dataset(dataset_name)
        df = _read_csv_resilient(path.read_bytes(), target)
        _load_dataframe_into_state(df, dataset_name)
        return {"status": "success", "dataset": dataset_name, "rows": len(df)}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/generate", response_model=GenerateResponse)
@api_router.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    _ensure_dataset_loaded()
    if app_state["df"] is None: return GenerateResponse(error="No dataset.")
    t0 = time.time()
    result = run_agentic_pipeline(req.query, app_state["schema_json"], app_state["sample_rows"], req.chat_history)
    dur = int((time.time() - t0) * 1000)
    
    if result.get("error"): return GenerateResponse(error=result["error"], duration_ms=dur)
    
    result_df = result.get("result_df")
    charts_cfg = result.get("charts", [])
    serialized_charts = []
    if result_df is not None and not result_df.empty:
        figs = build_figures(result_df, charts_cfg)
        fig_jsons = serialize_figures(figs)
        for cfg, fig_json in zip(charts_cfg, fig_jsons):
            serialized_charts.append({**cfg, "fig_json": fig_json})
    
    log_query(req.session_id, req.query, result.get("sql"), [], result.get("insights", []), None, dur)
    return GenerateResponse(
        intent=result.get("intent"), sql=result.get("sql"),
        data=dataframe_to_records(result_df.copy()) if result_df is not None else [],
        charts=serialized_charts, insights=result.get("insights", []),
        duration_ms=dur
    )

@app.get("/forecast")
@api_router.get("/forecast")
async def forecast():
    _ensure_dataset_loaded()
    if app_state["df"] is None: raise HTTPException(404, "No dataset.")
    df = app_state["df"]
    d_cols = [c for c in df.columns if any(x in c.lower() for x in ["date", "time"])]
    v_cols = [c for c in df.columns if df[c].dtype in (np.float64, np.int64) and "id" not in c.lower()]
    if not d_cols or not v_cols: return {"status": "unavailable", "data": []}
    
    try:
        temp = df[[d_cols[0], v_cols[0]]].copy()
        temp[d_cols[0]] = pd.to_datetime(temp[d_cols[0]], errors='coerce')
        temp = temp.dropna().sort_values(d_cols[0])
        resm = temp.set_index(d_cols[0])[v_cols[0]].resample('ME').sum().reset_index()
        x = np.arange(len(resm))
        y = resm[v_cols[0]].values
        if len(x) < 2: return {"status": "unavailable", "data": []}
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        f_x = np.arange(len(x), len(x)+6)
        f_y = [max(0, v) for v in p(f_x)]
        f_data = [{"date": str(d.date()), "value": float(v), "type": "actual"} for d, v in zip(resm[d_cols[0]], resm[v_cols[0]])]
        last = resm[d_cols[0]].iloc[-1]
        for i, val in enumerate(f_y):
            f_data.append({"date": str((last + pd.DateOffset(months=i+1)).date()), "value": float(val), "type": "forecast"})
        return {"status": "success", "data": f_data}
    except Exception as e: return {"status": "error", "message": str(e)}

@app.get("/api/distributions")
@api_router.get("/distributions")
async def distributions():
    _ensure_dataset_loaded()
    if app_state["df"] is None: raise HTTPException(404, "No dataset.")
    return compute_distributions(app_state["df"])

@app.get("/api/sample-queries")
@api_router.get("/sample-queries")
async def sample_queries():
    return [{"query": "Top 10 categories", "icon": "📊"}]

@app.post("/presentation")
@api_router.post("/presentation")
async def presentation(req: dict):
    _ensure_dataset_loaded()
    if app_state["df"] is None: raise HTTPException(404, "No dataset.")
    query = req.get("query", "Summarize findings")
    try:
        data = generate_presentation_json(query, app_state["schema_json"], app_state["sample_rows"])
        return data
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/analyze")
@api_router.post("/analyze")
async def analyze(req: dict):
    _ensure_dataset_loaded()
    if app_state["df"] is None: raise HTTPException(404, "No dataset.")
    task = req.get("task", "auto")
    df = app_state["df"]
    
    # Auto-detect if not specified
    if task == "auto":
        detection = detect_task_type(df)
        task = detection["task"]
        target = detection.get("target_col")
    else:
        target = req.get("target")

    try:
        if task == "binary_classification" or task == "multiclass_classification":
            return compute_classification_metrics(df, target)
        elif task == "regression":
            return compute_regression_metrics(df, target)
        elif task == "clustering":
            return compute_clustering(df)
        else:
            return profile_dataset(df)
    except Exception as e:
        raise HTTPException(500, str(e))

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
