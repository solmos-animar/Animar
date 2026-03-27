import streamlit as st
from secciones.landing import show_landing, LOGO_SIDEBAR, LOGO_MOD

# ── Imports de todas las secciones ───────────────────────────────────────────
from secciones.admin_colegios   import show_admin_colegios
from secciones.admin_dashboard  import show_admin_dashboard
from secciones.admin_docentes   import show_admin_docentes
from secciones.admin_kyc        import show_admin_kyc
from secciones.sociogramas      import show_sociogramas
from secciones.student_contenido import show_student_contenido
from secciones.student_encuesta  import show_student_encuesta
from secciones.student_home      import show_student_home
from secciones.teacher_alertas   import show_teacher_alertas
from secciones.teacher_aulas     import show_teacher_aulas
from secciones.teacher_dashboard import show_teacher_dashboard
from secciones.teacher_reportes  import show_teacher_reportes
from secciones.teacher_sociograma import show_teacher_sociograma

st.set_page_config(
    page_title="ConVivir — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  .block-container { padding-top: 1rem !important; }
  div[data-testid="stTabs"] {
      position: sticky;
      top: 0;
      z-index: 999;
      background: white;
      padding-bottom: 4px;
      border-bottom: 2px solid #e0d8d0;
  }
  div[data-testid="stTabs"] button {
      font-weight: 700;
      font-size: 13px;
      color: #7a8a82;
  }
  div[data-testid="stTabs"] button[aria-selected="true"] {
      color: #1a2e2a;
      border-bottom: 3px solid #4db8a0;
  }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TABS — siempre visibles
# ════════════════════════════════════════════════════════════════════════════

(
    tab_inicio,
    tab_admin,
    tab_directora,   # placeholder — agregar sección cuando esté lista
    tab_docente,
    tab_alumno,
    tab_tutor,       # placeholder — agregar sección cuando esté lista
    tab_moderadora,  # placeholder — agregar sección cuando esté lista
) = st.tabs([
    "🏠 Inicio",
    "🏛️ Admin",
    "👩‍💼 Directora",
    "👨‍🏫 Docente",
    "🎒 Alumno",
    "👨‍👩‍👧 Tutor",
    "🛡️ Moderadora",
])

# ── Inicio ────────────────────────────────────────────────────────────────────
with tab_inicio:
    show_landing()

# ── Admin Global ──────────────────────────────────────────────────────────────
with tab_admin:
    subtab_dash, subtab_colegios, subtab_docentes, subtab_kyc = st.tabs([
        "📊 Dashboard",
        "🏫 Colegios",
        "👨‍🏫 Docentes",
        "📋 KYC",
    ])
    with subtab_dash:
        show_admin_dashboard()
    with subtab_colegios:
        show_admin_colegios()
    with subtab_docentes:
        show_admin_docentes()
    with subtab_kyc:
        show_admin_kyc()

# ── Directora ─────────────────────────────────────────────────────────────────
with tab_directora:
    st.info("🚧 Sección Directora en construcción.")

# ── Docente ───────────────────────────────────────────────────────────────────
with tab_docente:
    subtab_dash_t, subtab_aulas, subtab_sociograma, subtab_alertas, subtab_reportes = st.tabs([
        "📊 Dashboard",
        "🚪 Aulas",
        "🕸️ Sociograma",
        "🚨 Alertas",
        "📈 Reportes",
    ])
    with subtab_dash_t:
        show_teacher_dashboard()
    with subtab_aulas:
        show_teacher_aulas()
    with subtab_sociograma:
        show_sociogramas()
        show_teacher_sociograma()
    with subtab_alertas:
        show_teacher_alertas()
    with subtab_reportes:
        show_teacher_reportes()

# ── Alumno ────────────────────────────────────────────────────────────────────
with tab_alumno:
    subtab_home, subtab_encuesta, subtab_contenido = st.tabs([
        "🏠 Inicio",
        "📝 Encuesta",
        "📚 Contenido",
    ])
    with subtab_home:
        show_student_home()
    with subtab_encuesta:
        show_student_encuesta()
    with subtab_contenido:
        show_student_contenido()

# ── Tutor ─────────────────────────────────────────────────────────────────────
with tab_tutor:
    st.info("🚧 Sección Tutor en construcción.")

# ── Moderadora ────────────────────────────────────────────────────────────────
with tab_moderadora:
    st.info("🚧 Sección Moderadora en construcción.")
