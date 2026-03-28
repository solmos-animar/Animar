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
load_css("utilidades/mobile.css")

# ── Inicializar estado ────────────────────────────────────────────────────────
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"
if "current_page" not in st.session_state:
    st.session_state.current_page = "student_home"
if "user" not in st.session_state:
    st.session_state.user = {"name": "Lucas Martínez"}

# ── Navegación en sidebar (funciona en todos los dispositivos) ────────────────
with st.sidebar:
    st.markdown("### ConVivir")
    st.markdown("---")

    if st.button("🏠 Inicio", use_container_width=True):
        st.session_state.seccion = "inicio"
        st.rerun()

    st.markdown("**— Colegio —**")
    if st.button("👩‍💼 Dirección", use_container_width=True):
        st.session_state.seccion = "direccion"
        st.rerun()
    if st.button("👨‍🏫 Docente", use_container_width=True):
        st.session_state.seccion = "docente"
        st.rerun()
    if st.button("🎒 Alumno", use_container_width=True):
        st.session_state.seccion = "alumno"
        st.rerun()
    if st.button("👨‍👩‍👧 Familia", use_container_width=True):
        st.session_state.seccion = "familia"
        st.rerun()

    st.markdown("**— Animar —**")
    if st.button("🛡️ Moderador", use_container_width=True):
        st.session_state.seccion = "moderador"
        st.rerun()
    if st.button("🏛️ Admin Global", use_container_width=True):
        st.session_state.seccion = "admin"
        st.rerun()

# ── Renderizar sección activa ─────────────────────────────────────────────────
seccion = st.session_state.seccion

if seccion == "inicio":
    show_landing()
elif seccion == "direccion":
    render_direccion()
elif seccion == "docente":
    render_docente()
elif seccion == "alumno":
    render_estudiantes()
elif seccion == "familia":
    render_familia()
elif seccion == "moderador":
    render_moderador()
elif seccion == "admin":
    render_global_admin()
