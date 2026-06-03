# app/pages/03_reports.py
"""
Reports page — browse and download past compliance scan reports.
Noir Amber UI redesign.
"""
import sys
import os
# Inject project root path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
import textwrap
from pathlib import Path
from storage.database import get_all_scans, get_result, delete_scan
from app.styles.theme import GLOBAL_CSS
from app.components.ui import risk_badge, empty_state

st.set_page_config(page_title="Scan Archive", page_icon="⚠", layout="wide", initial_sidebar_state="expanded")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── PAGE HEADER ────────────────────────────────────────────────────────────────
st.markdown(textwrap.dedent("""
<div class="page-header">
  <span class="module-label">Module 03</span>
  <h1>Scan Archive</h1>
  <p>Browse, review, and download past compliance scan reports.</p>
</div>
"""), unsafe_allow_html=True)

scans = get_all_scans()

# ── EMPTY STATE ────────────────────────────────────────────────────────────────
if not scans:
    st.markdown(textwrap.dedent("""
    <div style="text-align:center;padding:64px 24px;border:1px dashed var(--border);border-radius:var(--radius-xl);margin-top:24px">
      <div style="font-size:40px;color:var(--border-bright);margin-bottom:16px">○</div>
      <div style="font-size:15px;font-weight:600;color:var(--text-secondary);margin-bottom:8px">No scans on record</div>
      <div style="font-size:14px;color:var(--text-muted)">
        Your archive is empty. Upload a document to run your first scan.
      </div>
    </div>
    """), unsafe_allow_html=True)
    st.stop()

# ── GLOBAL ANALYTICS DASHBOARD ───────────────────────────────────────────
import pandas as pd
import plotly.graph_objects as go

def _noir_bar(x_vals, y_vals, colors, height=200):
    """Plotly bar chart styled for enterprise dark theme."""
    fig = go.Figure(go.Bar(
        x=x_vals, y=y_vals,
        marker_color=colors,
        marker_line_color="rgba(0,0,0,0)",
        marker_line_width=0,
    ))
    fig.update_layout(
        paper_bgcolor="#1C1F2B", plot_bgcolor="#1C1F2B",
        font=dict(family="Inter, sans-serif", color="#64748B", size=11),
        margin=dict(l=0, r=0, t=8, b=0), height=height, showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#64748B", size=10), linecolor="#2E3347"),
        yaxis=dict(showgrid=True, gridcolor="rgba(46,51,71,0.8)", zeroline=False, tickfont=dict(color="#64748B", size=10), linecolor="#2E3347"),
    )
    return fig

df = pd.DataFrame(scans)
if not df.empty and "scanned_at" in df.columns:
    df["scanned_at"] = pd.to_datetime(df["scanned_at"])
    df["date"] = df["scanned_at"].dt.date
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown('<div class="caption-label" style="margin-bottom:8px">Scans over time</div>', unsafe_allow_html=True)
        timeline_df = df.groupby("date").size().reset_index(name="scans")
        st.plotly_chart(
            _noir_bar([str(d) for d in timeline_df["date"]], timeline_df["scans"], colors="#6366F1"),
            use_container_width=True, config={"displayModeBar": False}
        )

    with col_chart2:
        st.markdown('<div class="caption-label" style="margin-bottom:8px">Risk distribution</div>', unsafe_allow_html=True)
        risk_df = df.groupby("highest_risk").size().reset_index(name="count")
        risk_colors_map = {"low": "#22C55E", "medium": "#F59E0B", "high": "#F97316", "critical": "#EF4444"}
        bar_colors = [risk_colors_map.get(str(r), "#6366F1") for r in risk_df["highest_risk"]]
        st.plotly_chart(
            _noir_bar(risk_df["highest_risk"].astype(str), risk_df["count"], colors=bar_colors),
            use_container_width=True, config={"displayModeBar": False}
        )

# ── TOTAL SCANS ────────────────────────────────────────────────────────────────
st.markdown(textwrap.dedent(f"""
<div style="display:inline-flex;align-items:center;gap:16px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:14px 22px;margin-bottom:20px;margin-top:20px">
  <div class="caption-label">Total scans</div>
  <div style="font-family:var(--font-mono);font-size:30px;font-weight:600;color:var(--text)">{len(scans)}</div>
</div>
"""), unsafe_allow_html=True)

# ── SCAN CARDS ─────────────────────────────────────────────────────────────────
risk_emoji_map = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
risk_color_map = {
    "critical": "var(--red)",
    "high": "var(--high)",
    "medium": "var(--medium)",
    "low": "var(--low)",
}

for scan in scans:
    risk = scan.get("highest_risk", "low")
    r_emoji = risk_emoji_map.get(risk, "⚪")
    r_color = risk_color_map.get(risk, "var(--text-muted)")
    scan_date = scan.get("scanned_at", "")[:16]
    scan_id = scan.get("upload_id", "")

    # Date / ID label above expander
    st.markdown(textwrap.dedent(f"""
    <div style="font-family:var(--font-mono);font-size:12px;color:var(--text-muted);margin-bottom:2px">
      {scan_date} &nbsp;·&nbsp; {scan_id}
    </div>
    """), unsafe_allow_html=True)

    pdf_name_short = scan["pdf_name"][:40]
    total_flags = scan.get("total_flags", 0)

    with st.expander(
        f"{r_emoji}  {pdf_name_short}  —  {total_flags} flags  ·  {risk.upper()}"
    ):
        # Metrics grid
        st.markdown(textwrap.dedent(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;margin-bottom:16px">
          <div style="background:var(--surface);padding:14px 16px">
            <div class="caption-label" style="margin-bottom:6px">Pages</div>
            <div style="font-family:var(--font-mono);font-size:22px;font-weight:600;color:var(--info)">{scan.get("total_pages", 0)}</div>
          </div>
          <div style="background:var(--surface);padding:14px 16px">
            <div class="caption-label" style="margin-bottom:6px">Flags</div>
            <div style="font-family:var(--font-mono);font-size:22px;font-weight:600;color:var(--text)">{total_flags}</div>
          </div>
          <div style="background:var(--surface);padding:14px 16px">
            <div class="caption-label" style="margin-bottom:6px">Risk level</div>
            <div style="font-size:15px;font-weight:700;color:{r_color}">{risk.upper()}</div>
          </div>
          <div style="background:var(--surface);padding:14px 16px">
            <div class="caption-label" style="margin-bottom:6px">Scan ID</div>
            <div style="font-family:var(--font-mono);font-size:13px;color:var(--text-muted)">{scan_id}</div>
          </div>
        </div>
        """), unsafe_allow_html=True)

        # Download report PDF
        report_path = scan.get("report_path")
        if report_path and Path(report_path).exists():
            with open(report_path, "rb") as f:
                st.download_button(
                    label="↓  Download Compliance Report",
                    data=f.read(),
                    file_name=f"compliance_{scan_id}.pdf",
                    mime="application/pdf",
                    key=f"dl_{scan_id}",
                )
        else:
            st.markdown(textwrap.dedent("""
            <div style="font-size:13px;color:var(--medium);padding:8px 0">
              ⚠ Report PDF not found (may have been deleted or moved)
            </div>
            """), unsafe_allow_html=True)

        # Full result JSON toggle
        full = get_result(scan_id)
        if full and "data" in full:
            show_json = st.toggle("Show Raw JSON Summary", key=f"json_{scan_id}")
            if show_json:
                st.json(full["data"].get("summary", {}))

        # Danger zone — delete
        st.markdown(textwrap.dedent("""
        <div style="height:1px;background:var(--border-subtle);margin:12px 0"></div>
        <div class="caption-label" style="margin-bottom:6px;color:var(--critical)">Danger zone</div>
        """), unsafe_allow_html=True)

        if st.button("Delete scan", key=f"del_{scan_id}"):
            delete_scan(scan_id)
            st.toast("Scan deleted.", icon="🗑️")
            st.rerun()

    # Spacer between scan cards
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
