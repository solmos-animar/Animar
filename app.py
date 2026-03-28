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

# ── 2. Cargar Estilos ─────────────────────────────────────────────────────────
with open("utilidades/desktop.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── 3. Sidebar Visual (HTML + Botones Streamlit) ──────────────────────────────
# Estructura azul oscuro del sidebar
st.markdown("""
<div class="sidebar">
    <h1>ConVivir</h1>
    <div class="sub">Documento de Análisis · v1.1</div>
</div>
""", unsafe_allow_html=True)

# Botones de navegación inyectados en el sidebar
with st.container():
    # Contenedor para posicionar botones sobre el fondo azul
    st.markdown('<div class="sidebar-nav-container">', unsafe_allow_html=True)
    
    if st.button("📋 Resumen Ejecutivo", key="nav_ini"):
        st.session_state.seccion = "inicio"
        st.rerun()
        
    if st.button("🚀 Dashboard Dirección", key="nav_dir"):
        st.session_state.seccion = "direccion"
        st.rerun()
        
    if st.button("🎒 Vista Alumno", key="nav_alu"):
        st.session_state.seccion = "alumno"
        st.rerun()
        
    st.markdown('<div class="sidebar-footer">Confidencial · 2026</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── 4. Renderizado Dinámico ───────────────────────────────────────────────────
# Usamos bloques try/except para evitar que la app se rompa si falta un archivo
st.markdown('<div class="main-area">', unsafe_allow_html=True)

seccion = st.session_state.seccion

try:
    if seccion == "inicio":
        from secciones.landing import show_landing
        show_landing()
    elif seccion == "direccion":
        from secciones.direccion import render as render_direccion
        render_direccion()
    elif seccion == "alumno":
        # Intentamos importar con el nombre que definiste
        from secciones.estudiantes import render as render_estudiantes
        render_estudiantes()
except ImportError as e:
    st.error(f"Error de archivo: No se encontró el módulo en la carpeta 'secciones'. Verifica que el nombre del archivo sea correcto. (Detalle: {e})")
except Exception as e:
    st.error(f"Ocurrió un error inesperado: {e}")

st.markdown('</div>', unsafe_allow_html=True)
