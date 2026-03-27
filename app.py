import streamlit as st
from secciones.landing import show_landing, LOGO_SIDEBAR, LOGO_MOD

st.set_page_config(
    page_title="ConVivir — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos globales ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #1a2e2a; }
  [data-testid="stSidebar"] * { color: white !important; }
  [data-testid="stSidebar"] hr { border-color: rgba(77,184,160,0.25); }
  .main .block-container { padding-top: 1rem; }
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

  /* ── Tabs superiores ── */
  div[data-testid="stTabs"] > div:first-child {
      background: #0e1c19;
      border-radius: 12px 12px 0 0;
      padding: 4px 8px 0;
  }
  div[data-testid="stTabs"] button[data-baseweb="tab"] {
      font-size: 13px !important;
      font-weight: 700 !important;
      color: rgba(255,255,255,0.45) !important;
      border-radius: 8px 8px 0 0 !important;
      padding: 10px 18px !important;
      border: none !important;
      background: transparent !important;
      transition: all .15s !important;
  }
  div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
      color: rgba(255,255,255,0.85) !important;
      background: rgba(77,184,160,0.12) !important;
  }
  div[data-testid="stTabs"] button[aria-selected="true"] {
      color: #4db8a0 !important;
      background: #1a2e2a !important;
      border-bottom: 2px solid #4db8a0 !important;
  }
  /* Separadores de grupo: opacos, no interactivos */
  div[data-testid="stTabs"] button[data-baseweb="tab"]:disabled,
  div[data-testid="stTabs"] button[data-baseweb="tab"][aria-disabled="true"] {
      color: rgba(77,184,160,0.5) !important;
      cursor: default !important;
      font-size: 10px !important;
      letter-spacing: 1.5px !important;
      text-transform: uppercase !important;
      padding: 10px 10px !important;
  }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DEFINICIÓN DE PERFILES
# ══════════════════════════════════════════════════════════════════════════════

PROFILES = {
    "admin_global": {
        "label": "Admin Global", "icon": "🏛️",
        "role": "admin", "name": "Administrador Global",
        "email": "admin@convivir.ar", "password": "admin123",
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
        "email": "directora@colegio.ar", "password": "directora123",
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
        "email": "docente@colegio.ar", "password": "docente123",
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
        "email": "alumno@colegio.ar", "password": "alumno123",
        "group": "Colegio",
        "pages": [
            {"name": "Encuesta Sociométrica", "icon": "📝"},
            {"name": "Contenido Alumnos",     "icon": "🎒"},
        ],
    },
    "tutor": {
        "label": "Tutor", "icon": "👨‍👩‍👧",
        "role": "family", "name": "Carlos Martínez",
        "email": "tutor@colegio.ar", "password": "tutor123",
        "group": "Colegio",
        "pages": [
            {"name": "Mi Alumno",      "icon": "👨‍👩‍👧"},
            {"name": "Recursos Hogar", "icon": "🏠"},
        ],
    },
    "moderadora": {
        "label": "Moderadora", "icon": "🛡️",
        "role": "moderator", "name": "Lic. Sofía Herrera",
        "email": "moderadora@animar.ar", "password": "moderadora123",
        "group": "Animar",
        "pages": [
            {"name": "Moderación Contenido", "icon": "🛡️"},
            {"name": "Alertas Críticas",     "icon": "🚨"},
            {"name": "Reportes Animar",      "icon": "📊"},
        ],
    },
}

# Orden de tabs: los keys "__sep_*" son separadores de grupo (no clickeables)
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

# ── Estado de sesión ──────────────────────────────────────────────────────────
if "logged_in"         not in st.session_state: st.session_state.logged_in         = False
if "user"              not in st.session_state: st.session_state.user              = None
if "active_profile"    not in st.session_state: st.session_state.active_profile    = None
if "show_login_panel"  not in st.session_state: st.session_state.show_login_panel  = False


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
        st.session_state.active_profile = None
        st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# DASHBOARDS POR ROL
# ════════════════════════════════════════════════════════════════════════════

def render_dashboard(profile_key: str):
    p    = PROFILES[profile_key]
    user = st.session_state.user

    render_sidebar(profile_key)

    first_name = user["name"].split()[0] if p["role"] != "admin" else user["name"]
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; margin-bottom:4px;">
            <span style="font-size:36px;">{p['icon']}</span>
            <div>
                <h1 style="margin:0;">Bienvenida/o, {first_name}</h1>
                <p style="color:#7a8a82; margin:0; font-size:14px;">
                    {p['group']} · {p['label']} — {user['email']}
                </p>
            </div>
        </div>
        <hr style="border-color:rgba(77,184,160,0.15); margin:16px 0;">
    """, unsafe_allow_html=True)

    role = p["role"]
    if role == "admin":           _dash_admin()
    elif role == "director":      _dash_director()
    elif role == "teacher":       _dash_teacher()
    elif role == "student":       _dash_student()
    elif role == "family":        _dash_family()
    elif role == "moderator":     _dash_moderator()


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
    with c3: st.metric("Alertas abiertas",  "2",  delta_color="inverse")
    st.markdown("### Estado institucional")
    st.markdown('<div class="alert-medium"><b>ATENCIÓN:</b> 2 alertas de riesgo activas en 4º Año "A".</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-low"><b>OK:</b> 5º Año "B" — sin alertas activas.</div>', unsafe_allow_html=True)

def _dash_teacher():
    st.markdown("### Mis Aulas Activas")
    c1, c2, _ = st.columns(3)
    with c1:
        st.markdown("""<div style="background:white;border:2px solid #e0d8d0;border-radius:16px;padding:20px;">
            <h4 style="margin:0;color:#1a2e2a;">4º Año "A"</h4>
            <p style="font-size:12px;color:#7a8a82;">32 Alumnos · 1 Alerta Alta</p>
            <span class="badge-teacher">SOCIOGRAMA ACTIVO</span></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div style="background:white;border:2px solid #e0d8d0;border-radius:16px;padding:20px;">
            <h4 style="margin:0;color:#1a2e2a;">5º Año "B"</h4>
            <p style="font-size:12px;color:#7a8a82;">28 Alumnos · 0 Alertas</p>
            <span class="badge-admin">REPORTES LISTOS</span></div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Alertas Preventivas")
    st.markdown('<div class="alert-high"><b>RIESGO ALTO:</b> Lucas Martínez (4ºA) — aislado extremo. Intervención recomendada.</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-medium"><b>RIESGO MEDIO:</b> Conflicto grupal entre subgrupos en 5ºB.</div>', unsafe_allow_html=True)

def _dash_student():
    st.markdown("### Tu espacio, Lucas")
    st.info("📝 Tenés una encuesta pendiente de completar para tu aula.")
    st.markdown("### Contenido para vos")
    st.markdown('<div class="alert-low"><b>Nuevo:</b> ¿Qué hacer si ves que alguien es excluido? — Guía para alumnos.</div>', unsafe_allow_html=True)

def _dash_family():
    st.markdown("### Panel de Carlos Martínez")
    st.markdown("**Alumno vinculado:** Lucas Martínez — 4º Año A")
    st.markdown('<div class="alert-low"><b>Sin alertas activas</b> para Lucas esta semana.</div>', unsafe_allow_html=True)
    st.markdown("### Recursos para el hogar")
    st.markdown("📥 Guía de convivencia familiar — descargable")

def _dash_moderator():
    c1, c2 = st.columns(2)
    with c1: st.metric("Contenidos para revisar", "7")
    with c2: st.metric("Alertas críticas activas", "1", delta_color="inverse")
    st.markdown("### Cola de moderación")
    st.markdown('<div class="alert-high"><b>CRÍTICO:</b> Reporte de 4ºA — Colegio San Martín. Requiere revisión manual.</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-low"><b>OK:</b> Contenido M4 actualizado y publicado.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PANTALLA DE LOGIN (landing + selector de perfil)
# ════════════════════════════════════════════════════════════════════════════

def show_login():
    show_landing()

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;700;800&display=swap');
    .pwidget {
        background:white; border-radius:20px; border:2px solid #e0d8d0;
        padding:28px 14px 22px; text-align:center; cursor:pointer;
        box-shadow:0 4px 20px rgba(26,46,42,0.06); transition:all .18s;
    }
    .pwidget:hover { border-color:#4db8a0; transform:translateY(-4px); box-shadow:0 12px 32px rgba(77,184,160,0.18); }
    .pwidget-ico  { font-size:40px; margin-bottom:10px; display:block; }
    .pwidget-name { font-family:'Sora',sans-serif; font-size:14px; font-weight:800; color:#1a2e2a; margin-bottom:4px; }
    .pwidget-desc { font-size:11px; color:#8a9a92; line-height:1.5; }
    div[data-testid="stVerticalBlock"] > div:first-child {
        position:fixed; top:14px; right:52px; z-index:200;
    }
    div[data-testid="stVerticalBlock"] > div:first-child .stButton > button {
        background:#4db8a0 !important; border:none !important;
        font-family:'Sora',sans-serif !important; font-weight:700 !important;
        border-radius:8px !important; padding:9px 22px !important;
        font-size:14px !important; color:white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col_btn = st.columns([12, 1])
    with col_btn:
        if st.button("Ingresar →", type="primary", key="open_login"):
            st.session_state.show_login_panel = True
            st.rerun()

    if not st.session_state.show_login_panel:
        return

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align:center; margin-bottom:32px;">
            <div style="transform:scale(0.5); transform-origin:center top;">{LOGO_SIDEBAR}</div>
            <h2 style="font-family:'Sora',sans-serif; font-size:24px; font-weight:800;
                       color:#1a2e2a; letter-spacing:-0.5px; margin:12px 0 6px;">
                Seleccioná tu perfil
            </h2>
            <p style="font-size:13px; color:#7a8a82;">Acceso directo al dashboard de cada rol</p>
        </div>
    """, unsafe_allow_html=True)

    # Grupo Animar
    st.markdown("**🏛️ Animar**")
    a1, a2, *_ = st.columns(6)
    with a1:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">🏛️</span><div class="pwidget-name">Admin Global</div><div class="pwidget-desc">Backoffice central</div></div>', unsafe_allow_html=True)
        if st.button("Ingresar", key="btn_admin_global", use_container_width=True):
            auto_login("admin_global")
    with a2:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">🛡️</span><div class="pwidget-name">Moderadora</div><div class="pwidget-desc">Contenido y alertas</div></div>', unsafe_allow_html=True)
        if st.button("Ingresar", key="btn_moderadora", use_container_width=True):
            auto_login("moderadora")

    st.markdown("<br>", unsafe_allow_html=True)

    # Grupo Colegio
    st.markdown("**🏫 Colegio**")
    c1, c2, c3, c4, *_ = st.columns(6)
    with c1:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">👩‍💼</span><div class="pwidget-name">Directora</div><div class="pwidget-desc">Panel institucional</div></div>', unsafe_allow_html=True)
        if st.button("Ingresar", key="btn_directora", use_container_width=True):
            auto_login("directora")
    with c2:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">👨‍🏫</span><div class="pwidget-name">Docente</div><div class="pwidget-desc">Aulas y sociograma</div></div>', unsafe_allow_html=True)
        if st.button("Ingresar", key="btn_docente", use_container_width=True):
            auto_login("docente")
    with c3:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">🎒</span><div class="pwidget-name">Alumno</div><div class="pwidget-desc">Encuesta y contenido</div></div>', unsafe_allow_html=True)
        if st.button("Ingresar", key="btn_alumno", use_container_width=True):
            auto_login("alumno")
    with c4:
        st.markdown('<div class="pwidget"><span class="pwidget-ico">👨‍👩‍👧</span><div class="pwidget-name">Tutor</div><div class="pwidget-desc">Seguimiento familiar</div></div>', unsafe_allow_html=True)
        if st.button("Ingresar", key="btn_tutor", use_container_width=True):
            auto_login("tutor")


# ════════════════════════════════════════════════════════════════════════════
# PANTALLA PRINCIPAL POST-LOGIN: tabs superiores
# ════════════════════════════════════════════════════════════════════════════

def show_main():
    # Construir labels de tabs
    tab_labels = []
    for key in TAB_ORDER:
        if key == "__sep_colegio__":
            tab_labels.append("┊ Colegio")
        elif key == "__sep_animar__":
            tab_labels.append("┊ Animar")
        else:
            p = PROFILES[key]
            tab_labels.append(f"{p['icon']} {p['label']}")

    tabs = st.tabs(tab_labels)

    for tab, key in zip(tabs, TAB_ORDER):
        with tab:
            if key.startswith("__sep"):
                group = "Colegio" if "colegio" in key else "Animar"
                st.markdown(
                    f"<p style='color:#7a8a82; font-size:13px; padding:8px 0;'>"
                    f"Seleccioná un perfil del grupo <b>{group}</b> en las pestañas de la barra superior.</p>",
                    unsafe_allow_html=True
                )
            else:
                # Actualizar perfil activo si el usuario cambió de tab
                if st.session_state.active_profile != key:
                    p = PROFILES[key]
                    st.session_state.active_profile = key
                    st.session_state.user = {
                        "email": p["email"],
                        "role":  p["role"],
                        "name":  p["name"],
                    }
                render_dashboard(key)


# ════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ════════════════════════════════════════════════════════════════════════════

if st.session_state.logged_in:
    show_main()
else:
    show_login()
