# app/pages/02_rules.py
"""
Compliance Rules Editor — configure detection rules via UI.
Changes take effect on the next scan — no restart needed.
Noir Amber UI redesign.
"""
import sys
import os
# Inject project root path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
import textwrap
from config.rules import load_rules, save_rules
from app.styles.theme import GLOBAL_CSS

st.set_page_config(page_title="Detection Rules", page_icon="⟁", layout="wide", initial_sidebar_state="expanded")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── PAGE HEADER ────────────────────────────────────────────────────────────────
st.markdown(textwrap.dedent("""
<div class="page-header">
  <span class="module-label">Module 02</span>
  <h1>Detection Rules</h1>
  <p>Configure what gets flagged. Changes apply on the next scan — no restart required.</p>
</div>
<div class="notice-banner">
  ⚡️ Live config — all rules are persisted to rules.json and loaded on next pipeline run
</div>
"""), unsafe_allow_html=True)

rules = load_rules()

with st.form("compliance_rules_form"):

    # ── PII DETECTION ──────────────────────────────────────────────────────
    st.markdown(textwrap.dedent("""
    <div style="display:flex;align-items:center;gap:12px;padding:16px 0 12px;border-bottom:1px solid var(--border-subtle);margin-bottom:16px">
      <div style="width:3px;height:20px;background:var(--critical);border-radius:2px"></div>
      <div>
        <div class="caption-label" style="color:var(--critical);margin-bottom:3px">Detection module</div>
        <div style="font-size:16px;font-weight:600;color:var(--text)">PII Detection</div>
      </div>
      <span class="badge badge-critical" style="margin-left:auto">Active</span>
    </div>
    """), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        pii_enabled = st.toggle("Enable PII Detection", value=rules["pii"]["enabled"])
        detect_email = st.checkbox("Email Addresses", value=rules["pii"].get("detect_email", True))
        detect_phone = st.checkbox("Phone Numbers", value=rules["pii"].get("detect_phone", True))
        detect_ssn = st.checkbox("SSN / Aadhaar / PAN", value=rules["pii"].get("detect_ssn_aadhaar", True))
    with col2:
        detect_credit_card = st.checkbox("Credit/Debit Cards", value=rules["pii"].get("detect_credit_card", True))
        detect_address = st.checkbox("Physical Addresses", value=rules["pii"].get("detect_address", True))
        detect_dob = st.checkbox("Dates of Birth", value=rules["pii"].get("detect_dob", True))
        st.markdown('<div class="caption-label" style="margin-bottom:4px">MINIMUM CONFIDENCE THRESHOLD</div>', unsafe_allow_html=True)
        pii_confidence = st.slider(
            "Minimum PII Confidence Threshold",
            0.5, 1.0,
            value=rules["pii"].get("min_confidence", 0.75),
            step=0.05,
            help="Flags below this confidence level are ignored",
            label_visibility="collapsed",
        )

    # ── CONFIDENTIALITY DETECTION ──────────────────────────────────────────
    st.markdown(textwrap.dedent("""
    <div style="height:1px;background:var(--border-subtle);margin:24px 0"></div>
    <div style="display:flex;align-items:center;gap:12px;padding:16px 0 12px;border-bottom:1px solid var(--border-subtle);margin-bottom:16px">
      <div style="width:3px;height:20px;background:var(--high);border-radius:2px"></div>
      <div>
        <div class="caption-label" style="color:var(--high);margin-bottom:3px">Detection module</div>
        <div style="font-size:16px;font-weight:600;color:var(--text)">Confidentiality Detection</div>
      </div>
      <span class="badge badge-high" style="margin-left:auto">Active</span>
    </div>
    """), unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        conf_enabled = st.toggle("Enable Confidentiality Detection", value=rules["confidentiality"]["enabled"])
        detect_api_keys = st.checkbox("API Keys & Tokens", value=rules["confidentiality"].get("detect_api_keys", True))
        detect_passwords = st.checkbox("Passwords & Secrets", value=rules["confidentiality"].get("detect_passwords", True))
        detect_trade_secrets = st.checkbox("Trade Secrets", value=rules["confidentiality"].get("detect_trade_secrets", True))
    with col4:
        detect_financial = st.checkbox("Financial Forecasts", value=rules["confidentiality"].get("detect_financial_data", True))
        detect_ma = st.checkbox("M&A Information", value=rules["confidentiality"].get("detect_merger_acquisition", True))
        st.markdown('<div class="caption-label" style="margin-bottom:4px">MINIMUM CONFIDENCE THRESHOLD</div>', unsafe_allow_html=True)
        conf_confidence = st.slider(
            "Minimum Confidentiality Threshold",
            0.5, 1.0,
            value=rules["confidentiality"].get("min_confidence", 0.70),
            step=0.05,
            label_visibility="collapsed",
        )

    # ── CUSTOM KEYWORDS ────────────────────────────────────────────────────
    st.markdown(textwrap.dedent("""
    <div style="background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius);padding:12px 16px;margin-bottom:8px;margin-top:12px">
      <div class="caption-label" style="margin-bottom:4px">Custom keyword targeting</div>
      <div style="font-size:13px;color:var(--text-muted)">
        One keyword per line · case-insensitive · flagged as CUSTOM_KEYWORD
      </div>
    </div>
    """), unsafe_allow_html=True)

    current_keywords = "\n".join(rules.get("confidentiality", {}).get("custom_keywords", []))
    custom_keywords_text = st.text_area(
        "Custom keywords (one per line)",
        value=current_keywords,
        height=100,
        help="These words will always be flagged as CUSTOM_KEYWORD in confidentiality checks",
        label_visibility="collapsed",
    )

    # ── ENCODING & LANGUAGE ────────────────────────────────────────────────
    st.markdown(textwrap.dedent("""
    <div style="height:1px;background:var(--border-subtle);margin:24px 0"></div>
    <div style="display:flex;align-items:center;gap:12px;padding:16px 0 12px;border-bottom:1px solid var(--border-subtle);margin-bottom:16px">
      <div style="width:3px;height:20px;background:var(--info);border-radius:2px"></div>
      <div>
        <div class="caption-label" style="color:var(--info);margin-bottom:3px">Detection module</div>
        <div style="font-size:16px;font-weight:600;color:var(--text)">Encoding &amp; Language</div>
      </div>
      <span class="badge badge-info" style="margin-left:auto">Active</span>
    </div>
    """), unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        enc_enabled = st.toggle("Enable Encoding Check", value=rules["encoding"]["enabled"])
        require_utf8 = st.checkbox("Require UTF-8 Encoding", value=rules["encoding"].get("require_utf8", True))
        flag_non_ascii = st.checkbox("Flag Non-ASCII Characters", value=rules["encoding"].get("flag_non_ascii", True))
    with col6:
        non_ascii_threshold = st.number_input(
            "Non-ASCII character threshold (flag if count exceeds)",
            min_value=1, max_value=100,
            value=rules["encoding"].get("non_ascii_threshold", 5),
        )
        st.markdown('<div class="caption-label" style="margin-bottom:4px">MINIMUM CONFIDENCE THRESHOLD</div>', unsafe_allow_html=True)
        enc_confidence = st.slider(
            "Min Encoding Detection Confidence",
            0.5, 1.0,
            value=rules["encoding"].get("min_encoding_confidence", 0.85),
            step=0.05,
            label_visibility="collapsed",
        )

    # ── ABUSE & UNLAWFUL CONTENT ───────────────────────────────────────────
    st.markdown(textwrap.dedent("""
    <div style="height:1px;background:var(--border-subtle);margin:24px 0"></div>
    <div style="display:flex;align-items:center;gap:12px;padding:16px 0 12px;border-bottom:1px solid var(--border-subtle);margin-bottom:16px">
      <div style="width:3px;height:20px;background:var(--medium);border-radius:2px"></div>
      <div>
        <div class="caption-label" style="color:var(--medium);margin-bottom:3px">Detection module</div>
        <div style="font-size:16px;font-weight:600;color:var(--text)">Abuse &amp; Unlawful Content</div>
      </div>
      <span class="badge badge-medium" style="margin-left:auto">Active</span>
    </div>
    """), unsafe_allow_html=True)

    col7, col8 = st.columns(2)
    with col7:
        abuse_enabled = st.toggle("Enable Abuse Detection", value=rules["abuse"]["enabled"])
        detect_hate = st.checkbox("Hate Speech", value=rules["abuse"].get("detect_hate_speech", True))
        detect_sexual = st.checkbox("Sexual Content", value=rules["abuse"].get("detect_sexual_content", True))
        detect_violence = st.checkbox("Violence Incitement", value=rules["abuse"].get("detect_violence_incitement", True))
    with col8:
        detect_illegal = st.checkbox("Illegal Content", value=rules["abuse"].get("detect_illegal_content", True))
        detect_harassment = st.checkbox("Harassment", value=rules["abuse"].get("detect_harassment", True))
        sensitivity = st.select_slider(
            "AI Detection Sensitivity",
            options=["low", "medium", "high", "very_high"],
            value=rules.get("sensitivity", "high"),
        )

    # ── SAVE BUTTON ────────────────────────────────────────────────────────
    st.markdown(textwrap.dedent("""
    <div style="height:1px;background:var(--border-subtle);margin:24px 0"></div>
    <div style="background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius);padding:16px;margin-bottom:16px;display:flex;justify-content:space-between;align-items:center">
      <div>
        <div class="caption-label" style="margin-bottom:4px">Save configuration</div>
        <div style="font-size:13px;color:var(--text-muted)">Changes persist to rules.json immediately</div>
      </div>
      <div style="font-size:12px;color:var(--text-muted)">Next scan will use new rules</div>
    </div>
    """), unsafe_allow_html=True)

    submitted = st.form_submit_button("Save Rules", type="primary", use_container_width=True)

if submitted:
    custom_keywords_list = [
        kw.strip() for kw in custom_keywords_text.split("\n")
        if kw.strip()
    ]

    updated_rules = {
        **rules,
        "sensitivity": sensitivity,
        "pii": {
            "enabled": pii_enabled,
            "detect_email": detect_email,
            "detect_phone": detect_phone,
            "detect_ssn_aadhaar": detect_ssn,
            "detect_credit_card": detect_credit_card,
            "detect_address": detect_address,
            "detect_dob": detect_dob,
            "min_confidence": pii_confidence,
            "risk_threshold": "medium",
        },
        "confidentiality": {
            "enabled": conf_enabled,
            "detect_api_keys": detect_api_keys,
            "detect_passwords": detect_passwords,
            "detect_trade_secrets": detect_trade_secrets,
            "detect_financial_data": detect_financial,
            "detect_merger_acquisition": detect_ma,
            "custom_keywords": custom_keywords_list,
            "min_confidence": conf_confidence,
        },
        "encoding": {
            "enabled": enc_enabled,
            "require_utf8": require_utf8,
            "allowed_languages": ["en"],
            "min_encoding_confidence": enc_confidence,
            "flag_non_ascii": flag_non_ascii,
            "non_ascii_threshold": non_ascii_threshold,
        },
        "abuse": {
            "enabled": abuse_enabled,
            "detect_hate_speech": detect_hate,
            "detect_sexual_content": detect_sexual,
            "detect_violence_incitement": detect_violence,
            "detect_illegal_content": detect_illegal,
            "detect_harassment": detect_harassment,
            "sensitivity_level": sensitivity,
            "zero_tolerance_categories": ["child_safety", "terrorism"],
        },
    }

    save_rules(updated_rules)

    st.markdown(textwrap.dedent("""
    <div style="background:var(--low-bg);border:1px solid var(--low-border);border-radius:var(--radius);padding:14px 18px;display:flex;align-items:center;gap:12px;animation:fadeSlideUp 0.3s ease">
      <span style="font-size:18px;color:var(--low)">&#10003;</span>
      <div>
        <div style="font-size:14px;font-weight:600;color:var(--low);margin-bottom:2px">Rules saved successfully</div>
        <div style="font-size:13px;color:var(--text-muted)">New detection rules will apply on the next scan run.</div>
      </div>
    </div>
    """), unsafe_allow_html=True)

# ── RULE SANDBOX ─────────────────────────────────────────────────────────────
st.markdown(textwrap.dedent("""
<div style="height:1px;background:var(--border-subtle);margin:32px 0 24px"></div>
<div class="caption-label">Rule sandbox (test environment)</div>
<div style="font-size:16px;font-weight:600;color:var(--text);margin:8px 0 16px">Test Custom Keywords</div>
"""), unsafe_allow_html=True)

test_string = st.text_input("Enter a sample text to test if your currently saved custom keywords will catch it:", key="sandbox_input")
if test_string:
    import re
    saved_rules = load_rules()
    kws = saved_rules.get("confidentiality", {}).get("custom_keywords", [])
    
    matches = []
    if kws:
        for kw in kws:
            if re.search(r'\\b' + re.escape(kw) + r'\\b', test_string, re.IGNORECASE):
                matches.append(kw)
            elif kw.lower() in test_string.lower(): # Fallback if boundary fails for special chars
                if kw not in matches:
                    matches.append(kw)
                
    if matches:
        st.markdown(textwrap.dedent(f"""
        <div style="background:var(--critical-bg);border-left:3px solid var(--critical);border-radius:0 var(--radius) var(--radius) 0;padding:12px 16px;margin-top:8px">
          <span style="font-size:14px;font-weight:500;color:var(--critical)">🚩 Match found: {', '.join(matches)}</span>
        </div>
        """), unsafe_allow_html=True)
    else:
        st.markdown(textwrap.dedent("""
        <div style="background:var(--low-bg);border-left:3px solid var(--low);border-radius:0 var(--radius) var(--radius) 0;padding:12px 16px;margin-top:8px">
          <span style="font-size:14px;font-weight:500;color:var(--low)">✓ No matches found (pass)</span>
        </div>
        """), unsafe_allow_html=True)
