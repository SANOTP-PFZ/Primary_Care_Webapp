import streamlit as st
import os
import base64
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Zavzpret QoQ Report", layout="wide", initial_sidebar_state="collapsed")

# --- Helper: load logo as base64 ---
def get_logo_base64(filename):
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", filename)
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_logo_base64("zavz_logo.png")

# --- Zavzpret Data (from source table - Nasal market) ---
quarters = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]

claims_data = {
    "Quarter": quarters,
    "TRX CLAIMS": [11205, 14272, 15974, 18508, 14399, 16355, 17641, 19435, 17815, 6498],
    "NBRX CLAIMS": [4999, 5842, 5718, 6300, 5103, 5756, 5933, 6284, 5742, 2233],
    "TRX CLAIMS DIFFERENCE": [None, 356700, 186.169831602, 87.327935223, 28.505131638, 14.595011211, 10.435708026, 5.00864491, 23.723869713, -60.269030877],
    "NBRX CLAIMS DIFFERENCE": [None, 292000, 33.973758201, 40.280561122, 2.080416083, -1.472098596, 3.760055964, -0.253968254, 12.522045855, -61.205698402],
}

df = pd.DataFrame(claims_data)

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
        margin: 10px 50px 30px;
        font-family: 'Inter', sans-serif;
        max-width: calc(100% - 100px);
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
""", unsafe_allow_html=True)

# --- Top Ribbon ---
if logo_b64:
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" />'
else:
    logo_html = '<div class="logo-placeholder">LOGO</div>'

st.markdown(f"""
<div class="top-ribbon">
    {logo_html}
    <span class="title">Zavzpret QoQ Report</span>
</div>
""", unsafe_allow_html=True)

# --- Back button ---
if st.button("← Back to Home"):
    st.switch_page("app.py")

# --- Latest quarter KPIs: Claims Difference ---
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

# --- TRX Claims Trend ---
st.markdown('<div class="section-title">TRX Claims Trend — Zavzpret</div>', unsafe_allow_html=True)

fig_trx = go.Figure()
fig_trx.add_trace(go.Scatter(
    x=df["Quarter"],
    y=df["TRX CLAIMS"],
    mode="lines+markers",
    name="TRX Claims",
    line=dict(color="#1A3E6E", width=3),
    marker=dict(size=7),
    hovertemplate="<b>Zavzpret TRX</b><br>%{x}<br>%{y:,.0f}<extra></extra>"
))

fig_trx.update_layout(
    height=380,
    margin=dict(l=50, r=30, t=20, b=40),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#1A3E6E"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=13)),
    xaxis=dict(showgrid=False, tickfont=dict(size=12)),
    yaxis=dict(showgrid=True, gridcolor="rgba(26, 62, 110, 0.06)", tickfont=dict(size=12), title="", separatethousands=True),
    hovermode="x unified"
)
st.plotly_chart(fig_trx, use_container_width=True)

# --- NBRX Claims Trend ---
st.markdown('<div class="section-title">NBRx Claims Trend — Zavzpret</div>', unsafe_allow_html=True)

fig_nbrx = go.Figure()
fig_nbrx.add_trace(go.Scatter(
    x=df["Quarter"],
    y=df["NBRX CLAIMS"],
    mode="lines+markers",
    name="NBRx Claims",
    line=dict(color="#2EAF7D", width=3),
    marker=dict(size=7),
    hovertemplate="<b>Zavzpret NBRx</b><br>%{x}<br>%{y:,.0f}<extra></extra>"
))

fig_nbrx.update_layout(
    height=380,
    margin=dict(l=50, r=30, t=20, b=40),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#1A3E6E"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=13)),
    xaxis=dict(showgrid=False, tickfont=dict(size=12)),
    yaxis=dict(showgrid=True, gridcolor="rgba(26, 62, 110, 0.06)", tickfont=dict(size=12), title="", separatethousands=True),
    hovermode="x unified"
)
st.plotly_chart(fig_nbrx, use_container_width=True)

# --- Raw Data Tables ---
st.markdown('<div class="section-title">Raw Data Tables</div>', unsafe_allow_html=True)

claims_display = df[["Quarter", "TRX CLAIMS", "NBRX CLAIMS"]].copy()
claims_display["TRX CLAIMS"] = claims_display["TRX CLAIMS"].apply(lambda x: f"{x:,.0f}")
claims_display["NBRX CLAIMS"] = claims_display["NBRX CLAIMS"].apply(lambda x: f"{x:,.0f}")

diff_display = df[["Quarter", "TRX CLAIMS DIFFERENCE", "NBRX CLAIMS DIFFERENCE"]].copy()

def fmt_diff(val):
    if val is None or pd.isna(val):
        return "—"
    return f"{val:.1f}%"

diff_display["TRX CLAIMS DIFFERENCE"] = diff_display["TRX CLAIMS DIFFERENCE"].apply(fmt_diff)
diff_display["NBRX CLAIMS DIFFERENCE"] = diff_display["NBRX CLAIMS DIFFERENCE"].apply(fmt_diff)

# Claims table (collapsible)
with st.expander("Zavzpret Claims — Raw Data", expanded=False):
    claims_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>TRX Claims</th><th>NBRx Claims</th></tr></thead><tbody>'
    for _, row in claims_display.iterrows():
        claims_html += f'<tr><td>{row["Quarter"]}</td><td>{row["TRX CLAIMS"]}</td><td>{row["NBRX CLAIMS"]}</td></tr>'
    claims_html += '</tbody></table>'
    st.markdown(claims_html, unsafe_allow_html=True)

# Claims Difference table (collapsible)
with st.expander("Zavzpret Claims Difference (vs STLY %)", expanded=False):
    diff_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>TRX Claims Diff (%)</th><th>NBRx Claims Diff (%)</th></tr></thead><tbody>'
    for _, row in diff_display.iterrows():
        diff_html += f'<tr><td>{row["Quarter"]}</td><td>{row["TRX CLAIMS DIFFERENCE"]}</td><td>{row["NBRX CLAIMS DIFFERENCE"]}</td></tr>'
    diff_html += '</tbody></table>'
    st.markdown(diff_html, unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# --- Download section ---
st.markdown('<div class="section-title">Download Reports</div>', unsafe_allow_html=True)

export_df = df.copy()
export_df = export_df.rename(columns={
    "Quarter": "Quarter",
    "TRX CLAIMS": "TRX Claims",
    "NBRX CLAIMS": "NBRx Claims",
    "TRX CLAIMS DIFFERENCE": "TRX Claims Diff (%)",
    "NBRX CLAIMS DIFFERENCE": "NBRx Claims Diff (%)",
})

def generate_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        export_df.to_excel(writer, sheet_name="Zavzpret Claims", index=False)
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
        elements.append(Paragraph("Zavzpret — Claims Report", title_style))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>Latest Quarter:</b> {latest_period}", kpi_style))
        elements.append(Paragraph(f"<b>TRX Claims Difference (YoY):</b> {trx_diff_str}", kpi_style))
        elements.append(Paragraph(f"<b>NBRx Claims Difference (YoY):</b> {nbrx_diff_str}", kpi_style))
        elements.append(Spacer(1, 10))

        # --- TRX Claims Chart ---
        elements.append(Paragraph("TRX Claims Trend — Zavzpret", heading_style))
        trx_img_bytes = BytesIO(fig_trx.to_image(format="png", width=900, height=350, scale=2))
        elements.append(Image(trx_img_bytes, width=7.5*inch, height=2.8*inch))
        elements.append(Spacer(1, 10))

        # --- NBRX Claims Chart ---
        elements.append(Paragraph("NBRx Claims Trend — Zavzpret", heading_style))
        nbrx_img_bytes = BytesIO(fig_nbrx.to_image(format="png", width=900, height=350, scale=2))
        elements.append(Image(nbrx_img_bytes, width=7.5*inch, height=2.8*inch))
        elements.append(Spacer(1, 10))

        # --- Raw Claims Table ---
        elements.append(Paragraph("Zavzpret Claims — Raw Data", heading_style))
        claims_table_data = [["Quarter", "TRX Claims", "NBRx Claims"]]
        for _, row in df.iterrows():
            claims_table_data.append([row["Quarter"], f"{row['TRX CLAIMS']:,.0f}", f"{row['NBRX CLAIMS']:,.0f}"])
        t = Table(claims_table_data, colWidths=[1.5*inch, 2*inch, 2*inch])
        t.setStyle(table_style)
        elements.append(t)
        elements.append(Spacer(1, 10))

        # --- Claims Difference Table ---
        elements.append(Paragraph("Zavzpret Claims Difference (YoY %)", heading_style))
        diff_table_data = [["Quarter", "TRX Claims Diff (%)", "NBRx Claims Diff (%)"]]
        for _, row in diff_display.iterrows():
            diff_table_data.append([row["Quarter"], row["TRX CLAIMS DIFFERENCE"], row["NBRX CLAIMS DIFFERENCE"]])
        t = Table(diff_table_data, colWidths=[1.5*inch, 2*inch, 2*inch])
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
        file_name="zavzpret_claims.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
with col2:
    pdf_data = generate_pdf()
    if pdf_data:
        st.download_button(
            label="📄 Download PDF",
            data=pdf_data,
            file_name="zavzpret_claims.pdf",
            mime="application/pdf"
        )
    else:
        st.info("Install `reportlab` for PDF export: pip install reportlab")
