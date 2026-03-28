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

# Cargamos el CSS de escritorio
load_css("utilidades/desktop.css")

# ── Inicializar estado ────────────────────────────────────────────────────────
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"
if "current_page" not in st.session_state:
    st.session_state.current_page = "student_home"
if "user" not in st.session_state:
    st.session_state.user = {"name": "Lucas Martínez"}

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
    // Buscamos en el documento principal de Streamlit
    const mainDoc = window.parent.document;
    // Buscamos específicamente el contenedor de navegación oculto
    const navZone = mainDoc.getElementById("nav-zone");
    if (!navZone) return;

    // Buscamos todos los botones dentro de esa zona
    const buttons = Array.from(navZone.querySelectorAll('button'));
    const target = buttons.find(btn => btn.innerText.trim().toLowerCase() === key.toLowerCase());
    
    if (target) {{
        target.click();
    }} else {{
        console.error("No se encontró el botón para: " + key);
    }}
}}
</script>
""", unsafe_allow_html=True)

# ── Espaciador para la Navbar ─────────────────────────────────────────────────
st.markdown('<div class="nav-spacer"></div>', unsafe_allow_html=True)

# ── Renderizar sección activa ─────────────────────────────────────────────────
if st.session_state.seccion == "inicio":
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

# ── Botones Reales (Ocultos al final del DOM) ─────────────────────────────────
st.markdown('<div id="nav-zone" class="hidden-nav">', unsafe_allow_html=True)
secciones_lista = ["inicio", "direccion", "docente", "alumno", "familia", "moderador", "admin"]
cols_hidden = st.columns(len(secciones_lista))
for i, key in enumerate(secciones_lista):
    with cols_hidden[i]:
        if st.button(key, key=f"nav_btn_{key}"):
            st.session_state.seccion = key
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
