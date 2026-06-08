"""
Home page renderer for the Primary Care Monthly Report Dashboard.
Displays brand cards grid with navigation to individual brand pages.
"""

import streamlit as st
from shared import get_logo_base64, HOME_PAGE_CSS, render_ribbon


def render():
    """Render the home page with brand cards."""
    # Load logos
    logo_b64 = get_logo_base64("logo.png")
    nurtec_logo_b64 = get_logo_base64("nurtec_logo.png")
    zavz_logo_b64 = get_logo_base64("zavz_logo.png")
    eliquis_logo_b64 = get_logo_base64("eliquis.png")
    prevnar_logo_b64 = get_logo_base64("prevnar.png")
    comirnaty_logo_b64 = get_logo_base64("comirnaty.png")
    abrysvo_logo_b64 = get_logo_base64("abrysvo.png")
    pax_logo_b64 = get_logo_base64("pax.png")

    # Apply CSS
    st.markdown(HOME_PAGE_CSS, unsafe_allow_html=True)

    # Top Ribbon
    render_ribbon(logo_b64, "Primary Care Monthly Report Dashboard")

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # Data Summary Glossary
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

    # Brand definitions
    brands = [
        {"name": "Nurtec", "logo": nurtec_logo_b64, "page_key": "nurtec"},
        {"name": "Zavzpret", "logo": zavz_logo_b64, "page_key": "zavzpret"},
        {"name": "Eliquis", "logo": eliquis_logo_b64, "page_key": "eliquis"},
        {"name": "Prevnar", "logo": prevnar_logo_b64, "page_key": "prevnar"},
        {"name": "Comirnaty", "logo": comirnaty_logo_b64, "page_key": "comirnaty"},
        {"name": "Abrysvo", "logo": abrysvo_logo_b64, "page_key": "abrysvo"},
        {"name": "Paxlovid", "logo": pax_logo_b64, "page_key": "paxlovid"},
    ]

    # Render brand cards in rows of 3
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
                    st.session_state["current_page"] = brand["page_key"]
                    st.rerun()
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; right: 0; text-align: center; padding: 14px 0; background: #F8FAFD; border-top: 1px solid rgba(26, 62, 110, 0.08);">
        <span style="color: #9EAAB8; font-size: 12px; font-family: 'Inter', sans-serif; font-weight: 400;">Developed by ZS Primary Care Team</span>
    </div>
    """, unsafe_allow_html=True)
