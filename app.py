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

# ── 1. Lógica de Navegación Robusta (Query Params) ────────────────────────────
# Leemos la URL. Si no hay nada, por defecto es 'inicio'
query_params = st.query_params
if "p" not in query_params:
    st.query_params["p"] = "inicio"

seccion_actual = st.query_params.get("p", "inicio")

# ── 2. Cargar Estilos ─────────────────────────────────────────────────────────
def load_css(filepath: str):
    with open(filepath) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("utilidades/desktop.css")

# ── 3. Navbar (Enlaces directos que cambian la URL) ───────────────────────────
def nav_item(label, key):
    active_class = "active" if seccion_actual == key else ""
    # Creamos un link que recarga la página con el parámetro p=key
    return f'<a href="/?p={key}" target="_self" class="nav-item {active_class}">{label}</a>'

st.markdown(f"""
<div class="topnav">
  <div class="topnav-inner">
    <div class="topnav-logo"><a href="/?p=inicio" target="_self" style="text-decoration:none; color:inherit;">Con<em>Vivir</em></a></div>
    <nav class="topnav-links">
        {nav_item('Inicio', 'inicio')}
        <span class="nav-sep">|</span>
        <span class="nav-group">Colegio</span>
        {nav_item('Dirección', 'direccion')}
        {nav_item('Docente', 'docente')}
        {nav_item('Alumno', 'alumno')}
        {nav_item('Familia', 'familia')}
        <span class="nav-sep">|</span>
        <span class="nav-group">Animar</span>
        {nav_item('Moderador', 'moderador')}
        {nav_item('Admin', 'admin')}
    </nav>
  </div>
</div>
<div class="nav-spacer"></div>
""", unsafe_allow_html=True)

# ── 4. Renderizar Sección ─────────────────────────────────────────────────────
# Inicializamos el estado de usuario por si las moscas
if "user" not in st.session_state:
    st.session_state.user = {"name": "Lucas Martínez"}

if seccion_actual == "inicio":
    show_landing()
elif seccion_actual == "alumno":
    render_estudiantes()
elif seccion_actual == "direccion":
    render_direccion()
elif seccion_actual == "docente":
    render_docente()
elif seccion_actual == "familia":
    render_familia()
elif seccion_actual == "moderador":
    render_moderador()
elif seccion_actual == "admin":
    render_global_admin()
