"""
InsightPulse AI - Plotly Chart Builder v5.0
=====================================================================
Converts LLM JSON chart configs + query result DataFrames into
fully interactive, dark-theme Plotly figures.

Supports: bar, hbar, line, pie, donut, heatmap, scatter,
          treemap, radar, table, area, funnel
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Optional

# ── Brand palette - sci-fi neon spectrum
BRAND_COLORS = [
    "#6366F1",  # indigo
    "#8B5CF6",  # violet
    "#EC4899",  # pink
    "#14B8A6",  # teal
    "#F59E0B",  # amber
    "#10B981",  # emerald
    "#3B82F6",  # blue
    "#EF4444",  # red
    "#06B6D4",  # cyan
    "#84CC16",  # lime
    "#F97316",  # orange
    "#A855F7",  # purple
    "#22D3EE",  # sky
    "#FB7185",  # rose
    "#34D399",  # green
]

FONT_FAMILY = "Inter, 'Outfit', system-ui, -apple-system, sans-serif"

# ── Base dark layout applied to all figures
BASE_LAYOUT = dict(
    paper_bgcolor="rgba(10, 10, 30, 0.0)",   # transparent - lets page bg show
    plot_bgcolor="rgba(10, 10, 30, 0.0)",
    font=dict(family=FONT_FAMILY, color="#E2E8F0", size=13),
    margin=dict(l=20, r=20, t=55, b=30),
    colorway=BRAND_COLORS,
    hoverlabel=dict(
        bgcolor="#1E1E40",
        font_size=13,
        font_family=FONT_FAMILY,
        bordercolor="#6366F1"
    ),
    xaxis=dict(
        gridcolor="rgba(99,102,241,0.08)",
        tickfont=dict(color="#94A3B8"),
        linecolor="rgba(99,102,241,0.15)",
        zerolinecolor="rgba(99,102,241,0.15)"
    ),
    yaxis=dict(
        gridcolor="rgba(99,102,241,0.08)",
        tickfont=dict(color="#94A3B8"),
        linecolor="rgba(99,102,241,0.15)",
        zerolinecolor="rgba(99,102,241,0.15)"
    ),
    legend=dict(
        bgcolor="rgba(15,15,35,0.6)",
        bordercolor="rgba(99,102,241,0.2)",
        borderwidth=1,
        font=dict(color="#CBD5E1", size=12)
    )
)


def _apply_base_layout(fig: go.Figure, title: str, height: int = 430) -> go.Figure:
    """Apply the standard InsightPulse dark theme to any figure."""
    layout = dict(**BASE_LAYOUT)
    layout["title"] = dict(
        text=f"<b>{title}</b>",
        font=dict(size=17, color="#A5B4FC", family=FONT_FAMILY),
        x=0.01, xanchor="left"
    )
    layout["height"] = height
    fig.update_layout(**layout)
    return fig


def _safe_col(df: pd.DataFrame, col: Optional[str]) -> Optional[str]:
    """Return col if it's a valid column in df, else None."""
    return col if col and col in df.columns else None


# ────────────────────────────────────────────────────────────────────────────
# CHART BUILDERS
# ────────────────────────────────────────────────────────────────────────────

def build_bar_chart(df: pd.DataFrame, cfg: dict) -> go.Figure:
    x_col = _safe_col(df, cfg.get("x_col")) or df.columns[0]
    y_col = _safe_col(df, cfg.get("y_col")) or df.columns[-1]
    color_col = _safe_col(df, cfg.get("color_col"))
    orientation = cfg.get("orientation", "v")
    title = cfg.get("title", "Bar Chart")
    height = cfg.get("layout", {}).get("height", 430)

    if orientation == "h":
        return build_hbar_chart(df, cfg)

    fig = px.bar(
        df, x=x_col, y=y_col,
        color=color_col,
        color_discrete_sequence=BRAND_COLORS,
        text=y_col
    )
    fig.update_traces(
        texttemplate='%{text:,.0f}' if df[y_col].max() > 100 else '%{text:.2f}',
        textposition='outside',
        marker_line_color='rgba(255,255,255,0.05)',
        marker_line_width=0.5
    )
    return _apply_base_layout(fig, title, height)


def build_hbar_chart(df: pd.DataFrame, cfg: dict) -> go.Figure:
    """Horizontal bar - best for rankings."""
    x_col = _safe_col(df, cfg.get("x_col")) or df.columns[-1]
    y_col = _safe_col(df, cfg.get("y_col")) or df.columns[0]
    title = cfg.get("title", "Ranking")
    height = cfg.get("layout", {}).get("height", 430)

    if x_col not in df.columns or y_col not in df.columns:
        return build_error_figure(f"Missing columns: {x_col} or {y_col}")

    # Sort ascending so highest appears at top
    df_s = df.sort_values(x_col, ascending=True).tail(20)

    # Gradient colors based on rank
    n = len(df_s)
    colors = [
        f"rgba(99, 102, 241, {0.35 + 0.65 * (i / max(n - 1, 1)):.2f})"
        for i in range(n)
    ]

    numeric_col = df_s[x_col]
    is_float = numeric_col.dtype in [float, "float64", "float32"]
    text_vals = [f"{v:,.2f}" if is_float else f"{v:,}" for v in numeric_col]

    fig = go.Figure(go.Bar(
        x=df_s[x_col],
        y=df_s[y_col].astype(str),
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.05)', width=0.5)
        ),
        text=text_vals,
        textposition='outside',
        hovertemplate=f"<b>%{{y}}</b><br>{x_col}: %{{x:,.2f}}<extra></extra>"
    ))
    return _apply_base_layout(fig, title, height)


def build_line_chart(df: pd.DataFrame, cfg: dict) -> go.Figure:
    x_col = _safe_col(df, cfg.get("x_col")) or df.columns[0]
    y_col = _safe_col(df, cfg.get("y_col")) or df.columns[-1]
    color_col = _safe_col(df, cfg.get("color_col"))
    title = cfg.get("title", "Trend")
    height = cfg.get("layout", {}).get("height", 430)

    if color_col:
        fig = px.line(
            df, x=x_col, y=y_col, color=color_col,
            color_discrete_sequence=BRAND_COLORS,
            markers=True
        )
    else:
        fig = px.line(df, x=x_col, y=y_col, markers=True)
        fig.update_traces(
            line=dict(color=BRAND_COLORS[0], width=3),
            marker=dict(size=8, color=BRAND_COLORS[1],
                        line=dict(color="#0F0F2A", width=2))
        )

    # Add shaded area under the line for visual richness
    if not color_col and y_col in df.columns:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y_col],
            fill='tozeroy',
            fillcolor='rgba(99,102,241,0.05)',
            line=dict(color='rgba(0,0,0,0)'),
            showlegend=False,
            hoverinfo='skip'
        ))

    fig.update_traces(
        hovertemplate=f"<b>%{{x}}</b><br>{y_col}: %{{y:,.2f}}<extra></extra>",
        selector=dict(type='scatter', mode='lines+markers')
    )
    return _apply_base_layout(fig, title, height)


def build_pie_chart(df: pd.DataFrame, cfg: dict) -> go.Figure:
    x_col = _safe_col(df, cfg.get("x_col")) or df.columns[0]  # labels
    y_col = _safe_col(df, cfg.get("y_col")) or df.columns[-1]  # values
    chart_type = cfg.get("type", "pie")
    title = cfg.get("title", "Distribution")
    height = cfg.get("layout", {}).get("height", 430)

    hole = 0.45 if chart_type in ("donut", "pie") else 0.0

    labels = df[x_col] if x_col else df.iloc[:, 0]
    values = df[y_col] if y_col else df.iloc[:, 1]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=hole,
        marker=dict(
            colors=BRAND_COLORS,
            line=dict(color='rgba(10,10,30,0.8)', width=2)
        ),
        textfont=dict(size=12, color="#E2E8F0"),
        hovertemplate="<b>%{label}</b><br>Value: %{value:,.2f}<br>Share: %{percent}<extra></extra>",
        textinfo="percent+label"
    ))

    # Central label for donut
    if hole > 0:
        try:
            total = float(values.sum())
            fig.add_annotation(
                text=f"<b>Total<br>{total:,.0f}</b>",
                x=0.5, y=0.5,
                font=dict(size=14, color="#A5B4FC"),
                showarrow=False
            )
        except Exception:
            pass

    return _apply_base_layout(fig, title, height)


def build_heatmap(df: pd.DataFrame, cfg: dict) -> go.Figure:
    x_col = _safe_col(df, cfg.get("x_col")) or df.columns[0]
    y_col = _safe_col(df, cfg.get("y_col")) or df.columns[1]
    z_col = _safe_col(df, cfg.get("color_col") or cfg.get("z_col")) or df.columns[-1]
    title = cfg.get("title", "Heatmap")
    height = cfg.get("layout", {}).get("height", 500)

    if not all(c in df.columns for c in [x_col, y_col, z_col]):
        return build_error_figure(f"Heatmap needs x, y, z columns. Got: {x_col}, {y_col}, {z_col}")

    try:
        pivot = df.pivot_table(index=y_col, columns=x_col, values=z_col, aggfunc="mean")
    except Exception as e:
        return build_error_figure(f"Cannot pivot: {e}")

    # Limit size for display
    if pivot.shape[0] > 30:
        pivot = pivot.iloc[:30]
    if pivot.shape[1] > 20:
        pivot = pivot.iloc[:, :20]

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[str(c) for c in pivot.columns],
        y=[str(r) for r in pivot.index],
        colorscale="Viridis",
        hoverongaps=False,
        texttemplate="%{z:.3f}",
        colorbar=dict(
            title=dict(text=z_col, font=dict(color="#94A3B8")),
            tickfont=dict(color="#94A3B8")
        ),
        hovertemplate=f"<b>%{{y}} × %{{x}}</b><br>{z_col}: %{{z:.4f}}<extra></extra>"
    ))
    return _apply_base_layout(fig, title, height)


def build_scatter(df: pd.DataFrame, cfg: dict) -> go.Figure:
    x_col = _safe_col(df, cfg.get("x_col")) or df.select_dtypes(include="number").columns[0]
    y_col = _safe_col(df, cfg.get("y_col")) or df.select_dtypes(include="number").columns[-1]
    color_col = _safe_col(df, cfg.get("color_col"))
    title = cfg.get("title", "Scatter Plot")
    height = cfg.get("layout", {}).get("height", 430)

    # Safe hover name
    str_cols = df.select_dtypes(include="object").columns
    hover_name = str_cols[0] if len(str_cols) > 0 else None

    # Try OLS trendline - fall back gracefully without statsmodels
    try:
        import statsmodels  # noqa: F401 - check availability
        trendline = "ols"
        trendline_color = BRAND_COLORS[2]
    except ImportError:
        trendline = None
        trendline_color = None

    fig = px.scatter(
        df, x=x_col, y=y_col,
        color=color_col,
        color_discrete_sequence=BRAND_COLORS,
        trendline=trendline,
        trendline_color_override=trendline_color,
        hover_name=hover_name
    )
    fig.update_traces(
        marker=dict(size=9, opacity=0.80, line=dict(color='rgba(255,255,255,0.3)', width=0.5)),
        selector=dict(mode="markers")
    )
    return _apply_base_layout(fig, title, height)


def build_treemap(df: pd.DataFrame, cfg: dict) -> go.Figure:
    x_col = _safe_col(df, cfg.get("x_col")) or df.columns[0]  # labels
    y_col = _safe_col(df, cfg.get("y_col")) or df.columns[-1]  # values
    color_col = _safe_col(df, cfg.get("color_col"))
    title = cfg.get("title", "Treemap")
    height = cfg.get("layout", {}).get("height", 480)

    parents = df[color_col].tolist() if color_col else [""] * len(df)

    fig = go.Figure(go.Treemap(
        labels=df[x_col].astype(str),
        parents=parents,
        values=df[y_col],
        textinfo="label+value+percent parent",
        marker=dict(colorscale="Viridis", line=dict(color="rgba(10,10,30,0.5)", width=1)),
        hovertemplate="<b>%{label}</b><br>Value: %{value:,.2f}<extra></extra>"
    ))
    return _apply_base_layout(fig, title, height)


def build_table(df: pd.DataFrame, cfg: dict) -> go.Figure:
    title = cfg.get("title", "Data Table")
    height = cfg.get("layout", {}).get("height", 400)

    header_vals = list(df.columns)
    formatted_cells = []
    for col in df.columns:
        if df[col].dtype in [float, "float64", "float32"]:
            formatted_cells.append([f"{v:,.4f}" if pd.notna(v) else "-" for v in df[col]])
        elif df[col].dtype in [int, "int64", "int32"]:
            formatted_cells.append([f"{v:,}" if pd.notna(v) else "-" for v in df[col]])
        else:
            formatted_cells.append([str(v) if pd.notna(v) else "-" for v in df[col]])

    row_colors = [
        ["rgba(15,15,35,0.9)" if i % 2 == 0 else "rgba(25,25,50,0.9)" for i in range(len(df))]
    ]

    fig = go.Figure(go.Table(
        header=dict(
            values=[f"<b>{h}</b>" for h in header_vals],
            fill_color="rgba(99,102,241,0.25)",
            font=dict(color="#A5B4FC", size=13, family=FONT_FAMILY),
            line_color="rgba(99,102,241,0.2)",
            align="left",
            height=38
        ),
        cells=dict(
            values=formatted_cells,
            fill_color=row_colors,
            font=dict(color="#E2E8F0", size=12, family=FONT_FAMILY),
            line_color="rgba(99,102,241,0.08)",
            align="left",
            height=32
        )
    ))
    return _apply_base_layout(fig, title, height)


def build_radar(df: pd.DataFrame, cfg: dict) -> go.Figure:
    title = cfg.get("title", "Radar Chart")
    height = cfg.get("layout", {}).get("height", 480)

    numeric_cols = df.select_dtypes(include=[float, int]).columns.tolist()
    if len(numeric_cols) < 2:
        return build_table(df, cfg)

    str_cols = df.select_dtypes(include=["object"]).columns
    str_col = str_cols[0] if len(str_cols) > 0 else None

    fig = go.Figure()
    rows = list(df.iterrows())[:6]   # max 6 entities
    for i, (_, row) in enumerate(rows):
        r_vals = [float(row[c]) for c in numeric_cols if pd.notna(row[c])]
        theta = [c for c in numeric_cols if pd.notna(row[c])]
        name = str(row[str_col]) if str_col else f"Row {i+1}"
        fig.add_trace(go.Scatterpolar(
            r=r_vals + [r_vals[0]],
            theta=theta + [theta[0]],
            fill='toself',
            name=name,
            line=dict(color=BRAND_COLORS[i % len(BRAND_COLORS)], width=2),
            fillcolor=f"rgba({','.join(str(int(c, 16)) for c in [BRAND_COLORS[i % len(BRAND_COLORS)][1:3], BRAND_COLORS[i % len(BRAND_COLORS)][3:5], BRAND_COLORS[i % len(BRAND_COLORS)][5:7]])}, 0.1)",
            opacity=0.85
        ))

    fig.update_layout(polar=dict(
        bgcolor="rgba(15,15,35,0.5)",
        radialaxis=dict(visible=True, gridcolor="rgba(99,102,241,0.1)", tickfont=dict(color="#64748B")),
        angularaxis=dict(gridcolor="rgba(99,102,241,0.1)", tickfont=dict(color="#94A3B8"))
    ))
    return _apply_base_layout(fig, title, height)


def build_area_chart(df: pd.DataFrame, cfg: dict) -> go.Figure:
    """Stacked / filled area chart - good for multi-series trends."""
    x_col = _safe_col(df, cfg.get("x_col")) or df.columns[0]
    y_col = _safe_col(df, cfg.get("y_col")) or df.columns[-1]
    color_col = _safe_col(df, cfg.get("color_col"))
    title = cfg.get("title", "Area Chart")
    height = cfg.get("layout", {}).get("height", 430)

    if color_col:
        fig = px.area(df, x=x_col, y=y_col, color=color_col,
                      color_discrete_sequence=BRAND_COLORS)
    else:
        fig = px.area(df, x=x_col, y=y_col,
                      color_discrete_sequence=BRAND_COLORS)
    return _apply_base_layout(fig, title, height)


def build_funnel(df: pd.DataFrame, cfg: dict) -> go.Figure:
    """Funnel chart - good for conversion/stage analysis."""
    x_col = _safe_col(df, cfg.get("x_col")) or df.columns[0]
    y_col = _safe_col(df, cfg.get("y_col")) or df.columns[-1]
    title = cfg.get("title", "Funnel")
    height = cfg.get("layout", {}).get("height", 430)

    fig = go.Figure(go.Funnel(
        y=df[x_col].astype(str),
        x=df[y_col],
        marker=dict(color=BRAND_COLORS[:len(df)]),
        textposition="inside",
        hovertemplate="<b>%{y}</b><br>Value: %{x:,.2f}<extra></extra>"
    ))
    return _apply_base_layout(fig, title, height)


def build_error_figure(message: str) -> go.Figure:
    """Return an informative error placeholder figure."""
    fig = go.Figure()
    fig.add_annotation(
        text=f"[WARN]️ {message}",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=15, color="#EF4444", family=FONT_FAMILY),
        align="center"
    )
    return _apply_base_layout(fig, "Chart Error", 300)


# ── Chart type dispatch table
CHART_BUILDERS = {
    "bar":     build_bar_chart,
    "hbar":    build_hbar_chart,
    "line":    build_line_chart,
    "pie":     build_pie_chart,
    "donut":   build_pie_chart,
    "heatmap": build_heatmap,
    "scatter": build_scatter,
    "treemap": build_treemap,
    "table":   build_table,
    "radar":   build_radar,
    "area":    build_area_chart,
    "funnel":  build_funnel,
}


def build_figures(df: pd.DataFrame, chart_configs: List[dict]) -> List[go.Figure]:
    """
    Build all Plotly figures from LLM chart configs + query result DataFrame.
    Returns list of figures (same length as chart_configs).
    Each failure produces an error placeholder figure instead of crashing.
    """
    figures = []
    for cfg in chart_configs:
        chart_type = cfg.get("type", "bar").lower().strip()
        builder = CHART_BUILDERS.get(chart_type, build_bar_chart)
        try:
            fig = builder(df, cfg)
            figures.append(fig)
        except Exception as e:
            print(f"[ChartBuilder] Error building '{chart_type}': {e}")
            figures.append(build_error_figure(f"Chart render failed: {e}"))
    return figures


def serialize_figures(figures: List[go.Figure]) -> List[str]:
    """Serialize Plotly figures to JSON strings for HTTP transport."""
    return [fig.to_json() for fig in figures]
