import streamlit as st
from secciones.landing import show_landing
from secciones.estudiantes import render

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
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"
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
tab_inicio, tab_alumno = st.tabs([
    "🏠 Inicio",
    "🎒 Alumno",
])

with tab_inicio:
    show_landing()

with tab_alumno:
    render()
