import streamlit as st

st.set_page_config(
    page_title="ConVivir en grande — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos globales ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #1a2e2a; }
  [data-testid="stSidebar"] * { color: white !important; }
  .main .block-container { padding-top: 2rem; }
  h1, h2 { color: #0a1f5c; }
  .cv-tag {
    display:inline-flex; background:rgba(26,111,255,0.1); border:1px solid rgba(74,158,255,0.22);
    border-radius:100px; padding:5px 14px; font-size:10.5px; font-weight:700; color:#60a5fa; margin-bottom:22px;
  }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LOGOS SVG (Corregidos)
# ══════════════════════════════════════════════════════════════════════════════

LOGO_NAV = (
    '<svg width="148" height="40" viewBox="0 0 296 80" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4,76 L24,8 L32,8 L32,76 Z" fill="#4db8a0"/>'
    '<path d="M60,76 L40,8 L32,8 L32,76 Z" fill="#4db8a0"/>'
    '<text x="74" y="50" font-family="Arial Black" font-size="32" font-weight="900" fill="#1a2e2a">CONVIVIR</text>'
    '</svg>'
)

LOGO_HERO = (
    '<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="100" cy="100" r="80" fill="#4db8a0" opacity="0.2"/>'
    '<path d="M60,140 L100,40 L140,140 Z" fill="#4db8a0"/>'
    '<text x="100" y="180" text-anchor="middle" font-family="Arial Black" font-size="24" fill="white">CONVIVIR</text>'
    '</svg>'
)

# ── Estado de sesión ──────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_panel" not in st.session_state:
    st.session_state.login_panel = None

# ── CSS de la landing ─────────────────────────────────────────────────────────
LANDING_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;700;800&family=DM+Sans:wght@400;500&display=swap');
.block-container { padding:0!important; max-width:100%!important; }
header[data-testid="stHeader"] { display:none; }

.cv { font-family:'DM Sans',sans-serif; background:#03091a; color:#dde8f8; min-height:100vh; }
.cv-nav {
    position:fixed; top:0; left:0; right:0; z-index:100;
    display:flex; align-items:center; justify-content:space-between;
    padding:0 52px; height:66px;
    background:rgba(3,9,26,0.9); backdrop-filter:blur(20px);
    border-bottom:1px solid rgba(74,158,255,0.1);
}
.cv-hero {
    min-height:100vh; display:flex; flex-direction:column; justify-content:center;
    padding:120px 52px 80px; position:relative; overflow:hidden;
    background: radial-gradient(ellipse 90% 65% at 50% -5%, rgba(26,111,255,0.2) 0%, transparent 65%), #03091a;
}
.cv-hero h1 {
    font-family:'Sora',sans-serif; font-size:clamp(40px, 6vw, 72px); font-weight:800;
    line-height:1.1; color:#fff; margin-bottom:20px; letter-spacing:-2px;
}
.cv-hero h1 em { font-style:normal; color:#4a9eff; }
.cv-hero-sub { font-size:18px; color:rgba(221,232,248,0.6); max-width:600px; line-height:1.6; }
</style>
"""

# ── Funciones de Interfaz ─────────────────────────────────────────────────────

def show_landing():
    st.markdown(LANDING_CSS, unsafe_allow_html=True)
    
    html_content = f"""
    <div class="cv">
        <nav class="cv-nav">
            <div class="cv-logo">{LOGO_NAV}</div>
            <div style="color:rgba(255,255,255,0.4); font-size:13px; font-weight:500;">EDUCAR EN GRANDE</div>
        </nav>

        <section class="cv-hero">
            <div style="display:grid; grid-template-columns: 1.2fr 0.8fr; align-items:center; max-width:1200px; margin:0 auto;">
                <div>
                    <div class="cv-tag">PROPUESTA EDUCATIVA 2026</div>
                    <h1>ConVivir<br><em>en grande</em></h1>
                    <p class="cv-hero-sub">
                        Transformamos la convivencia escolar fortaleciendo los vínculos. 
                        Una plataforma diseñada para crear entornos seguros donde 
                        cada estudiante puede crecer con confianza.
                    </p>
                </div>
                <div style="display:flex; justify-content:center;">{LOGO_HERO}</div>
            </div>
        </section>
        
        <footer style="padding:40px; text-align:center; color:rgba(255,255,255,0.2); font-size:11px; border-top:1px solid rgba(255,255,255,0.05);">
            © 2026 ConVivir — La convivencia positiva es la base del aprendizaje.
        </footer>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

    # Botón flotante para ingresar
    _, col_btn = st.columns([10, 2])
    with col_btn:
        if st.button("Ingresar →", type="primary"):
            st.session_state.login_panel = True
            st.rerun()

def show_login_form():
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.subheader("Acceso a la plataforma")
        st.text_input("Email")
        st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            st.session_state.logged_in = True
            st.rerun()
        if st.button("← Volver"):
            st.session_state.login_panel = None
            st.rerun()

def show_dashboard():
    st.sidebar.markdown(LOGO_NAV, unsafe_allow_html=True)
    st.sidebar.write("---")
    st.title("Panel de Gestión")
    st.success("¡Bienvenido a ConVivir en grande!")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()

# ── Lógica de Navegación ──────────────────────────────────────────────────────

if st.session_state.logged_in:
    show_dashboard()
elif st.session_state.login_panel:
    show_login_form()
else:
    show_landing()
