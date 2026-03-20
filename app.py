import streamlit as st

st.set_page_config(
    page_title="ConVivir — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos globales ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #0f2240; }
  [data-testid="stSidebar"] * { color: white !important; }
  [data-testid="stSidebar"] .stRadio label { color: rgba(255,255,255,0.8) !important; }
  [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }
  .main .block-container { padding-top: 2rem; }
  h1 { color: #0f2240; }
  h2 { color: #0f2240; }
  h3 { color: #1a56a0; }
  .metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    border: 1px solid #ebe9e4;
    box-shadow: 0 2px 8px rgba(15,34,64,0.08);
    margin-bottom: 1rem;
  }
  .badge-admin   { background:#e8effe; color:#1a56a0; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-teacher { background:#e6f4ee; color:#1d7a55; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-student { background:#fde8d0; color:#d4580a; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .alert-high   { background:#fdeaea; border-left:4px solid #c0392b; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-medium { background:#fef3e2; border-left:4px solid #d4580a; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-low    { background:#e6f4ee; border-left:4px solid #1d7a55; border-radius:8px; padding:12px 16px; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ── Datos de usuarios de prueba ───────────────────────────────────────────────
USERS = {
    "admin@convivir.ar":    {"password": "admin123",   "role": "admin",   "name": "Administrador"},
    "docente@colegio.ar":   {"password": "docente123", "role": "teacher", "name": "Prof. María García"},
    "alumno@colegio.ar":    {"password": "alumno123",  "role": "student", "name": "Lucas Martínez"},
}

# ── Estado de sesión ──────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# ── Login ─────────────────────────────────────────────────────────────────────
def show_login():
    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:center; margin-bottom:2rem;'>
          <span style='font-size:48px;'>🕸️</span>
          <h1 style='font-size:2.2rem; margin:0.2rem 0 0.1rem;'>ConVivir</h1>
          <p style='color:#5c5852; font-size:1rem; margin:0;'>Plataforma de Convivencia Escolar</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("### Iniciar sesión")
            email = st.text_input("Email", placeholder="usuario@ejemplo.ar")
            password = st.text_input("Contraseña", type="password")

            if st.button("Ingresar", use_container_width=True, type="primary"):
                user = USERS.get(email)
                if user and user["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        "email": email,
                        "role": user["role"],
                        "name": user["name"],
                    }
                    st.rerun()
                else:
                    st.error("Email o contraseña incorrectos.")

            st.markdown("---")
            st.markdown("**Usuarios de prueba:**")
            st.code("admin@convivir.ar   / admin123\ndocente@colegio.ar  / docente123\nalumno@colegio.ar   / alumno123")

# ── Sidebar con navegación ────────────────────────────────────────────────────
def show_sidebar():
    user = st.session_state.user
    role = user["role"]

    with st.sidebar:
        st.markdown(f"## 🕸️ ConVivir")
        st.markdown("---")
        st.markdown(f"👤 **{user['name']}**")
        badge = {"admin": "badge-admin", "teacher": "badge-teacher", "student": "badge-student"}[role]
        labels = {"admin": "Administrador", "teacher": "Docente", "student": "Alumno"}
        st.markdown(f"<span class='{badge}'>{labels[role]}</span>", unsafe_allow_html=True)
        st.markdown("---")

        if role == "admin":
            pages = {
                "🏛️ Dashboard Admin": "admin_dashboard",
                "🏫 Colegios": "admin_colegios",
                "👨‍🏫 Docentes": "admin_docentes",
                "✅ KYC / Validaciones": "admin_kyc",
            }
        elif role == "teacher":
            pages = {
                "📊 Mi Dashboard": "teacher_dashboard",
                "🚪 Gestión de Aulas": "teacher_aulas",
                "🕸️ Sociograma": "teacher_sociograma",
                "🚨 Alertas": "teacher_alertas",
                "📋 Reportes": "teacher_reportes",
            }
        else:
            pages = {
                "🏠 Inicio": "student_home",
                "📝 Encuesta Sociométrica": "student_encuesta",
                "📚 Contenido Educativo": "student_contenido",
            }

        if "current_page" not in st.session_state:
            st.session_state.current_page = list(pages.values())[0]

        for label, key in pages.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()

        st.markdown("---")
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.current_page = None
            st.rerun()

# ── Router de páginas ─────────────────────────────────────────────────────────
def route():
    page = st.session_state.get("current_page", "")
    role = st.session_state.user["role"]

    # Admin
    if page == "admin_dashboard" or (role == "admin" and not page):
        from pages import admin_dashboard; admin_dashboard.render()
    elif page == "admin_colegios":
        from pages import admin_colegios; admin_colegios.render()
    elif page == "admin_docentes":
        from pages import admin_docentes; admin_docentes.render()
    elif page == "admin_kyc":
        from pages import admin_kyc; admin_kyc.render()

    # Docente
    elif page == "teacher_dashboard" or (role == "teacher" and not page):
        from pages import teacher_dashboard; teacher_dashboard.render()
    elif page == "teacher_aulas":
        from pages import teacher_aulas; teacher_aulas.render()
    elif page == "teacher_sociograma":
        from pages import teacher_sociograma; teacher_sociograma.render()
    elif page == "teacher_alertas":
        from pages import teacher_alertas; teacher_alertas.render()
    elif page == "teacher_reportes":
        from pages import teacher_reportes; teacher_reportes.render()

    # Alumno
    elif page == "student_home" or (role == "student" and not page):
        from pages import student_home; student_home.render()
    elif page == "student_encuesta":
        from pages import student_encuesta; student_encuesta.render()
    elif page == "student_contenido":
        from pages import student_contenido; student_contenido.render()

# ── Main ──────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    show_login()
else:
    show_sidebar()
    route()
