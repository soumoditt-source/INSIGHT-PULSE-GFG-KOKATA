import streamlit as st
import json
import plotly.graph_objects as go

def render():
    st.markdown("<h2 style='margin-bottom:0;'>[STAR] Starred Dashboards</h2>", unsafe_allow_html=True)
    st.caption("Access your saved interactive visualizations.")

    from crm.crm_db import get_starred
    try:
        stars = get_starred(st.session_state.session_id)
        if not stars:
            st.info("No starred dashboards yet. Click '[STAR] Star' in the Chat Dashboard to save results.")
            return

        for i, row in enumerate(stars):
            # Keys: session_id, title, user_query, generated_sql, chart_configs, insights, starred_at, notes
            title = row.get('title', 'Saved Dashboard')
            query = row.get('user_query', '')
            charts = row.get('chart_configs', [])
            insights = row.get('insights', [])
            ts = row.get('starred_at', '')

            with st.container():
                st.markdown(f"### {title}")
                st.caption(f"Original Query: *{query}* | Saved on: {ts}")
                
                if charts:
                    for j, c in enumerate(charts):
                        try:
                            fig = go.Figure(c.get("fig_json", {}))
                            st.plotly_chart(fig, use_container_width=True, key=f"star_cht_{i}_{j}")
                        except: pass
                
                if insights:
                    for ins in insights:
                        st.markdown(f"💡 {ins}")
                st.divider()
    except Exception as e:
        st.error(f"Starred Engine Error: {e}")
        st.info("Check if plotly and data structures are consistent.")
