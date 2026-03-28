import streamlit as st
from secciones.landing import show_landing
from secciones.estudiantes import render as render_estudiantes
from secciones.direccion import render as render_direccion
from secciones.docente import render as render_docente
from secciones.familia import render as render_familia
from secciones.moderador import render as render_moderador
from secciones.global_admin import render as render_global_admin

st.set_page_config(
    page_title="ConVivir — Gestión de Convivencia",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Lógica de Navegación ──────────────────────────────────────────────────────
query_params = st.query_params
seccion_actual = query_params.get("p", "inicio")

# ── Cargar Estilos ────────────────────────────────────────────────────────────
with open("utilidades/desktop.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Navbar ────────────────────────────────────────────────────────────────────
def nav_item(label, key):
    active_class = "active" if seccion_actual == key else ""
    return f'<a href="/?p={key}" target="_self" class="nav-item {active_class}">{label}</a>'

st.markdown(f"""
<div class="topnav">
  <div class="topnav-inner">
    <div class="topnav-logo"><a href="/?p=inicio" target="_self">Con<em>Vivir</em></a></div>
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

# ── Renderizado de Secciones ──────────────────────────────────────────────────
# Si es la landing, no ponemos padding extra para que el hero sea full-width
if seccion_actual == "inicio":
    st.markdown('<div class="landing-wrapper">', unsafe_allow_html=True)
    show_landing()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Contenedor principal con el padding del documento de análisis
    st.markdown('<div style="padding: 48px 56px;">', unsafe_allow_html=True)
    
    if seccion_actual == "alumno":
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
        
    st.markdown('</div>', unsafe_allow_html=True)
