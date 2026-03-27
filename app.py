import streamlit as st
from secciones.landing import show_landing
from secciones.estudiantes import render

st.set_page_config(
    page_title="ConVivir",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inicializar estado
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"
if "current_page" not in st.session_state:
    st.session_state.current_page = "student_home"
if "user" not in st.session_state:
    st.session_state.user = {"name": "Lucas Martínez"}

st.markdown("""
<style>
  /* Ocultar elementos de Streamlit */
  [data-testid="stSidebarNav"] { display: none; }
  [data-testid="stHeader"]     { display: none; }
  .block-container { padding: 0 !important; }

  /* Ocultar la navbar original de la landing */
  .cv-nav { display: none !important; }

  /* Navbar custom fija arriba */
  .menu-bar {
      position: fixed;
      top: 0; left: 0; right: 0;
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 52px;
      height: 66px;
      background: rgba(3,9,26,0.95);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(74,158,255,0.15);
      font-family: 'Sora', sans-serif;
  }
  .menu-logo {
      font-size: 20px; font-weight: 800; color: white; letter-spacing: -0.4px;
  }
  .menu-logo em { font-style: normal; color: #4a9eff; }

  /* Empujar el contenido para que no quede bajo la navbar */
  .cv-hero { padding-top: 120px !important; }
</style>

<!-- Navbar fija con logo -->
<div class="menu-bar">
  <div class="menu-logo">Con<em>Vivir</em></div>
</div>
""", unsafe_allow_html=True)

# ── Menú de tabs (debajo de la navbar fija, sticky) ──────────────────────────
tab_inicio, tab_alumno = st.tabs([
    "🏠 Inicio",
    "🎒 Alumno",
])

with tab_inicio:
    show_landing()

with tab_alumno:
    render()
