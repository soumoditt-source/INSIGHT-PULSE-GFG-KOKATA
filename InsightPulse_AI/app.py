"""
InsightPulse AI - FINAL STABLE ENTRY POINT v5.0
=====================================================================
Run: python run.py   (starts backend + frontend together)
  or: streamlit run app.py   (frontend only, backend must be running)
"""
import streamlit as st
import sys
import os
from pathlib import Path

# ── Path setup
PROJECT_ROOT = Path(__file__).parent.absolute()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ── Load env
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

from ui_utils import inject_css, FLOATING_CHATBOT_HTML, api_health, api_upload

# ────────────────────────────────────────────────────────────────────
# Page config - must be FIRST Streamlit call
# ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InsightPulse AI",
    page_icon="[ENGINE]",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()

# ────────────────────────────────────────────────────────────────────
# Session state initialization - FIXED: initialize ALL required keys
# ────────────────────────────────────────────────────────────────────
_defaults = {
    "page":           "Home",
    "theme":          "dark",
    "session_id":     "SHINOBI_USER",
    "chat_history":   [],          # ← CRITICAL FIX: was missing, crashed Chat page
    "df_loaded":      False,       # ← CRITICAL FIX: was missing, blocked all pages
    "dataset_name":   "",
    "current_prompt": None,
}
for key, val in _defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ────────────────────────────────────────────────────────────────────
# Sidebar - Navigation + Dataset Upload + Status
# ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 class='gradient-text'>[ENGINE] InsightPulse</h2>", unsafe_allow_html=True)
    st.caption("Conversational BI · Powered by Gemini 2.0")
    st.divider()

    # ── Navigation
    pages = {
        "🏠 Home":        "Home",
        "💬 Data Chat":   "Chat",
        "🔬 ML Lab":      "ML",
        "📊 Profiler":    "Data",
        "🗺️ Map View":   "Map",
        "📋 History":     "History",
        "[STAR] Starred":     "Starred",
        "❓ FAQ":         "FAQ",
    }
    for label, pg in pages.items():
        btn_type = "primary" if st.session_state.page == pg else "secondary"
        if st.button(label, key=f"nav_{pg}", use_container_width=True, type=btn_type):
            st.session_state.page = pg
            st.rerun()

    st.divider()

    # ── Dataset Upload widget (CRITICAL FIX: was missing entirely)
    st.markdown("**📂 Upload Dataset**")
    uploaded = st.file_uploader(
        "CSV or Excel",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed",
        key="file_uploader"
    )
    if uploaded is not None:
        with st.spinner("📊 Loading dataset..."):
            result = api_upload(uploaded)
        if result.get("status") == "success":
            st.session_state.df_loaded = True     # ← CRITICAL FIX
            st.session_state.dataset_name = result.get("filename", "")
            st.session_state.chat_history = []    # reset history on new upload
            st.success(f"[OK] {result.get('rows', 0):,} rows loaded!")
            st.caption(f"Quality: {result.get('data_quality', {}).get('grade', 'N/A')}")
        else:
            st.error(f"[X] {result.get('message', 'Upload failed.')}")

    # ── Backend health status
    st.divider()
    healthy, hdata = api_health()
    if healthy:
        rows = hdata.get("rows", 0)
        dname = hdata.get("dataset_name", "")
        if not st.session_state.df_loaded and rows > 0:
            # Backend has auto-loaded the default dataset - sync session state
            st.session_state.df_loaded = True
            st.session_state.dataset_name = dname
        col1, col2 = st.columns(2)
        col1.markdown("<span class='badge-ok'>● ONLINE</span>", unsafe_allow_html=True)
        if rows > 0:
            st.caption(f"📊 {dname[:28]}")
            st.caption(f"🗂 {rows:,} rows")
    else:
        st.markdown("<span class='badge-err'>● OFFLINE</span>", unsafe_allow_html=True)
        st.caption("Start backend: `python run.py`")

    st.divider()
    st.markdown(
        "<p style='font-size:0.72rem;color:#475569;text-align:center;'>"
        "Team Full Stack Shinobi<br>GFG × JISCE Kolkata 2026</p>",
        unsafe_allow_html=True
    )

# ────────────────────────────────────────────────────────────────────
# Page Router
# ────────────────────────────────────────────────────────────────────
target = st.session_state.page
try:
    if target == "Home":
        import pages.home as p;         p.render()
    elif target == "Chat":
        import pages.chat as p;         p.render()
    elif target == "ML":
        import pages.ml_lab as p;       p.render()
    elif target == "Data":
        import pages.data_explorer as p; p.render()
    elif target == "Map":
        import pages.map_view as p;     p.render()
    elif target == "History":
        import pages.history as p;      p.render()
    elif target == "Starred":
        import pages.starred as p;      p.render()
    elif target == "FAQ":
        import pages.faq_page as p;     p.render()
except Exception as e:
    st.error(f"[X] Error loading **{target}** page: `{e}`")
    st.exception(e)

# ── Floating AI chatbot bubble (Puter.js powered)
st.components.v1.html(FLOATING_CHATBOT_HTML, height=0)
