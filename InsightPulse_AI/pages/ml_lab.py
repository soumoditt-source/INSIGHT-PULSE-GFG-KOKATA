import streamlit as st
import pandas as pd
from ui_utils import api_analyze, api_health, api_profile

def render():
    st.markdown("<h2 style='margin-bottom:0;'>🔬 ML Analysis Lab</h2>", unsafe_allow_html=True)
    st.caption("100% Accurate Machine Learning Metrics: Classification, Regression, Clustering.")
    
    healthy, _ = api_health()
    if not healthy:
        st.warning("[WARN]️ Please upload a dataset to run ML Analysis.")
        return

    st.markdown("""
<div class='card' style='margin-bottom:1.5rem;'>
  <b>Welcome to the ML Lab.</b> Select a target column to predict. 
  The engine auto-detects <b>RandomForest</b> tasks or <b>K-Means</b> clustering.
</div>
""", unsafe_allow_html=True)

    profile = api_profile()
    if not profile:
        st.error("Could not fetch data profile.")
        return

    all_cols_raw = list(profile.get("dtypes", {}).keys())
    num_cols = [s["column"] for s in profile.get("numeric_stats", [])]
    cat_cols = [c for c in all_cols_raw if c not in num_cols]
    all_cols = ["-- Auto Detect (Clustering) --"] + cat_cols + num_cols

    col1, col2 = st.columns([1, 1])
    target = col1.selectbox("🎯 Target Column", all_cols)
    task_override = col2.selectbox("⚙️ Task Type", ["auto", "classification", "regression", "clustering"])

    if st.button("🚀 Analyze Now", use_container_width=True, type="primary"):
        with st.spinner("🤖 Training ML models..."):
            payload = {}
            if task_override != "auto": payload["task"] = task_override
            if target != "-- Auto Detect (Clustering) --": payload["target_col"] = target
            res = api_analyze(payload)
            
        if "error" in res:
            st.error(f"[X] Analysis failed: {res['error']}")
            return
            
        st.success(f"[OK] Training Complete: **{res.get('task','').upper()}**")
        
        metrics = res.get("metrics", {})
        if res.get("task") == "classification":
            c1, c2, c3 = st.columns(3)
            c1.metric("Accuracy", f"{metrics.get('accuracy',0)*100:.1f}%")
            c2.metric("F1 Score", f"{metrics.get('f1_score',0):.3f}")
            c3.metric("Precision", f"{metrics.get('precision',0):.3f}")
        elif res.get("task") == "regression":
            c1, c2, c3 = st.columns(3)
            c1.metric("R² Score", f"{metrics.get('r2_score',0):.3f}")
            c2.metric("RMSE", f"{metrics.get('rmse',0):.2f}")
            c3.metric("MAE", f"{metrics.get('mae',0):.2f}")
        elif res.get("task") == "clustering":
            st.metric("Optimal Clusters", res.get("optimal_k", 0))
            st.metric("Silhouette Score", f"{res.get('silhouette_score',0):.3f}")

        fi = res.get("feature_importance", [])
        if fi:
            st.markdown("#### 🌟 Top Predictors")
            fi_df = pd.DataFrame(fi)
            st.bar_chart(fi_df.set_index("feature")["importance"])
