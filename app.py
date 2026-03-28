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

# ── Botones invisibles de navegación ─────────────────────────────────────────
# Ocultos con CSS — la navbar custom los clickea via JS
with st.container():
    cols = st.columns(7)
    secciones = ["inicio", "direccion", "docente", "alumno", "familia", "moderador", "admin"]
    for col, key in zip(cols, secciones):
        with col:
            if st.button(key, key=f"nav_{key}"):
                st.session_state.seccion = key
                st.rerun()

# ── Navbar custom HTML ────────────────────────────────────────────────────────
seccion_actual = st.session_state.seccion

def nav_class(key):
    return "nb-item active" if seccion_actual == key else "nb-item"

st.markdown(f"""
<div class="menu-bar">
  <div class="menu-logo">Con<em>Vivir</em></div>
  <div class="nb-toggle" onclick="toggleMenu()" id="nb-toggle">☰</div>
</div>

<div class="nb-menu" id="nb-menu">
  <div class="{nav_class('inicio')}"    onclick="navClick('inicio')">🏠 Inicio</div>
  <div class="nb-sep"></div>
  <span class="nb-group-label">Colegio</span>
  <div class="{nav_class('direccion')}" onclick="navClick('direccion')">👩‍💼 Dirección</div>
  <div class="{nav_class('docente')}"   onclick="navClick('docente')">👨‍🏫 Docente</div>
  <div class="{nav_class('alumno')}"    onclick="navClick('alumno')">🎒 Alumno</div>
  <div class="{nav_class('familia')}"   onclick="navClick('familia')">👨‍👩‍👧 Familia</div>
  <div class="nb-sep"></div>
  <span class="nb-group-label">Animar</span>
  <div class="{nav_class('moderador')}" onclick="navClick('moderador')">🛡️ Moderador</div>
  <div class="{nav_class('admin')}"     onclick="navClick('admin')">🏛️ Admin Global</div>
</div>

<script>
function toggleMenu() {{
    const menu = document.getElementById('nb-menu');
    const toggle = document.getElementById('nb-toggle');
    const isOpen = menu.classList.toggle('open');
    toggle.textContent = isOpen ? '✕' : '☰';
}}

function navClick(key) {{
    document.getElementById('nb-menu').classList.remove('open');
    document.getElementById('nb-toggle').textContent = '☰';
    const btns = window.parent.document.querySelectorAll('[data-testid="stButton"] button');
    for (let btn of btns) {{
        if (btn.innerText.trim() === key) {{
            btn.click();
            break;
        }}
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
