import streamlit as st
from secciones.landing import show_landing
from secciones.estudiantes import render as render_estudiantes
from secciones.direccion import render as render_direccion

st.set_page_config(
    page_title="ConVivir — v1.1",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 1. Estado inicial
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"

# 2. Cargar CSS
with open("utilidades/desktop.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Sidebar (Menú a la izquierda)
st.markdown(f"""
    <div class="sidebar">
        <h1>ConVivir</h1>
        <div class="sub">Documento de Análisis · v1.1</div>
    </div>
""", unsafe_allow_html=True)

# Los botones se renderizan "encima" del div sidebar mediante Streamlit
with st.sidebar: # Esto es un truco visual, en realidad usaremos el CSS anterior
    pass 

# Colocamos los botones en un contenedor lateral
with st.container():
    # Este bloque flota a la izquierda por el CSS de .sidebar
    st.markdown('<div style="position:fixed; left:24px; top:120px; width:222px; z-index:1001;">', unsafe_allow_html=True)
    if st.button("📋 Resumen Ejecutivo", key="nav_ini"):
        st.session_state.seccion = "inicio"
        st.rerun()
    if st.button("👥 Actores", key="nav_act"):
        st.session_state.seccion = "actores" # Puedes crear esta sección luego
    if st.button("🚀 Dashboard Dirección", key="nav_dir"):
        st.session_state.seccion = "direccion"
        st.rerun()
    if st.button("🎒 Vista Alumno", key="nav_alu"):
        st.session_state.seccion = "alumno"
        st.rerun()
    st.markdown('<div style="margin-top:280px; font-size:12px; opacity:0.5; color:white;">Confidencial · 2026</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Área de Contenido
st.markdown('<div class="main-area">', unsafe_allow_html=True)

if st.session_state.seccion == "inicio":
    st.markdown('<div class="landing-container">', unsafe_allow_html=True)
    show_landing()
    st.markdown('</div>', unsafe_allow_html=True)
elif st.session_state.seccion == "direccion":
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    render_direccion()
    st.markdown('</div>', unsafe_allow_html=True)
elif st.session_state.seccion == "alumno":
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    render_estudiantes()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
