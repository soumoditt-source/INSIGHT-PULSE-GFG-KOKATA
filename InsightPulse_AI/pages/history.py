import streamlit as st
import json

def render():
    st.markdown("<h2 style='margin-bottom:0;'>📋 Query History Audit</h2>", unsafe_allow_html=True)
    st.caption("Your complete session history and execution logs.")

    from crm.crm_db import get_history
    try:
        hist = get_history(st.session_state.session_id)
        if not hist:
            st.info("No query history found. Start a conversation in the Chat Dashboard!")
            return

        for row in hist:
            # Keys: session_id, timestamp, user_query, generated_sql, chart_types, insights, error, duration_ms
            query = row.get('user_query', 'Unknown')
            sql = row.get('generated_sql')
            insights = row.get('insights', [])
            err = row.get('error')
            dur = row.get('duration_ms', 0)
            ts = row.get('timestamp', '')

            with st.expander(f"{ts} - 🗣️ {query[:60]}..."):
                col1, col2 = st.columns(2)
                col1.metric("Execution Time", f"{dur/1000.0:.2f}s")
                col2.metric("Status", "[OK] Success" if not err else "[X] Failed")
                
                if err:
                    st.error(f"Error: {err}")
                if sql:
                    st.markdown("**Generated SQL:**")
                    st.code(sql, language="sql")
                if insights:
                    st.markdown("**AI Insights:**")
                    for ins in insights:
                        st.markdown(f"- {ins}")
    except Exception as e:
        st.error(f"History Engine Error: {e}")
