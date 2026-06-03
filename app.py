import streamlit as st
import os
import base64

st.set_page_config(page_title="Primary Care Monthly Report Dashboard", layout="wide", initial_sidebar_state="collapsed")

# --- Helper: load logo as base64 ---
def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def get_brand_logo_base64(filename):
    logo_path = os.path.join(os.path.dirname(__file__), "assets", filename)
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_logo_base64()
nurtec_logo_b64 = get_brand_logo_base64("nurtec_logo.png")
zavz_logo_b64 = get_brand_logo_base64("zavz_logo.png")
eliquis_logo_b64 = get_brand_logo_base64("eliquis.png")
prevnar_logo_b64 = get_brand_logo_base64("prevnar.png")
comirnaty_logo_b64 = get_brand_logo_base64("comirnaty.png")
abrysvo_logo_b64 = get_brand_logo_base64("abrysvo.png")
pax_logo_b64 = get_brand_logo_base64("pax.png")

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
""", unsafe_allow_html=True)

# --- Top Ribbon ---
if logo_b64:
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" />'
else:
    logo_html = '<div class="logo-placeholder">LOGO</div>'

st.markdown(f"""
<div class="top-ribbon">
    {logo_html}
    <span class="title">Primary Care Monthly Report Dashboard</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# --- Data Summary Glossary ---
st.markdown("""
<div style="padding: 0 50px;">
    <div style="background: #FFFFFF; border-radius: 14px; padding: 24px 32px; box-shadow: 0 2px 12px rgba(26, 62, 110, 0.06); border: 1px solid rgba(26, 62, 110, 0.08); border-left: 5px solid #5BABDE;">
        <div style="font-size: 16px; font-weight: 700; color: #1A3E6E; margin-bottom: 16px; font-family: 'Inter', sans-serif; letter-spacing: 0.3px;">Data Summary</div>
        <table style="width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif;">
            <thead>
                <tr style="border-bottom: 2px solid #E8EDF3;">
                    <th style="text-align: left; padding: 10px 16px; font-size: 13px; font-weight: 600; color: #6B7C93; text-transform: uppercase; letter-spacing: 0.5px;">Data Source</th>
                    <th style="text-align: left; padding: 10px 16px; font-size: 13px; font-weight: 600; color: #6B7C93; text-transform: uppercase; letter-spacing: 0.5px;">Data Availability</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid #F0F3F7;">
                    <td style="padding: 12px 16px; font-size: 14px; color: #2C3E50;">NPA</td>
                    <td style="padding: 12px 16px; font-size: 14px; color: #2C3E50;">Till May 2026</td>
                </tr>
                <tr style="border-bottom: 1px solid #F0F3F7;">
                    <td style="padding: 12px 16px; font-size: 14px; color: #2C3E50;">DDD</td>
                    <td style="padding: 12px 16px; font-size: 14px; color: #2C3E50;">Till May 2026</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
brands = [
    {"name": "Nurtec", "logo": nurtec_logo_b64, "page": "pages/nurtec.py"},
    {"name": "Zavzpret", "logo": zavz_logo_b64, "page": "pages/zavzpret.py"},
    {"name": "Eliquis", "logo": eliquis_logo_b64, "page": "pages/eliquis.py"},
    {"name": "Prevnar", "logo": prevnar_logo_b64, "page": None},
    {"name": "Comirnaty", "logo": comirnaty_logo_b64, "page": None},
    {"name": "Abrysvo", "logo": abrysvo_logo_b64, "page": None},
    {"name": "Paxlovid", "logo": pax_logo_b64, "page": None},
]

# --- Render brand cards in rows of 3 ---
for row_start in range(0, len(brands), 3):
    row_brands = brands[row_start:row_start + 3]
    cols = st.columns(3)
    for i, brand in enumerate(row_brands):
        with cols[i]:
            # Show brand logo
            if brand["logo"]:
                st.markdown(
                    f'<div class="brand-logo"><img src="data:image/png;base64,{brand["logo"]}" /></div>',
                    unsafe_allow_html=True
                )
            # Clickable button with brand name
            if st.button(brand["name"], key=f'{brand["name"].lower()}_btn', use_container_width=True):
                st.session_state["selected_brand"] = brand["name"]
                if brand["page"]:
                    st.switch_page(brand["page"])
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; text-align: center; padding: 14px 0; background: #F8FAFD; border-top: 1px solid rgba(26, 62, 110, 0.08);">
    <span style="color: #9EAAB8; font-size: 12px; font-family: 'Inter', sans-serif; font-weight: 400;">Developed by ZS Primary Care Team</span>
</div>
""", unsafe_allow_html=True)
