"""
Shared CSS, helpers, and utilities for the Primary Care Dashboard.
Used by all brand pages and the home page.
"""

import streamlit as st
import os
import base64

# --- Asset path resolution ---
LIB_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(LIB_DIR, "assets")


def get_logo_base64(filename):
    """Load an image from assets/ and return as base64 string."""
    logo_path = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


# --- Common CSS for brand detail pages ---
BRAND_PAGE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    .block-container {
        padding-top: 0rem !important;
        max-width: 100% !important;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #F8FAFD 0%, #EEF2F7 100%);
    }

    .top-ribbon {
        background: linear-gradient(135deg, #5BABDE 0%, #7EC8E3 50%, #A3D9F0 100%);
        padding: 34px 50px;
        display: flex;
        align-items: center;
        gap: 16px;
        margin: -1rem -1rem 0 -1rem;
        width: calc(100% + 2rem);
        box-shadow: 0 4px 16px rgba(91, 171, 222, 0.25);
        position: relative;
        overflow: hidden;
    }
    .top-ribbon::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse at 80% 50%, rgba(255,255,255,0.05) 0%, transparent 50%);
    }
    .top-ribbon img {
        height: 64px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15));
        position: relative;
        z-index: 1;
    }
    .top-ribbon .logo-placeholder {
        width: 48px;
        height: 48px;
        background: rgba(255,255,255,0.95);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: #2A5A8C;
        font-size: 11px;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .top-ribbon .title {
        color: #FFFFFF;
        font-size: 30px;
        font-weight: 700;
        letter-spacing: 0.3px;
        position: relative;
        z-index: 1;
        text-shadow: 0 1px 2px rgba(0,0,0,0.15);
    }

    /* KPI cards */
    .kpi-container {
        display: flex;
        gap: 24px;
        padding: 30px 50px 10px;
    }
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid rgba(26, 62, 110, 0.08);
        border-radius: 14px;
        padding: 24px 32px;
        flex: 1;
        box-shadow: 0 2px 12px rgba(26, 62, 110, 0.06);
        border-top: 4px solid #1A3E6E;
    }
    .kpi-card .kpi-label {
        color: #6B7C93;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    .kpi-card .kpi-value {
        color: #1A3E6E;
        font-size: 36px;
        font-weight: 800;
    }
    .kpi-card .kpi-value.positive {
        color: #2EAF7D;
    }
    .kpi-card .kpi-value.negative {
        color: #E85D4A;
    }
    .kpi-card .kpi-period {
        color: #9EAAB8;
        font-size: 12px;
        font-weight: 400;
        margin-top: 6px;
    }

    /* Section title */
    .section-title {
        padding: 20px 50px 5px;
        color: #1A3E6E;
        font-size: 18px;
        font-weight: 700;
    }

    /* Table styling */
    .claims-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 30px;
        font-family: 'Inter', sans-serif;
    }
    .claims-table th {
        background: #1A3E6E;
        color: #FFFFFF;
        padding: 12px 18px;
        text-align: right;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .claims-table th:first-child {
        text-align: left;
        border-radius: 8px 0 0 0;
    }
    .claims-table th:last-child {
        border-radius: 0 8px 0 0;
    }
    .claims-table td {
        padding: 11px 18px;
        text-align: right;
        font-size: 13px;
        color: #2C3E50;
        border-bottom: 1px solid #EEF2F7;
    }
    .claims-table td:first-child {
        text-align: left;
        font-weight: 600;
        color: #1A3E6E;
    }
    .claims-table tr:nth-child(even) {
        background: #F8FAFD;
    }
    .claims-table tr:hover {
        background: #EBF2FA;
    }

    /* Back & download buttons */
    .stButton > button, .stDownloadButton > button {
        background: #FFFFFF !important;
        border: 1px solid rgba(26, 62, 110, 0.15) !important;
        border-radius: 10px !important;
        color: #1A3E6E !important;
        font-weight: 600 !important;
        padding: 8px 20px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: #F0F4F8 !important;
        box-shadow: 0 4px 12px rgba(26, 62, 110, 0.1) !important;
    }
</style>
"""

# --- Common CSS for home page ---
HOME_PAGE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }

    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Top ribbon */
    .top-ribbon {
        background: linear-gradient(135deg, #5BABDE 0%, #7EC8E3 50%, #A3D9F0 100%);
        padding: 34px 50px;
        display: flex;
        align-items: center;
        gap: 16px;
        margin: -1rem -1rem 0 -1rem;
        width: calc(100% + 2rem);
        box-shadow: 0 4px 16px rgba(91, 171, 222, 0.25);
        position: relative;
        overflow: hidden;
    }
    .top-ribbon::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse at 80% 50%, rgba(255,255,255,0.05) 0%, transparent 50%);
    }
    .top-ribbon img {
        height: 64px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15));
        position: relative;
        z-index: 1;
    }
    .top-ribbon .logo-placeholder {
        width: 48px;
        height: 48px;
        background: rgba(255,255,255,0.95);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: #2A5A8C;
        font-size: 11px;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .top-ribbon .title {
        color: #FFFFFF;
        font-size: 30px;
        font-weight: 700;
        letter-spacing: 0.3px;
        position: relative;
        z-index: 1;
        text-shadow: 0 1px 2px rgba(0,0,0,0.15);
    }

    /* Page body background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #F8FAFD 0%, #EEF2F7 100%);
    }

    /* Brand card buttons */
    .stButton > button {
        background: #FFFFFF !important;
        border: 1px solid rgba(26, 62, 110, 0.10) !important;
        border-radius: 18px !important;
        padding: 40px 32px !important;
        color: #1A3E6E !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 16px rgba(26, 62, 110, 0.08), 0 2px 6px rgba(0,0,0,0.04) !important;
        position: relative !important;
        min-height: 180px !important;
        border-top: 5px solid #5BABDE !important;
        line-height: 1.2 !important;
    }
    .stButton > button > div,
    .stButton > button > div > p,
    .stButton > button p,
    .stButton > button span {
        font-size: 20px !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }
    .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 16px 40px rgba(26, 62, 110, 0.18), 0 6px 16px rgba(0,0,0,0.08) !important;
        border-color: rgba(26, 62, 110, 0.20) !important;
        border-top: 5px solid #1A3E6E !important;
        background: #FAFCFF !important;
    }
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }

    /* Brand logo displayed above buttons */
    .brand-logo {
        display: flex;
        justify-content: center;
        padding: 20px 0 4px 0;
    }
    .brand-logo img {
        height: 55px;
        object-fit: contain;
    }
</style>
"""


def render_ribbon(logo_b64, title):
    """Render the top ribbon with logo and title."""
    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" />'
    else:
        logo_html = '<div class="logo-placeholder">LOGO</div>'

    st.markdown(f"""
    <div class="top-ribbon">
        {logo_html}
        <span class="title">{title}</span>
    </div>
    """, unsafe_allow_html=True)


def render_back_button():
    """Render back to home button using session state navigation."""
    if st.button("\u2190 Back to Home"):
        st.session_state["current_page"] = "home"
        st.rerun()
