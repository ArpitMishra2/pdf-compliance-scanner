# app/pages/06_ds_reports.py
"""
Module 06 — Source Analytics
Risk trend charts, compliance scores, flagged column heatmap, change history.
"""
import streamlit as st
import textwrap
import json
from datetime import datetime, timedelta

from storage.database import DataSourceDB, init_ds_db
from connectors.factory import CONNECTOR_META
from app.styles.theme import GLOBAL_CSS

try:
    import plotly.graph_objects as go
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

st.set_page_config(page_title="Source Analytics", page_icon="◈", layout="wide", initial_sidebar_state="expanded")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
init_ds_db()

# ── CHART THEME ────────────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="#1C1F2B",
    plot_bgcolor="#1C1F2B",
    font=dict(family="Inter, sans-serif", color="#64748B"),
    xaxis=dict(gridcolor="rgba(46,51,71,0.8)", linecolor="#2E3347"),
    yaxis=dict(gridcolor="rgba(46,51,71,0.8)", linecolor="#2E3347"),
    margin=dict(l=0, r=0, t=24, b=0),
)
INDIGO = "#6366F1"
GREEN  = "#22C55E"
RED    = "#EF4444"
AMBER  = "#F59E0B"

# ── PAGE HEADER ────────────────────────────────────────────────────────────────
st.markdown(textwrap.dedent("""
<div class="page-header">
  <span class="module-label">Module 06</span>
  <h1>Source Analytics</h1>
  <p>Risk trends, compliance scores, flagged column analytics, and change history.</p>
</div>
"""), unsafe_allow_html=True)

sources = DataSourceDB.get_all_sources()
if not sources:
    st.info("No data sources registered. Add sources in Module 04 and run scans in Module 05.")
    st.stop()

# ── OVERVIEW TILES ─────────────────────────────────────────────────────────────
latest_trends = DataSourceDB.get_all_latest_trends()
trends_by_source = {t["source_id"]: t for t in latest_trends}

st.markdown('<div class="caption-label" style="margin-bottom:10px">Cross-source risk overview</div>', unsafe_allow_html=True)

cols = st.columns(min(len(sources), 4))
RISK_ORDER = ["low", "medium", "high", "critical"]
RISK_COLORS = {"low": "var(--low)", "high": "var(--high)", "medium": "var(--medium)", "critical": "var(--red)"}
RISK_BADGES = {"low": "badge-low", "medium": "badge-medium", "high": "badge-high", "critical": "badge-critical"}

for i, src in enumerate(sources[:4]):
    meta = CONNECTOR_META.get(src["source_type"], {"icon": "🔌", "label": src["source_type"]})
    trend = trends_by_source.get(src["source_id"])

    risk_score  = f"{trend['risk_score']:.0f}" if trend else "—"
    compliance  = f"{trend['compliance_pct']:.1f}%" if trend else "—"
    violations  = str(trend["total_violations"]) if trend else "—"
    source_risk = "low"
    if trend:
        pct = trend.get("compliance_pct", 100)
        if pct < 70:  source_risk = "critical"
        elif pct < 85: source_risk = "high"
        elif pct < 95: source_risk = "medium"

    risk_color = RISK_COLORS.get(source_risk, "var(--text)")

    with cols[i % 4]:
        st.markdown(textwrap.dedent(f"""
        <div style="background:var(--surface);border:1px solid var(--border);padding:20px;border-radius:var(--radius-xl);text-align:center">
          <div style="font-size:24px;margin-bottom:8px">{meta['icon']}</div>
          <div style="font-size:14px;font-weight:600;color:var(--text);margin-bottom:4px">{src['name'][:18]}</div>
          <div style="font-family:var(--font-mono);font-size:36px;font-weight:700;color:{risk_color};margin:10px 0">{risk_score}</div>
          <div class="caption-label" style="margin-bottom:8px">Risk score</div>
          <div style="font-family:var(--font-mono);font-size:14px;color:var(--low)">{compliance}</div>
          <div class="caption-label" style="font-size:10px">Compliance</div>
          <div style="font-family:var(--font-mono);font-size:14px;color:var(--text-secondary);margin-top:8px">{violations}</div>
          <div class="caption-label" style="font-size:10px">Violations</div>
        </div>
        """), unsafe_allow_html=True)

st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

# ── SOURCE SELECTOR ────────────────────────────────────────────────────────────
source_map = {
    f"{CONNECTOR_META.get(s['source_type'], {}).get('icon', '🔌')} {s['name']}": s
    for s in sources
}
selected_label = st.selectbox("Focus Source", options=list(source_map.keys()),
                              label_visibility="collapsed")
source = source_map[selected_label]
source_id = source["source_id"]

# ── TREND PERIOD SELECTOR ──────────────────────────────────────────────────────
col_period, col_refresh = st.columns([2, 1])
with col_period:
    period = st.radio("Trend period", ["30 days", "60 days", "90 days"],
                      horizontal=True, label_visibility="collapsed")
with col_refresh:
    if st.button("↺  REFRESH", use_container_width=True):
        st.rerun()

period_days = int(period.split()[0])
trends = DataSourceDB.get_risk_trends(source_id, days=period_days)

# ── RISK TREND LINE CHART ──────────────────────────────────────────────────────
st.markdown('<div class="caption-label" style="margin:16px 0 8px">Risk score over time</div>', unsafe_allow_html=True)
if not trends:
    st.markdown(textwrap.dedent("""
    <div style="text-align:center;padding:40px;border:1px dashed var(--border);border-radius:var(--radius-lg);font-size:14px;color:var(--text-muted)">
      No trend data yet — run a scan first.
    </div>
    """), unsafe_allow_html=True)
elif HAS_PLOTLY:
    dates   = [t["trend_date"] for t in trends]
    risk_scores = [t["risk_score"] for t in trends]
    pii_counts  = [t["pii_count"] for t in trends]
    conf_counts = [t["confidential_count"] for t in trends]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=risk_scores,
        mode="lines+markers",
        name="Risk Score",
        line=dict(color=INDIGO, width=2),
        marker=dict(size=6, color=INDIGO),
        fill="tozeroy",
        fillcolor="rgba(99,102,241,0.08)",
    ))
    fig.add_trace(go.Bar(x=dates, y=pii_counts, name="PII Violations",
                         marker_color=RED, opacity=0.6))
    fig.add_trace(go.Bar(x=dates, y=conf_counts, name="Confidential",
                         marker_color=AMBER, opacity=0.6))
    fig.update_layout(**CHART_LAYOUT, height=280, barmode="stack",
                      legend=dict(orientation="h", y=1.0, x=0))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Install plotly for interactive charts: `pip install plotly`")
    if trends:
        st.dataframe([{"date": t["trend_date"], "risk_score": t["risk_score"],
                       "violations": t["total_violations"]} for t in trends])

# ── COMPLIANCE GAUGE ───────────────────────────────────────────────────────────
if trends and HAS_PLOTLY:
    latest = trends[-1]
    comp_pct = latest.get("compliance_pct", 100.0)

    st.markdown('<div class="caption-label" style="margin:16px 0 8px">Latest compliance score</div>', unsafe_allow_html=True)
    col_gauge, col_breakdown = st.columns([1, 2])

    with col_gauge:
        gauge_color = RED if comp_pct < 70 else (AMBER if comp_pct < 90 else GREEN)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=comp_pct,
            domain={"x": [0, 1], "y": [0, 1]},
            number={"suffix": "%", "font": {"family": "JetBrains Mono", "color": gauge_color, "size": 32}},
            gauge={
                "axis": {"range": [0, 100], "tickfont": {"size": 11}},
                "bar": {"color": gauge_color},
                "bgcolor": "rgba(0,0,0,0)",
                "steps": [
                    {"range": [0, 70], "color": "rgba(248,113,113,0.15)"},
                    {"range": [70, 90], "color": "rgba(232,168,56,0.10)"},
                    {"range": [90, 100], "color": "rgba(79,209,128,0.10)"},
                ],
                "threshold": {"line": {"color": "#fff", "width": 2}, "thickness": 0.75, "value": comp_pct},
            }
        ))
        fig_gauge.update_layout(**CHART_LAYOUT, height=220)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_breakdown:
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;padding-top:8px">
          <div style="background:var(--surface);padding:14px;text-align:center">
            <div class="caption-label" style="margin-bottom:4px">PII flags</div>
            <div style="font-family:var(--font-mono);font-size:26px;color:{RED};font-weight:600">{latest.get('pii_count', 0)}</div>
          </div>
          <div style="background:var(--surface);padding:14px;text-align:center">
            <div class="caption-label" style="margin-bottom:4px">Confidential</div>
            <div style="font-family:var(--font-mono);font-size:26px;color:{AMBER};font-weight:600">{latest.get('confidential_count', 0)}</div>
          </div>
          <div style="background:var(--surface);padding:14px;text-align:center">
            <div class="caption-label" style="margin-bottom:4px">Total violations</div>
            <div style="font-family:var(--font-mono);font-size:26px;color:var(--text);font-weight:600">{latest.get('total_violations', 0)}</div>
          </div>
          <div style="background:var(--surface);padding:14px;text-align:center">
            <div class="caption-label" style="margin-bottom:4px">Risk score</div>
            <div style="font-family:var(--font-mono);font-size:26px;color:{gauge_color};font-weight:600">{latest.get('risk_score', 0):.1f}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── CHANGE HISTORY ─────────────────────────────────────────────────────────────
st.markdown('<div class="caption-label" style="margin:24px 0 8px">Schema change history</div>', unsafe_allow_html=True)
changes = DataSourceDB.get_changes(source_id, limit=20)

if not changes:
    st.markdown(textwrap.dedent("""
    <div style="font-size:14px;color:var(--text-muted);text-align:center;padding:24px;border:1px dashed var(--border);border-radius:var(--radius-lg)">
      No schema changes recorded
    </div>
    """), unsafe_allow_html=True)
else:
    SEV_MAP = {"critical": "badge-critical", "high": "badge-high", "medium": "badge-medium", "low": "badge-low"}
    for chg in changes:
        sev = chg.get("severity", "medium")
        ts = chg.get("detected_at", "")[:16]
        detail = chg.get("change_detail", {})
        if isinstance(detail, str):
            try: detail = json.loads(detail)
            except: detail = {}
        detail_str = json.dumps(detail, ensure_ascii=False)[:120]

        st.markdown(textwrap.dedent(f"""
        <div style="background:var(--surface);border-left:3px solid var(--{'critical' if sev=='critical' else 'high' if sev=='high' else 'medium' if sev=='medium' else 'low'});padding:10px 16px;margin-bottom:4px;border-radius:0 var(--radius) var(--radius) 0">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
            <span style="font-family:var(--font-mono);font-size:11px;color:var(--text-muted)">{ts}</span>
            <span style="font-size:12px;font-weight:600;color:var(--text-secondary)">{chg.get('change_type', '').replace('_', ' ').title()}</span>
            <span style="font-family:var(--font-mono);font-size:12px;color:var(--text)">{chg.get('entity_name', '')}</span>
            <span class="badge {SEV_MAP.get(sev, 'badge-info')}" style="margin-left:auto">{sev.capitalize()}</span>
          </div>
          <div style="font-family:var(--font-mono);font-size:11px;color:var(--text-muted)">{detail_str}</div>
        </div>
        """), unsafe_allow_html=True)

# ── SNAPSHOT HISTORY ───────────────────────────────────────────────────────────
st.markdown('<div class="caption-label" style="margin:24px 0 8px">Metadata snapshot history</div>', unsafe_allow_html=True)
snapshots = DataSourceDB.get_snapshot_history(source_id, limit=8)

if snapshots:
    snap_rows = [
        {
            "Snapshot ID": s["snapshot_id"][:14],
            "Schema Hash": s["schema_hash"][:16],
            "Tables": s["table_count"],
            "Columns": s["column_count"],
            "Captured At": (s.get("captured_at") or "")[:16],
        }
        for s in snapshots
    ]
    st.dataframe(snap_rows, use_container_width=True)
else:
    st.info("No snapshots yet. Run a scan to create the first snapshot.")
