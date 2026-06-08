"""
Primary Care Monthly Report Dashboard - Single File for Dataiku DSS
Paste this entire file into the Dataiku DSS Streamlit webapp editor.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Primary Care Monthly Report Dashboard", layout="wide", initial_sidebar_state="collapsed")

# =====================================================
# COMMON CSS
# =====================================================

BRAND_PAGE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    .block-container { padding-top: 0rem !important; max-width: 100% !important; }
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    [data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #F8FAFD 0%, #EEF2F7 100%); }
    .top-ribbon { background: linear-gradient(135deg, #5BABDE 0%, #7EC8E3 50%, #A3D9F0 100%); padding: 34px 50px; display: flex; align-items: center; gap: 16px; margin: -1rem -1rem 0 -1rem; width: calc(100% + 2rem); box-shadow: 0 4px 16px rgba(91, 171, 222, 0.25); position: relative; overflow: hidden; }
    .top-ribbon::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(ellipse at 80% 50%, rgba(255,255,255,0.05) 0%, transparent 50%); }
    .top-ribbon img { height: 64px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15)); position: relative; z-index: 1; }
    .top-ribbon .logo-placeholder { width: 48px; height: 48px; background: rgba(255,255,255,0.95); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; color: #2A5A8C; font-size: 11px; position: relative; z-index: 1; }
    .top-ribbon .title { color: #FFFFFF; font-size: 30px; font-weight: 700; letter-spacing: 0.3px; position: relative; z-index: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.15); }
    .kpi-container { display: flex; gap: 24px; padding: 30px 50px 10px; }
    .kpi-card { background: #FFFFFF; border: 1px solid rgba(26, 62, 110, 0.08); border-radius: 14px; padding: 24px 32px; flex: 1; box-shadow: 0 2px 12px rgba(26, 62, 110, 0.06); border-top: 4px solid #1A3E6E; }
    .kpi-card .kpi-label { color: #6B7C93; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }
    .kpi-card .kpi-value { color: #1A3E6E; font-size: 36px; font-weight: 800; }
    .kpi-card .kpi-value.positive { color: #2EAF7D; }
    .kpi-card .kpi-value.negative { color: #E85D4A; }
    .kpi-card .kpi-period { color: #9EAAB8; font-size: 12px; font-weight: 400; margin-top: 6px; }
    .section-title { padding: 20px 50px 5px; color: #1A3E6E; font-size: 18px; font-weight: 700; }
    .claims-table { width: 100%; border-collapse: collapse; margin: 10px 0 30px; font-family: 'Inter', sans-serif; }
    .claims-table th { background: #1A3E6E; color: #FFFFFF; padding: 12px 18px; text-align: right; font-size: 13px; font-weight: 600; }
    .claims-table th:first-child { text-align: left; border-radius: 8px 0 0 0; }
    .claims-table th:last-child { border-radius: 0 8px 0 0; }
    .claims-table td { padding: 11px 18px; text-align: right; font-size: 13px; color: #2C3E50; border-bottom: 1px solid #EEF2F7; }
    .claims-table td:first-child { text-align: left; font-weight: 600; color: #1A3E6E; }
    .claims-table tr:nth-child(even) { background: #F8FAFD; }
    .claims-table tr:hover { background: #EBF2FA; }
    .stButton > button, .stDownloadButton > button { background: #FFFFFF !important; border: 1px solid rgba(26, 62, 110, 0.15) !important; border-radius: 10px !important; color: #1A3E6E !important; font-weight: 600 !important; padding: 8px 20px !important; transition: all 0.2s ease !important; }
    .stButton > button:hover, .stDownloadButton > button:hover { background: #F0F4F8 !important; box-shadow: 0 4px 12px rgba(26, 62, 110, 0.1) !important; }
</style>
"""

HOME_PAGE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; max-width: 100% !important; }
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    .top-ribbon { background: linear-gradient(135deg, #5BABDE 0%, #7EC8E3 50%, #A3D9F0 100%); padding: 34px 50px; display: flex; align-items: center; gap: 16px; margin: -1rem -1rem 0 -1rem; width: calc(100% + 2rem); box-shadow: 0 4px 16px rgba(91, 171, 222, 0.25); position: relative; overflow: hidden; }
    .top-ribbon::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(ellipse at 80% 50%, rgba(255,255,255,0.05) 0%, transparent 50%); }
    .top-ribbon img { height: 64px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15)); position: relative; z-index: 1; }
    .top-ribbon .logo-placeholder { width: 48px; height: 48px; background: rgba(255,255,255,0.95); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; color: #2A5A8C; font-size: 11px; position: relative; z-index: 1; }
    .top-ribbon .title { color: #FFFFFF; font-size: 30px; font-weight: 700; letter-spacing: 0.3px; position: relative; z-index: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.15); }
    [data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #F8FAFD 0%, #EEF2F7 100%); }
    .stButton > button { background: #FFFFFF !important; border: 1px solid rgba(26, 62, 110, 0.10) !important; border-radius: 18px !important; padding: 40px 32px !important; color: #1A3E6E !important; font-size: 20px !important; font-weight: 700 !important; font-family: 'Inter', sans-serif !important; cursor: pointer !important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; box-shadow: 0 4px 16px rgba(26, 62, 110, 0.08), 0 2px 6px rgba(0,0,0,0.04) !important; position: relative !important; min-height: 180px !important; border-top: 5px solid #5BABDE !important; line-height: 1.2 !important; }
    .stButton > button > div, .stButton > button > div > p, .stButton > button p, .stButton > button span { font-size: 20px !important; font-weight: 700 !important; line-height: 1.2 !important; }
    .stButton > button:hover { transform: translateY(-4px) !important; box-shadow: 0 16px 40px rgba(26, 62, 110, 0.18), 0 6px 16px rgba(0,0,0,0.08) !important; border-color: rgba(26, 62, 110, 0.20) !important; border-top: 5px solid #1A3E6E !important; background: #FAFCFF !important; }
    .stButton > button:active { transform: translateY(-1px) !important; }
    .brand-logo { display: flex; justify-content: center; padding: 20px 0 4px 0; }
    .brand-logo img { height: 55px; object-fit: contain; }
</style>
"""


# =====================================================
# HELPERS
# =====================================================

def render_ribbon(title):
    st.markdown(f"""
    <div class="top-ribbon">
        <div class="logo-placeholder">PC</div>
        <span class="title">{title}</span>
    </div>
    """, unsafe_allow_html=True)


def render_back_button():
    if st.button("\u2190 Back to Home"):
        st.session_state["current_page"] = "home"
        st.rerun()


def render_market_share_brand(brand_name, title, quarters, trx_market_share, nbrx_market_share, claims_df, brand_colors):
    """Generic renderer for brands with TRX/NBRX market share charts."""
    st.markdown(BRAND_PAGE_CSS, unsafe_allow_html=True)
    render_ribbon(title)
    render_back_button()

    # KPIs
    latest_period = quarters[-1]
    latest_row = claims_df[claims_df["Quarter"] == latest_period].iloc[0]

    trx_val = f"{latest_row['TRX MARKET SHARE']:.1f}%"
    nbrx_val = f"{latest_row['NBRX MARKET SHARE']:.1f}%"

    trx_ms_diff = latest_row["TRX MARKET SHARE DIFF"]
    nbrx_ms_diff = latest_row["NBRX MARKET SHARE DIFF"]

    if pd.notna(trx_ms_diff):
        trx_diff_sign = "+" if trx_ms_diff >= 0 else ""
        trx_diff_color = "#2EAF7D" if trx_ms_diff >= 0 else "#E85D4A"
        trx_diff_html = f'<span style="font-size:18px; color:{trx_diff_color}; font-weight:600;">({trx_diff_sign}{trx_ms_diff:.1f}pp vs STLY)</span>'
    else:
        trx_diff_html = ""

    if pd.notna(nbrx_ms_diff):
        nbrx_diff_sign = "+" if nbrx_ms_diff >= 0 else ""
        nbrx_diff_color = "#2EAF7D" if nbrx_ms_diff >= 0 else "#E85D4A"
        nbrx_diff_html = f'<span style="font-size:18px; color:{nbrx_diff_color}; font-weight:600;">({nbrx_diff_sign}{nbrx_ms_diff:.1f}pp vs STLY)</span>'
    else:
        nbrx_diff_html = ""

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">{brand_name} TRX Market Share</div>
            <div class="kpi-value">{trx_val} {trx_diff_html}</div>
            <div class="kpi-period">Latest: {latest_period}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">{brand_name} NBRx Market Share</div>
            <div class="kpi-value">{nbrx_val} {nbrx_diff_html}</div>
            <div class="kpi-period">Latest: {latest_period}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # TRX Market Share Chart
    market_name = title.replace(" QoQ Report", "")
    st.markdown(f'<div class="section-title">TRX Market Share Trend \u2014 {market_name} Market</div>', unsafe_allow_html=True)

    brands_list = list(trx_market_share.keys())
    fig_trx = go.Figure()
    for i, brand in enumerate(brands_list):
        fig_trx.add_trace(go.Scatter(
            x=quarters, y=trx_market_share[brand],
            mode="lines+markers", name=brand,
            line=dict(color=brand_colors.get(brand, "#999999"), width=3 if brand == brand_name or brand == brands_list[0] else 2),
            marker=dict(size=7 if brand == brand_name or brand == brands_list[0] else 5),
            hovertemplate=f"<b>{brand}</b><br>%{{x}}<br>%{{y:.1f}}%<extra></extra>"
        ))

    fig_trx.update_layout(
        height=420, margin=dict(l=50, r=30, t=20, b=40),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#1A3E6E"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=12)),
        xaxis=dict(showgrid=False, tickfont=dict(size=12)),
        yaxis=dict(showgrid=True, gridcolor="rgba(26, 62, 110, 0.06)", ticksuffix="%", tickfont=dict(size=12), title=""),
        hovermode="x unified"
    )
    st.plotly_chart(fig_trx, use_container_width=True)

    # NBRX Market Share Chart
    st.markdown(f'<div class="section-title">NBRx Market Share Trend \u2014 {market_name} Market</div>', unsafe_allow_html=True)

    fig_nbrx = go.Figure()
    for i, brand in enumerate(brands_list):
        fig_nbrx.add_trace(go.Scatter(
            x=quarters, y=nbrx_market_share[brand],
            mode="lines+markers", name=brand,
            line=dict(color=brand_colors.get(brand, "#999999"), width=3 if brand == brand_name or brand == brands_list[0] else 2),
            marker=dict(size=7 if brand == brand_name or brand == brands_list[0] else 5),
            hovertemplate=f"<b>{brand}</b><br>%{{x}}<br>%{{y:.1f}}%<extra></extra>"
        ))

    fig_nbrx.update_layout(
        height=420, margin=dict(l=50, r=30, t=20, b=40),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#1A3E6E"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=12)),
        xaxis=dict(showgrid=False, tickfont=dict(size=12)),
        yaxis=dict(showgrid=True, gridcolor="rgba(26, 62, 110, 0.06)", ticksuffix="%", tickfont=dict(size=12), title=""),
        hovermode="x unified"
    )
    st.plotly_chart(fig_nbrx, use_container_width=True)

    # Raw Data Table
    st.markdown('<div class="section-title">Raw Data Tables</div>', unsafe_allow_html=True)
    with st.expander(f"{brand_name} Claims & Market Share Data", expanded=False):
        st.dataframe(claims_df, use_container_width=True, hide_index=True)

    # Excel Download
    st.markdown('<div class="section-title">Download Reports</div>', unsafe_allow_html=True)

    def generate_excel():
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            claims_df.to_excel(writer, sheet_name=f"{brand_name} Report", index=False)
        return output.getvalue()

    st.download_button(
        label="\U0001f4e5 Download Excel",
        data=generate_excel(),
        file_name=f"{brand_name.lower()}_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# =====================================================
# HOME PAGE
# =====================================================

def render_home():
    st.markdown(HOME_PAGE_CSS, unsafe_allow_html=True)
    render_ribbon("Primary Care Monthly Report Dashboard")
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # Data Summary
    st.markdown("""
    <div style="padding: 0 50px;">
        <div style="background: #FFFFFF; border-radius: 14px; padding: 24px 32px; box-shadow: 0 2px 12px rgba(26, 62, 110, 0.06); border: 1px solid rgba(26, 62, 110, 0.08); border-left: 5px solid #5BABDE;">
            <div style="font-size: 16px; font-weight: 700; color: #1A3E6E; margin-bottom: 16px;">Data Summary</div>
            <table style="width: 100%; border-collapse: collapse;">
                <thead><tr style="border-bottom: 2px solid #E8EDF3;">
                    <th style="text-align: left; padding: 10px 16px; font-size: 13px; font-weight: 600; color: #6B7C93; text-transform: uppercase;">Data Source</th>
                    <th style="text-align: left; padding: 10px 16px; font-size: 13px; font-weight: 600; color: #6B7C93; text-transform: uppercase;">Data Availability</th>
                </tr></thead>
                <tbody>
                    <tr style="border-bottom: 1px solid #F0F3F7;"><td style="padding: 12px 16px; font-size: 14px;">NPA</td><td style="padding: 12px 16px; font-size: 14px;">Till May 2026</td></tr>
                    <tr style="border-bottom: 1px solid #F0F3F7;"><td style="padding: 12px 16px; font-size: 14px;">DDD</td><td style="padding: 12px 16px; font-size: 14px;">Till May 2026</td></tr>
                </tbody>
            </table>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    brands = [
        {"name": "Nurtec", "page_key": "nurtec"},
        {"name": "Zavzpret", "page_key": "zavzpret"},
        {"name": "Eliquis", "page_key": "eliquis"},
        {"name": "Prevnar", "page_key": "prevnar"},
        {"name": "Comirnaty", "page_key": "comirnaty"},
        {"name": "Abrysvo", "page_key": "abrysvo"},
        {"name": "Paxlovid", "page_key": "paxlovid"},
    ]

    for row_start in range(0, len(brands), 3):
        row_brands = brands[row_start:row_start + 3]
        cols = st.columns(3)
        for i, brand in enumerate(row_brands):
            with cols[i]:
                if st.button(brand["name"], key=f'{brand["name"].lower()}_btn', use_container_width=True):
                    st.session_state["current_page"] = brand["page_key"]
                    st.rerun()
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; padding: 14px 0; border-top: 1px solid rgba(26, 62, 110, 0.08); margin-top: 40px;">
        <span style="color: #9EAAB8; font-size: 12px;">Developed by ZS Primary Care Team</span>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# NURTEC PAGE
# =====================================================

def render_nurtec():
    quarters = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]
    trx_ms = {"Nurtec": [45.03,45.31,44.85,44.88,43.42,43.15,42.66,42.6,42.73,43.22], "Ubrelvy": [33.48,33.39,33.08,32.64,32.94,33.08,33.27,33.33,32.54,31.71], "Qulipta": [21.49,21.3,22.06,22.48,23.64,23.77,24.07,24.07,24.72,25.07]}
    nbrx_ms = {"Nurtec": [43.06,43.91,43.9,44.0,42.82,42.45,41.29,42.06,43.14,43.21], "Ubrelvy": [35.97,35.66,35.24,34.63,35.33,35.88,36.51,36.12,35.43,35.51], "Qulipta": [20.97,20.43,20.85,21.37,21.85,21.67,22.2,21.82,21.43,21.28]}
    claims = pd.DataFrame({"Quarter": quarters, "TRX CLAIMS": [676214,750986,781454,838399,771398,836705,874415,931369,894657,315451], "NBRX CLAIMS": [102162,108147,110278,111502,110073,111782,112903,115924,120180,42793], "TRX MARKET SHARE": trx_ms["Nurtec"], "NBRX MARKET SHARE": nbrx_ms["Nurtec"], "TRX MARKET SHARE DIFF": [-2.46,-1.69,-1.59,-1.65,-1.61,-2.16,-2.2,-2.28,-0.68,0.04], "NBRX MARKET SHARE DIFF": [-1.09,-0.15,-0.18,-0.4,-0.24,-1.47,-2.62,-1.94,0.32,0.68]})
    colors = {"Nurtec": "#1A3E6E", "Ubrelvy": "#E85D4A", "Qulipta": "#2EAF7D"}
    render_market_share_brand("Nurtec", "Nurtec QoQ Report", quarters, trx_ms, nbrx_ms, claims, colors)


# =====================================================
# ELIQUIS PAGE
# =====================================================

def render_eliquis():
    quarters = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]
    trx_ms = {"Eliquis": [63.57,64.24,64.91,65.36,66.29,67.19,68.22,69.09,69.32,69.86], "Xarelto": [19.66,19.46,19.23,19.06,18.28,17.69,17.07,16.6,16.1,15.9], "Warfarin": [14.49,14.08,13.6,13.28,13.03,12.69,12.41,12.0,12.41,12.22], "Dabigatran": [0.65,0.76,0.85,0.95,1.12,1.28,1.37,1.46,1.67,1.76], "Jantoven": [1.26,1.16,1.14,1.13,1.1,1.01,0.82,0.75,0.43,0.19], "Pradaxa": [0.34,0.28,0.24,0.2,0.14,0.11,0.09,0.07,0.05,0.04], "Savaysa": [0.03,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02]}
    nbrx_ms = {"Eliquis": [70.41,71.72,71.82,72.79,72.07,73.98,74.83,76.01,74.22,75.41], "Xarelto": [18.93,18.57,18.49,17.68,15.95,14.89,14.08,13.78,13.53,12.59], "Warfarin": [7.0,6.57,6.45,6.26,7.29,6.96,7.29,6.35,8.02,7.95], "Dabigatran": [1.5,1.82,2.05,2.22,3.26,3.06,2.97,3.14,3.8,3.82], "Jantoven": [1.57,1.05,1.0,0.89,1.27,0.98,0.71,0.62,0.37,0.19], "Pradaxa": [0.57,0.24,0.17,0.14,0.14,0.11,0.1,0.08,0.04,0.03], "Savaysa": [0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.01,0.02,0.01]}
    claims = pd.DataFrame({"Quarter": quarters, "TRX CLAIMS": [8166943,8306783,8462802,8660513,8663784,8901849,9150074,9455957,9059954,3129304], "NBRX CLAIMS": [588952,534822,514489,530382,580618,549959,550523,552535,622412,206482], "TRX MARKET SHARE": trx_ms["Eliquis"], "NBRX MARKET SHARE": nbrx_ms["Eliquis"], "TRX MARKET SHARE DIFF": [4.49,4.17,3.98,3.47,2.72,2.95,3.3,3.73,3.03,2.99], "NBRX MARKET SHARE DIFF": [3.79,3.18,2.35,2.17,1.66,2.27,3.01,3.22,2.15,1.65]})
    colors = {"Eliquis": "#1A3E6E", "Xarelto": "#E85D4A", "Warfarin": "#2EAF7D", "Dabigatran": "#F59E0B", "Jantoven": "#8B5CF6", "Pradaxa": "#EC4899", "Savaysa": "#6B7280"}
    render_market_share_brand("Eliquis", "Eliquis QoQ Report", quarters, trx_ms, nbrx_ms, claims, colors)


# =====================================================
# PREVNAR PAGE
# =====================================================

def render_prevnar():
    quarters = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]
    trx_ms = {"Prevnar 20": [92.68,94.19,94.9,88.72,70.14,60.92,57.21,53.96,55.8,53.44], "Capvaxive": [None,None,0.42,8.22,27.33,36.62,40.87,44.53,42.24,44.54], "Pneumovax 23": [6.71,5.4,4.45,2.92,2.43,2.36,1.84,1.46,1.86,1.96], "Vaxneuvance": [0.21,0.21,0.16,0.11,0.09,0.1,0.07,0.05,0.1,0.05]}
    nbrx_ms = {"Prevnar 20": [94.64,95.59,95.67,89.0,69.04,58.81,55.55,52.34,53.1,50.54], "Capvaxive": [None,None,0.46,8.76,29.28,39.56,43.22,46.84,45.94,48.43], "Pneumovax 23": [5.08,4.21,3.72,2.14,1.61,1.56,1.17,0.78,0.93,0.99], "Vaxneuvance": [0.16,0.15,0.13,0.09,0.07,0.07,0.05,0.04,0.03,0.04]}
    claims = pd.DataFrame({"Quarter": quarters, "TRX CLAIMS": [467511,457695,753373,1181105,674224,413769,581060,824692,332435,92632], "NBRX CLAIMS": [404568,403308,685803,1086286,611654,363503,526041,747516,284236,78618], "TRX MARKET SHARE": trx_ms["Prevnar 20"], "NBRX MARKET SHARE": nbrx_ms["Prevnar 20"], "TRX MARKET SHARE DIFF": [8.01,3.38,1.67,-5.11,-22.54,-33.28,-37.69,-34.76,-14.34,-9.61], "NBRX MARKET SHARE DIFF": [6.46,2.54,1.05,-6.23,-25.6,-36.78,-40.11,-36.65,-15.94,-10.78]})
    colors = {"Prevnar 20": "#1A3E6E", "Capvaxive": "#E85D4A", "Pneumovax 23": "#2EAF7D", "Vaxneuvance": "#F59E0B"}
    render_market_share_brand("Prevnar 20", "Prevnar QoQ Report", quarters, trx_ms, nbrx_ms, claims, colors)


# =====================================================
# COMIRNATY PAGE
# =====================================================

def render_comirnaty():
    quarters = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]
    trx_ms = {"Comirnaty": [51.16,52.59,56.96,57.83,60.31,62.46,58.37,57.22,59.72,56.28], "Spikevax": [47.53,46.63,41.34,39.19,37.55,37.3,20.38,18.3,14.69,10.66], "Novavax": [1.32,0.78,1.7,2.98,2.14,0.24,0.0,0.0,0.0,None], "mNexspike": [None,None,None,None,None,None,21.25,24.48,25.58,33.05]}
    nbrx_ms = {"Comirnaty": [51.74,54.98,58.07,59.49,60.61,64.84,45.7,51.7,56.96,45.81], "Spikevax": [46.63,43.66,38.64,36.4,36.91,34.79,17.96,16.95,15.72,16.5], "Novavax": [1.63,1.36,3.28,4.11,2.49,0.37,0.0,0.0,0.0,None], "mNexspike": [None,None,None,None,None,None,36.34,31.35,27.32,37.69]}
    claims = pd.DataFrame({"Quarter": quarters, "TRX CLAIMS": [1810747,926770,6318005,9231509,1268831,1148486,4287950,7252353,918723,371287], "NBRX CLAIMS": [1405390,440245,2971756,6458670,947985,421263,1954950,5033935,656542,108686], "TRX MARKET SHARE": trx_ms["Comirnaty"], "NBRX MARKET SHARE": nbrx_ms["Comirnaty"], "TRX MARKET SHARE DIFF": [-11.7,-5.99,-2.95,8.59,9.16,9.88,1.41,-0.62,-0.59,-5.1], "NBRX MARKET SHARE DIFF": [-11.49,-4.3,1.62,12.24,8.86,9.86,-12.37,-7.79,-3.65,-17.74]})
    colors = {"Comirnaty": "#1A3E6E", "Spikevax": "#E85D4A", "Novavax": "#2EAF7D", "mNexspike": "#F59E0B"}
    render_market_share_brand("Comirnaty", "Comirnaty QoQ Report", quarters, trx_ms, nbrx_ms, claims, colors)


# =====================================================
# ABRYSVO PAGE
# =====================================================

def render_abrysvo():
    quarters = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]
    trx_ms = {"Abrysvo": [31.71,31.91,36.74,44.11,45.72,44.22,47.11,49.89,53.06,50.32], "Arexvy": [68.29,68.09,63.0,54.55,52.69,54.15,51.55,47.99,45.22,47.67], "Mresvia": [None,None,0.27,1.34,1.59,1.63,1.33,2.12,1.72,2.02]}
    nbrx_ms = {"Abrysvo": [31.29,31.47,37.22,44.28,45.77,44.36,47.35,50.13,53.79,51.4], "Arexvy": [68.71,68.53,62.54,54.73,53.23,54.94,51.89,48.51,45.28,47.73], "Mresvia": [None,None,0.24,0.99,1.0,0.69,0.76,1.36,0.92,0.87]}
    claims = pd.DataFrame({"Quarter": quarters, "TRX CLAIMS": [602293,189471,391749,874056,370250,169698,358144,619491,258226,64519], "NBRX CLAIMS": [563604,174626,360175,811310,336972,154061,339284,586148,240039,59929], "TRX MARKET SHARE": trx_ms["Abrysvo"], "NBRX MARKET SHARE": nbrx_ms["Abrysvo"], "TRX MARKET SHARE DIFF": [None,None,1.44,12.8,14.01,12.31,10.38,5.79,7.34,5.93], "NBRX MARKET SHARE DIFF": [None,None,1.95,13.14,14.48,12.89,10.12,5.85,8.02,6.84]})
    colors = {"Abrysvo": "#1A3E6E", "Arexvy": "#E85D4A", "Mresvia": "#2EAF7D"}
    render_market_share_brand("Abrysvo", "Abrysvo QoQ Report", quarters, trx_ms, nbrx_ms, claims, colors)


# =====================================================
# PAXLOVID PAGE
# =====================================================

def render_paxlovid():
    quarters = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]
    trx_ms = {"Paxlovid": [89.54,92.4,93.52,93.52,94.78,95.79,96.29,96.0,95.71,95.41], "Lagevrio": [10.46,7.6,6.48,6.48,5.22,4.21,3.71,4.0,4.29,4.59]}
    nbrx_ms = {"Paxlovid": [90.08,92.82,94.01,94.55,95.72,96.41,96.77,96.91,96.81,96.54], "Lagevrio": [9.92,7.18,5.99,5.45,4.28,3.59,3.23,3.09,3.19,3.46]}
    claims = pd.DataFrame({"Quarter": quarters, "TRX CLAIMS": [1659927,571683,2073919,695790,623056,298538,709705,287980,248239,30982], "NBRX CLAIMS": [1513456,509056,1864977,623227,569288,272461,661798,263463,227132,28174], "TRX MARKET SHARE": trx_ms["Paxlovid"], "NBRX MARKET SHARE": nbrx_ms["Paxlovid"], "TRX MARKET SHARE DIFF": [1.76,3.28,4.27,5.07,5.24,3.39,2.77,2.48,0.93,0.28], "NBRX MARKET SHARE DIFF": [2.12,3.72,4.66,5.52,5.64,3.59,2.75,2.36,1.09,0.63]})
    colors = {"Paxlovid": "#1A3E6E", "Lagevrio": "#E85D4A"}
    render_market_share_brand("Paxlovid", "Paxlovid QoQ Report", quarters, trx_ms, nbrx_ms, claims, colors)


# =====================================================
# ZAVZPRET PAGE (claims only, no market share)
# =====================================================

def render_zavzpret():
    quarters = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]
    claims_data = {
        "Quarter": quarters,
        "TRX CLAIMS": [11205,14272,15974,18508,14399,16355,17641,19435,17815,6498],
        "NBRX CLAIMS": [4999,5842,5718,6300,5103,5756,5933,6284,5742,2233],
        "TRX CLAIMS DIFFERENCE": [None,356700,186.17,87.33,28.51,14.6,10.44,5.01,23.72,-60.27],
        "NBRX CLAIMS DIFFERENCE": [None,292000,33.97,40.28,2.08,-1.47,3.76,-0.25,12.52,-61.21],
    }
    df = pd.DataFrame(claims_data)

    st.markdown(BRAND_PAGE_CSS, unsafe_allow_html=True)
    render_ribbon("Zavzpret QoQ Report")
    render_back_button()

    # KPIs
    latest_period = "2026Q2"
    latest_row = df[df["Quarter"] == latest_period].iloc[0]
    trx_diff = latest_row["TRX CLAIMS DIFFERENCE"]
    nbrx_diff = latest_row["NBRX CLAIMS DIFFERENCE"]

    trx_diff_str = f"+{trx_diff:.1f}%" if trx_diff >= 0 else f"{trx_diff:.1f}%"
    nbrx_diff_str = f"+{nbrx_diff:.1f}%" if nbrx_diff >= 0 else f"{nbrx_diff:.1f}%"
    trx_class = "positive" if trx_diff >= 0 else "negative"
    nbrx_class = "positive" if nbrx_diff >= 0 else "negative"

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Zavzpret TRX Claims Difference (YoY)</div>
            <div class="kpi-value {trx_class}">{trx_diff_str}</div>
            <div class="kpi-period">Latest: {latest_period}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Zavzpret NBRx Claims Difference (YoY)</div>
            <div class="kpi-value {nbrx_class}">{nbrx_diff_str}</div>
            <div class="kpi-period">Latest: {latest_period}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # TRX Claims Trend
    st.markdown('<div class="section-title">TRX Claims Trend \u2014 Zavzpret</div>', unsafe_allow_html=True)
    fig_trx = go.Figure()
    fig_trx.add_trace(go.Scatter(x=df["Quarter"], y=df["TRX CLAIMS"], mode="lines+markers", name="TRX Claims", line=dict(color="#1A3E6E", width=3), marker=dict(size=7)))
    fig_trx.update_layout(height=380, margin=dict(l=50,r=30,t=20,b=40), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", color="#1A3E6E"), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(26,62,110,0.06)", separatethousands=True), hovermode="x unified")
    st.plotly_chart(fig_trx, use_container_width=True)

    # NBRX Claims Trend
    st.markdown('<div class="section-title">NBRx Claims Trend \u2014 Zavzpret</div>', unsafe_allow_html=True)
    fig_nbrx = go.Figure()
    fig_nbrx.add_trace(go.Scatter(x=df["Quarter"], y=df["NBRX CLAIMS"], mode="lines+markers", name="NBRx Claims", line=dict(color="#2EAF7D", width=3), marker=dict(size=7)))
    fig_nbrx.update_layout(height=380, margin=dict(l=50,r=30,t=20,b=40), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", color="#1A3E6E"), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(26,62,110,0.06)", separatethousands=True), hovermode="x unified")
    st.plotly_chart(fig_nbrx, use_container_width=True)

    # Raw Data
    with st.expander("Zavzpret Claims Data", expanded=False):
        st.dataframe(df, use_container_width=True, hide_index=True)

    # Download
    st.markdown('<div class="section-title">Download Reports</div>', unsafe_allow_html=True)

    def generate_excel():
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Zavzpret Claims", index=False)
        return output.getvalue()

    st.download_button(label="\U0001f4e5 Download Excel", data=generate_excel(), file_name="zavzpret_claims.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# =====================================================
# ROUTING
# =====================================================

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

page = st.session_state["current_page"]

if page == "home":
    render_home()
elif page == "nurtec":
    render_nurtec()
elif page == "zavzpret":
    render_zavzpret()
elif page == "eliquis":
    render_eliquis()
elif page == "prevnar":
    render_prevnar()
elif page == "comirnaty":
    render_comirnaty()
elif page == "abrysvo":
    render_abrysvo()
elif page == "paxlovid":
    render_paxlovid()
