import streamlit as st
import os
import base64

st.set_page_config(page_title="ZS Primary Care", layout="wide", initial_sidebar_state="collapsed")

# --- Helper: load logo as base64 ---
def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_logo_base64()

# --- Custom CSS ---
st.markdown("""
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
        background: linear-gradient(135deg, #0D2137 0%, #1A3E6E 50%, #234B7E 100%);
        padding: 22px 50px;
        display: flex;
        align-items: center;
        gap: 24px;
        margin: -1rem -1rem 0 -1rem;
        width: calc(100% + 2rem);
        box-shadow: 0 4px 20px rgba(13, 33, 55, 0.3);
        position: relative;
        overflow: hidden;
    }
    .top-ribbon::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse at 80% 50%, rgba(255,255,255,0.03) 0%, transparent 50%);
    }
    .top-ribbon img {
        height: 48px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
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
        color: #1A3E6E;
        font-size: 11px;
        position: relative;
        z-index: 1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    .top-ribbon .title {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: 700;
        position: relative;
        z-index: 1;
        text-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    .top-ribbon .title-accent {
        color: rgba(255,255,255,0.6);
        font-size: 24px;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }

    /* Back button */
    .back-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        background: #FFFFFF;
        border: 1px solid rgba(26, 62, 110, 0.15);
        border-radius: 10px;
        color: #1A3E6E;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin: 30px 0 20px 50px;
    }
    .back-btn:hover {
        background: #F0F4F8;
        box-shadow: 0 4px 12px rgba(26, 62, 110, 0.1);
    }

    /* Brand header */
    .brand-header {
        padding: 50px 50px 30px;
        text-align: center;
    }
    .brand-header h1 {
        color: #1A3E6E;
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .brand-header p {
        color: #6B7C93;
        font-size: 16px;
        font-weight: 400;
    }

    .stButton > button {
        background: #FFFFFF !important;
        border: 1px solid rgba(26, 62, 110, 0.15) !important;
        border-radius: 10px !important;
        color: #1A3E6E !important;
        font-weight: 600 !important;
        padding: 8px 20px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: #F0F4F8 !important;
        box-shadow: 0 4px 12px rgba(26, 62, 110, 0.1) !important;
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
    <span class="title">ZS</span>
    <span class="title-accent">|</span>
    <span class="title">Primary Care</span>
</div>
""", unsafe_allow_html=True)

# --- Back button ---
if st.button("← Back to Home"):
    st.switch_page("app.py")

# --- Brand Content ---
brand = st.session_state.get("selected_brand", "Unknown")

st.markdown(f"""
<div class="brand-header">
    <h1>{brand}</h1>
    <p>Content for {brand} will be available here soon.</p>
</div>
""", unsafe_allow_html=True)
