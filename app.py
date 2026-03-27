import streamlit as st
from secciones.landing import show_landing, LOGO_SIDEBAR, LOGO_MOD

st.set_page_config(
    page_title="ConVivir — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos globales post-login ───────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #1a2e2a; }
  [data-testid="stSidebar"] * { color: white !important; }
  [data-testid="stSidebar"] hr { border-color: rgba(77,184,160,0.25); }
  .main .block-container { padding-top: 0 !important; padding-left: 1.5rem !important; padding-right: 1.5rem !important; }
  h1 { color: #0a1f5c; }
  h2 { color: #0a1f5c; }
  h3 { color: #1a56a0; }
  .badge-admin     { background:#e8effe; color:#1a56a0; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-director  { background:#e8effe; color:#1a56a0; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-teacher   { background:#e6f4ee; color:#1d7a55; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-student   { background:#fde8d0; color:#d4580a; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-family    { background:#f0eaff; color:#5b3fa0; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-moderator { background:#fde8ea; color:#c0392b; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .alert-high   { background:#fdeaea; border-left:4px solid #c0392b; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-medium { background:#fef3e2; border-left:4px solid #d4580a; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-low    { background:#e6f4ee; border-left:4px solid #1d7a55; border-radius:8px; padding:12px 16px; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PERFILES
# ══════════════════════════════════════════════════════════════════════════════

PROFILES = {
    "admin_global": {
        "label": "Admin Global", "icon": "🏛️",
        "role": "admin", "name": "Administrador Global",
        "email": "admin@convivir.ar",
        "group": "Animar",
        "pages": [
            {"name": "Gestión Colegios", "icon": "🏛️"},
            {"name": "Validación KYC",   "icon": "📋"},
            {"name": "Auditoría",        "icon": "🔐"},
        ],
    },
    "directora": {
        "label": "Directora", "icon": "👩‍💼",
        "role": "director", "name": "Dir. Ana Rodríguez",
        "email": "directora@colegio.ar",
        "group": "Colegio",
        "pages": [
            {"name": "Panel Institucional", "icon": "🏫"},
            {"name": "Docentes",            "icon": "👨‍🏫"},
            {"name": "Reportes Globales",   "icon": "📊"},
        ],
    },
    "docente": {
        "label": "Docente", "icon": "👨‍🏫",
        "role": "teacher", "name": "Prof. María García",
        "email": "docente@colegio.ar",
        "group": "Colegio",
        "pages": [
            {"name": "Mis Aulas",          "icon": "🚪"},
            {"name": "Sociograma",         "icon": "LOGO_MOD"},
            {"name": "Contenido Guía",     "icon": "📚"},
            {"name": "Alertas y Reportes", "icon": "📊"},
        ],
    },
    "alumno": {
        "label": "Alumno", "icon": "🎒",
        "role": "student", "name": "Lucas Martínez",
        "email": "alumno@colegio.ar",
        "group": "Colegio",
        "pages": [
            {"name": "Encuesta Sociométrica", "icon": "📝"},
            {"name": "Contenido Alumnos",     "icon": "🎒"},
        ],
    },
    "tutor": {
        "label": "Tutor", "icon": "👨‍👩‍👧",
        "role": "family", "name": "Carlos Martínez",
        "email": "tutor@colegio.ar",
        "group": "Colegio",
        "pages": [
            {"name": "Mi Alumno",      "icon": "👨‍👩‍👧"},
            {"name": "Recursos Hogar", "icon": "🏠"},
        ],
    },
    "moderadora": {
        "label": "Moderadora", "icon": "🛡️",
        "role": "moderator", "name": "Lic. Sofía Herrera",
        "email": "moderadora@animar.ar",
        "group": "Animar",
        "pages": [
            {"name": "Moderación Contenido", "icon": "🛡️"},
            {"name": "Alertas Críticas",     "icon": "🚨"},
            {"name": "Reportes Animar",      "icon": "📊"},
        ],
    },
}

# Orden visual de los tabs (con separadores de grupo)
TAB_ORDER = [
    "admin_global",
    "__sep_colegio__",
    "directora",
    "docente",
    "alumno",
    "tutor",
    "__sep_animar__",
    "moderadora",
]

REAL_TABS = [k for k in TAB_ORDER if not k.startswith("__sep")]

# ── Estado de sesión ──────────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "logged_in":        False,
        "user":             None,
        "active_profile":   "admin_global",
        "show_login_panel": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ════════════════════════════════════════════════════════════════════════════
# LOGIN AUTOMÁTICO
# ════════════════════════════════════════════════════════════════════════════

def auto_login(profile_key: str):
    p = PROFILES[profile_key]
    st.session_state.logged_in      = True
    st.session_state.active_profile = profile_key
    st.session_state.user = {
        "email": p["email"],
        "role":  p["role"],
        "name":  p["name"],
    }
    st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# BARRA DE TABS HTML (reemplaza st.tabs)
# ════════════════════════════════════════════════════════════════════════════

def render_tab_bar():
    """
    Renderiza la barra de tabs como HTML puro.
    Los clics se capturan con botones invisibles de Streamlit superpuestos.
    """
    active = st.session_state.active_profile

    # ── CSS de la barra ──────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@700;800&display=swap');

    .tabbar-wrap {
        width: 100%;
        background: #0e1c19;
        border-radius: 14px 14px 0 0;
        padding: 0 12px;
        display: flex;
        align-items: flex-end;
        gap: 2px;
        margin-bottom: 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.18);
        overflow-x: auto;
    }
    .tabbar-wrap::-webkit-scrollbar { height: 3px; }
    .tabbar-wrap::-webkit-scrollbar-thumb { background: #4db8a0; border-radius: 2px; }

    .tab-item {
        display: flex; align-items: center; gap: 6px;
        padding: 12px 16px 11px;
        font-family: 'Sora', sans-serif;
        font-size: 13px; font-weight: 700;
        color: rgba(255,255,255,0.42);
        border-radius: 10px 10px 0 0;
        cursor: pointer;
        transition: all .15s;
        white-space: nowrap;
        border-bottom: 2px solid transparent;
        user-select: none;
    }
    .tab-item:hover {
        color: rgba(255,255,255,0.85);
        background: rgba(77,184,160,0.1);
    }
    .tab-item.active {
        color: #4db8a0;
        background: #1a2e2a;
        border-bottom: 2px solid #4db8a0;
    }
    .tab-sep {
        padding: 10px 8px;
        font-size: 9px; font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase;
        color: rgba(77,184,160,0.35);
        display: flex; align-items: center;
        white-space: nowrap; cursor: default;
        border-left: 1px solid rgba(77,184,160,0.12);
        border-right: 1px solid rgba(77,184,160,0.12);
        margin: 0 4px;
    }
    .tab-content-area {
        background: #f7f9f8;
        border: 1px solid rgba(77,184,160,0.15);
        border-top: none;
        border-radius: 0 0 14px 14px;
        padding: 24px 28px;
        min-height: 200px;
    }

    /* Ocultar los botones nativos de Streamlit que usamos para capturar clics */
    .tab-btn-row { display: flex; gap: 2px; margin: 0; padding: 0; }
    .tab-btn-row .stButton { margin: 0 !important; padding: 0 !important; }
    .tab-btn-row .stButton > button {
        opacity: 0 !important;
        position: absolute !important;
        height: 44px !important;
        min-width: 60px !important;
        cursor: pointer !important;
        border: none !important;
        background: transparent !important;
        z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── HTML de la barra ─────────────────────────────────────────────────────
    tabs_html = '<div class="tabbar-wrap">'
    for key in TAB_ORDER:
        if key == "__sep_colegio__":
            tabs_html += '<div class="tab-sep">Colegio</div>'
        elif key == "__sep_animar__":
            tabs_html += '<div class="tab-sep">Animar</div>'
        else:
            p = PROFILES[key]
            active_class = " active" if key == active else ""
            tabs_html += (
                f'<div class="tab-item{active_class}" id="tab-{key}">'
                f'{p["icon"]} {p["label"]}'
                f'</div>'
            )
    tabs_html += '</div>'
    st.markdown(tabs_html, unsafe_allow_html=True)

    # ── Botones invisibles superpuestos para capturar clics ──────────────────
    # Los posicionamos en una fila debajo (Streamlit no permite superposición real),
    # pero los ocultamos visualmente y los mostramos con st.columns alineados.
    cols = st.columns(len(REAL_TABS))
    for col, key in zip(cols, REAL_TABS):
        with col:
            p = PROFILES[key]
            label = f"{p['icon']} {p['label']}"
            if st.button(label, key=f"tabclick_{key}", use_container_width=True):
                st.session_state.active_profile = key
                st.session_state.user = {
                    "email": p["email"],
                    "role":  p["role"],
                    "name":  p["name"],
                }
                st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════

def render_sidebar(profile_key: str):
    p    = PROFILES[profile_key]
    user = st.session_state.user

    st.sidebar.markdown(
        f'<div style="padding:10px 0 20px 0;">{LOGO_SIDEBAR}</div>',
        unsafe_allow_html=True
    )
    st.sidebar.markdown(f"""
        <div style="padding:10px 0;">
            <span class="badge-{user['role']}">{p['group']} · {p['label']}</span>
            <h3 style="color:white; margin:8px 0 2px 0; font-size:16px;">{user['name']}</h3>
            <p style="color:rgba(255,255,255,0.5); font-size:12px; margin:0;">{user['email']}</p>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")

    for page in p["pages"]:
        icon_html = LOGO_MOD if page["icon"] == "LOGO_MOD" else page["icon"]
        st.sidebar.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; padding:10px 0;
                        color:rgba(255,255,255,0.7); cursor:pointer;">
                <div style="width:24px; text-align:center;">{icon_html}</div>
                <span style="font-size:14px;">{page['name']}</span>
            </div>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión", key="logout", use_container_width=True):
        st.session_state.logged_in      = False
        st.session_state.user           = None
        st.session_state.active_profile = "admin_global"
        st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# DASHBOARDS
# ════════════════════════════════════════════════════════════════════════════

def render_dashboard(profile_key: str):
    p    = PROFILES[profile_key]
    user = st.session_state.user
    first = user["name"].split()[0]

    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:14px; margin: 20px 0 4px;">
            <span style="font-size:32px;">{p['icon']}</span>
            <div>
                <h1 style="margin:0; font-size:26px;">Bienvenida/o, {first}</h1>
                <p style="color:#7a8a82; margin:0; font-size:13px;">
                    {p['group']} · {p['label']} — {user['email']}
                </p>
            </div>
        </div>
        <hr style="border-color:rgba(77,184,160,0.2); margin:14px 0 20px;">
    """, unsafe_allow_html=True)

    role = p["role"]
    if role == "admin":       _dash_admin()
    elif role == "director":  _dash_director()
    elif role == "teacher":   _dash_teacher()
    elif role == "student":   _dash_student()
    elif role == "family":    _dash_family()
    elif role == "moderator": _dash_moderator()


def _dash_admin():
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Colegios activos",   "14", "+2 este mes")
    with c2: st.metric("Docentes validados", "87", "+5 esta semana")
    with c3: st.metric("KYC pendientes",     "3",  delta_color="inverse")
    st.markdown("### Colegios recientes")
    st.markdown('<div class="alert-low"><b>Nuevo:</b> Colegio San Martín completó el KYC. Pendiente de aprobación final.</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-medium"><b>Pendiente:</b> Escuela N°42 — documentación incompleta.</div>', unsafe_allow_html=True)

def _dash_director():
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Docentes activos",  "12")
    with c2: st.metric("Aulas habilitadas", "8")
    with c3: st.metric("Alertas abiertas",  "2", delta_color="inverse")
    st.markdown("### Estado institucional")
    st.markdown('<div class="alert-medium"><b>ATENCIÓN:</b> 2 alertas de riesgo activas en 4º Año "A".</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-low"><b>OK:</b> 5º Año "B" — sin alertas activas.</div>', unsafe_allow_html=True)

def _dash_teacher():
    st.markdown("### Mis Aulas Activas")
    c1, c2, _ = st.columns(3)
    with c1:
        st.markdown("""<div style="background:white;border:2px solid #e0d8d0;border-radius:14px;padding:18px;">
            <h4 style="margin:0;color:#1a2e2a;">4º Año "A"</h4>
            <p style="font-size:12px;color:#7a8a82;margin:4px 0 8px;">32 Alumnos · 1 Alerta Alta</p>
            <span class="badge-teacher">SOCIOGRAMA ACTIVO</span></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div style="background:white;border:2px solid #e0d8d0;border-radius:14px;padding:18px;">
            <h4 style="margin:0;color:#1a2e2a;">5º Año "B"</h4>
            <p style="font-size:12px;color:#7a8a82;margin:4px 0 8px;">28 Alumnos · 0 Alertas</p>
            <span class="badge-admin">REPORTES LISTOS</span></div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Alertas Preventivas")
    st.markdown('<div class="alert-high"><b>RIESGO ALTO:</b> Lucas Martínez (4ºA) — aislado extremo. Intervención recomendada.</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-medium"><b>RIESGO MEDIO:</b> Conflicto grupal entre subgrupos en 5ºB.</div>', unsafe_allow_html=True)

def _dash_student():
    st.info("📝 Tenés una encuesta pendiente de completar para tu aula.")
    st.markdown("### Contenido para vos")
    st.markdown('<div class="alert-low"><b>Nuevo:</b> ¿Qué hacer si ves que alguien es excluido? — Guía para alumnos.</div>', unsafe_allow_html=True)

def _dash_family():
    st.markdown("**Alumno vinculado:** Lucas Martínez — 4º Año A")
    st.markdown('<div class="alert-low"><b>Sin alertas activas</b> para Lucas esta semana.</div>', unsafe_allow_html=True)
    st.markdown("📥 Guía de convivencia familiar — descargable")

def _dash_moderator():
    c1, c2 = st.columns(2)
    with c1: st.metric("Contenidos para revisar",  "7")
    with c2: st.metric("Alertas críticas activas", "1", delta_color="inverse")
    st.markdown("### Cola de moderación")
    st.markdown('<div class="alert-high"><b>CRÍTICO:</b> Reporte de 4ºA — Colegio San Martín. Requiere revisión manual.</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-low"><b>OK:</b> Contenido M4 actualizado y publicado.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PANTALLA LOGIN (landing + selector de perfil)
# ════════════════════════════════════════════════════════════════════════════

def show_login():
    show_landing()

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;700;800&display=swap');
    .pwidget {
        background:white; border-radius:18px; border:2px solid #e0d8d0;
        padding:24px 12px 20px; text-align:center;
        box-shadow:0 4px 18px rgba(26,46,42,0.06); transition:all .18s;
    }
    .pwidget:hover { border-color:#4db8a0; transform:translateY(-3px); box-shadow:0 10px 28px rgba(77,184,160,0.18); }
    .pwidget-ico  { font-size:38px; margin-bottom:8px; display:block; }
    .pwidget-name { font-family:'Sora',sans-serif; font-size:13px; font-weight:800; color:#1a2e2a; margin-bottom:3px; }
    .pwidget-desc { font-size:10.5px; color:#8a9a92; line-height:1.45; }

    /* Botón Ingresar → fijo sobre la navbar de la landing */
    div[data-testid="stVerticalBlock"] > div:first-child {
        position:fixed; top:14px; right:52px; z-index:9999;
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

    # Botón flotante en la navbar
    _, col_btn = st.columns([12, 1])
    with col_btn:
        if st.button("Ingresar →", type="primary", key="open_login"):
            st.session_state.show_login_panel = True
            st.rerun()

    if not st.session_state.show_login_panel:
        return

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align:center; margin-bottom:28px;">
            <div style="transform:scale(0.45); transform-origin:center top; margin-bottom:-30px;">{LOGO_SIDEBAR}</div>
            <h2 style="font-family:'Sora',sans-serif; font-size:22px; font-weight:800;
                       color:#1a2e2a; letter-spacing:-0.5px; margin:0 0 4px;">
                Seleccioná tu perfil
            </h2>
            <p style="font-size:12px; color:#7a8a82;">Acceso directo al dashboard de cada rol</p>
        </div>
    """, unsafe_allow_html=True)

    # Grupo Animar
    st.markdown(
        "<p style='font-size:11px; font-weight:700; letter-spacing:2px; "
        "text-transform:uppercase; color:#4db8a0; margin-bottom:8px;'>🏛️ Animar</p>",
        unsafe_allow_html=True
    )
    a1, a2, *_ = st.columns(6)
    with a1:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">🏛️</span><div class="pwidget-name">Admin Global</div><div class="pwidget-desc">Backoffice central</div></div>', unsafe_allow_html=True)
        if st.button("Entrar", key="btn_admin_global", use_container_width=True):
            auto_login("admin_global")
    with a2:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">🛡️</span><div class="pwidget-name">Moderadora</div><div class="pwidget-desc">Contenido y alertas</div></div>', unsafe_allow_html=True)
        if st.button("Entrar", key="btn_moderadora", use_container_width=True):
            auto_login("moderadora")

    st.markdown("<br>", unsafe_allow_html=True)

    # Grupo Colegio
    st.markdown(
        "<p style='font-size:11px; font-weight:700; letter-spacing:2px; "
        "text-transform:uppercase; color:#4db8a0; margin-bottom:8px;'>🏫 Colegio</p>",
        unsafe_allow_html=True
    )
    c1, c2, c3, c4, *_ = st.columns(6)
    with c1:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">👩‍💼</span><div class="pwidget-name">Directora</div><div class="pwidget-desc">Panel institucional</div></div>', unsafe_allow_html=True)
        if st.button("Entrar", key="btn_directora", use_container_width=True):
            auto_login("directora")
    with c2:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">👨‍🏫</span><div class="pwidget-name">Docente</div><div class="pwidget-desc">Aulas y sociograma</div></div>', unsafe_allow_html=True)
        if st.button("Entrar", key="btn_docente", use_container_width=True):
            auto_login("docente")
    with c3:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">🎒</span><div class="pwidget-name">Alumno</div><div class="pwidget-desc">Encuesta y contenido</div></div>', unsafe_allow_html=True)
        if st.button("Entrar", key="btn_alumno", use_container_width=True):
            auto_login("alumno")
    with c4:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">👨‍👩‍👧</span><div class="pwidget-name">Tutor</div><div class="pwidget-desc">Seguimiento familiar</div></div>', unsafe_allow_html=True)
        if st.button("Entrar", key="btn_tutor", use_container_width=True):
            auto_login("tutor")


# ════════════════════════════════════════════════════════════════════════════
# PANTALLA PRINCIPAL POST-LOGIN
# ════════════════════════════════════════════════════════════════════════════

def show_main():
    active = st.session_state.active_profile
    render_sidebar(active)
    render_tab_bar()          # barra de tabs HTML + botones invisibles
    render_dashboard(active)  # contenido del perfil activo


# ════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ════════════════════════════════════════════════════════════════════════════

if st.session_state.logged_in:
    show_main()
else:
    show_login()
