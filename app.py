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

# ── Botones reales de Streamlit (ocultos con CSS) ─────────────────────────────
# IMPORTANTE: El texto aquí debe coincidir exactamente con el argumento de go()
secciones = ["inicio", "direccion", "docente", "alumno", "familia", "moderador", "admin"]
cols = st.columns(len(secciones))
for col, key in zip(cols, secciones):
    with col:
        if st.button(key, key=f"nav_{key}"):
            st.session_state.seccion = key
            st.rerun()

# ── Navbar blanca minimalista ─────────────────────────────────────────────────
seccion_actual = st.session_state.seccion

def cls(key):
    return "nav-item active" if seccion_actual == key else "nav-item"

st.markdown(f"""
<div class="topnav">
  <div class="topnav-inner">
    <div class="topnav-logo">Con<em>Vivir</em></div>
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
    // Buscamos en el DOM del padre donde Streamlit renderiza los botones reales
    const doc = window.parent.document;
    const buttons = Array.from(doc.querySelectorAll('button[kind="secondary"], button[kind="primary"], [data-testid="stButton"] button'));
    
    // Buscamos el botón cuyo texto coincida con la clave enviada
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
