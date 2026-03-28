import streamlit as st
from utilidades.header import render_header
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

if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"

# Cargar CSS
with open("utilidades/desktop.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Renderizar Header
render_header()

# Espacio para que el contenido no quede tapado
st.markdown('<div class="nav-spacer"></div>', unsafe_allow_html=True)

# Lógica de Secciones
seccion = st.session_state.seccion

if seccion == "inicio":
    show_landing()
elif seccion == "alumno":
    render_estudiantes()
elif seccion == "direccion":
    render_direccion()
elif seccion == "docente":
    render_docente()
elif seccion == "familia":
    render_familia()
elif seccion == "moderador":
    render_moderador()
elif seccion == "admin":
    render_global_admin()
