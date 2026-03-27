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

# ── Inicializar estado ────────────────────────────────────────────────────────
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"
if "current_page" not in st.session_state:
    st.session_state.current_page = "student_home"
if "user" not in st.session_state:
    st.session_state.user = {"name": "Lucas Martínez"}

# ── Navbar: logo + menú custom ────────────────────────────────────────────────
st.markdown("""
<div class="menu-bar">
  <div class="menu-logo">Con<em>Vivir</em></div>
</div>
<div class="nb-menu">
  <div class="nb-item" id="nb-inicio"    onclick="nbClick('inicio')">🏠 Inicio</div>
  <div class="nb-sep"></div>
  <span class="nb-group-label">Colegio</span>
  <div class="nb-item" id="nb-direccion" onclick="nbClick('direccion')">👩‍💼 Dirección</div>
  <div class="nb-item" id="nb-docente"   onclick="nbClick('docente')">👨‍🏫 Docente</div>
  <div class="nb-item" id="nb-alumno"    onclick="nbClick('alumno')">🎒 Alumno</div>
  <div class="nb-item" id="nb-familia"   onclick="nbClick('familia')">👨‍👩‍👧 Familia</div>
  <div class="nb-sep"></div>
  <span class="nb-group-label">Animar</span>
  <div class="nb-item" id="nb-moderador" onclick="nbClick('moderador')">🛡️ Moderador</div>
  <div class="nb-item" id="nb-admin"     onclick="nbClick('admin')">🏛️ Admin Global</div>
</div>

<script>
function nbClick(seccion) {
  // Marcar activo visualmente
  document.querySelectorAll('.nb-item').forEach(i => i.classList.remove('active'));
  const el = document.getElementById('nb-' + seccion);
  if (el) el.classList.add('active');

  // Enviar al backend de Streamlit via query param + reload
  const url = new URL(window.parent.location.href);
  url.searchParams.set('seccion', seccion);
  window.parent.location.href = url.toString();
}

// Marcar activo el item actual al cargar
const params = new URLSearchParams(window.parent.location.search);
const current = params.get('seccion') || 'inicio';
const el = document.getElementById('nb-' + current);
if (el) el.classList.add('active');
</script>
""", unsafe_allow_html=True)

# ── Leer sección desde query params ──────────────────────────────────────────
params = st.query_params
if "seccion" in params:
    st.session_state.seccion = params["seccion"]

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
else:
    show_landing()
