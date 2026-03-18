"""
InsightPulse AI - Home Page v5.0
Bento grid hero + feature showcase + quick query launcher.
"""
import streamlit as st


def render():
    # Inline CSS for bento grid + metric pills (supplement global CSS)
    st.markdown("""
<style>
.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
  margin-top: 1.5rem;
}
.bento-item {
  background: rgba(19,19,46,0.7);
  border: 1px solid rgba(99,102,241,0.12);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  position: relative;
  overflow: hidden;
}
.bento-item::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(99,102,241,0.03), transparent);
  pointer-events: none;
}
.bento-item:hover {
  transform: translateY(-5px) scale(1.01);
  border-color: rgba(99,102,241,0.4);
  box-shadow: 0 12px 40px rgba(0,0,0,0.35), 0 0 30px rgba(99,102,241,0.15);
}
.bento-col-2 { grid-column: span 2; }
.bento-col-3 { grid-column: span 3; }
.bento-em    { font-size: 2.5rem; margin-bottom: 0.8rem; display: block; }

.metric-pill {
  display: inline-block;
  padding: 4px 11px;
  border-radius: 20px;
  background: rgba(99,102,241,0.1);
  border: 1px solid rgba(99,102,241,0.22);
  color: #A5B4FC !important;
  font-size: 0.76rem;
  font-weight: 600;
  margin: 3px 3px;
  letter-spacing: 0.2px;
}

@media (max-width: 1024px) {
  .bento-grid { grid-template-columns: repeat(2, 1fr); }
  .bento-col-2, .bento-col-3 { grid-column: span 2; }
}
@media (max-width: 640px) {
  .bento-grid { grid-template-columns: 1fr; }
  .bento-col-2, .bento-col-3 { grid-column: span 1; }
}
</style>
""", unsafe_allow_html=True)

    # ── Hero Section
    st.markdown("""
<div style="text-align:center; padding: 2rem 0 1.5rem;">
  <div style="display:inline-block; padding:4px 14px; border-radius:30px;
              background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.2);
              color:#818CF8; font-weight:700; font-size:0.82rem; margin-bottom:1rem;
              letter-spacing:1.5px; text-transform:uppercase;">
    ✨ Conversational BI Engine · Gemini 2.0 Flash · DuckDB
  </div>
  <h1 style="font-size:3.2rem; font-weight:900; margin-bottom:0.5rem; letter-spacing:-2px;
             line-height:1.1;">
    Talk to your
    <span class="gradient-text"> Data.</span>
  </h1>
  <p style="font-size:1.15rem; color:#94A3B8; max-width:620px; margin:0.8rem auto 0;
            line-height:1.65;">
    Upload any dataset. Ask questions in plain English. Get instant multi-chart
    dashboards, zero-hallucination insights, and ML-powered analysis - all in seconds.
  </p>
</div>
""", unsafe_allow_html=True)

    # Dataset status banner
    if st.session_state.get("df_loaded"):
        dname = st.session_state.get("dataset_name", "Dataset")
        st.markdown(
            f"<div style='text-align:center; margin-bottom:1rem;'>"
            f"<span class='badge-ok'>✓ {dname} loaded - start asking!</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("👈 Upload a CSV/Excel file in the sidebar to begin, or the default Amazon Sales dataset will load automatically.")

    # ── Bento Feature Grid
    st.markdown("""
<div class="bento-grid">

  <div class="bento-item bento-col-2"
       style="background:linear-gradient(135deg,rgba(30,27,75,0.5),rgba(15,23,42,0.4));">
    <span class="bento-em">💬</span>
    <h3 style="margin:0 0 0.5rem; font-size:1.45rem;">Conversational Dashboard</h3>
    <p style="color:#94A3B8; margin:0; font-size:0.92rem; line-height:1.6;">
      Ask: <em>"Top 10 categories by revenue"</em> -> Get fully interactive Plotly charts,
      AI-generated insights, and the raw SQL - all in one shot.
      Powered by an <strong>agentic self-correcting loop</strong> (up to 3 auto-retries on SQL errors).
    </p>
  </div>

  <div class="bento-item">
    <span class="bento-em">🔬</span>
    <h3 style="margin:0 0 0.5rem; font-size:1.15rem;">ML Lab</h3>
    <p style="color:#94A3B8; margin:0; font-size:0.87rem;">
      Auto-detect: Classification, Regression, or Clustering.
      Get AUC-ROC, F1, R², RMSE, Silhouette scores, and feature importance.
    </p>
  </div>

  <div class="bento-item">
    <span class="bento-em">📊</span>
    <h3 style="margin:0 0 0.5rem; font-size:1.15rem;">Data Profiler</h3>
    <p style="color:#94A3B8; margin:0; font-size:0.87rem;">
      Missing value maps, distribution histograms, correlation matrices,
      outlier detection, and an A-F data quality grade.
    </p>
  </div>

  <div class="bento-item">
    <span class="bento-em">🗺️</span>
    <h3 style="margin:0 0 0.5rem; font-size:1.15rem;">Geo Map View</h3>
    <p style="color:#94A3B8; margin:0; font-size:0.87rem;">
      Auto-detects lat/lon or city/state/country columns and renders
      interactive satellite maps.
    </p>
  </div>

  <div class="bento-item">
    <span class="bento-em">📋</span>
    <h3 style="margin:0 0 0.5rem; font-size:1.15rem;">Enterprise CRM</h3>
    <p style="color:#94A3B8; margin:0; font-size:0.87rem;">
      Full query audit trail, execution logs, starred dashboards,
      and session analytics saved to SQLite.
    </p>
  </div>

  <div class="bento-item bento-col-2"
       style="background:linear-gradient(135deg,rgba(99,102,241,0.05),rgba(236,72,153,0.04));">
    <span class="bento-em">🚀</span>
    <h3 style="margin:0 0 0.8rem; font-size:1.45rem;">Powered by 30+ Features</h3>
    <div style="display:flex; flex-wrap:wrap; gap:0; margin-top:0.25rem;">
      <span class="metric-pill">Gemini 2.0 Flash</span>
      <span class="metric-pill">Agentic SQL Loop</span>
      <span class="metric-pill">DuckDB In-Memory</span>
      <span class="metric-pill">RAG Schema Engine</span>
      <span class="metric-pill">Puter.js AI Chat</span>
      <span class="metric-pill">Multi-Chart Plotly</span>
      <span class="metric-pill">scikit-learn ML</span>
      <span class="metric-pill">Any CSV/Excel Upload</span>
      <span class="metric-pill">Zero Hallucinations</span>
      <span class="metric-pill">Dark/Light Mode</span>
      <span class="metric-pill">CRM SQLite</span>
      <span class="metric-pill">Auto Self-Correction</span>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown(
        "<p style='text-align:center; color:#475569; font-size:0.78rem;'>"
        "InsightPulse AI v5.0 · GFG × JISCE Kolkata Hackathon 2026 · "
        "Team Full Stack Shinobi 🥷</p>",
        unsafe_allow_html=True
    )
