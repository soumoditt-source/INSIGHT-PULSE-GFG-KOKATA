"""
InsightPulse AI - Conversational Dashboard Page v5.0
=====================================================================
The core page: NL query -> Agentic SQL -> Live Plotly charts + Insights.
Charts are rendered from Plotly JSON returned by backend.
"""
import streamlit as st
import json
import time
import plotly.graph_objects as go
from ui_utils import api_generate, api_sample_queries


def render():
    st.markdown(
        "<h2 style='margin-bottom:0;'>💬 Conversational Dashboard</h2>",
        unsafe_allow_html=True
    )
    st.caption("Ask any business question. Get instant AI-powered charts and insights.")

    # ── Guard: require backend to be online with data
    if not st.session_state.get("df_loaded", False):
        st.info(
            "📂 **No dataset loaded yet.**\n\n"
            "Upload a CSV or Excel file in the sidebar, or wait for the default "
            "Amazon Sales dataset to load automatically."
        )
        return

    # ── Sample queries expander
    with st.expander("💡 Example Queries - click to try", expanded=False):
        samples = api_sample_queries()
        if samples:
            cols = st.columns(2)
            for i, sq in enumerate(samples[:8]):
                with cols[i % 2]:
                    label = f"{sq.get('icon','📊')} {sq['query']}"
                    if st.button(label, key=f"sq_{i}", use_container_width=True):
                        st.session_state.current_prompt = sq["query"]
                        st.rerun()

    st.divider()

    # ── Chat history replay
    for i, msg in enumerate(st.session_state.get("chat_history", [])):
        role = msg.get("role", "user")
        with st.chat_message(role, avatar="👤" if role == "user" else "[ENGINE]"):
            if role == "user":
                st.markdown(f"**{msg['content']}**")
            else:
                content = msg.get("content", {})
                if isinstance(content, dict):
                    _render_ai_response(content, is_history=True, prompt="")
                else:
                    st.markdown(str(content))

    # ── Chat input
    prompt = st.chat_input("Ask about your data...  e.g. 'Top 10 categories by revenue'")

    # Handle sample query click
    pending = st.session_state.get("current_prompt")
    if pending:
        prompt = pending
        st.session_state.current_prompt = None

    if prompt:
        # Store and display user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**{prompt}**")

        with st.chat_message("ai", avatar="[ENGINE]"):
            with st.spinner("🧠 Analyzing your question..."):
                res = api_generate(
                    prompt,
                    st.session_state.get("session_id", "default"),
                    st.session_state.get("chat_history", [])
                )

            if res.get("error"):
                st.error(f"[X] {res['error']}")
                if res.get("followup_suggestions"):
                    st.markdown("**💡 Try instead:**")
                    for sug in res["followup_suggestions"]:
                        if st.button(f"-> {sug}", key=f"sug_{hash(sug)}"):
                            st.session_state.current_prompt = sug
                            st.rerun()
                st.session_state.chat_history.append({"role": "ai", "content": res})
            else:
                _render_ai_response(res, is_history=False, prompt=prompt)
                st.session_state.chat_history.append({"role": "ai", "content": res})


def _render_ai_response(res: dict, is_history: bool, prompt: str = ""):
    """Render a full AI response: timing, insights, charts, SQL, follow-ups."""
    if res.get("error"):
        st.error(res["error"])
        return

    # ── Timing + row count
    dur = res.get("duration_ms", 0) / 1000.0
    row_count = res.get("row_count", 0)
    agent_meta = res.get("agent_metadata", {})
    retries = agent_meta.get("retries", 0)

    cols = st.columns([2, 2, 2, 4])
    cols[0].metric("[TIME] Time", f"{dur:.2f}s")
    cols[1].metric("📊 Rows", f"{row_count:,}")
    cols[2].metric("🔁 Retries", retries)
    if res.get("intent"):
        cols[3].markdown(
            f"<span class='badge-ok'>{res['intent'].upper()}</span>",
            unsafe_allow_html=True
        )

    # ── AI Insights
    insights = res.get("insights", [])
    if insights:
        st.markdown("**💡 AI Insights**")
        for ins in insights:
            st.markdown(f"<div class='insight-row'>💡 {ins}</div>", unsafe_allow_html=True)

    # ── Charts - CRITICAL FIX: parse fig_json string -> go.Figure
    charts = res.get("charts", [])
    if charts:
        # Render multi-chart grid (2 columns if > 1 chart)
        n = len(charts)
        if n == 1:
            _render_single_chart(charts[0], idx=0)
        else:
            chart_cols = st.columns(min(n, 2))
            for i, chart_cfg in enumerate(charts[:4]):
                with chart_cols[i % 2]:
                    _render_single_chart(chart_cfg, idx=i)
    elif not res.get("error"):
        st.info("No charts generated - try asking for a specific visualization.")

    # ── SQL + data expander
    with st.expander("🔍 View SQL & Raw Data", expanded=False):
        sql = res.get("sql", "")
        if sql:
            st.markdown(f"<div class='sql-box'>{sql}</div>", unsafe_allow_html=True)
        data = res.get("data", [])
        if data:
            import pandas as pd
            df = pd.DataFrame(data)
            st.dataframe(df.head(50), use_container_width=True)

    # ── Follow-up suggestions
    followups = res.get("followup_suggestions", [])
    if followups and not is_history:
        st.markdown("**🔄 Follow-up questions:**")
        fcols = st.columns(len(followups[:3]))
        for i, sug in enumerate(followups[:3]):
            with fcols[i]:
                if st.button(f"-> {sug}", key=f"fu_{i}_{time.time_ns()}", use_container_width=True):
                    st.session_state.current_prompt = sug
                    st.rerun()

    # ── Star button
    if not is_history and res.get("sql"):
        if st.button("[STAR] Save Dashboard", key=f"star_{time.time_ns()}"):
            try:
                from crm.crm_db import star_dashboard
                star_dashboard(
                    st.session_state.get("session_id", "default"),
                    f"Dashboard: {prompt[:40]}",
                    prompt,
                    res.get("sql", ""),
                    [{k: v for k, v in c.items() if k != "fig_json"} for c in charts],
                    insights
                )
                st.toast("[OK] Dashboard saved to Starred!")
            except Exception as e:
                st.toast(f"Could not save: {e}")


def _render_single_chart(chart_cfg: dict, idx: int):
    """Render one chart from its serialized Plotly JSON string."""
    fig_json = chart_cfg.get("fig_json")
    title = chart_cfg.get("title", f"Chart {idx + 1}")

    if not fig_json:
        st.warning(f"[WARN]️ No chart data for: {title}")
        return

    try:
        # CRITICAL FIX: fig_json is a JSON string from fig.to_json()
        # Parse it back into a go.Figure
        if isinstance(fig_json, str):
            fig_dict = json.loads(fig_json)
        else:
            fig_dict = fig_json   # already a dict (fallback)

        fig = go.Figure(fig_dict)
        st.plotly_chart(
            fig,
            use_container_width=True,
            key=f"chart_{idx}_{time.time_ns()}"
        )
    except Exception as e:
        st.error(f"Chart render error ({title}): {e}")
