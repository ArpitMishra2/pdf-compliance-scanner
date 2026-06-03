# app/main.py
"""
Streamlit entry point — enterprise landing page.
"""
import sys
import os
# Inject project root path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import textwrap
from app.styles.theme import GLOBAL_CSS

st.set_page_config(
    page_title="PDF Compliance Scanner",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

from app.components.ui import render_common_sidebar

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
render_common_sidebar()

# ── PAGE HEADER ────────────────────────────────────────────────────────────────
st.markdown(textwrap.dedent("""
<div class="page-header" style="padding-bottom:32px">
  <span class="module-label">Document compliance platform</span>
  <h1 style="font-size:32px;margin-bottom:10px">PDF Compliance Scanner</h1>
  <p style="font-size:16px;max-width:560px">
    Automated detection of PII, confidential data, encoding issues, and abusive content —
    with AI-powered analysis and detailed compliance reports.
  </p>
</div>
"""), unsafe_allow_html=True)

# ── FEATURE CARDS (2×2 grid) ──────────────────────────────────────────────────
cards = [
    {
        "icon": "🔍",
        "icon_bg": "rgba(239,68,68,0.12)",
        "badge_class": "badge-critical",
        "badge_label": "Critical",
        "title": "PII Detection",
        "desc": "Emails, phone numbers, Aadhaar, SSN, passports — nothing slips past. Regex speed combined with AI semantic understanding.",
        "stat": "12 pattern types · dual-engine",
        "delay": "0s",
    },
    {
        "icon": "🔐",
        "icon_bg": "rgba(249,115,22,0.12)",
        "badge_class": "badge-high",
        "badge_label": "High",
        "title": "Confidentiality",
        "desc": "AWS keys, GitHub tokens, passwords, salary data. If it shouldn't be in the document, it won't stay undetected.",
        "stat": "15 credential patterns · AI semantic",
        "delay": "0.08s",
    },
    {
        "icon": "📝",
        "icon_bg": "rgba(56,189,248,0.12)",
        "badge_class": "badge-info",
        "badge_label": "Medium",
        "title": "Encoding Guard",
        "desc": "UTF-8 validation, OCR corruption detection, multilingual content analysis. Documents should be consistent and readable.",
        "stat": "6 check types · rule-based",
        "delay": "0.16s",
    },
    {
        "icon": "🚨",
        "icon_bg": "rgba(245,158,11,0.12)",
        "badge_class": "badge-medium",
        "badge_label": "Critical",
        "title": "Abuse Detection",
        "desc": "Threats, hate speech, harassment, illegal content. Three detection layers for comprehensive protection.",
        "stat": "3-layer detection · zero-tolerance",
        "delay": "0.24s",
    },
]

row1_l, row1_r = st.columns(2)
row2_l, row2_r = st.columns(2)
cols = [row1_l, row1_r, row2_l, row2_r]

for col, card in zip(cols, cards):
    with col:
        st.markdown(textwrap.dedent(f"""
        <div class="feature-card animate-fadein" style="animation-delay:{card['delay']}">
          <div class="card-icon-line">
            <div class="card-icon" style="background:{card['icon_bg']}">{card['icon']}</div>
            <span class="badge {card['badge_class']}">{card['badge_label']}</span>
          </div>
          <h3 class="card-title">{card['title']}</h3>
          <p class="card-desc">{card['desc']}</p>
          <div class="card-footer-line">
            <span style="font-family:var(--font-mono);font-size:12px;color:var(--text-muted)">{card['stat']}</span>
          </div>
        </div>
        """), unsafe_allow_html=True)

# ── STATS BAR ─────────────────────────────────────────────────────────────────
st.markdown(textwrap.dedent("""
<div class="stats-bar animate-fadein-2">
  <div class="stats-bar-item">
    <div class="stats-bar-value">12</div>
    <div class="stats-bar-label">PII pattern types</div>
  </div>
  <div class="stats-bar-item">
    <div class="stats-bar-value">15</div>
    <div class="stats-bar-label">Credential patterns</div>
  </div>
  <div class="stats-bar-item">
    <div class="stats-bar-value">3×</div>
    <div class="stats-bar-label">Abuse detection layers</div>
  </div>
  <div class="stats-bar-item">
    <div class="stats-bar-value" style="color:var(--indigo)">LangGraph</div>
    <div class="stats-bar-label">Orchestration engine</div>
  </div>
</div>
"""), unsafe_allow_html=True)

# ── BOTTOM NAVIGATION HINT ────────────────────────────────────────────────────
st.markdown(textwrap.dedent("""
<div style="text-align:center;padding:36px 0 12px;animation:fadeSlideUp 0.4s ease 0.3s both">
  <p style="font-family:var(--font-sans);font-size:14px;color:var(--text-muted)">
    Use the sidebar to navigate between modules and begin scanning
  </p>
</div>
"""), unsafe_allow_html=True)
