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

# Cargamos los estilos
load_css("utilidades/desktop.css")

# ── Inicializar estado ────────────────────────────────────────────────────────
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"
if "current_page" not in st.session_state:
    st.session_state.current_page = "student_home"
if "user" not in st.session_state:
    st.session_state.user = {"name": "Lucas Martínez"}

# ── Botones reales de Streamlit (ocultos con CSS) ─────────────────────────────
# Los colocamos en un contenedor identificado para el script de JS
secciones_lista = ["inicio", "direccion", "docente", "alumno", "familia", "moderador", "admin"]

with st.container():
    st.markdown('<div id="st-nav-buttons" style="display:none">', unsafe_allow_html=True)
    for key in secciones_lista:
        if st.button(key, key=f"btn_{key}"):
            st.session_state.seccion = key
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Navbar blanca minimalista ─────────────────────────────────────────────────
seccion_actual = st.session_state.seccion

def cls(key):
    return "nav-item active" if seccion_actual == key else "nav-item"

st.markdown(f"""
<div class="topnav">
  <div class="topnav-inner">
    <div class="topnav-logo" onclick="go('inicio')" style="cursor:pointer">Con<em>Vivir</em></div>
    <nav class="topnav-links">
      <span class="{cls('inicio')}"    onclick="go('inicio')">Inicio</span>
      <span class="nav-sep">|</span>
      <span class="nav-group">Colegio</span>
      <span class="{cls('direccion')}" onclick="go('direccion')">Dirección</span>
      <span class="{cls('docente')}"   onclick="go('docente')">Docente</span>
      <span class="{cls('alumno')}"    onclick="go('alumno')">Alumno</span>
      <span class="{cls('familia')}"   onclick="go('familia')">Familia</span>
      <span class="nav-sep">|</span>
      <span class="nav-group">Animar</span>
      <span class="{cls('moderador')}" onclick="go('moderador')">Moderador</span>
      <span class="{cls('admin')}"     onclick="go('admin')">Admin</span>
    </nav>
  </div>
</div>

<script>
function go(key) {{
    // Buscamos los botones dentro del contenedor específico que creamos arriba
    const navContainer = window.parent.document.getElementById('st-nav-buttons');
    const buttons = Array.from(window.parent.document.querySelectorAll('button'));
    
    // Filtramos por el texto exacto del botón
    const target = buttons.find(btn => btn.innerText.trim().toLowerCase() === key.toLowerCase());
    
    if (target) {{
        target.click();
    }} else {{
        console.warn("Navegación: No se encontró el botón para " + key);
    }}
}}
</script>
""", unsafe_allow_html=True)

# ── Renderizar sección activa ─────────────────────────────────────────────────
# Agregamos un div de espaciado para que el contenido no quede debajo de la navbar
st.markdown('<div style="height: 52px;"></div>', unsafe_allow_html=True)

if st.session_state.seccion == "inicio":
    # La landing suele tener su propio contenedor con fondo oscuro en su archivo landing.py
    show_landing()
elif st.session_state.seccion == "alumno":
    render_estudiantes()
elif st.session_state.seccion == "direccion":
    render_direccion()
elif st.session_state.seccion == "docente":
    render_docente()
elif st.session_state.seccion == "familia":
    render_familia()
elif st.session_state.seccion == "moderador":
    render_moderador()
elif st.session_state.seccion == "admin":
    render_global_admin()
