import streamlit as st
import os
import base64
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Nurtec QoQ Report", layout="wide", initial_sidebar_state="collapsed")

# --- Helper: load logo as base64 ---
def get_logo_base64(filename):
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", filename)
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_logo_base64("nurtec_logo.png")

# --- Market Share Data (Oral CGRP: Nurtec, Ubrelvy, Qulipta) ---
data = {
    "BRAND": ["Nurtec"]*10 + ["Ubrelvy"]*10 + ["Qulipta"]*10,
    "TIME PERIOD": ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"] * 3,
    "TRX MARKET SHARE": [
        # Nurtec
        45.03, 45.31, 44.85, 44.88, 43.42, 43.15, 42.66, 42.6, 42.73, 43.22,
        # Ubrelvy
        33.48, 33.39, 33.08, 32.64, 32.94, 33.08, 33.27, 33.33, 32.54, 31.71,
        # Qulipta
        21.49, 21.3, 22.06, 22.48, 23.64, 23.77, 24.07, 24.07, 24.72, 25.07,
    ],
    "NBRX MARKET SHARE": [
        # Nurtec
        43.06, 43.91, 43.9, 44.0, 42.82, 42.45, 41.29, 42.06, 43.14, 43.21,
        # Ubrelvy
        35.97, 35.66, 35.24, 34.63, 35.33, 35.88, 36.51, 36.12, 35.43, 35.51,
        # Qulipta
        20.97, 20.43, 20.85, 21.37, 21.85, 21.67, 22.2, 21.82, 21.43, 21.28,
    ],
    "TRX MS DIFF VS STLY": [
        # Nurtec
        -2.46, -1.69, -1.59, -1.65, -1.61, -2.16, -2.2, -2.28, -0.68, 0.04,
        # Ubrelvy
        -1.73, -1.5, -1.39, -1.02, -0.54, -0.3, 0.19, 0.69, -0.4, -1.22,
        # Qulipta
        4.19, 3.2, 2.98, 2.67, 2.15, 2.46, 2.01, 1.59, 1.08, 1.18,
    ],
    "NBRX MS DIFF VS STLY": [
        # Nurtec
        -1.09, -0.15, -0.18, -0.4, -0.24, -1.47, -2.62, -1.94, 0.32, 0.68,
        # Ubrelvy
        -1.42, -1.05, -0.16, -0.69, -0.64, 0.22, 1.27, 1.48, 0.1, -0.2,
        # Qulipta
        2.51, 1.2, 0.34, 1.09, 0.88, 1.25, 1.35, 0.46, -0.42, -0.48,
    ],
}

df = pd.DataFrame(data)

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
""", unsafe_allow_html=True)

# --- Top Ribbon ---
if logo_b64:
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" />'
else:
    logo_html = '<div class="logo-placeholder">LOGO</div>'

st.markdown(f"""
<div class="top-ribbon">
    {logo_html}
    <span class="title">Nurtec QoQ Report</span>
</div>
""", unsafe_allow_html=True)

# --- Back button ---
if st.button("← Back to Home"):
    st.switch_page("app.py")

# --- Latest quarter KPIs for Nurtec ---
latest_period = "2026Q2"
nurtec_df = df[df["BRAND"] == "Nurtec"]
nurtec_latest = nurtec_df[nurtec_df["TIME PERIOD"] == latest_period]

trx_val = f"{nurtec_latest['TRX MARKET SHARE'].values[0]:.1f}%"
nbrx_val = f"{nurtec_latest['NBRX MARKET SHARE'].values[0]:.1f}%"

# Market share difference (vs STLY) from data
trx_ms_diff = nurtec_latest['TRX MS DIFF VS STLY'].values[0]
nbrx_ms_diff = nurtec_latest['NBRX MS DIFF VS STLY'].values[0]

trx_diff_sign = "+" if trx_ms_diff >= 0 else ""
nbrx_diff_sign = "+" if nbrx_ms_diff >= 0 else ""
trx_diff_color = "#2EAF7D" if trx_ms_diff >= 0 else "#E85D4A"
nbrx_diff_color = "#2EAF7D" if nbrx_ms_diff >= 0 else "#E85D4A"

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Nurtec TRX Market Share</div>
        <div class="kpi-value">{trx_val} <span style="font-size:18px; color:{trx_diff_color}; font-weight:600;">({trx_diff_sign}{trx_ms_diff:.1f}pp vs STLY)</span></div>
        <div class="kpi-period">Latest: {latest_period}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Nurtec NBRx Market Share</div>
        <div class="kpi-value">{nbrx_val} <span style="font-size:18px; color:{nbrx_diff_color}; font-weight:600;">({nbrx_diff_sign}{nbrx_ms_diff:.1f}pp vs STLY)</span></div>
        <div class="kpi-period">Latest: {latest_period}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- TRX Market Share Trend ---
st.markdown('<div class="section-title">TRX Market Share Trend — Oral CGRP Market</div>', unsafe_allow_html=True)

brand_colors = {"Nurtec": "#1A3E6E", "Ubrelvy": "#E85D4A", "Qulipta": "#2EAF7D"}

fig_trx = go.Figure()
for brand in ["Nurtec", "Ubrelvy", "Qulipta"]:
    brand_data = df[df["BRAND"] == brand].sort_values("TIME PERIOD")
    fig_trx.add_trace(go.Scatter(
        x=brand_data["TIME PERIOD"],
        y=brand_data["TRX MARKET SHARE"],
        mode="lines+markers",
        name=brand,
        line=dict(color=brand_colors[brand], width=3),
        marker=dict(size=7),
        hovertemplate=f"<b>{brand}</b><br>%{{x}}<br>%{{y:.1f}}%<extra></extra>"
    ))

fig_trx.update_layout(
    height=380,
    margin=dict(l=50, r=30, t=20, b=40),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#1A3E6E"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=13)),
    xaxis=dict(showgrid=False, tickfont=dict(size=12)),
    yaxis=dict(showgrid=True, gridcolor="rgba(26, 62, 110, 0.06)", ticksuffix="%", tickfont=dict(size=12), title=""),
    hovermode="x unified"
)
st.plotly_chart(fig_trx, use_container_width=True)

# --- NBRX Market Share Trend ---
st.markdown('<div class="section-title">NBRx Market Share Trend — Oral CGRP Market</div>', unsafe_allow_html=True)

fig_nbrx = go.Figure()
for brand in ["Nurtec", "Ubrelvy", "Qulipta"]:
    brand_data = df[df["BRAND"] == brand].sort_values("TIME PERIOD")
    fig_nbrx.add_trace(go.Scatter(
        x=brand_data["TIME PERIOD"],
        y=brand_data["NBRX MARKET SHARE"],
        mode="lines+markers",
        name=brand,
        line=dict(color=brand_colors[brand], width=3),
        marker=dict(size=7),
        hovertemplate=f"<b>{brand}</b><br>%{{x}}<br>%{{y:.1f}}%<extra></extra>"
    ))

fig_nbrx.update_layout(
    height=380,
    margin=dict(l=50, r=30, t=20, b=40),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#1A3E6E"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=13)),
    xaxis=dict(showgrid=False, tickfont=dict(size=12)),
    yaxis=dict(showgrid=True, gridcolor="rgba(26, 62, 110, 0.06)", ticksuffix="%", tickfont=dict(size=12), title=""),
    hovermode="x unified"
)
st.plotly_chart(fig_nbrx, use_container_width=True)

# --- TRX & NBRX Claims Tables ---
claims_data = {
    "Quarter": ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"],
    "Nurtec TRX": [676214, 750986, 781454, 838399, 771398, 836705, 874415, 931369, 894657, 315451],
    "Ubrelvy TRX": [502700, 553360, 576369, 609711, 585282, 641463, 681994, 728592, 681294, 231485],
    "Qulipta TRX": [322715, 353067, 384388, 420054, 420033, 460811, 493403, 526227, 517570, 182965],
    "Nurtec NBRx": [102162, 108147, 110278, 111502, 110073, 111782, 112903, 115924, 120180, 42793],
    "Ubrelvy NBRx": [85326, 87822, 88521, 87751, 90805, 94495, 99856, 99533, 98702, 35169],
    "Qulipta NBRx": [49758, 50306, 52379, 54139, 56159, 57075, 60709, 60140, 59695, 21074],
}
claims_df = pd.DataFrame(claims_data)

st.markdown('<div class="section-title">Raw Data Tables</div>', unsafe_allow_html=True)

trx_claims_df = claims_df[["Quarter", "Nurtec TRX", "Ubrelvy TRX", "Qulipta TRX"]].copy()
trx_claims_df.columns = ["Quarter", "Nurtec", "Ubrelvy", "Qulipta"]
# Format numbers with commas
trx_display = trx_claims_df.copy()
for col in ["Nurtec", "Ubrelvy", "Qulipta"]:
    trx_display[col] = trx_display[col].apply(lambda x: f"{x:,.0f}")

nbrx_claims_df = claims_df[["Quarter", "Nurtec NBRx", "Ubrelvy NBRx", "Qulipta NBRx"]].copy()
nbrx_claims_df.columns = ["Quarter", "Nurtec", "Ubrelvy", "Qulipta"]

quarters = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]
trx_ms_data = {
    "Quarter": quarters,
    "Nurtec": [df[(df["BRAND"]=="Nurtec") & (df["TIME PERIOD"]==q)]["TRX MARKET SHARE"].values[0] for q in quarters],
    "Ubrelvy": [df[(df["BRAND"]=="Ubrelvy") & (df["TIME PERIOD"]==q)]["TRX MARKET SHARE"].values[0] for q in quarters],
    "Qulipta": [df[(df["BRAND"]=="Qulipta") & (df["TIME PERIOD"]==q)]["TRX MARKET SHARE"].values[0] for q in quarters],
}
trx_ms_display = pd.DataFrame(trx_ms_data)
for col in ["Nurtec", "Ubrelvy", "Qulipta"]:
    trx_ms_display[col] = trx_ms_display[col].apply(lambda x: f"{x:.1f}%")

nbrx_ms_data = {
    "Quarter": quarters,
    "Nurtec": [df[(df["BRAND"]=="Nurtec") & (df["TIME PERIOD"]==q)]["NBRX MARKET SHARE"].values[0] for q in quarters],
    "Ubrelvy": [df[(df["BRAND"]=="Ubrelvy") & (df["TIME PERIOD"]==q)]["NBRX MARKET SHARE"].values[0] for q in quarters],
    "Qulipta": [df[(df["BRAND"]=="Qulipta") & (df["TIME PERIOD"]==q)]["NBRX MARKET SHARE"].values[0] for q in quarters],
}
nbrx_ms_display = pd.DataFrame(nbrx_ms_data)
for col in ["Nurtec", "Ubrelvy", "Qulipta"]:
    nbrx_ms_display[col] = nbrx_ms_display[col].apply(lambda x: f"{x:.1f}%")

st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

# TRX Claims table (collapsible)
with st.expander("TRX Claims — Raw Data", expanded=False):
    trx_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>Nurtec</th><th>Ubrelvy</th><th>Qulipta</th></tr></thead><tbody>'
    for _, row in trx_display.iterrows():
        trx_html += f'<tr><td>{row["Quarter"]}</td><td>{row["Nurtec"]}</td><td>{row["Ubrelvy"]}</td><td>{row["Qulipta"]}</td></tr>'
    trx_html += '</tbody></table>'
    st.markdown(trx_html, unsafe_allow_html=True)

# NBRX Claims table (collapsible)
with st.expander("NBRx Claims — Raw Data", expanded=False):
    nbrx_display = nbrx_claims_df.copy()
    for col in ["Nurtec", "Ubrelvy", "Qulipta"]:
        nbrx_display[col] = nbrx_display[col].apply(lambda x: f"{x:,.0f}")
    nbrx_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>Nurtec</th><th>Ubrelvy</th><th>Qulipta</th></tr></thead><tbody>'
    for _, row in nbrx_display.iterrows():
        nbrx_html += f'<tr><td>{row["Quarter"]}</td><td>{row["Nurtec"]}</td><td>{row["Ubrelvy"]}</td><td>{row["Qulipta"]}</td></tr>'
    nbrx_html += '</tbody></table>'
    st.markdown(nbrx_html, unsafe_allow_html=True)

# TRX Market Share table (collapsible)
with st.expander("TRX Market Share (%) — Raw Data", expanded=False):
    trx_ms_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>Nurtec</th><th>Ubrelvy</th><th>Qulipta</th></tr></thead><tbody>'
    for _, row in trx_ms_display.iterrows():
        trx_ms_html += f'<tr><td>{row["Quarter"]}</td><td>{row["Nurtec"]}</td><td>{row["Ubrelvy"]}</td><td>{row["Qulipta"]}</td></tr>'
    trx_ms_html += '</tbody></table>'
    st.markdown(trx_ms_html, unsafe_allow_html=True)

# NBRX Market Share table (collapsible)
with st.expander("NBRx Market Share (%) — Raw Data", expanded=False):
    nbrx_ms_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>Nurtec</th><th>Ubrelvy</th><th>Qulipta</th></tr></thead><tbody>'
    for _, row in nbrx_ms_display.iterrows():
        nbrx_ms_html += f'<tr><td>{row["Quarter"]}</td><td>{row["Nurtec"]}</td><td>{row["Ubrelvy"]}</td><td>{row["Qulipta"]}</td></tr>'
    nbrx_ms_html += '</tbody></table>'
    st.markdown(nbrx_ms_html, unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# --- Download section ---
st.markdown('<div class="section-title">Download Reports</div>', unsafe_allow_html=True)

# Prepare export dataframe
export_df = df.copy()
export_df = export_df.rename(columns={
    "BRAND": "Brand",
    "TIME PERIOD": "Quarter",
    "TRX MARKET SHARE": "TRX Market Share (%)",
    "NBRX MARKET SHARE": "NBRx Market Share (%)",
})

# Excel download
def generate_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        export_df.to_excel(writer, sheet_name="Oral CGRP Market Share", index=False)
    return output.getvalue()

# PDF download — full page view
def generate_pdf():
    try:
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

        output = BytesIO()
        doc = SimpleDocTemplate(output, pagesize=landscape(letter), leftMargin=40, rightMargin=40, topMargin=30, bottomMargin=30)
        elements = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle("CustomTitle", parent=styles["Title"], fontSize=20, textColor=colors.HexColor("#1A3E6E"), spaceAfter=6)
        heading_style = ParagraphStyle("CustomHeading", parent=styles["Heading2"], fontSize=14, textColor=colors.HexColor("#1A3E6E"), spaceBefore=16, spaceAfter=8)
        kpi_style = ParagraphStyle("KPI", parent=styles["Normal"], fontSize=12, textColor=colors.HexColor("#1A3E6E"), spaceAfter=4)

        table_style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A3E6E")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D8E0")),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0F4F8")]),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ("TOPPADDING", (0, 1), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
        ])

        # --- Title & KPIs ---
        elements.append(Paragraph("Nurtec — Oral CGRP Market Report", title_style))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>Latest Quarter:</b> {latest_period}", kpi_style))
        elements.append(Paragraph(f"<b>Nurtec TRX Market Share:</b> {trx_val} ({trx_diff_sign}{trx_ms_diff:.1f}pp vs STLY)", kpi_style))
        elements.append(Paragraph(f"<b>Nurtec NBRx Market Share:</b> {nbrx_val} ({nbrx_diff_sign}{nbrx_ms_diff:.1f}pp vs STLY)", kpi_style))
        elements.append(Spacer(1, 10))

        # --- TRX Market Share Chart ---
        elements.append(Paragraph("TRX Market Share Trend — Oral CGRP Market", heading_style))
        trx_img_bytes = BytesIO(fig_trx.to_image(format="png", width=900, height=350, scale=2))
        elements.append(Image(trx_img_bytes, width=7.5*inch, height=2.8*inch))
        elements.append(Spacer(1, 10))

        # --- NBRX Market Share Chart ---
        elements.append(Paragraph("NBRx Market Share Trend — Oral CGRP Market", heading_style))
        nbrx_img_bytes = BytesIO(fig_nbrx.to_image(format="png", width=900, height=350, scale=2))
        elements.append(Image(nbrx_img_bytes, width=7.5*inch, height=2.8*inch))
        elements.append(Spacer(1, 10))

        # --- TRX Claims Table ---
        elements.append(Paragraph("TRX Claims — Oral CGRP Market", heading_style))
        trx_table_data = [["Quarter", "Nurtec", "Ubrelvy", "Qulipta"]]
        for _, row in trx_claims_df.iterrows():
            trx_table_data.append([row["Quarter"], f"{row['Nurtec']:,.0f}", f"{row['Ubrelvy']:,.0f}", f"{row['Qulipta']:,.0f}"])
        t = Table(trx_table_data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        t.setStyle(table_style)
        elements.append(t)
        elements.append(Spacer(1, 10))

        # --- NBRX Claims Table ---
        elements.append(Paragraph("NBRx Claims — Oral CGRP Market", heading_style))
        nbrx_table_data = [["Quarter", "Nurtec", "Ubrelvy", "Qulipta"]]
        for _, row in nbrx_claims_df.iterrows():
            nbrx_table_data.append([row["Quarter"], f"{row['Nurtec']:,.0f}", f"{row['Ubrelvy']:,.0f}", f"{row['Qulipta']:,.0f}"])
        t = Table(nbrx_table_data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        t.setStyle(table_style)
        elements.append(t)
        elements.append(Spacer(1, 10))

        # --- TRX Market Share Table ---
        elements.append(Paragraph("TRX Market Share (%) — Oral CGRP Market", heading_style))
        trx_ms_table_data = [["Quarter", "Nurtec", "Ubrelvy", "Qulipta"]]
        for _, row in trx_ms_display.iterrows():
            trx_ms_table_data.append([row["Quarter"], row["Nurtec"], row["Ubrelvy"], row["Qulipta"]])
        t = Table(trx_ms_table_data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        t.setStyle(table_style)
        elements.append(t)
        elements.append(Spacer(1, 10))

        # --- NBRX Market Share Table ---
        elements.append(Paragraph("NBRx Market Share (%) — Oral CGRP Market", heading_style))
        nbrx_ms_table_data = [["Quarter", "Nurtec", "Ubrelvy", "Qulipta"]]
        for _, row in nbrx_ms_display.iterrows():
            nbrx_ms_table_data.append([row["Quarter"], row["Nurtec"], row["Ubrelvy"], row["Qulipta"]])
        t = Table(nbrx_ms_table_data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        t.setStyle(table_style)
        elements.append(t)

        doc.build(elements)
        return output.getvalue()
    except ImportError:
        return None

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    st.download_button(
        label="📥 Download Excel",
        data=generate_excel(),
        file_name="nurtec_market_share.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
with col2:
    pdf_data = generate_pdf()
    if pdf_data:
        st.download_button(
            label="📄 Download PDF",
            data=pdf_data,
            file_name="nurtec_market_share.pdf",
            mime="application/pdf"
        )
    else:
        st.info("Install `reportlab` for PDF export: pip install reportlab")
