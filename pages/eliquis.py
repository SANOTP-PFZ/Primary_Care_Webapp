import streamlit as st
import os
import base64
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Eliquis QoQ Report", layout="wide", initial_sidebar_state="collapsed")

# --- Helper: load logo as base64 ---
def get_logo_base64(filename):
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", filename)
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_logo_base64("eliquis.png")

# --- Eliquis Market Share Data ---
quarters = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]

trx_market_share = {
    "Eliquis": [63.56526803, 64.233685013, 64.910910573, 65.355728932, 66.287349386, 67.192619774, 68.217762818, 69.086974117, 69.314747459, 69.859805417],
    "Xarelto": [19.659307566, 19.46262116, 19.22797907, 19.055411243, 18.280029451, 17.684563399, 17.069657226, 16.602052057, 16.097691746, 15.902069399],
    "Warfarin": [14.49323201, 14.085817022, 13.603589134, 13.278612887, 13.036894013, 12.695593521, 12.408279637, 12.005831206, 12.41542686, 12.224760499],
    "Dabigatran": [0.6547257313, 0.7624722368, 0.8506107041, 0.9497369099, 1.124967971, 1.281216727, 1.372827005, 1.460702011, 1.670641561, 1.76025139],
    "Jantoven": [1.258261126, 1.155562539, 1.13921501, 1.133982233, 1.104784438, 1.011777692, 0.8180241156, 0.7501470916, 0.4299664588, 0.1935519734],
    "Pradaxa": [0.3400962381, 0.2759094142, 0.2442402244, 0.2037980421, 0.1436412577, 0.1120448518, 0.09269329605, 0.07376316107, 0.05215447241, 0.04067493605],
    "Savaysa": [0.02910929904, 0.02393261504, 0.02345528394, 0.02272975275, 0.02233348414, 0.02218403525, 0.02075590253, 0.02053035684, 0.01937144259, 0.01888638633],
}

nbrx_market_share = {
    "Eliquis": [70.411155758, 71.718779544, 71.817889947, 72.794275079, 72.066568281, 73.984553564, 74.828296283, 76.014192086, 74.220809807, 75.407381438],
    "Xarelto": [18.928156835, 18.574104793, 18.489768, 17.67626859, 15.946499121, 14.886936448, 14.084937782, 13.778814776, 13.533111931, 12.585183075],
    "Warfarin": [6.99853069, 6.572431244, 6.446578631, 6.260602467, 7.293565968, 6.957757052, 7.288827875, 6.349568845, 8.021869913, 7.950785547],
    "Dabigatran": [1.495611796, 1.824006565, 2.051704403, 2.22466525, 3.26076838, 3.057807768, 2.973841773, 3.144930966, 3.802550695, 3.81817385],
    "Jantoven": [1.56889797, 1.052270219, 0.995142243, 0.888136766, 1.270372821, 0.982050009, 0.708970185, 0.621557222, 0.36799647, 0.191365193],
    "Pradaxa": [0.572899419, 0.238426972, 0.174209219, 0.13573903, 0.140628471, 0.113810179, 0.096232916, 0.07594059, 0.037682075, 0.033598469],
    "Savaysa": [0.024747533, 0.019980663, 0.024707557, 0.020312817, 0.021596959, 0.01708498, 0.018893186, 0.014995515, 0.015979108, 0.013512428],
}

# Eliquis claims data
eliquis_claims = {
    "Quarter": quarters,
    "TRX CLAIMS": [8166947, 8306792, 8462808, 8660519, 8663797, 8901857, 9150084, 9455968, 9059983, 3129312],
    "NBRX CLAIMS": [588952, 534822, 514489, 530382, 580618, 549959, 550523, 552535, 622412, 206482],
    "TRX MARKET SHARE": [63.56526803, 64.233685013, 64.910910573, 65.355728932, 66.287349386, 67.192619774, 68.217762818, 69.086974117, 69.314747459, 69.859805417],
    "NBRX MARKET SHARE": [70.411155758, 71.718779544, 71.817889947, 72.794275079, 72.066568281, 73.984553564, 74.828296283, 76.014192086, 74.220809807, 75.407381438],
    "TRX MARKET SHARE DIFF": [4.489980828, 4.182684787, 3.983594744, 3.4670991200, 2.722081356, 2.958934761, 3.306852245, 3.731245185, 3.027398073, 2.667185643],
    "NBRX MARKET SHARE DIFF": [3.789258013, 3.17671157, 2.351761272, 2.168484643, 1.655412523, 2.26577402, 3.010406336, 3.219917007, 2.154241526, 1.422827874],
}

df = pd.DataFrame(eliquis_claims)

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
    <span class="title">Eliquis QoQ Report</span>
</div>
""", unsafe_allow_html=True)

# --- Back button ---
if st.button("← Back to Home"):
    st.switch_page("app.py")

# --- Latest quarter KPIs ---
latest_period = "2026Q2"
latest_row = df[df["Quarter"] == latest_period].iloc[0]

trx_val = f"{latest_row['TRX MARKET SHARE']:.1f}%"
nbrx_val = f"{latest_row['NBRX MARKET SHARE']:.1f}%"

trx_ms_diff = latest_row["TRX MARKET SHARE DIFF"]
nbrx_ms_diff = latest_row["NBRX MARKET SHARE DIFF"]

trx_diff_sign = "+" if trx_ms_diff >= 0 else ""
nbrx_diff_sign = "+" if nbrx_ms_diff >= 0 else ""
trx_diff_color = "#2EAF7D" if trx_ms_diff >= 0 else "#E85D4A"
nbrx_diff_color = "#2EAF7D" if nbrx_ms_diff >= 0 else "#E85D4A"

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Eliquis TRX Market Share</div>
        <div class="kpi-value">{trx_val} <span style="font-size:18px; color:{trx_diff_color}; font-weight:600;">({trx_diff_sign}{trx_ms_diff:.1f}pp vs STLY)</span></div>
        <div class="kpi-period">Latest: {latest_period}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Eliquis NBRx Market Share</div>
        <div class="kpi-value">{nbrx_val} <span style="font-size:18px; color:{nbrx_diff_color}; font-weight:600;">({nbrx_diff_sign}{nbrx_ms_diff:.1f}pp vs STLY)</span></div>
        <div class="kpi-period">Latest: {latest_period}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- TRX Market Share Trend ---
st.markdown('<div class="section-title">TRX Market Share Trend — Oral Anticoagulant Market</div>', unsafe_allow_html=True)

brand_colors = {
    "Eliquis": "#1A3E6E",
    "Xarelto": "#E85D4A",
    "Warfarin": "#2EAF7D",
    "Dabigatran": "#F5A623",
    "Jantoven": "#9B59B6",
    "Pradaxa": "#3498DB",
    "Savaysa": "#95A5A6",
}

fig_trx = go.Figure()
for brand in ["Eliquis", "Xarelto", "Warfarin", "Dabigatran", "Jantoven", "Pradaxa", "Savaysa"]:
    fig_trx.add_trace(go.Scatter(
        x=quarters,
        y=trx_market_share[brand],
        mode="lines+markers",
        name=brand,
        line=dict(color=brand_colors[brand], width=3 if brand == "Eliquis" else 2),
        marker=dict(size=7 if brand == "Eliquis" else 5),
        hovertemplate=f"<b>{brand}</b><br>%{{x}}<br>%{{y:.1f}}%<extra></extra>"
    ))

fig_trx.update_layout(
    height=420,
    margin=dict(l=50, r=30, t=20, b=40),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#1A3E6E"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=12)),
    xaxis=dict(showgrid=False, tickfont=dict(size=12)),
    yaxis=dict(showgrid=True, gridcolor="rgba(26, 62, 110, 0.06)", ticksuffix="%", tickfont=dict(size=12), title=""),
    hovermode="x unified"
)
st.plotly_chart(fig_trx, use_container_width=True)

# --- NBRX Market Share Trend ---
st.markdown('<div class="section-title">NBRx Market Share Trend — Oral Anticoagulant Market</div>', unsafe_allow_html=True)

fig_nbrx = go.Figure()
for brand in ["Eliquis", "Xarelto", "Warfarin", "Dabigatran", "Jantoven", "Pradaxa", "Savaysa"]:
    fig_nbrx.add_trace(go.Scatter(
        x=quarters,
        y=nbrx_market_share[brand],
        mode="lines+markers",
        name=brand,
        line=dict(color=brand_colors[brand], width=3 if brand == "Eliquis" else 2),
        marker=dict(size=7 if brand == "Eliquis" else 5),
        hovertemplate=f"<b>{brand}</b><br>%{{x}}<br>%{{y:.1f}}%<extra></extra>"
    ))

fig_nbrx.update_layout(
    height=420,
    margin=dict(l=50, r=30, t=20, b=40),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#1A3E6E"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=12)),
    xaxis=dict(showgrid=False, tickfont=dict(size=12)),
    yaxis=dict(showgrid=True, gridcolor="rgba(26, 62, 110, 0.06)", ticksuffix="%", tickfont=dict(size=12), title=""),
    hovermode="x unified"
)
st.plotly_chart(fig_nbrx, use_container_width=True)

# --- Raw Data Tables ---
st.markdown('<div class="section-title">Raw Data Tables</div>', unsafe_allow_html=True)

# TRX Claims (collapsible)
with st.expander("Eliquis TRX Claims — Raw Data", expanded=False):
    trx_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>TRX Claims</th></tr></thead><tbody>'
    for _, row in df.iterrows():
        trx_html += f'<tr><td>{row["Quarter"]}</td><td>{row["TRX CLAIMS"]:,.0f}</td></tr>'
    trx_html += '</tbody></table>'
    st.markdown(trx_html, unsafe_allow_html=True)

# NBRX Claims (collapsible)
with st.expander("Eliquis NBRx Claims — Raw Data", expanded=False):
    nbrx_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>NBRx Claims</th></tr></thead><tbody>'
    for _, row in df.iterrows():
        nbrx_html += f'<tr><td>{row["Quarter"]}</td><td>{row["NBRX CLAIMS"]:,.0f}</td></tr>'
    nbrx_html += '</tbody></table>'
    st.markdown(nbrx_html, unsafe_allow_html=True)

# TRX Market Share (collapsible)
with st.expander("Eliquis TRX Market Share (%) — Raw Data", expanded=False):
    trx_ms_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>TRX Market Share (%)</th></tr></thead><tbody>'
    for _, row in df.iterrows():
        trx_ms_html += f'<tr><td>{row["Quarter"]}</td><td>{row["TRX MARKET SHARE"]:.1f}%</td></tr>'
    trx_ms_html += '</tbody></table>'
    st.markdown(trx_ms_html, unsafe_allow_html=True)

# NBRX Market Share (collapsible)
with st.expander("Eliquis NBRx Market Share (%) — Raw Data", expanded=False):
    nbrx_ms_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>NBRx Market Share (%)</th></tr></thead><tbody>'
    for _, row in df.iterrows():
        nbrx_ms_html += f'<tr><td>{row["Quarter"]}</td><td>{row["NBRX MARKET SHARE"]:.1f}%</td></tr>'
    nbrx_ms_html += '</tbody></table>'
    st.markdown(nbrx_ms_html, unsafe_allow_html=True)

# TRX Market Share Diff vs STLY (collapsible)
with st.expander("Eliquis TRX Market Share Diff (vs STLY) — Raw Data", expanded=False):
    trx_diff_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>TRX MS Diff (pp)</th></tr></thead><tbody>'
    for _, row in df.iterrows():
        val = row["TRX MARKET SHARE DIFF"]
        sign = "+" if val >= 0 else ""
        trx_diff_html += f'<tr><td>{row["Quarter"]}</td><td>{sign}{val:.2f}</td></tr>'
    trx_diff_html += '</tbody></table>'
    st.markdown(trx_diff_html, unsafe_allow_html=True)

# NBRX Market Share Diff vs STLY (collapsible)
with st.expander("Eliquis NBRx Market Share Diff (vs STLY) — Raw Data", expanded=False):
    nbrx_diff_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>NBRx MS Diff (pp)</th></tr></thead><tbody>'
    for _, row in df.iterrows():
        val = row["NBRX MARKET SHARE DIFF"]
        sign = "+" if val >= 0 else ""
        nbrx_diff_html += f'<tr><td>{row["Quarter"]}</td><td>{sign}{val:.2f}</td></tr>'
    nbrx_diff_html += '</tbody></table>'
    st.markdown(nbrx_diff_html, unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# --- Download section ---
st.markdown('<div class="section-title">Download Reports</div>', unsafe_allow_html=True)

export_df = df.rename(columns={
    "Quarter": "Quarter",
    "TRX CLAIMS": "TRX Claims",
    "NBRX CLAIMS": "NBRx Claims",
    "TRX MARKET SHARE": "TRX Market Share (%)",
    "NBRX MARKET SHARE": "NBRx Market Share (%)",
    "TRX MARKET SHARE DIFF": "TRX MS Diff vs STLY (pp)",
    "NBRX MARKET SHARE DIFF": "NBRx MS Diff vs STLY (pp)",
})

def generate_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        export_df.to_excel(writer, sheet_name="Eliquis Report", index=False)
    return output.getvalue()

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

        # Title & KPIs
        elements.append(Paragraph("Eliquis — Oral Anticoagulant Market Report", title_style))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>Latest Quarter:</b> {latest_period}", kpi_style))
        elements.append(Paragraph(f"<b>Eliquis TRX Market Share:</b> {trx_val} ({trx_diff_sign}{trx_ms_diff:.1f}pp vs STLY)", kpi_style))
        elements.append(Paragraph(f"<b>Eliquis NBRx Market Share:</b> {nbrx_val} ({nbrx_diff_sign}{nbrx_ms_diff:.1f}pp vs STLY)", kpi_style))
        elements.append(Spacer(1, 10))

        # TRX Market Share Chart
        elements.append(Paragraph("TRX Market Share Trend — Oral Anticoagulant Market", heading_style))
        trx_img_bytes = BytesIO(fig_trx.to_image(format="png", width=900, height=380, scale=2))
        elements.append(Image(trx_img_bytes, width=7.5*inch, height=2.8*inch))
        elements.append(Spacer(1, 10))

        # NBRX Market Share Chart
        elements.append(Paragraph("NBRx Market Share Trend — Oral Anticoagulant Market", heading_style))
        nbrx_img_bytes = BytesIO(fig_nbrx.to_image(format="png", width=900, height=380, scale=2))
        elements.append(Image(nbrx_img_bytes, width=7.5*inch, height=2.8*inch))
        elements.append(Spacer(1, 10))

        # Claims Table
        elements.append(Paragraph("Eliquis Claims Data", heading_style))
        claims_table_data = [["Quarter", "TRX Claims", "NBRx Claims"]]
        for _, row in df.iterrows():
            claims_table_data.append([row["Quarter"], f"{row['TRX CLAIMS']:,.0f}", f"{row['NBRX CLAIMS']:,.0f}"])
        t = Table(claims_table_data, colWidths=[1.5*inch, 2*inch, 2*inch])
        t.setStyle(table_style)
        elements.append(t)
        elements.append(Spacer(1, 10))

        # Market Share Table
        elements.append(Paragraph("Eliquis Market Share & Diff vs STLY", heading_style))
        ms_table_data = [["Quarter", "TRX MS (%)", "NBRx MS (%)", "TRX Diff (pp)", "NBRx Diff (pp)"]]
        for _, row in df.iterrows():
            trx_s = "+" if row["TRX MARKET SHARE DIFF"] >= 0 else ""
            nbrx_s = "+" if row["NBRX MARKET SHARE DIFF"] >= 0 else ""
            ms_table_data.append([
                row["Quarter"],
                f"{row['TRX MARKET SHARE']:.1f}%",
                f"{row['NBRX MARKET SHARE']:.1f}%",
                f"{trx_s}{row['TRX MARKET SHARE DIFF']:.2f}",
                f"{nbrx_s}{row['NBRX MARKET SHARE DIFF']:.2f}",
            ])
        t = Table(ms_table_data, colWidths=[1.2*inch, 1.4*inch, 1.4*inch, 1.4*inch, 1.4*inch])
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
        file_name="eliquis_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
with col2:
    pdf_data = generate_pdf()
    if pdf_data:
        st.download_button(
            label="📄 Download PDF",
            data=pdf_data,
            file_name="eliquis_report.pdf",
            mime="application/pdf"
        )
    else:
        st.info("Install `reportlab` for PDF export: pip install reportlab")
