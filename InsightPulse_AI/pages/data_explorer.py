import streamlit as st
import pandas as pd
from ui_utils import api_profile, api_distributions, api_health

def render():
    st.markdown("<h2 style='margin-bottom:0;'>📊 Data Explorer & Profiler</h2>", unsafe_allow_html=True)
    st.caption("Deep statistical analysis, missing values, and data quality grading.")

    healthy, _ = api_health()
    if not healthy:
        st.warning("[WARN]️ Please upload a dataset to run Data Profiling.")
        return

    with st.spinner("🔍 Profiling dataset..."):
        profile = api_profile()
        dists = api_distributions()

    if not profile:
        st.error("Failed to load profile. Backend might be down.")
        return

    # High level stats
    st.markdown("### 🏆 Quality Score")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{profile['shape']['rows']:,}")
    c2.metric("Columns", f"{profile['shape']['columns']}")
    c3.metric("Data Quality", f"{profile['data_quality_score']['score']}%")
    c4.metric("Grade", profile["data_quality_score"]["grade"])

    st.progress(profile["data_quality_score"]["score"] / 100)
    st.divider()

    # Missing Values
    st.markdown("### [WARN]️ Missing Values")
    miss = profile.get("missing_values", [])
    if not miss:
        st.success("Clean dataset! Zero missing values.")
    else:
        st.table(pd.DataFrame(miss))

    st.divider()

    # Numeric Distributions
    st.markdown("### 📈 Numeric Feature Distributions")
    num_stats = profile.get("numeric_stats", [])
    if num_stats:
        import plotly.graph_objects as go
        for stat in num_stats:
            col_name = stat["column"]
            with st.expander(f"📊 {col_name} (Outliers: {stat['outlier_count']})"):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Min", stat["min"])
                c2.metric("Max", stat["max"])
                c3.metric("Mean", stat["mean"])
                c4.metric("Skewness", stat["skewness"])
                
                if col_name in dists:
                    x = dists[col_name]["bin_edges"][:-1]
                    y = dists[col_name]["counts"]
                    fig = go.Figure(data=go.Bar(x=x, y=y, marker_color="#6366F1"))
                    fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("### 🔗 Top Correlations")
    corrs = profile.get("top_correlations", [])
    if corrs:
        st.table(pd.DataFrame(corrs))
    else:
        st.info("Not enough numeric columns for correlation analysis.")
