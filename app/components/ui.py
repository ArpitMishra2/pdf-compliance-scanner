# app/components/ui.py
"""
Reusable HTML component functions for the PDF Compliance Scanner.
Each function returns an HTML string for st.markdown(html, unsafe_allow_html=True).
"""

def risk_badge(risk_level: str) -> str:
    """Returns a styled badge span for critical/high/medium/low."""
    level = risk_level.lower()
    config = {
        "critical": ("badge-critical", "●"),
        "high":     ("badge-high",     "●"),
        "medium":   ("badge-medium",   "●"),
        "low":      ("badge-low",      "●"),
        "info":     ("badge-info",     "●"),
    }
    cls, dot = config.get(level, ("badge-info", "●"))
    return f'<span class="badge {cls}">{dot} {level.upper()}</span>'


def section_header(module_num: str, title: str, subtitle: str, accent_color: str = "var(--indigo)") -> str:
    """Returns the standard page header HTML with module label, title, subtitle."""
    return (
        f'<div class="page-header">'
        f'<span class="module-label">Module {module_num}</span>'
        f'<h1>{title}</h1>'
        f'<p>{subtitle}</p>'
        f'</div>'
    )


def metric_grid(metrics: list) -> str:
    """
    Renders a CSS grid of metric cells.
    metrics: list of {"label": str, "value": str/int, "color": str}
    """
    n = len(metrics)
    cells = ""
    for m in metrics:
        cells += (
            f'<div style="background:var(--surface);padding:18px 16px;text-align:center">'
            f'<div class="caption-label" style="margin-bottom:8px">{m["label"]}</div>'
            f'<div style="font-family:var(--font-mono);font-size:26px;font-weight:600;color:{m["color"]}">{m["value"]}</div>'
            f'</div>'
        )
    return (
        f'<div style="display:grid;grid-template-columns:repeat({n},1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;margin-bottom:24px">'
        f'{cells}'
        f'</div>'
    )


def alert_banner(message: str, alert_type: str = "info") -> str:
    """Returns a styled banner with left border and icon."""
    config = {
        "info":    ("var(--info)",     "var(--info-bg)",     "ℹ"),
        "warning": ("var(--medium)",   "var(--medium-bg)",   "⚠"),
        "error":   ("var(--critical)", "var(--critical-bg)", "✕"),
        "success": ("var(--low)",      "var(--low-bg)",      "✓"),
    }
    color, bg, icon = config.get(alert_type, config["info"])
    return (
        f'<div style="background:{bg};border-left:3px solid {color};border-radius:0 var(--radius) var(--radius) 0;padding:12px 16px;display:flex;align-items:center;gap:10px;margin:8px 0">'
        f'<span style="font-size:16px;color:{color}">{icon}</span>'
        f'<span style="font-family:var(--font-sans);font-size:14px;color:var(--text)">{message}</span>'
        f'</div>'
    )


def loading_message(message: str) -> str:
    """Returns an animated loading indicator."""
    return (
        f'<div style="font-family:var(--font-sans);font-size:14px;color:var(--text-secondary);'
        f'display:flex;align-items:center;gap:8px;padding:4px 0">'
        f'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--indigo);'
        f'animation:pulseDot 1.2s ease-in-out infinite"></span>'
        f'{message}'
        f'</div>'
    )


def section_divider(label: str = "") -> str:
    """Returns a full-width divider, optionally with a centered label."""
    if label:
        return (
            f'<div style="display:flex;align-items:center;gap:12px;margin:24px 0">'
            f'<div style="flex:1;height:1px;background:var(--border-subtle)"></div>'
            f'<div class="caption-label">{label}</div>'
            f'<div style="flex:1;height:1px;background:var(--border-subtle)"></div>'
            f'</div>'
        )
    return '<div style="height:1px;background:var(--border-subtle);margin:28px 0"></div>'


def flag_count_row(pii: int, confidential: int, encoding: int, abuse: int) -> str:
    """Returns a 4-cell horizontal strip with colored left accent bars."""
    return (
        f'<div class="caption-label" style="margin-bottom:10px">Issue breakdown</div>'
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;margin-bottom:24px">'
        f'<div style="background:var(--surface);padding:16px;border-left:3px solid var(--critical)">'
        f'<div class="caption-label" style="color:var(--critical);margin-bottom:6px">PII Flags</div>'
        f'<div style="font-family:var(--font-mono);font-size:28px;font-weight:600;color:var(--critical)">{pii}</div></div>'

        f'<div style="background:var(--surface);padding:16px;border-left:3px solid var(--high)">'
        f'<div class="caption-label" style="color:var(--high);margin-bottom:6px">Confidential</div>'
        f'<div style="font-family:var(--font-mono);font-size:28px;font-weight:600;color:var(--high)">{confidential}</div></div>'

        f'<div style="background:var(--surface);padding:16px;border-left:3px solid var(--info)">'
        f'<div class="caption-label" style="color:var(--info);margin-bottom:6px">Encoding</div>'
        f'<div style="font-family:var(--font-mono);font-size:28px;font-weight:600;color:var(--info)">{encoding}</div></div>'

        f'<div style="background:var(--surface);padding:16px;border-left:3px solid var(--medium)">'
        f'<div class="caption-label" style="color:var(--medium);margin-bottom:6px">Abuse</div>'
        f'<div style="font-family:var(--font-mono);font-size:28px;font-weight:600;color:var(--medium)">{abuse}</div></div>'

        f'</div>'
    )


def empty_state(title: str, subtitle: str, icon: str = "○") -> str:
    """Returns a centered empty state with icon and description."""
    return (
        f'<div style="text-align:center;padding:64px 24px;border:1px dashed var(--border);border-radius:var(--radius-xl);margin-top:24px">'
        f'<div style="font-size:40px;color:var(--border-bright);margin-bottom:16px">{icon}</div>'
        f'<div style="font-family:var(--font-sans);font-size:15px;font-weight:600;color:var(--text-secondary);margin-bottom:6px">{title}</div>'
        f'<div style="font-family:var(--font-sans);font-size:14px;color:var(--text-muted)">{subtitle}</div>'
        f'</div>'
    )


def terminal_block(lines: list, title: str = "Output") -> str:
    """Returns an HTML output block with colored status lines."""
    line_divs = ""
    for line in lines:
        s = line.strip()
        if s.startswith("ERROR"):
            color = "var(--critical)"
        elif s.startswith("WARNING"):
            color = "var(--medium)"
        elif s.startswith("OK"):
            color = "var(--low)"
        else:
            color = "var(--text-muted)"
        line_divs += f'<div style="color:{color};line-height:1.8">{line}</div>'

    return (
        f'<div style="border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;margin:12px 0">'
        f'<div style="background:var(--surface-2);padding:10px 16px;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--border)">'
        f'<div style="display:flex;gap:6px">'
        f'<div style="width:10px;height:10px;border-radius:50%;background:#FF5F57"></div>'
        f'<div style="width:10px;height:10px;border-radius:50%;background:#FEBC2E"></div>'
        f'<div style="width:10px;height:10px;border-radius:50%;background:#28C840"></div>'
        f'</div>'
        f'<div style="font-family:var(--font-sans);font-size:12px;font-weight:500;color:var(--text-muted)">{title}</div>'
        f'</div>'
        f'<div style="background:var(--bg);padding:16px;font-family:var(--font-mono);font-size:13px">{line_divs}</div>'
        f'</div>'
    )


def scan_result_header(
    pdf_name: str, upload_id: str, elapsed: float, highest_risk: str
) -> str:
    """Returns a styled scan completion header with filename, ID, timing, and risk badge."""
    badge_html = risk_badge(highest_risk)
    return (
        f'<div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-xl);'
        f'padding:20px 24px;display:flex;justify-content:space-between;align-items:center;margin:16px 0;'
        f'box-shadow:var(--shadow-sm)">'

        f'<div>'
        f'<div class="caption-label" style="margin-bottom:6px">Scan complete</div>'
        f'<div style="font-family:var(--font-sans);font-size:17px;font-weight:600;color:var(--text);margin-bottom:4px">{pdf_name}</div>'
        f'<div style="font-family:var(--font-mono);font-size:13px;color:var(--text-muted)">'
        f'ID: {upload_id} &nbsp;·&nbsp; {elapsed:.1f}s</div>'
        f'</div>'

        f'<div style="text-align:right">'
        f'{badge_html}'
        f'<div class="caption-label" style="margin-top:6px">Highest risk level</div>'
        f'</div>'

        f'</div>'
    )


def render_common_sidebar():
    """Renders the standard sidebar branding and API settings expander."""
    import streamlit as st
    import textwrap
    import os

    with st.sidebar:
        st.markdown(textwrap.dedent("""
        <div style="padding: 28px 0 20px">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
            <div style="width:28px;height:28px;border-radius:6px;background:var(--indigo);
              display:flex;align-items:center;justify-content:center;font-size:14px">🛡️</div>
            <div>
              <div style="font-family:var(--font-sans);font-size:14px;font-weight:700;color:var(--text);line-height:1.2">
                Compliance Scanner
              </div>
              <div style="font-family:var(--font-sans);font-size:11px;color:var(--text-muted)">
                AI-Powered Document Guard
              </div>
            </div>
          </div>
        </div>
        """), unsafe_allow_html=True)

        with st.expander("⚙ API Configuration", expanded=False):
            st.markdown("<div style='font-size:13px;color:var(--text-muted);margin-bottom:12px'>Override .env keys at runtime</div>", unsafe_allow_html=True)

            groq_key = st.text_input("Groq API Key", value=os.environ.get("GROQ_API_KEY", ""), type="password", help="Required for Llama3 models")
            if groq_key:
                os.environ["GROQ_API_KEY"] = groq_key

            gemini_key = st.text_input("Gemini API Key", value=os.environ.get("GOOGLE_API_KEY", ""), type="password", help="Required if AI_PROVIDER=gemini")
            if gemini_key:
                os.environ["GOOGLE_API_KEY"] = gemini_key

            anthropic_key = st.text_input("Anthropic API Key", value=os.environ.get("ANTHROPIC_API_KEY", ""), type="password", help="Required if AI_PROVIDER=anthropic")
            if anthropic_key:
                os.environ["ANTHROPIC_API_KEY"] = anthropic_key

        st.markdown(textwrap.dedent("""
        <div style="margin-top:12px;padding-top:16px;border-top:1px solid var(--border-subtle)">
          <div class="caption-label" style="margin-bottom:10px">Pipeline Stack</div>
          <div style="font-family:var(--font-sans);font-size:13px;color:var(--text-muted);line-height:2">
            Groq Llama 3<br>
            LangGraph DAG<br>
            PyMuPDF · ReportLab<br>
            ChromaDB RAG<br>
            SQLite Storage
          </div>
          <div style="margin-top:16px;display:flex;align-items:center;gap:6px">
            <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--low);animation:pulseDot 2s ease-in-out infinite"></span>
            <span style="font-family:var(--font-sans);font-size:12px;color:var(--text-muted)">All systems operational</span>
          </div>
        </div>
        """), unsafe_allow_html=True)
