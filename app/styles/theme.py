GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── DESIGN TOKENS ─────────────────────────────────────────────────────────── */
:root {
    /* Backgrounds */
    --bg:            #0F1117;
    --surface:       #1C1F2B;
    --surface-2:     #252836;
    --surface-3:     #2E3249;

    /* Borders */
    --border:        #2E3347;
    --border-subtle: #242736;
    --border-bright: #3D4463;

    /* Primary (Indigo) */
    --indigo:        #6366F1;
    --indigo-dim:    #4F52C8;
    --indigo-glow:   rgba(99,102,241,0.15);
    --indigo-subtle: rgba(99,102,241,0.08);

    /* Text */
    --text:          #E2E8F0;
    --text-secondary:#94A3B8;
    --text-muted:    #64748B;
    --text-disabled: #3D4A5C;

    /* Semantic Colors */
    --critical:      #EF4444;
    --critical-bg:   rgba(239,68,68,0.10);
    --critical-border:rgba(239,68,68,0.30);

    --high:          #F97316;
    --high-bg:       rgba(249,115,22,0.10);
    --high-border:   rgba(249,115,22,0.30);

    --medium:        #F59E0B;
    --medium-bg:     rgba(245,158,11,0.10);
    --medium-border: rgba(245,158,11,0.30);

    --low:           #22C55E;
    --low-bg:        rgba(34,197,94,0.10);
    --low-border:    rgba(34,197,94,0.30);

    --info:          #38BDF8;
    --info-bg:       rgba(56,189,248,0.10);
    --info-border:   rgba(56,189,248,0.30);

    /* Typography */
    --font-sans:     'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono:     'JetBrains Mono', 'Fira Code', monospace;

    /* Radius */
    --radius-sm:     4px;
    --radius:        6px;
    --radius-lg:     10px;
    --radius-xl:     14px;

    /* Shadows */
    --shadow-sm:     0 1px 2px rgba(0,0,0,0.3);
    --shadow:        0 2px 8px rgba(0,0,0,0.4);
    --shadow-lg:     0 8px 24px rgba(0,0,0,0.5);
}

/* ── 1. STREAMLIT CHROME ────────────────────────────────────────────────────── */
#MainMenu, header, footer {
    visibility: hidden !important;
}
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 100% !important;
}
body, .stApp {
    background: var(--bg) !important;
    font-family: var(--font-sans) !important;
}
body, .stApp, .stApp * {
    font-family: var(--font-sans);
    color: var(--text);
    -webkit-font-smoothing: antialiased;
}

/* ── 2. SIDEBAR ─────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] .stMarkdown h4 {
    font-family: var(--font-sans) !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    color: var(--text-secondary) !important;
}
/* Sidebar nav links */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    border-left: 2px solid transparent;
    padding-left: 10px;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    transition: all 0.12s ease;
    font-size: 14px;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label[data-selected="true"],
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    border-left: 2px solid var(--indigo) !important;
    background: var(--indigo-subtle) !important;
    color: var(--text) !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.04) !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label input {
    display: none;
}

/* ── 3. BUTTONS ─────────────────────────────────────────────────────────────── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border-bright) !important;
    color: var(--text-secondary) !important;
    font-family: var(--font-sans) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    padding: 8px 20px !important;
    border-radius: var(--radius) !important;
    transition: all 0.12s ease !important;
    box-shadow: var(--shadow-sm) !important;
}
.stButton > button:hover {
    background: var(--surface-2) !important;
    border-color: var(--border-bright) !important;
    color: var(--text) !important;
}
.stButton > button[kind="primary"],
.stButton > button.primary-btn {
    background: var(--indigo) !important;
    color: #fff !important;
    border-color: var(--indigo) !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(99,102,241,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--indigo-dim) !important;
    border-color: var(--indigo-dim) !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.4) !important;
}

/* ── 4. FILE UPLOADER ───────────────────────────────────────────────────────── */
[data-testid="stFileUploader"] > section,
.stFileUploader section {
    border: 1.5px dashed var(--border-bright) !important;
    background: var(--surface) !important;
    border-radius: var(--radius-lg) !important;
    padding: 28px !important;
    transition: border-color 0.15s ease, background 0.15s ease !important;
}
[data-testid="stFileUploader"] > section:hover,
.stFileUploader section:hover {
    border-color: var(--indigo) !important;
    background: var(--indigo-subtle) !important;
}
.stFileUploader section small {
    color: var(--text-muted) !important;
    font-family: var(--font-sans) !important;
}

/* ── 5. METRIC CARDS ────────────────────────────────────────────────────────── */
div[data-testid="stMetric"],
div[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 18px 22px !important;
    box-shadow: var(--shadow-sm) !important;
}
div[data-testid="stMetric"] label,
div[data-testid="stMetricLabel"] {
    font-family: var(--font-sans) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] {
    font-family: var(--font-mono) !important;
    font-size: 30px !important;
    color: var(--text) !important;
    font-weight: 600 !important;
}

/* ── 6. DATAFRAME ───────────────────────────────────────────────────────────── */
div[data-testid="stDataFrame"],
.stDataFrame {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
}
.stDataFrame thead th {
    background: var(--surface-2) !important;
    color: var(--text-secondary) !important;
    font-family: var(--font-sans) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border) !important;
}
.stDataFrame tbody tr:nth-child(even) {
    background: rgba(255,255,255,0.02) !important;
}
.stDataFrame tbody tr:hover {
    background: var(--indigo-subtle) !important;
}
.stDataFrame tbody td {
    font-family: var(--font-sans) !important;
    font-size: 14px !important;
    color: var(--text) !important;
    border-color: var(--border-subtle) !important;
}

/* ── 7. PROGRESS BAR ────────────────────────────────────────────────────────── */
.stProgress > div > div > div > div {
    background: var(--indigo) !important;
    border-radius: 100px !important;
}
.stProgress > div > div {
    background: var(--border) !important;
    border-radius: 100px !important;
}

/* ── 8. EXPANDER ────────────────────────────────────────────────────────────── */
.streamlit-expanderHeader,
div[data-testid="stExpander"] summary {
    font-family: var(--font-sans) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: var(--text) !important;
}
div[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--surface) !important;
    box-shadow: var(--shadow-sm) !important;
}
div[data-testid="stExpander"]:hover {
    border-color: var(--border-bright) !important;
}

/* ── 9. ALERTS ──────────────────────────────────────────────────────────────── */
div[data-testid="stAlert"][data-baseweb*="notification"] {
    border-radius: var(--radius) !important;
}
.stAlert .st-emotion-cache-icon,
.stAlert svg {
    display: none !important;
}
div[role="alert"].stInfo,
div[data-testid="stNotification"][kind="info"] {
    background: var(--info-bg) !important;
    border-left: 3px solid var(--info) !important;
    border-radius: 0 var(--radius) var(--radius) 0 !important;
    color: var(--text) !important;
}
div[role="alert"].stWarning,
div[data-testid="stNotification"][kind="warning"] {
    background: var(--medium-bg) !important;
    border-left: 3px solid var(--medium) !important;
    border-radius: 0 var(--radius) var(--radius) 0 !important;
    color: var(--text) !important;
}
div[role="alert"].stError,
div[data-testid="stNotification"][kind="error"] {
    background: var(--critical-bg) !important;
    border-left: 3px solid var(--critical) !important;
    border-radius: 0 var(--radius) var(--radius) 0 !important;
    color: var(--text) !important;
}
div[role="alert"].stSuccess,
div[data-testid="stNotification"][kind="success"] {
    background: var(--low-bg) !important;
    border-left: 3px solid var(--low) !important;
    border-radius: 0 var(--radius) var(--radius) 0 !important;
    color: var(--text) !important;
}

/* ── 10. SELECT / MULTISELECT ───────────────────────────────────────────────── */
.stSelectbox, .stMultiSelect {
    background: var(--surface) !important;
}
.stSelectbox > div, .stMultiSelect > div {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--surface) !important;
}
.stSelectbox > div:focus-within, .stSelectbox > div:hover,
.stMultiSelect > div:focus-within, .stMultiSelect > div:hover {
    border-color: var(--indigo) !important;
    box-shadow: 0 0 0 3px var(--indigo-glow) !important;
}
.stMultiSelect span[data-baseweb="tag"] {
    background: var(--indigo-subtle) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    color: #A5B4FC !important;
    font-family: var(--font-sans) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    border-radius: 100px !important;
}

/* ── 11. SLIDER ─────────────────────────────────────────────────────────────── */
.stSlider > div > div > div {
    background: var(--border) !important;
}
.stSlider > div > div > div > div {
    background: var(--indigo) !important;
}
.stSlider > div > div > div > div > div {
    background: var(--indigo) !important;
    border: 2px solid var(--bg) !important;
    width: 16px !important;
    height: 16px !important;
    border-radius: 50% !important;
    box-shadow: 0 0 0 3px var(--indigo-glow) !important;
}

/* ── 12. TOGGLE ─────────────────────────────────────────────────────────────── */
div[data-testid="stToggle"] label span[data-testid="stToggleSlider"] {
    background: var(--border-bright) !important;
}
div[data-testid="stToggle"] label input:checked + span[data-testid="stToggleSlider"] {
    background: var(--indigo) !important;
}

/* ── 13. FORM ───────────────────────────────────────────────────────────────── */
div[data-testid="stForm"] {
    border: 1px solid var(--border) !important;
    background: var(--surface) !important;
    border-radius: var(--radius-lg) !important;
    padding: 28px !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── 14. TEXT INPUTS ────────────────────────────────────────────────────────── */
.stTextInput > div > div input,
.stTextArea > div > div textarea {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: var(--font-sans) !important;
    font-size: 14px !important;
}
.stTextInput > div > div input:focus,
.stTextArea > div > div textarea:focus {
    border-color: var(--indigo) !important;
    box-shadow: 0 0 0 3px var(--indigo-glow) !important;
}
.stTextInput > div > div input::placeholder,
.stTextArea > div > div textarea::placeholder {
    color: var(--text-disabled) !important;
}

/* ── 15. NUMBER INPUT ───────────────────────────────────────────────────────── */
.stNumberInput > div > div input {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
    font-size: 14px !important;
}

/* ── 16. CUSTOM SCROLLBAR ───────────────────────────────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: var(--bg);
}
::-webkit-scrollbar-thumb {
    background: var(--border-bright);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--indigo);
}

/* ── 17. ANIMATIONS ─────────────────────────────────────────────────────────── */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes pulseIndigo {
    0%, 100% { box-shadow: 0 0 0 0 rgba(99,102,241,0); }
    50%       { box-shadow: 0 0 0 6px rgba(99,102,241,0.15); }
}
@keyframes pulseDot {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}
@keyframes ticker {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
}

/* ── 18. UTILITY CLASSES ────────────────────────────────────────────────────── */

/* Badges — pill style */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    font-family: var(--font-sans);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0;
    border-radius: 100px;
    white-space: nowrap;
}
.badge-critical {
    background: var(--critical-bg);
    color: #FCA5A5;
    border: 1px solid var(--critical-border);
}
.badge-high {
    background: var(--high-bg);
    color: #FDBA74;
    border: 1px solid var(--high-border);
}
.badge-medium {
    background: var(--medium-bg);
    color: #FCD34D;
    border: 1px solid var(--medium-border);
}
.badge-low {
    background: var(--low-bg);
    color: #86EFAC;
    border: 1px solid var(--low-border);
}
.badge-info {
    background: var(--info-bg);
    color: #7DD3FC;
    border: 1px solid var(--info-border);
}
.badge-indigo {
    background: var(--indigo-subtle);
    color: #A5B4FC;
    border: 1px solid rgba(99,102,241,0.3);
}

/* Typography helpers */
.mono {
    font-family: var(--font-mono) !important;
}
.label-xs {
    font-family: var(--font-sans);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-muted);
}
.caption-label {
    font-family: var(--font-sans);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-muted);
}

/* Animation utilities */
.animate-fadein {
    animation: fadeSlideUp 0.35s ease both;
}
.animate-fadein-2 {
    animation: fadeSlideUp 0.35s ease 0.08s both;
}
.animate-fadein-3 {
    animation: fadeSlideUp 0.35s ease 0.16s both;
}

/* ── 19. FEATURE CARDS (landing page) ───────────────────────────────────────── */
.feature-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 24px;
    transition: border-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
    cursor: default;
    height: 100%;
}
.feature-card:hover {
    border-color: var(--indigo);
    box-shadow: 0 0 0 1px var(--indigo), var(--shadow-lg);
    transform: translateY(-2px);
}
.feature-card .card-icon {
    width: 38px;
    height: 38px;
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-bottom: 14px;
}
.feature-card .card-title {
    font-family: var(--font-sans);
    font-size: 15px;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 8px;
    letter-spacing: 0;
}
.feature-card .card-desc {
    font-family: var(--font-sans);
    font-size: 14px;
    color: var(--text-muted);
    line-height: 1.65;
    margin: 0 0 16px;
}
.feature-card .card-icon-line {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
}
.feature-card .card-footer-line {
    padding-top: 14px;
    border-top: 1px solid var(--border-subtle);
}

/* ── 20. STATS BAR (landing page) ───────────────────────────────────────────── */
.stats-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin-top: 28px;
}
.stats-bar-item {
    background: var(--surface);
    padding: 18px 20px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.stats-bar-value {
    font-family: var(--font-mono);
    font-size: 22px;
    font-weight: 600;
    color: var(--text);
}
.stats-bar-label {
    font-family: var(--font-sans);
    font-size: 12px;
    color: var(--text-muted);
}

/* ── 21. PAGE LINK (sidebar nav) ────────────────────────────────────────────── */
a[data-testid="stPageLink-NavLink"] {
    font-family: var(--font-sans) !important;
    font-size: 14px !important;
    font-weight: 450 !important;
    letter-spacing: 0 !important;
    color: var(--text-muted) !important;
    border-left: 2px solid transparent;
    padding-left: 10px !important;
    transition: all 0.12s ease;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0 !important;
}
a[data-testid="stPageLink-NavLink"]:hover {
    color: var(--text) !important;
    border-left-color: var(--border-bright);
    background: rgba(255,255,255,0.04) !important;
}

/* ── 22. DOWNLOAD BUTTON ────────────────────────────────────────────────────── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid var(--border-bright) !important;
    color: var(--text-secondary) !important;
    font-family: var(--font-sans) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    padding: 8px 20px !important;
    border-radius: var(--radius) !important;
    transition: all 0.12s ease !important;
}
.stDownloadButton > button:hover {
    background: var(--indigo) !important;
    border-color: var(--indigo) !important;
    color: #fff !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.35) !important;
}

/* ── 23. TABS ───────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid var(--border);
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-sans);
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0;
    text-transform: none;
    color: var(--text-muted);
    padding: 10px 18px;
    border-bottom: 2px solid transparent;
    transition: color 0.12s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text);
}
.stTabs [aria-selected="true"] {
    color: var(--text) !important;
    border-bottom-color: var(--indigo) !important;
    font-weight: 600 !important;
}

/* ── 24. PLOTLY CHART CONTAINER ─────────────────────────────────────────────── */
.stPlotlyChart > div,
[data-testid="stPlotlyChart"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
}

/* ── 25. PAGE SECTION HEADERS ───────────────────────────────────────────────── */
.page-header {
    padding: 0 0 28px;
    animation: fadeSlideUp 0.35s ease both;
}
.page-header .module-label {
    font-family: var(--font-sans);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--indigo);
    opacity: 0.8;
    margin-bottom: 8px;
    display: block;
}
.page-header h1 {
    font-family: var(--font-sans) !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    margin: 0 0 8px !important;
    letter-spacing: -0.02em !important;
    line-height: 1.25 !important;
}
.page-header p {
    color: var(--text-secondary);
    font-size: 15px;
    margin: 0;
    line-height: 1.6;
}

/* ── 26. INLINE DIVIDER ─────────────────────────────────────────────────────── */
.section-divider {
    height: 1px;
    background: var(--border-subtle);
    margin: 28px 0;
}

/* ── 27. INFO BANNER / NOTICE ───────────────────────────────────────────────── */
.notice-banner {
    display: flex;
    align-items: center;
    gap: 10px;
    background: var(--indigo-subtle);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: var(--radius);
    padding: 10px 16px;
    margin-bottom: 24px;
    font-family: var(--font-sans);
    font-size: 13px;
    color: #A5B4FC;
}

/* ── 28. COPILOT CHAT STYLES ────────────────────────────────────────────────── */
.copilot-msg-user {
    background: var(--indigo-subtle);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg);
    padding: 14px 18px;
    margin: 0 0 12px 56px;
    font-family: var(--font-sans);
    font-size: 14px;
    color: var(--text);
    line-height: 1.6;
}
.copilot-msg-ai {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm) var(--radius-lg) var(--radius-lg) var(--radius-lg);
    padding: 14px 18px;
    margin: 0 56px 12px 0;
    font-family: var(--font-sans);
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.7;
}
.copilot-msg-ai strong { color: #A5B4FC; }
.copilot-label {
    font-family: var(--font-sans);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 5px;
}
.suggested-chip {
    display: inline-flex;
    align-items: center;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 6px 14px;
    font-family: var(--font-sans);
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
    margin: 4px;
    cursor: pointer;
    transition: all 0.12s ease;
}
.suggested-chip:hover {
    border-color: var(--indigo);
    color: #A5B4FC;
    background: var(--indigo-subtle);
}

/* THEME v3.0 — ENTERPRISE INDIGO — PDF COMPLIANCE SCANNER */
</style>
"""
