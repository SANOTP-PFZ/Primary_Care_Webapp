import streamlit as st
import os
import base64

st.set_page_config(page_title="ZS Primary Care", layout="wide", initial_sidebar_state="collapsed")

# --- Helper: load logo as base64 ---
def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_logo_base64()

# --- Custom CSS ---
st.markdown("""
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

    /* Top ribbon - lighter color */
    .top-ribbon {
        background: linear-gradient(135deg, #2A5A8C 0%, #3A7BC8 50%, #4A8FD9 100%);
        padding: 22px 50px;
        display: flex;
        align-items: center;
        gap: 16px;
        margin: -1rem -1rem 0 -1rem;
        width: calc(100% + 2rem);
        box-shadow: 0 4px 16px rgba(42, 90, 140, 0.25);
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
        height: 48px;
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
        font-size: 24px;
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

    /* Brand card styling - bigger, card-like */
    .stButton > button {
        background: #FFFFFF !important;
        border: 1px solid rgba(26, 62, 110, 0.10) !important;
        border-radius: 18px !important;
        padding: 50px 40px !important;
        color: #1A3E6E !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 16px rgba(26, 62, 110, 0.08), 0 2px 6px rgba(0,0,0,0.04) !important;
        position: relative !important;
        min-height: 140px !important;
        border-top: 5px solid #3A7BC8 !important;
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
</style>
""", unsafe_allow_html=True)

# --- Top Ribbon ---
if logo_b64:
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" />'
else:
    logo_html = '<div class="logo-placeholder">LOGO</div>'

st.markdown(f"""
<div class="top-ribbon">
    {logo_html}
    <span class="title">ZS Primary Care</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# --- Brand Cards in a horizontal row ---
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("💊  Nurtec", key="nurtec_btn", use_container_width=True):
        st.session_state["selected_brand"] = "Nurtec"
        st.switch_page("pages/nurtec.py")

with col2:
    if st.button("💉  Zavzpret", key="zavzpret_btn", use_container_width=True):
        st.session_state["selected_brand"] = "Zavzpret"
        st.switch_page("pages/zavzpret.py")

# --- Footer ---
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; text-align: center; padding: 14px 0; background: #F8FAFD; border-top: 1px solid rgba(26, 62, 110, 0.08);">
    <span style="color: #9EAAB8; font-size: 12px; font-family: 'Inter', sans-serif; font-weight: 400;">Developed by ZS Primary Care Team</span>
</div>
""", unsafe_allow_html=True)
