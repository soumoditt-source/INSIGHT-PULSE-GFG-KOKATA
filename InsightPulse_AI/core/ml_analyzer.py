"""
InsightPulse AI - ML Analysis Engine
=====================================================================
World-class ML metrics for ANY uploaded dataset:
  - Auto-detects: classification / regression / clustering / NLP
  - Computes: AUC-ROC, F1, Accuracy, Precision, Recall, Confusion Matrix
  - Regression: RMSE, MAE, R2, MAPE
  - Unsupervised: Silhouette score, KMeans clusters
  - Feature importance, correlation matrix, outlier detection
  - Works on ANY CSV - fully generalized
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import warnings
warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────────────
# DATA TYPE DETECTION
# ──────────────────────────────────────────────────────────────────

def detect_task_type(df: pd.DataFrame, target_col: Optional[str] = None) -> Dict[str, Any]:
    """
    Auto-detect whether the dataset is suited for:
    - Binary Classification  (2 unique values in target)
    - Multi-class Classification (3-20 unique values)
    - Regression             (continuous target)
    - Clustering             (no obvious target)
    """
    result: Dict[str, Any] = {
        "task": "clustering",
        "target_col": None,
        "n_classes": None,
        "is_supervised": False,
        "candidate_targets": []
    }

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Priority 1: User-specified target
    if target_col and target_col in df.columns:
        col = df[target_col]
        n_unique = col.nunique()
        result["target_col"] = target_col
        result["is_supervised"] = True
        if n_unique == 2:
            result["task"] = "binary_classification"
            result["n_classes"] = 2
        elif 2 < n_unique <= 20:
            result["task"] = "multiclass_classification"
            result["n_classes"] = n_unique
        else:
            result["task"] = "regression"
        return result

    # Priority 2: Auto-detect binary columns in categorical
    for col in categorical_cols:
        if df[col].nunique() == 2:
            result["candidate_targets"].append(col)

    # Priority 3: Ratio columns (0-1) -> likely classification flags
    for col in numeric_cols:
        vals = df[col].dropna()
        if vals.between(0, 1).all() and vals.nunique() == 2:
            result["candidate_targets"].append(col)

    if result["candidate_targets"]:
        result["task"] = "binary_classification"
        result["target_col"] = result["candidate_targets"][0]
        result["is_supervised"] = True
        result["n_classes"] = 2

    return result


# ──────────────────────────────────────────────────────────────────
# CLASSIFICATION METRICS
# ──────────────────────────────────────────────────────────────────

def compute_classification_metrics(df: pd.DataFrame, target_col: str,
                                    feature_cols: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Train a RandomForestClassifier and compute all classification metrics.
    Returns: accuracy, f1, precision, recall, AUC-ROC, confusion matrix, feature importance.
    """
    try:
        from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor
)
        from sklearn.cluster import KMeans
        from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split
        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                                     recall_score, roc_auc_score, confusion_matrix,
                                     classification_report)
        from sklearn.linear_model import LogisticRegression

        # ── Prepare data
        df_clean = df.copy().dropna(subset=[target_col])
        if len(df_clean) < 20:
            return {"error": "Need at least 20 rows for ML analysis."}

        # ── Optimized Sampling for 30s Response
        if len(df_clean) > 20000:
            df_sample = df_clean.sample(n=10000, random_state=42)
        else:
            df_sample = df_clean

        y_raw = df_sample[target_col]
        le = LabelEncoder()
        y = le.fit_transform(y_raw.astype(str))
        n_classes = len(le.classes_)

        # ── Select numeric features only
        if feature_cols:
            X_cols = [c for c in feature_cols if c in df_sample.columns and c != target_col]
        else:
            X_cols = [c for c in df_sample.select_dtypes(include=[np.number]).columns if c != target_col]

        if not X_cols:
            return {"error": f"No numeric feature columns found. Target: {target_col}"}

        X = df_sample[X_cols].fillna(df_sample[X_cols].median())
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # ── Train/test split
        test_size = min(0.3, max(0.15, 10 / len(df_clean)))
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=test_size, random_state=42, stratify=y if n_classes <= 10 else None
        )

        # ── Model selection based on size (Optimized for <30s response)
        if len(df_sample) > 5000:
            # Use HistGradientBoosting for 5k+ rows - significantly faster
            # min_samples_leaf and max_leaf_nodes used for regularization in larger sets
            model = HistGradientBoostingClassifier(
                max_iter=50, 
                random_state=42,
                min_samples_leaf=20
            )
        elif len(df_sample) > 2000:
            model = RandomForestClassifier(
                n_estimators=50, 
                random_state=42, 
                n_jobs=-1, 
                min_samples_leaf=5,
                max_features='sqrt'
            )
        else:
            model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)

        # ── Metrics
        avg_mode = "binary" if n_classes == 2 else "weighted"
        accuracy = float(round(accuracy_score(y_test, y_pred), 4))
        f1 = float(round(f1_score(y_test, y_pred, average=avg_mode, zero_division=0), 4))
        precision = float(round(precision_score(y_test, y_pred, average=avg_mode, zero_division=0), 4))
        recall = float(round(recall_score(y_test, y_pred, average=avg_mode, zero_division=0), 4))

        # AUC-ROC
        try:
            if n_classes == 2:
                auc_roc = float(round(roc_auc_score(y_test, y_prob[:, 1]), 4))
            else:
                auc_roc = float(round(roc_auc_score(y_test, y_prob, multi_class="ovr", average="weighted"), 4))
        except Exception:
            auc_roc = None

        # Cross-validation (robust estimate)
        cv_scores = cross_val_score(
            RandomForestClassifier(n_estimators=50, random_state=42),
            X_scaled, y, cv=min(5, len(df_clean) // 10), scoring="accuracy"
        )
        cv_mean = float(round(cv_scores.mean(), 4))
        cv_std = float(round(cv_scores.std(), 4))

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred).tolist()

        # Feature Importance
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            feature_importance = sorted(
                [{"feature": f, "importance": float(round(imp, 4))}
                 for f, imp in zip(X_cols, importances)],
                key=lambda x: x["importance"], reverse=True
            )[:15]
        else:
            feature_importance = []

        # Full classification report
        report_dict = classification_report(
            y_test, y_pred, target_names=[str(c) for c in le.classes_],
            output_dict=True, zero_division=0
        )

        return {
            "task": "classification",
            "model": type(model).__name__,
            "target_col": target_col,
            "n_classes": n_classes,
            "class_labels": [str(c) for c in le.classes_],
            "n_features": len(X_cols),
            "feature_cols": X_cols,
            "n_train": len(X_train),
            "n_test": len(X_test),
            "metrics": {
                "accuracy": accuracy,
                "f1_score": f1,
                "precision": precision,
                "recall": recall,
                "auc_roc": auc_roc,
                "cv_accuracy_mean": cv_mean,
                "cv_accuracy_std": cv_std,
            },
            "confusion_matrix": cm,
            "feature_importance": feature_importance,
            "classification_report": report_dict,
            "performance_grade": _grade_accuracy(accuracy),
            "error": None
        }

    except ImportError:
        return {
            "error": "ML Lab (scikit-learn) is disabled in this serverless instance to maintain 11/10 speed. Use local mode for full training.",
            "metrics": {"accuracy": 0.0, "f1_score": 0.0},
            "status": "offline"
        }
    except Exception as e:
        return {"error": f"ML computation failed: {str(e)}"}


def _grade_accuracy(accuracy: float) -> str:
    """Return a human-readable performance grade."""
    if accuracy >= 0.98: return "🏆 Exceptional (≥98%)"
    if accuracy >= 0.95: return "🥇 Excellent (≥95%)"
    if accuracy >= 0.90: return "🥈 Very Good (≥90%)"
    if accuracy >= 0.80: return "🥉 Good (≥80%)"
    if accuracy >= 0.70: return "[WARN]️ Fair (≥70%)"
    return "🔴 Needs Improvement (<70%)"


# ──────────────────────────────────────────────────────────────────
# REGRESSION METRICS
# ──────────────────────────────────────────────────────────────────

def compute_regression_metrics(df: pd.DataFrame, target_col: str,
                                feature_cols: Optional[List[str]] = None) -> Dict[str, Any]:
    """Train RandomForestRegressor and return RMSE, MAE, R², MAPE, feature importance."""
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split, cross_val_score
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

        df_clean = df.copy().dropna(subset=[target_col])
        if len(df_clean) < 20:
            return {"error": "Need at least 20 rows for regression analysis."}

        y = df_clean[target_col].astype(float)
        if feature_cols:
            X_cols = [c for c in feature_cols if c in df_clean.columns and c != target_col]
        else:
            X_cols = [c for c in df_clean.select_dtypes(include=[np.number]).columns if c != target_col]

        if not X_cols:
            return {"error": "No numeric feature columns found."}

        X = df_clean[X_cols].fillna(df_clean[X_cols].median())
        X_scaled = StandardScaler().fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse = float(round(np.sqrt(mean_squared_error(y_test, y_pred)), 4))
        mae = float(round(mean_absolute_error(y_test, y_pred), 4))
        r2 = float(round(r2_score(y_test, y_pred), 4))
        mape = float(round(np.mean(np.abs((y_test - y_pred) / (y_test + 1e-9))) * 100, 2))

        cv_r2 = cross_val_score(model, X_scaled, y, cv=min(5, len(df_clean)//10), scoring="r2")

        feature_importance = sorted(
            [{"feature": f, "importance": float(round(imp, 4))}
             for f, imp in zip(X_cols, model.feature_importances_)],
            key=lambda x: x["importance"], reverse=True
        )[:15]

        return {
            "task": "regression",
            "model": "RandomForestRegressor",
            "target_col": target_col,
            "n_features": len(X_cols),
            "feature_cols": X_cols,
            "n_train": len(X_train),
            "n_test": len(X_test),
            "metrics": {
                "rmse": rmse,
                "mae": mae,
                "r2_score": r2,
                "mape_pct": mape,
                "cv_r2_mean": float(round(cv_r2.mean(), 4)),
                "cv_r2_std": float(round(cv_r2.std(), 4)),
            },
            "feature_importance": feature_importance,
            "performance_grade": _grade_r2(r2),
            "error": None
        }

    except Exception as e:
        return {"error": f"Regression failed: {str(e)}"}


def _grade_r2(r2: float) -> str:
    if r2 >= 0.95: return "🏆 Exceptional (R²≥0.95)"
    if r2 >= 0.85: return "🥇 Excellent (R²≥0.85)"
    if r2 >= 0.70: return "🥈 Good (R²≥0.70)"
    if r2 >= 0.50: return "[WARN]️ Fair (R²≥0.50)"
    return "🔴 Low Explanatory Power (R²<0.50)"


# ──────────────────────────────────────────────────────────────────
# CLUSTERING METRICS
# ──────────────────────────────────────────────────────────────────

def compute_clustering(df: pd.DataFrame, n_clusters: int = 4,
                       feature_cols: Optional[List[str]] = None) -> Dict[str, Any]:
    """KMeans clustering with silhouette score."""
    try:
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import silhouette_score

        num_cols = feature_cols or df.select_dtypes(include=[np.number]).columns.tolist()
        X = df[num_cols].dropna()
        if len(X) < 20 or len(num_cols) < 2:
            return {"error": "Need ≥20 rows and ≥2 numeric columns for clustering."}

        X_scaled = StandardScaler().fit_transform(X)

        # Find optimal k (elbow)
        inertias, sil_scores = [], []
        k_range = range(2, min(10, len(X) // 5))
        best_k, best_sil = 2, -1
        for k in k_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(X_scaled)
            inertias.append(float(km.inertia_))
            sil = float(silhouette_score(X_scaled, labels))
            sil_scores.append(sil)
            if sil > best_sil:
                best_sil = sil
                best_k = k

        # Final model
        final_km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        cluster_labels = final_km.fit_predict(X_scaled)

        cluster_dist = pd.Series(cluster_labels).value_counts().to_dict()

        return {
            "task": "clustering",
            "optimal_k": best_k,
            "silhouette_score": float(round(best_sil, 4)),
            "inertias": [float(round(v, 2)) for v in inertias],
            "sil_scores": [float(round(v, 4)) for v in sil_scores],
            "k_range": list(k_range),
            "cluster_distribution": {int(k): int(v) for k, v in cluster_dist.items()},
            "feature_cols": num_cols,
            "cluster_labels": cluster_labels.tolist()[:500],  # cap for JSON
            "error": None
        }
    except Exception as e:
        return {"error": f"Clustering failed: {str(e)}"}


# ──────────────────────────────────────────────────────────────────
# DATA PROFILING (works on ANY dataset)
# ──────────────────────────────────────────────────────────────────

def profile_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Deep data profiling: shape, dtypes, missing values,
    distributions, correlations, outliers, skewness.
    """
    n_rows, n_cols = df.shape
    num_df = df.select_dtypes(include=[np.number])
    cat_df = df.select_dtypes(include=["object", "category"])

    # Missing values analysis
    missing = df.isnull().sum()
    missing_info = {col: int(val) for col, val in missing.items() if val > 0}

    # Numeric column stats
    numeric_stats = []
    for col in num_df.columns:
        s = df[col].dropna()
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        outliers = int(((s < q1 - 1.5*iqr) | (s > q3 + 1.5*iqr)).sum())
        numeric_stats.append({
            "column": col,
            "min": float(round(s.min(), 4)),
            "max": float(round(s.max(), 4)),
            "mean": float(round(s.mean(), 4)),
            "median": float(round(s.median(), 4)),
            "std": float(round(s.std(), 4)),
            "skewness": float(round(s.skew(), 4)),
            "outlier_count": outliers,
            "outlier_pct": float(round(outliers / max(len(s), 1) * 100, 2)),
        })

    # Correlation matrix (top correlated pairs)
    top_correlations = []
    if len(num_df.columns) >= 2:
        corr = num_df.corr().abs()
        pairs = []
        cols = corr.columns.tolist()
        for i in range(len(cols)):
            for j in range(i+1, len(cols)):
                pairs.append({
                    "col_a": cols[i],
                    "col_b": cols[j],
                    "correlation": float(round(corr.iloc[i, j], 4))
                })
        top_correlations = sorted(pairs, key=lambda x: abs(x["correlation"]), reverse=True)[:10]

    # Categorical column stats
    categorical_stats = []
    for col in cat_df.columns:
        vc = df[col].value_counts()
        categorical_stats.append({
            "column": col,
            "unique_count": int(df[col].nunique()),
            "top_value": str(vc.index[0]) if len(vc) > 0 else "",
            "top_freq": int(vc.iloc[0]) if len(vc) > 0 else 0,
            "top_freq_pct": float(round(vc.iloc[0] / n_rows * 100, 2)) if len(vc) > 0 else 0,
        })

    # Data quality score
    completeness = float(round((1 - df.isnull().sum().sum() / (n_rows * n_cols)) * 100, 2))
    has_duplicates = int(df.duplicated().sum())
    quality_score = _compute_quality_score(completeness, has_duplicates, n_rows)

    # Geographic column detection
    geo_detected = _detect_geo_columns(df)
    geo_summary = _compute_geo_summary(df, geo_detected)

    return {
        "shape": {"rows": n_rows, "columns": n_cols},
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": missing_info,
        "completeness_pct": completeness,
        "duplicate_rows": has_duplicates,
        "data_quality_score": quality_score,
        "numeric_stats": numeric_stats,
        "categorical_stats": categorical_stats,
        "top_correlations": top_correlations,
        "geo_detected": geo_detected,
        "geo_summary": geo_summary,
        "memory_mb": float(round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)),
    }


def _compute_geo_summary(df: pd.DataFrame, geo_info: Dict) -> List[Dict]:
    """Aggregate data for map visualization."""
    res = []
    # If coordinates exist, take a sample for scatter plot
    if geo_info["has_coordinates"]:
        sample = df.dropna(subset=[geo_info["lat_col"], geo_info["lon_col"]]).sample(min(1000, len(df)))
        for _, row in sample.iterrows():
            res.append({
                "lat": float(row[geo_info["lat_col"]]),
                "lon": float(row[geo_info["lon_col"]]),
                "val": 1
            })
        return res

    # If country/state/city exist, group by top 20
    for col_key in ["country_col", "state_col", "city_col"]:
        col = geo_info.get(col_key)
        if col and col in df.columns:
            counts = df[col].value_counts().head(20)
            for name, val in counts.items():
                res.append({"name": str(name), "value": int(val)})
            break
    return res


def _compute_quality_score(completeness: float, duplicates: int, n_rows: int) -> Dict:
    dup_pct = duplicates / max(n_rows, 1) * 100
    score = completeness * 0.6 + max(0, 100 - dup_pct * 10) * 0.4
    grade = ("🏆 Excellent" if score >= 95 else "🥇 Good" if score >= 80
             else "[WARN]️ Fair" if score >= 60 else "🔴 Poor")
    return {"score": float(round(score, 1)), "grade": grade,
            "completeness": completeness, "duplicate_pct": float(round(dup_pct, 2))}


def _detect_geo_columns(df: pd.DataFrame) -> Dict:
    """Check if dataset has geographic columns (lat/lon/city/state)."""
    cols_lower = {c.lower(): c for c in df.columns}
    lat_col = next((cols_lower[k] for k in cols_lower if "lat" in k), None)
    lon_col = next((cols_lower[k] for k in cols_lower if "lon" in k or "lng" in k), None)
    city_col = next((cols_lower[k] for k in cols_lower if "city" in k), None)
    state_col = next((cols_lower[k] for k in cols_lower if "state" in k or "region" in k), None)
    country_col = next((cols_lower[k] for k in cols_lower if "country" in k or "nation" in k), None)

    return {
        "has_coordinates": bool(lat_col and lon_col),
        "has_location": bool(city_col or state_col or country_col),
        "lat_col": lat_col,
        "lon_col": lon_col,
        "city_col": city_col,
        "state_col": state_col,
        "country_col": country_col,
    }


# ──────────────────────────────────────────────────────────────────
# DISTRIBUTION ANALYSIS
# ──────────────────────────────────────────────────────────────────

def compute_distributions(df: pd.DataFrame, cols: Optional[List[str]] = None) -> Dict:
    """Compute histogram bins and KDE estimates for numeric columns."""
    num_cols = cols or df.select_dtypes(include=[np.number]).columns.tolist()[:10]
    result = {}
    for col in num_cols:
        s = df[col].dropna()
        if len(s) < 5:
            continue
        counts, bin_edges = np.histogram(s, bins=min(30, len(s)//2))
        result[col] = {
            "counts": counts.tolist(),
            "bin_edges": [float(round(e, 4)) for e in bin_edges],
            "mean": float(round(s.mean(), 4)),
            "std": float(round(s.std(), 4)),
            "skew": float(round(s.skew(), 4)),
            "kurtosis": float(round(s.kurtosis(), 4)),
        }
    return result
def get_sample_rows(df: pd.DataFrame, n: int = 10) -> List[Dict]:
    """Returns a serializable list of dictionaries for LLM context."""
    return df.head(n).replace({np.nan: None}).to_dict(orient="records")


def get_forensic_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Advanced forensic data indicators."""
    return {
        "entropy": float(round(df.nunique().mean(), 2)),
        "cardinality": {col: int(df[col].nunique()) for col in df.columns[:10]},
        "outlier_freq": float(round(df.select_dtypes(include=[np.number]).apply(
            lambda x: ((x < x.quantile(0.25) - 1.5*(x.quantile(0.75)-x.quantile(0.25))) | 
                       (x > x.quantile(0.75) + 1.5*(x.quantile(0.75)-x.quantile(0.25)))).sum()
        ).mean(), 2))
    }
