import streamlit as st
from secciones.landing import show_landing
from secciones.estudiantes import render

st.set_page_config(
    page_title="ConVivir",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  [data-testid="stSidebarNav"] { display: none; }
  .block-container { padding-top: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# Inicializar estado
if "current_page" not in st.session_state:
    st.session_state.current_page = "student_home"
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"
if "user" not in st.session_state:
    st.session_state.user = {"name": "Lucas Martínez"}

# ── Menú simple ───────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Inicio", use_container_width=True):
        st.session_state.seccion = "inicio"
with col2:
    if st.button("🎒 Alumno", use_container_width=True):
        st.session_state.seccion = "alumno"

st.markdown("---")

# ── Contenido según sección activa ────────────────────────────────────────────
if st.session_state.seccion == "inicio":
    show_landing()
elif st.session_state.seccion == "alumno":
    render()
