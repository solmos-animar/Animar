import streamlit as st

LOGO_NAV = (
    '<svg width="148" height="40" viewBox="0 0 296 80" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4,76 L24,8 L32,8 L32,76 Z" fill="#4db8a0"/>'
    '<path d="M60,76 L40,8 L32,8 L32,76 Z" fill="#4db8a0"/>'
    '<circle cx="32" cy="23" r="7.5" fill="#0e1c19"/>'
    '<path d="M32,30.5 Q21,25 17,14" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round" fill="none"/>'
    '<path d="M32,30.5 Q43,25 47,14" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round" fill="none"/>'
    '<line x1="32" y1="30.5" x2="32" y2="48" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round"/>'
    '<line x1="32" y1="48" x2="26" y2="61" stroke="#0e1c19" stroke-width="4.5" stroke-linecap="round"/>'
    '<line x1="32" y1="48" x2="38" y2="61" stroke="#0e1c19" stroke-width="4.5" stroke-linecap="round"/>'
    '<rect x="27" y="3" width="10" height="7" rx="1.5" fill="#e8621a"/>'
    '<text x="74" y="50" font-family="Arial Black,Impact,sans-serif" font-size="36" font-weight="900" fill="#1a2e2a" letter-spacing="1">ANIMAR</text>'
    '<text x="74" y="66" font-family="Arial,sans-serif" font-size="9.5" font-weight="400" fill="#4db8a0" letter-spacing="2.5">INFANCIAS &amp; EDUCACI&#xD3;N</text>'
    '</svg>'
)

LOGO_HERO = (
    '<svg width="200" height="228" viewBox="0 0 200 228" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M8,182 L70,10 L100,10 L100,182 Z" fill="#4db8a0"/>'
    '<path d="M192,182 L130,10 L100,10 L100,182 Z" fill="#4db8a0"/>'
    '<circle cx="100" cy="48" r="17" fill="#0e1c19"/>'
    '<path d="M100,65 Q74,53 58,32" stroke="#0e1c19" stroke-width="13" stroke-linecap="round" fill="none"/>'
    '<path d="M100,65 Q126,53 142,32" stroke="#0e1c19" stroke-width="13" stroke-linecap="round" fill="none"/>'
    '<line x1="100" y1="65" x2="100" y2="108" stroke="#0e1c19" stroke-width="13" stroke-linecap="round"/>'
    '<line x1="100" y1="108" x2="83" y2="140" stroke="#0e1c19" stroke-width="11" stroke-linecap="round"/>'
    '<line x1="100" y1="108" x2="117" y2="140" stroke="#0e1c19" stroke-width="11" stroke-linecap="round"/>'
    '<rect x="88" y="2" width="24" height="15" rx="3" fill="#e8621a"/>'
    '<text x="100" y="207" text-anchor="middle" font-family="Arial Black,Impact,sans-serif" font-size="38" font-weight="900" fill="white" letter-spacing="2">ANIMAR</text>'
    '<text x="100" y="224" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="400" fill="rgba(221,232,228,0.55)" letter-spacing="2.5">INFANCIAS &amp; EDUCACI&#xD3;N</text>'
    '</svg>'
)

LOGO_MOD = (
    '<svg width="42" height="42" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="100" height="100" rx="14" fill="rgba(77,184,160,0.15)"/>'
    '<path d="M8,94 L33,12 L50,12 L50,94 Z" fill="#4db8a0"/>'
    '<path d="M92,94 L67,12 L50,12 L50,94 Z" fill="#4db8a0"/>'
    '<circle cx="50" cy="30" r="9" fill="#0e1c19"/>'
    '<path d="M50,39 Q38,33 31,21" stroke="#0e1c19" stroke-width="6.5" stroke-linecap="round" fill="none"/>'
    '<path d="M50,39 Q62,33 69,21" stroke="#0e1c19" stroke-width="6.5" stroke-linecap="round" fill="none"/>'
    '<line x1="50" y1="39" x2="50" y2="58" stroke="#0e1c19" stroke-width="6.5" stroke-linecap="round"/>'
    '<line x1="50" y1="58" x2="43" y2="72" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round"/>'
    '<line x1="50" y1="58" x2="57" y2="72" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round"/>'
    '<rect x="44" y="6" width="12" height="8" rx="2" fill="#e8621a"/>'
    '</svg>'
)

LOGO_SIDEBAR = (
    '<svg width="148" height="40" viewBox="0 0 296 80" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4,76 L24,8 L32,8 L32,76 Z" fill="#4db8a0"/>'
    '<path d="M60,76 L40,8 L32,8 L32,76 Z" fill="#4db8a0"/>'
    '<circle cx="32" cy="23" r="7.5" fill="#0e1c19"/>'
    '<path d="M32,30.5 Q21,25 17,14" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round" fill="none"/>'
    '<path d="M32,30.5 Q43,25 47,14" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round" fill="none"/>'
    '<line x1="32" y1="30.5" x2="32" y2="48" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round"/>'
    '<line x1="32" y1="48" x2="26" y2="61" stroke="#0e1c19" stroke-width="4.5" stroke-linecap="round"/>'
    '<line x1="32" y1="48" x2="38" y2="61" stroke="#0e1c19" stroke-width="4.5" stroke-linecap="round"/>'
    '<rect x="27" y="3" width="10" height="7" rx="1.5" fill="#e8621a"/>'
    '<text x="74" y="50" font-family="Arial Black,Impact,sans-serif" font-size="36" font-weight="900" fill="white" letter-spacing="1">ANIMAR</text>'
    '<text x="74" y="66" font-family="Arial,sans-serif" font-size="9.5" font-weight="400" fill="rgba(77,184,160,0.65)" letter-spacing="2.5">INFANCIAS &amp; EDUCACI&#xD3;N</text>'
    '</svg>'
)


def show_landing():
    full_html = (
        # CSS ya está en desktop.css — solo el HTML aquí
        LANDING_HTML_1 + LOGO_NAV
        + LANDING_HTML_2 + LOGO_HERO
        + LANDING_HTML_3 + LOGO_MOD
        + LANDING_HTML_4 + LOGO_NAV
        + LANDING_HTML_5
    )
    st.markdown(full_html, unsafe_allow_html=True)


LANDING_HTML_1 = """
<div class="cv">
  <nav
