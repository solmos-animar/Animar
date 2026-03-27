import streamlit as st
from secciones.landing import show_landing
from secciones.estudiantes import render as render_estudiantes
from secciones.direccion import render as render_direccion
from secciones.docente import render as render_docente
from secciones.familia import render as render_familia
from secciones.moderador import render as render_moderador
from secciones.global_admin import render as render_global_admin

st.set_page_config(
    page_title="ConVivir",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def load_css(filepath: str):
    with open(filepath) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("utilidades/desktop.css")

# ── Inicializar estado ────────────────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "student_home"
if "user" not in st.session_state:
    st.session_state.user = {"name": "Lucas Martínez"}

# ── Navbar fija ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="menu-bar">
  <div class="menu-logo">Con<em>Vivir</em></div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_inicio, tab_direccion, tab_docente, tab_alumno, tab_familia, tab_moderador, tab_admin = st.tabs([
    "🏠 Landing",
    "👩‍💼 Dirección",
    "👨‍🏫 Docente",
    "🎒 Alumno",
    "👨‍👩‍👧 Familia",
    "🛡️ Moderador",
    "🏛️ Admin Global",
])

with tab_inicio:
    show_landing()

with tab_direccion:
    render_direccion()

with tab_docente:
    render_docente()

with tab_alumno:
    render_estudiantes()

with tab_familia:
    render_familia()

with tab_moderador:
    render_moderador()

with tab_admin:
    render_global_admin()
