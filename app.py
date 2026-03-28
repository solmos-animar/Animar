import streamlit as st
from secciones.landing import show_landing
from secciones.estudiantes import render as render_estudiantes
from secciones.direccion import render as render_direccion

st.set_page_config(page_title="ConVivir", layout="wide")

with open("utilidades/desktop.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"

# Render Sidebar
st.markdown('<div class="cv-sidebar"><h1>ConVivir</h1><div class="sub">Documento de Análisis · v1.1</div></div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="position:fixed; left:20px; top:120px; width:230px; z-index:200;">', unsafe_allow_html=True)
    if st.button("📋 Resumen Ejecutivo"):
        st.session_state.seccion = "inicio"
        st.rerun()
    if st.button("🚀 Dashboard Dirección"):
        st.session_state.seccion = "direccion"
        st.rerun()
    if st.button("🎒 Vista Alumno"):
        st.session_state.seccion = "alumno"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Main Area
st.markdown('<div class="cv-content">', unsafe_allow_html=True)
if st.session_state.seccion == "inicio":
    show_landing()
elif st.session_state.seccion == "direccion":
    render_direccion()
elif st.session_state.seccion == "alumno":
    render_estudiantes()
st.markdown('</div>', unsafe_allow_html=True)
