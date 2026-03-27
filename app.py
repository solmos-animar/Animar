import streamlit as st
from secciones.landing import show_landing, LOGO_SIDEBAR, LOGO_MOD
from secciones.estudiantes import show_estudiantes

st.set_page_config(
    page_title="ConVivir — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Estilos globales ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  .block-container { padding-top: 1rem !important; }

  /* Barra de tabs siempre visible y fija arriba */
  div[data-testid="stTabs"] {
      position: sticky;
      top: 0;
      z-index: 999;
      background: white;
      padding-bottom: 4px;
      border-bottom: 2px solid #e0d8d0;
  }

  /* Estilo de los tabs */
  div[data-testid="stTabs"] button {
      font-weight: 700;
      font-size: 13px;
      color: #7a8a82;
  }
  div[data-testid="stTabs"] button[aria-selected="true"] {
      color: #1a2e2a;
      border-bottom: 3px solid #4db8a0;
  }

  /* Separadores de grupo entre tabs */
  .tab-group-label {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: #4db8a0;
      padding: 0 8px;
      display: flex;
      align-items: center;
  }
</style>
""", unsafe_allow_html=True)

# ── Estado de sesión ──────────────────────────────────────────────────────────
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0  # 0 = Landing (inicio)

# ════════════════════════════════════════════════════════════════════════════
# MENÚ DE TABS — siempre visible
# Orden: Inicio | Admin Global | — Colegio — | Directora | Docente | Alumno | Tutor | — Animar — | Moderadora
# ════════════════════════════════════════════════════════════════════════════

tab_inicio, tab_admin, tab_directora, tab_docente, tab_alumno, tab_tutor, tab_moderadora = st.tabs([
    "🏠 Inicio",
    "🏛️ Admin Global",
    "👩‍💼 Directora",
    "👨‍🏫 Docente",
    "🎒 Alumno",
    "👨‍👩‍👧 Tutor",
    "🛡️ Moderadora",
])

# ── Contenido de cada tab ─────────────────────────────────────────────────────

with tab_inicio:
    show_landing()

with tab_admin:
    st.markdown("### 🏛️ Admin Global")
    st.info("Sección en construcción.")

with tab_directora:
    st.markdown("### 👩‍💼 Directora")
    st.info("Sección en construcción.")

with tab_docente:
    st.markdown("### 👨‍🏫 Docente")
    st.info("Sección en construcción.")

with tab_alumno:
    st.markdown("### 🎒 Alumno")
    show_estudiantes()   # ← ya existe en secciones/estudiantes.py

with tab_tutor:
    st.markdown("### 👨‍👩‍👧 Tutor")
    st.info("Sección en construcción.")

with tab_moderadora:
    st.markdown("### 🛡️ Moderadora")
    st.info("Sección en construcción.")
