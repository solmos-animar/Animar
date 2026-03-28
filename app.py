import streamlit as st

st.set_page_config(
    page_title="ConVivir — v1.1",
    layout="wide",
    initial_sidebar_state="expanded", # Ahora lo dejamos expandido
)

# ── 1. Inicializar Estado ─────────────────────────────────────────────────────
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"

# ── 2. Cargar Estilos ─────────────────────────────────────────────────────────
with open("utilidades/desktop.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── 3. Sidebar de Navegación ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-title">ConVivir</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">Documento de Análisis · v1.1</div>', unsafe_allow_html=True)
    
    if st.button("📋 Resumen Ejecutivo", key="nav_ini"):
        st.session_state.seccion = "inicio"
        st.rerun()
        
    if st.button("🚀 Dashboard Dirección", key="nav_dir"):
        st.session_state.seccion = "direccion"
        st.rerun()
        
    if st.button("🎒 Vista Alumno", key="nav_alu"):
        st.session_state.seccion = "alumno"
        st.rerun()
        
    st.markdown('<br><br><div style="color:rgba(255,255,255,0.3); font-size:11px; padding: 0 16px;">Confidencial · 2026</div>', unsafe_allow_html=True)

# ── 4. Renderizado del Contenido ──────────────────────────────────────────────
seccion = st.session_state.seccion

if seccion == "inicio":
    st.markdown('<div class="landing-dark">', unsafe_allow_html=True)
    try:
        from secciones.landing import show_landing
        show_landing()
    except Exception as e:
        st.error(f"Error cargando landing: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

elif seccion == "direccion":
    st.markdown('<div style="padding: 60px;">', unsafe_allow_html=True)
    try:
        from secciones.direccion import render as render_direccion
        render_direccion()
    except Exception as e:
        st.error(f"Error cargando dirección: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

elif seccion == "alumno":
    st.markdown('<div style="padding: 60px;">', unsafe_allow_html=True)
    try:
        from secciones.estudiantes import render as render_estudiantes
        render_estudiantes()
    except Exception as e:
        st.error(f"Error cargando estudiantes: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
