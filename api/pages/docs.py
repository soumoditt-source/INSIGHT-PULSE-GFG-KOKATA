import streamlit as st
from ui_utils import BACKEND

def render():
    st.markdown("<h2 style='margin-bottom:0;'>📖 API Documentation & Swagger</h2>", unsafe_allow_html=True)
    st.caption("InsightPulse AI exposes a full REST API built on FastAPI.")

    st.markdown(f"""
    ### 🌐 Interactive API Docs
    The FastAPI Swagger UI is running at:
    [**{BACKEND}/docs**]({BACKEND}/docs)
    
    ### 🔌 Core API Endpoints
    * `POST /generate` - Text-to-SQL + Chart pipeline.
    * `POST /analyze` - Auto-ML Engine.
    * `POST /upload` - CSV ingestion.
    * `GET /profile` - Data profiling.
    * `GET /health` - System status.
    """)
    st.info("Floating AI assistant uses Puter.js for free LLM access.")
