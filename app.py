import streamlit as st
from secciones.landing import show_landing
from secciones.estudiantes import render

st.set_page_config(
    page_title="ConVivir",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  [data-testid="stSidebarNav"] { display: none; }
  .block-container { padding-top: 0 !important; }
</style>
""", unsafe_allow_html=True)

# Inicializar estado
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"
if "current_page" not in st.session_state:
    st.session_state.current_page = "student_home"
if "user" not in st.session_state:
    st.session_state.user = {"name": "Lucas Martínez"}

# ── Menú en el sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📍 Menú")
    st.markdown("---")
    if st.button("🏠 Inicio", use_container_width=True):
        st.session_state.seccion = "inicio"
        st.rerun()
    if st.button("🎒 Alumno", use_container_width=True):
        st.session_state.seccion = "alumno"
        st.rerun()

# ── Contenido ─────────────────────────────────────────────────────────────────
if st.session_state.seccion == "inicio":
    show_landing()
elif st.session_state.seccion == "alumno":
    render()
