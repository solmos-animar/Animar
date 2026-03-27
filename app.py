import streamlit as st
from secciones.landing import show_landing, LOGO_SIDEBAR, LOGO_MOD

st.set_page_config(
    page_title="ConVivir — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos globales (pantallas internas post-login) ──────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #1a2e2a; }
  [data-testid="stSidebar"] * { color: white !important; }
  [data-testid="stSidebar"] hr { border-color: rgba(77,184,160,0.25); }
  .main .block-container { padding-top: 2rem; }
  h1 { color: #0a1f5c; }
  h2 { color: #0a1f5c; }
  h3 { color: #1a56a0; }
  .badge-admin   { background:#e8effe; color:#1a56a0; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-teacher { background:#e6f4ee; color:#1d7a55; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-student { background:#fde8d0; color:#d4580a; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .alert-high   { background:#fdeaea; border-left:4px solid #c0392b; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-medium { background:#fef3e2; border-left:4px solid #d4580a; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-low    { background:#e6f4ee; border-left:4px solid #1d7a55; border-radius:8px; padding:12px 16px; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ── Credenciales demo por perfil ───────────────────────────────────────────────
CREDS = {
    "colegio":  {"email": "docente@colegio.ar",  "password": "docente123", "role": "teacher", "name": "Prof. María García"},
    "admin":    {"email": "admin@convivir.ar",    "password": "admin123",   "role": "admin",   "name": "Administrador"},
    "familia":  {"email": "familia@colegio.ar",   "password": "familia123", "role": "family",  "name": "Carlos Martínez"},
    "alumno":   {"email": "alumno@colegio.ar",    "password": "alumno123",  "role": "student", "name": "Lucas Martínez"},
}

# ── Estado de sesión ──────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "login_panel" not in st.session_state:
    st.session_state.login_panel = None  # None | "select" | "colegio" | "admin" | "familia" | "alumno"


# ════════════════════════════════════════════════════════════════════════════
# AUTENTICACIÓN
# ════════════════════════════════════════════════════════════════════════════

def do_login(profile, email_input, pass_input):
    cred = CREDS[profile]
    if email_input == cred["email"] and pass_input == cred["password"]:
        st.session_state.logged_in   = True
        st.session_state.login_panel = None
        st.session_state.user = {
            "email": cred["email"],
            "role":  cred["role"],
            "name":  cred["name"],
        }
        st.rerun()
    else:
        st.error("Email o contraseña incorrectos.")


# ════════════════════════════════════════════════════════════════════════════
# PANTALLA DE LOGIN
# ════════════════════════════════════════════════════════════════════════════

def show_login():
    # 1. Renderizar la landing completa desde secciones/landing.py
    show_landing()

    # 2. CSS del selector de perfiles (overlay sobre la landing)
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;700;800&display=swap');

    .login-header { text-align:center; margin-bottom:40px; }
    .login-title  { font-family:'Sora',sans-serif; font-size:26px; font-weight:800; color:#1a2e2a; letter-spacing:-0.5px; margin:16px 0 6px; }
    .login-sub    { font-size:14px; color:#7a8a82; margin:0; }

    .pwidget {
        background:white; border-radius:20px; border:2px solid #e0d8d0;
        padding:32px 16px 26px; text-align:center; cursor:pointer;
        box-shadow:0 4px 20px rgba(26,46,42,0.06); transition:all .18s;
    }
    .pwidget:hover {
        border-color:#4db8a0; transform:translateY(-4px);
        box-shadow:0 12px 32px rgba(77,184,160,0.18);
    }
    .pwidget-ico  { font-size:48px; margin-bottom:14px; display:block; }
    .pwidget-name { font-family:'Sora',sans-serif; font-size:16px; font-weight:800; color:#1a2e2a; margin-bottom:6px; }
    .pwidget-desc { font-size:12px; color:#8a9a92; line-height:1.5; }
    .pwidget-active {
        border-color:#4db8a0 !important;
        background:linear-gradient(160deg,#f0faf7,white) !important;
        box-shadow:0 8px 28px rgba(77,184,160,0.2) !important;
    }

    .login-form-wrap {
        background:white; border-radius:20px; border:2px solid #4db8a0;
        padding:28px 32px; width:100%; max-width:400px; margin-top:24px;
        box-shadow:0 8px 32px rgba(77,184,160,0.15);
    }
    .login-form-title { font-family:'Sora',sans-serif; font-size:17px; font-weight:800; color:#1a2e2a; margin-bottom:4px; }
    .login-form-hint  { font-size:11.5px; color:#9aaa9a; margin-bottom:20px; }

    /* Botón "Ingresar →" fijo en la navbar */
    div[data-testid="stVerticalBlock"] > div:first-child {
        position:fixed; top:14px; right:52px; z-index:200;
    }
    div[data-testid="stVerticalBlock"] > div:first-child .stButton > button {
        background:#4db8a0 !important; border:none !important;
        font-family:'Sora',sans-serif !important; font-weight:700 !important;
        border-radius:8px !important; padding:9px 22px !important;
        font-size:14px !important; color:white !important;
    }
    div[data-testid="stVerticalBlock"] > div:first-child .stButton > button:hover {
        background:#2a9a82 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 3. Botón "Ingresar →" flotante en la navbar
    _, col_btn = st.columns([12, 1])
    with col_btn:
        if st.button("Ingresar →", type="primary", key="open_login"):
            st.session_state.login_panel = "select"
            st.rerun()

    # Si no se activó el panel, no mostrar nada más
    if st.session_state.login_panel is None:
        return

    panel = st.session_state.login_panel

    # Fondo claro para la zona del selector
    st.markdown("""
    <style>
    .main > div { background:#f5f0eb !important; }
    .block-container { padding-top:0 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    with st.container():
        # Encabezado del selector
        st.markdown(f"""
        <div class="login-header">
            <div style="transform:scale(0.5); transform-origin:center top;">{LOGO_SIDEBAR}</div>
            <h2 class="login-title">Seleccioná tu perfil</h2>
            <p class="login-sub">Para acceder a la plataforma de convivencia escolar</p>
        </div>
        """, unsafe_allow_html=True)

        # ── Los 4 widgets de perfil ───────────────────────────────────────────
        p1, p2, p3, p4 = st.columns(4)

        with p1:
            st.markdown(f"""
            <div class="pwidget{' pwidget-active' if panel=='colegio' else ''}">
                <span class="pwidget-ico">🏫</span>
                <h3 class="pwidget-name">Colegio</h3>
                <p class="pwidget-desc">Docentes y equipo directivo</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Acceder", key="p_colegio", use_container_width=True):
                st.session_state.login_panel = "colegio"
                st.rerun()

        with p2:
            st.markdown(f"""
            <div class="pwidget{' pwidget-active' if panel=='admin' else ''}">
                <span class="pwidget-ico">🏛️</span>
                <h3 class="pwidget-name">Administrador</h3>
                <p class="pwidget-desc">Backoffice central Animar</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Acceder", key="p_admin", use_container_width=True):
                st.session_state.login_panel = "admin"
                st.rerun()

        with p3:
            st.markdown(f"""
            <div class="pwidget{' pwidget-active' if panel=='familia' else ''}">
                <span class="pwidget-ico">👨‍👩‍👧</span>
                <h3 class="pwidget-name">Familia</h3>
                <p class="pwidget-desc">Tutores legales y familias</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Acceder", key="p_familia", use_container_width=True):
                st.session_state.login_panel = "familia"
                st.rerun()

        with p4:
            st.markdown(f"""
            <div class="pwidget{' pwidget-active' if panel=='alumno' else ''}">
                <span class="pwidget-ico">🎒</span>
                <h3 class="pwidget-name">Alumno</h3>
                <p class="pwidget-desc">Estudiantes registrados</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Acceder", key="p_alumno", use_container_width=True):
                st.session_state.login_panel = "alumno"
                st.rerun()

        # ── Formulario del perfil seleccionado ────────────────────────────────
        if panel != "select":
            st.markdown("---")
            c1, c2, c3 = st.columns([1, 1.5, 1])
            with c2:
                names = {
                    "colegio": "Docente / Directivo",
                    "admin":   "Administrador Animar",
                    "familia": "Familia / Tutor",
                    "alumno":  "Alumno",
                }
                st.markdown(f"""
                <div class="login-form-wrap">
                    <h4 class="login-form-title">Ingresar como {names[panel]}</h4>
                    <p class="login-form-hint">Usá las credenciales demo proporcionadas.</p>
                </div>
                """, unsafe_allow_html=True)

                email_input = st.text_input("Email",       value=CREDS[panel]["email"])
                pass_input  = st.text_input("Contraseña",  type="password", value=CREDS[panel]["password"])

                st.markdown("""
                <style>
                div.stButton > button[key="btn_do_login"] {
                    background-color: #e8621a !important;
                    border-color: #e8621a !important;
                }
                </style>
                """, unsafe_allow_html=True)

                if st.button("Iniciar Sesión", key="btn_do_login", use_container_width=True, type="primary"):
                    do_login(panel, email_input, pass_input)


# ════════════════════════════════════════════════════════════════════════════
# PANTALLA PRINCIPAL POST-LOGIN
# ════════════════════════════════════════════════════════════════════════════

def get_pages():
    """Devuelve las páginas disponibles según el rol del usuario."""
    pages_by_role = {
        "admin": [
            {"name": "Gestión Colegios", "icon": "🏛️"},
            {"name": "Validación KYC",   "icon": "📋"},
            {"name": "Auditoría",        "icon": "🔐"},
        ],
        "teacher": [
            {"name": "Mis Aulas",         "icon": "🚪"},
            {"name": "Sociograma",        "icon": "LOGO_MOD"},
            {"name": "Contenido Guía",    "icon": "📚"},
            {"name": "Alertas y Reportes","icon": "📊"},
        ],
        "student": [
            {"name": "Encuesta Sociométrica", "icon": "📝"},
            {"name": "Contenido Alumnos",     "icon": "🎒"},
        ],
        "family": [
            {"name": "Mi Alumno",       "icon": "👨‍👩‍👧"},
            {"name": "Recursos Hogar",  "icon": "🏠"},
        ],
    }
    return pages_by_role.get(st.session_state.user["role"], [])


def show_main():
    user = st.session_state.user

    # ── Sidebar ───────────────────────────────────────────────────────────────
    st.sidebar.markdown(f"""
        <div style="padding:10px 0 20px 0;">{LOGO_SIDEBAR}</div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"""
        <div style="padding:10px 0;">
            <span class="badge-{user['role']}">Perfil {user['role'].upper()}</span>
            <h3 style="color:white; margin:8px 0 2px 0; font-size:16px;">{user['name']}</h3>
            <p style="color:rgba(255,255,255,0.5); font-size:12px; margin:0;">{user['email']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    for p in get_pages():
        icon_html = LOGO_MOD if p["icon"] == "LOGO_MOD" else p["icon"]
        st.sidebar.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; padding:10px 0; color:rgba(255,255,255,0.7); cursor:pointer;">
                <div style="width:24px; text-align:center;">{icon_html}</div>
                <span style="font-size:14px;">{p['name']}</span>
            </div>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    if st.sidebar.button("Cerrar Sesión", key="logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user      = None
        st.rerun()

    # ── Dashboard de bienvenida ───────────────────────────────────────────────
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px;">
            <div style="transform:scale(0.8); transform-origin:left center;">{LOGO_SIDEBAR}</div>
            <h1>Bienvenida, {user['name'].split()[0]}</h1>
        </div>
        <p style="color:#7a8a82;">Panel de Docente Validado — Colegio Modelo Nacional</p>
        <hr style="border-color:rgba(77,184,160,0.1);">
    """, unsafe_allow_html=True)

    st.markdown("### Mis Aulas Activas")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="pwidget" style="text-align:left; padding:20px;">
            <h4 style="margin:0; color:#1a2e2a;">4º Año "A"</h4>
            <p style="font-size:12px; color:#7a8a82;">32 Alumnos • 1 Alerta Alta</p>
            <span class="badge-teacher">SOCIOGRAMA ACTIVO</span>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="pwidget" style="text-align:left; padding:20px; border-color:rgba(74,158,255,0.2);">
            <h4 style="margin:0; color:#1a2e2a;">5º Año "B"</h4>
            <p style="font-size:12px; color:#7a8a82;">28 Alumnos • 0 Alertas</p>
            <span class="badge-admin">REPORTES LISTOS</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Resumen de Alertas Preventivas")

    st.markdown('<div class="alert-high"><b>RIESGO ALTO:</b> Lucas Martínez (4ºA) identificado como "Aislado extremo". Se recomienda intervención.</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-medium"><b>RIESGO MEDIO:</b> Conflicto grupal detectado entre subgrupos en 5ºB.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ════════════════════════════════════════════════════════════════════════════

if st.session_state.logged_in:
    show_main()
else:
    show_login()
