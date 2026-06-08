"""Paxlovid brand page - COVID Oral Treatment Market Share Report."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from shared import get_logo_base64, BRAND_PAGE_CSS, render_ribbon, render_back_button


def render():
    """Render the Paxlovid QoQ Report page."""
    logo_b64 = get_logo_base64("pax.png")

    # --- COVID Oral Treatment Market Share Data ---
    quarters = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]

    trx_market_share = {
        "Paxlovid": [89.54, 92.4, 93.52, 93.52, 94.78, 95.79, 96.29, 96.0, 95.71, 95.41],
        "Lagevrio": [10.46, 7.6, 6.48, 6.48, 5.22, 4.21, 3.71, 4.0, 4.29, 4.59],
    }

    nbrx_market_share = {
        "Paxlovid": [90.08, 92.82, 94.01, 94.55, 95.72, 96.41, 96.77, 96.91, 96.81, 96.54],
        "Lagevrio": [9.92, 7.18, 5.99, 5.45, 4.28, 3.59, 3.23, 3.09, 3.19, 3.46],
    }

    paxlovid_claims = {
        "Quarter": quarters,
        "TRX CLAIMS": [1659927, 571683, 2073919, 695790, 623056, 298538, 709705, 287980, 248239, 30982],
        "NBRX CLAIMS": [1513456, 509056, 1864977, 623227, 569288, 272461, 661798, 263463, 227132, 28174],
        "TRX MARKET SHARE": [89.54, 92.4, 93.52, 93.52, 94.78, 95.79, 96.29, 96.0, 95.71, 95.41],
        "NBRX MARKET SHARE": [90.08, 92.82, 94.01, 94.55, 95.72, 96.41, 96.77, 96.91, 96.81, 96.54],
        "TRX MARKET SHARE DIFF": [1.76, 3.28, 4.27, 5.07, 5.24, 3.39, 2.77, 2.48, 0.93, 0.28],
        "NBRX MARKET SHARE DIFF": [2.12, 3.72, 4.66, 5.52, 5.64, 3.59, 2.75, 2.36, 1.09, 0.63],
    }

    df = pd.DataFrame(paxlovid_claims)

    # --- CSS ---
    st.markdown(BRAND_PAGE_CSS, unsafe_allow_html=True)

    # --- Top Ribbon ---
    render_ribbon(logo_b64, "Paxlovid QoQ Report")

    # --- Back button ---
    render_back_button()

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
            <div class="kpi-label">Paxlovid TRX Market Share</div>
            <div class="kpi-value">{trx_val} <span style="font-size:18px; color:{trx_diff_color}; font-weight:600;">({trx_diff_sign}{trx_ms_diff:.1f}pp vs STLY)</span></div>
            <div class="kpi-period">Latest: {latest_period}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Paxlovid NBRx Market Share</div>
            <div class="kpi-value">{nbrx_val} <span style="font-size:18px; color:{nbrx_diff_color}; font-weight:600;">({nbrx_diff_sign}{nbrx_ms_diff:.1f}pp vs STLY)</span></div>
            <div class="kpi-period">Latest: {latest_period}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- TRX Market Share Trend ---
    st.markdown('<div class="section-title">TRX Market Share Trend \u2014 COVID Oral Treatment Market</div>', unsafe_allow_html=True)

    brand_colors = {"Paxlovid": "#1A3E6E", "Lagevrio": "#E85D4A"}

    fig_trx = go.Figure()
    for brand in ["Paxlovid", "Lagevrio"]:
        fig_trx.add_trace(go.Scatter(
            x=quarters,
            y=trx_market_share[brand],
            mode="lines+markers",
            name=brand,
            line=dict(color=brand_colors[brand], width=3 if brand == "Paxlovid" else 2),
            marker=dict(size=7 if brand == "Paxlovid" else 5),
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
    st.markdown('<div class="section-title">NBRx Market Share Trend \u2014 COVID Oral Treatment Market</div>', unsafe_allow_html=True)

    fig_nbrx = go.Figure()
    for brand in ["Paxlovid", "Lagevrio"]:
        fig_nbrx.add_trace(go.Scatter(
            x=quarters,
            y=nbrx_market_share[brand],
            mode="lines+markers",
            name=brand,
            line=dict(color=brand_colors[brand], width=3 if brand == "Paxlovid" else 2),
            marker=dict(size=7 if brand == "Paxlovid" else 5),
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

    with st.expander("Paxlovid TRX Claims \u2014 Raw Data", expanded=False):
        trx_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>TRX Claims</th></tr></thead><tbody>'
        for _, row in df.iterrows():
            trx_html += f'<tr><td>{row["Quarter"]}</td><td>{row["TRX CLAIMS"]:,.0f}</td></tr>'
        trx_html += '</tbody></table>'
        st.markdown(trx_html, unsafe_allow_html=True)

    with st.expander("Paxlovid NBRx Claims \u2014 Raw Data", expanded=False):
        nbrx_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>NBRx Claims</th></tr></thead><tbody>'
        for _, row in df.iterrows():
            nbrx_html += f'<tr><td>{row["Quarter"]}</td><td>{row["NBRX CLAIMS"]:,.0f}</td></tr>'
        nbrx_html += '</tbody></table>'
        st.markdown(nbrx_html, unsafe_allow_html=True)

    with st.expander("Paxlovid TRX Market Share (%) \u2014 Raw Data", expanded=False):
        trx_ms_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>TRX Market Share (%)</th></tr></thead><tbody>'
        for _, row in df.iterrows():
            trx_ms_html += f'<tr><td>{row["Quarter"]}</td><td>{row["TRX MARKET SHARE"]:.1f}%</td></tr>'
        trx_ms_html += '</tbody></table>'
        st.markdown(trx_ms_html, unsafe_allow_html=True)

    with st.expander("Paxlovid NBRx Market Share (%) \u2014 Raw Data", expanded=False):
        nbrx_ms_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>NBRx Market Share (%)</th></tr></thead><tbody>'
        for _, row in df.iterrows():
            nbrx_ms_html += f'<tr><td>{row["Quarter"]}</td><td>{row["NBRX MARKET SHARE"]:.1f}%</td></tr>'
        nbrx_ms_html += '</tbody></table>'
        st.markdown(nbrx_ms_html, unsafe_allow_html=True)

    with st.expander("Paxlovid TRX Market Share Diff (vs STLY) \u2014 Raw Data", expanded=False):
        trx_diff_html = '<table class="claims-table"><thead><tr><th>Quarter</th><th>TRX MS Diff (pp)</th></tr></thead><tbody>'
        for _, row in df.iterrows():
            val = row["TRX MARKET SHARE DIFF"]
            sign = "+" if val >= 0 else ""
            trx_diff_html += f'<tr><td>{row["Quarter"]}</td><td>{sign}{val:.2f}</td></tr>'
        trx_diff_html += '</tbody></table>'
        st.markdown(trx_diff_html, unsafe_allow_html=True)

    with st.expander("Paxlovid NBRx Market Share Diff (vs STLY) \u2014 Raw Data", expanded=False):
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
            export_df.to_excel(writer, sheet_name="Paxlovid Report", index=False)
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

            elements.append(Paragraph("Paxlovid \u2014 COVID Oral Treatment Market Report", title_style))
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(f"<b>Latest Quarter:</b> {latest_period}", kpi_style))
            elements.append(Paragraph(f"<b>Paxlovid TRX Market Share:</b> {trx_val} ({trx_diff_sign}{trx_ms_diff:.1f}pp vs STLY)", kpi_style))
            elements.append(Paragraph(f"<b>Paxlovid NBRx Market Share:</b> {nbrx_val} ({nbrx_diff_sign}{nbrx_ms_diff:.1f}pp vs STLY)", kpi_style))
            elements.append(Spacer(1, 10))

            elements.append(Paragraph("TRX Market Share Trend \u2014 COVID Oral Treatment Market", heading_style))
            trx_img_bytes = BytesIO(fig_trx.to_image(format="png", width=900, height=380, scale=2))
            elements.append(Image(trx_img_bytes, width=7.5*inch, height=2.8*inch))
            elements.append(Spacer(1, 10))

            elements.append(Paragraph("NBRx Market Share Trend \u2014 COVID Oral Treatment Market", heading_style))
            nbrx_img_bytes = BytesIO(fig_nbrx.to_image(format="png", width=900, height=380, scale=2))
            elements.append(Image(nbrx_img_bytes, width=7.5*inch, height=2.8*inch))
            elements.append(Spacer(1, 10))

            elements.append(Paragraph("Paxlovid Claims Data", heading_style))
            claims_table_data = [["Quarter", "TRX Claims", "NBRx Claims"]]
            for _, row in df.iterrows():
                claims_table_data.append([row["Quarter"], f"{row['TRX CLAIMS']:,.0f}", f"{row['NBRX CLAIMS']:,.0f}"])
            t = Table(claims_table_data, colWidths=[1.5*inch, 2*inch, 2*inch])
            t.setStyle(table_style)
            elements.append(t)
            elements.append(Spacer(1, 10))

            elements.append(Paragraph("Paxlovid Market Share & Diff vs STLY", heading_style))
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
            label="\U0001f4e5 Download Excel",
            data=generate_excel(),
            file_name="paxlovid_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col2:
        pdf_data = generate_pdf()
        if pdf_data:
            st.download_button(
                label="\U0001f4c4 Download PDF",
                data=pdf_data,
                file_name="paxlovid_report.pdf",
                mime="application/pdf"
            )
        else:
            st.info("Install `reportlab` for PDF export: pip install reportlab")
