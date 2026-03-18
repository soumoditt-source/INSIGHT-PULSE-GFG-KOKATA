"""
InsightPulse AI - RAG Schema Engine v5.0
=====================================================================
Dynamically builds rich schema context for any uploaded dataset.
Pre-loaded with domain knowledge for Amazon Sales + Insurance datasets.
Auto-generalizes for any other CSV.
"""
import json
import pandas as pd
from pathlib import Path
from typing import Optional

# -----------------------------------------------------------------
# DOMAIN KNOWLEDGE LIBRARIES
# These provide human-readable column descriptions injected into LLM prompts.
# For unknown columns, a smart auto-description is generated.
# -----------------------------------------------------------------

AMAZON_SALES_DESCRIPTIONS = {
    "order_id":          "Unique identifier for each sales order (integer key)",
    "order_date":        "Date the order was placed (format: YYYY-MM-DD)",
    "product_id":        "Unique product identifier (integer)",
    "product_category":  "Product category (e.g., Electronics, Clothing, Books, Home, Sports)",
    "price":             "Original listed price of the product (USD)",
    "discount_percent":  "Discount percentage applied to the product (0-100%)",
    "quantity_sold":     "Number of units sold in this order (integer count)",
    "customer_region":   "Geographic region of the customer (e.g., North America, Europe, Asia)",
    "payment_method":    "Payment method used (e.g., UPI, Credit Card, Debit Card, Net Banking)",
    "rating":            "Customer rating score (1.0 - 5.0, higher is better)",
    "review_count":      "Number of customer reviews for this product",
    "discounted_price":  "Final price after discount = price * (1 - discount_percent/100) (USD)",
    "total_revenue":     "Total revenue from this order = discounted_price * quantity_sold (USD)",
}

INSURANCE_CLAIMS_DESCRIPTIONS = {
    "life_insurer":                          "Name of the life insurance company",
    "year":                                  "Financial year (e.g., 2021-22, 2022-23)",
    "category":                              "Type of claim: 'Individual Death Claim' or 'Group Death Claim'",
    "claims_paid_ratio_no":                  "Settlement ratio by count (0-1, higher=better)",
    "claims_paid_ratio_amt":                 "Settlement ratio by amount (0-1, higher=better)",
    "claims_repudiated_rejectedrationo__":   "Denial ratio by count (0-1, lower=better)",
    "claims_pending_ratio_no":               "Backlog ratio by count (0-1, lower=better)",
    "claims_paid_amt":                       "Total amount paid (INR Crore)",
    "claims_paid_no":                        "Number of claims paid (count)",
    "total_claims_amt":                      "Total monetary value of all claims (INR Crore)",
    "total_claims_no":                       "Total number of claims processed (count)",
    "claims_repudiated_rejected_amt_":       "Denial value (INR Crore)",
    "claims_pending_amt":                    "Backlog value (INR Crore)",
}

# -----------------------------------------------------------------
# FEW-SHOT EXAMPLES - Amazon Sales
# -----------------------------------------------------------------

AMAZON_FEW_SHOTS = [
    {
        "query": "Top 10 products by total revenue",
        "sql": "SELECT product_id, product_category, SUM(total_revenue) AS total_rev FROM sales GROUP BY product_id, product_category ORDER BY total_rev DESC LIMIT 10",
        "chart_type": "hbar",
        "reasoning": "Ranking query -> horizontal bar chart sorted by revenue"
    },
    {
        "query": "Monthly revenue trend",
        "sql": "SELECT DATE_TRUNC('month', CAST(order_date AS DATE)) AS month, SUM(total_revenue) AS monthly_revenue FROM sales GROUP BY month ORDER BY month ASC",
        "chart_type": "line",
        "reasoning": "Time series -> line chart with month on X axis"
    },
    {
        "query": "Revenue breakdown by product category",
        "sql": "SELECT product_category, SUM(total_revenue) AS total_rev FROM sales GROUP BY product_category ORDER BY total_rev DESC",
        "chart_type": "pie",
        "reasoning": "Part-of-whole -> donut/pie chart"
    },
    {
        "query": "Heatmap of average rating by category and region",
        "sql": "SELECT product_category, customer_region, AVG(rating) AS avg_rating FROM sales GROUP BY product_category, customer_region",
        "chart_type": "heatmap",
        "reasoning": "2D matrix -> heatmap colored by average rating value"
    },
    {
        "query": "Correlation between price and rating",
        "sql": "SELECT product_category AS label, AVG(price) AS avg_price, AVG(rating) AS avg_rating, COUNT(*) AS order_count FROM sales GROUP BY product_category",
        "chart_type": "scatter",
        "reasoning": "Two numeric metrics -> scatter plot"
    },
    {
        "query": "Revenue by payment method",
        "sql": "SELECT payment_method, SUM(total_revenue) AS total_rev, COUNT(*) AS order_count FROM sales GROUP BY payment_method ORDER BY total_rev DESC",
        "chart_type": "bar",
        "reasoning": "Categorical comparison -> vertical bar chart"
    },
    {
        "query": "Top regions by average discount",
        "sql": "SELECT customer_region, AVG(discount_percent) AS avg_discount, SUM(total_revenue) AS total_rev FROM sales GROUP BY customer_region ORDER BY avg_discount DESC",
        "chart_type": "hbar",
        "reasoning": "Regional comparison -> horizontal bar with color by revenue"
    },
]

GENERIC_FEW_SHOTS = [
    {
        "query": "Show me the top 10 rows",
        "sql": "SELECT * FROM sales LIMIT 10",
        "chart_type": "table",
        "reasoning": "Raw data view -> table"
    },
    {
        "query": "Count rows by category",
        "sql": "SELECT {cat_col} AS category, COUNT(*) AS count FROM sales GROUP BY {cat_col} ORDER BY count DESC LIMIT 20",
        "chart_type": "bar",
        "reasoning": "Count aggregation -> bar chart"
    },
]


def _detect_domain(df: pd.DataFrame) -> str:
    """Detect whether this is Amazon Sales, Insurance Claims, or a generic dataset."""
    cols_lower = set(c.lower() for c in df.columns)
    if "order_id" in cols_lower and "total_revenue" in cols_lower:
        return "amazon_sales"
    if "life_insurer" in cols_lower and "claims_paid_ratio_no" in cols_lower:
        return "insurance_claims"
    return "generic"


def _auto_describe_column(col: str, dtype_str: str, sample_vals: list) -> str:
    """Generate a smart auto-description for unknown columns."""
    col_lower = col.lower().replace("_", " ")

    # Date patterns
    if any(kw in col_lower for kw in ["date", "time", "created", "updated", "timestamp"]):
        return f"Date/time column: {col}"

    # ID patterns
    if col_lower.endswith(" id") or col_lower == "id":
        return f"Unique identifier: {col}"

    # Ratio patterns
    if any(kw in col_lower for kw in ["ratio", "rate", "pct", "percent", "share"]):
        return f"Ratio/percentage metric: {col} (typically 0-1 or 0-100)"

    # Amount/revenue patterns
    if any(kw in col_lower for kw in ["revenue", "sales", "amount", "price", "cost", "value", "profit"]):
        return f"Financial metric (currency): {col}"

    # Count patterns
    if any(kw in col_lower for kw in ["count", "number", "qty", "quantity", "total", "num"]):
        return f"Count/quantity metric: {col}"

    if dtype_str.startswith("float") or dtype_str.startswith("int"):
        return f"Numeric metric: {col}"

    # Categorical - show unique values
    if len(sample_vals) <= 10:
        return f"Categorical: {col}. Values: {sample_vals}"
    return f"Categorical: {col} ({len(sample_vals)} unique values)"


def build_schema_context(df: pd.DataFrame, dataset_name: str = "") -> dict:
    """
    Build a rich, annotated schema context dict for LLM prompt injection.
    Works for ANY dataset - auto-detects domain and enriches with descriptions.
    """
    domain = _detect_domain(df)

    # Select description library
    if domain == "amazon_sales":
        desc_lib = AMAZON_SALES_DESCRIPTIONS
        few_shots = AMAZON_FEW_SHOTS
        domain_notes = [
            "Prices and revenue are in USD",
            "discount_percent is 0-100 (e.g., 20 = 20% off)",
            "discounted_price = price × (1 - discount_percent/100)",
            "total_revenue = discounted_price × quantity_sold",
            "rating is 1.0-5.0 (higher = better customer satisfaction)",
            "Table is named 'sales' in DuckDB - always use FROM sales",
            "For date operations: CAST(order_date AS DATE), DATE_TRUNC, EXTRACT",
        ]
    elif domain == "insurance_claims":
        desc_lib = INSURANCE_CLAIMS_DESCRIPTIONS
        few_shots = []
        domain_notes = [
            "Amounts are in INR Crore (Indian currency)",
            "Ratios are 0-1 (multiply by 100 for percentage)",
            "Table is named 'sales' in DuckDB - always use FROM sales",
            "Individual vs Group Claims: filter using 'category' column",
            "Performance: higher 'claims_paid_ratio_no' = higher efficiency",
        ]
    else:
        desc_lib = {}
        few_shots = GENERIC_FEW_SHOTS
        domain_notes = [
            f"Dataset: {dataset_name or 'Custom Upload'}",
            "Table is named 'sales' in DuckDB - always use FROM sales",
            "Use exact column names as listed in schema",
        ]

    # Build column metadata
    columns = []
    # Pre-calculate numeric and categorical columns once for efficiency
    numeric_cols = {col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])}
    categorical_cols = {col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])}

    for col in df.columns:
        dtype_str = str(df[col].dtype)
        uniques = df[col].dropna().unique().tolist()

        if col in numeric_cols: # Using the pre-calculated set
            try:
                s = df[col].dropna()
                col_info = {
                    "name": col,
                    "type": "numeric",
                    "description": desc_lib.get(col, _auto_describe_column(col, dtype_str, [])),
                    "min": float(f"{df[col].min():.4f}") if not df[col].empty else 0.0,
                    "max": float(f"{df[col].max():.4f}") if not df[col].empty else 0.0,
                    "avg": float(f"{df[col].mean():.4f}") if not df[col].empty else 0.0,
                    "std": float(f"{df[col].std():.4f}") if not df[col].empty else 0.0,
                    "sample_values": df[col].head(3).tolist()
                }
            except Exception:
                col_info = {"name": col, "type": "numeric",
                            "description": desc_lib.get(col, col)}
        else:
            sample_vals = [str(v) for v in uniques[:15]]
            col_info = {
                "name": col,
                "type": "categorical" if len(uniques) <= 50 else "text",
                "description": desc_lib.get(col, _auto_describe_column(col, dtype_str, sample_vals)),
                "unique_count": int(df[col].nunique()),
                "sample_values": sample_vals[:15]
            }
        columns.append(col_info)

    return {
        "table_name": "sales",   # always 'sales' in DuckDB - critical for SQL
        "domain": domain,
        "dataset_name": dataset_name,
        "total_rows": int(len(df)),
        "total_columns": len(df.columns),
        "columns": columns,
        "few_shot_examples": few_shots,
        "domain_notes": domain_notes,
    }
