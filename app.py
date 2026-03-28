import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="ConVivir — v1.1",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 1. Inicializar Estado ─────────────────────────────────────────────────────
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"
if "user" not in st.session_state:
    st.session_state.user = {"name": "Lucas Martínez"}

# ── 2. Cargar Estilos ─────────────────────────────────────────────────────────
with open("utilidades/desktop.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── 3. Sidebar (Menú a la izquierda) ──────────────────────────────────────────
# Dibujamos el fondo azul oscuro
st.markdown('<div class="cv-sidebar"><h1>ConVivir</h1><div class="sub">Documento de Análisis · v1.1</div></div>', unsafe_allow_html=True)

# Colocamos los botones de Streamlit
with st.container():
    st.markdown('<div style="position:fixed; left:20px; top:120px; width:230px; z-index:200;">', unsafe_allow_html=True)
    
    if st.button("📋 Resumen Ejecutivo", key="nav_ini"):
        st.session_state.seccion = "inicio"
        st.rerun()
        
    if st.button("🚀 Dashboard Dirección", key="nav_dir"):
        st.session_state.seccion = "direccion"
        st.rerun()
        
    if st.button("🎒 Vista Alumno", key="nav_alu"):
        st.session_state.seccion = "alumno"
        st.rerun()
    
    st.markdown('<div style="margin-top:280px; font-size:12px; opacity:0.5; color:white;">Confidencial · 2026</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── 4. Área de Contenido Principal ────────────────────────────────────────────
st.markdown('<div class="cv-content">', unsafe_allow_html=True)

seccion = st.session_state.seccion

if seccion == "inicio":
    from secciones.landing import show_landing
    show_landing()

elif seccion == "alumno":
    # Importación dinámica para evitar el ImportError al inicio
    try:
        from secciones.estudiantes import render
        render()
    except Exception as e:
        st.error(f"No se pudo cargar la vista de Alumno. Error: {e}")

elif seccion == "direccion":
    try:
        from secciones.direccion import render as render_dir
        render_dir()
    except Exception as e:
        st.error(f"No se pudo cargar la vista de Dirección. Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)
