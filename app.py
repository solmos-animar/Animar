import streamlit as st
from secciones.landing import show_landing
from secciones.estudiantes import show_estudiantes  # ← vamos a corregir esto

st.set_page_config(
    page_title="ConVivir — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Ocultar las páginas automáticas del sidebar
st.markdown("""
<style>
  [data-testid="stSidebarNav"] { display: none; }
  .block-container { padding-top: 1rem !important; }
  div[data-testid="stTabs"] button { font-weight: 700; font-size: 13px; }
  div[data-testid="stTabs"] button[aria-selected="true"] {
      color: #1a2e2a;
      border-bottom: 3px solid #4db8a0;
  }
</style>
""", unsafe_allow_html=True)

tab_inicio, tab_alumno = st.tabs([
    "🏠 Inicio",
    "🎒 Alumno",
])

with tab_inicio:
    show_landing()

with tab_alumno:
    show_estudiantes()
