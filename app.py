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
if "current_page" not in st.session_state:
    st.session_state.current_page = "student_home"
if "user" not in st.session_state:
    st.session_state.user = {"name": "Lucas Martínez"}

# ── Navbar custom ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="menu-bar">
  <div class="menu-logo">Con<em>Vivir</em></div>
  <div class="nb-toggle" onclick="toggleMenu()" id="nb-toggle">☰</div>
</div>

<div class="nb-menu" id="nb-menu">
  <div class="nb-item active" onclick="nbClick(0)">🏠 Inicio</div>
  <div class="nb-sep"></div>
  <span class="nb-group-label">Colegio</span>
  <div class="nb-item" onclick="nbClick(1)">👩‍💼 Dirección</div>
  <div class="nb-item" onclick="nbClick(2)">👨‍🏫 Docente</div>
  <div class="nb-item" onclick="nbClick(3)">🎒 Alumno</div>
  <div class="nb-item" onclick="nbClick(4)">👨‍👩‍👧 Familia</div>
  <div class="nb-sep"></div>
  <span class="nb-group-label">Animar</span>
  <div class="nb-item" onclick="nbClick(5)">🛡️ Moderador</div>
  <div class="nb-item" onclick="nbClick(6)">🏛️ Admin Global</div>
</div>

<script>
function toggleMenu() {
    const menu = document.getElementById('nb-menu');
    const toggle = document.getElementById('nb-toggle');
    const isOpen = menu.classList.toggle('open');
    toggle.textContent = isOpen ? '✕' : '☰';
}

function nbClick(index) {
    document.querySelectorAll('.nb-item').forEach((el, i) => {
        el.classList.toggle('active', i === index);
    });
    document.getElementById('nb-menu').classList.remove('open');
    document.getElementById('nb-toggle').textContent = '☰';
    const tabs = window.parent.document.querySelectorAll('[data-testid="stTabs"] button[role="tab"]');
    if (tabs[index]) tabs[index].click();
}
</script>
""", unsafe_allow_html=True)

# ── Tabs reales (ocultos, controlados por la navbar) ──────────────────────────
tabs = st.tabs(["Inicio", "Dirección", "Docente", "Alumno", "Familia", "Moderador", "Admin Global"])

with tabs[0]: show_landing()
with tabs[1]: render_direccion()
with tabs[2]: render_docente()
with tabs[3]: render_estudiantes()
with tabs[4]: render_familia()
with tabs[5]: render_moderador()
with tabs[6]: render_global_admin()
