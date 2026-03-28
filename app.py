import streamlit as st

st.set_page_config(
    page_title="ConVivir",
    layout="wide",
    initial_sidebar_state="expanded" # Obligamos a que inicie abierto
)

# Cargar el CSS que bloquea las flechas
with open("utilidades/desktop.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"

# Sidebar Nativo
with st.sidebar:
    st.markdown('<h1 style="color:white; font-size:28px;">ConVivir</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.5);">v1.1 · 2026</p>', unsafe_allow_html=True)
    st.divider()
    
    if st.button("📋 Resumen Ejecutivo", use_container_width=True):
        st.session_state.seccion = "inicio"
    
    if st.button("🚀 Dashboard Dirección", use_container_width=True):
        st.session_state.seccion = "direccion"
    
    if st.button("🎒 Vista Alumno", use_container_width=True):
        st.session_state.seccion = "alumno"

# Render de secciones
seccion = st.session_state.seccion
if seccion == "inicio":
    from secciones.landing import show_landing
    show_landing()
elif seccion == "direccion":
    from secciones.direccion import render
    render()
elif seccion == "alumno":
    from secciones.estudiantes import render
    render()
