import streamlit as st

# 1. Configuración básica (Nativa)
st.set_page_config(
    page_title="ConVivir — Gestión Escolar",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicializar el estado de navegación
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"

# 3. Sidebar Nativo (Fácil para tus colaboradoras)
with st.sidebar:
    st.title("ConVivir")
    st.write("v1.1 · 2026")
    st.divider() # Línea separadora nativa
    
    # Botones simples. Al hacer clic, Streamlit recarga la sección automáticamente.
    if st.button("📋 Resumen Ejecutivo", use_container_width=True):
        st.session_state.seccion = "inicio"
    
    if st.button("🚀 Dashboard Dirección", use_container_width=True):
        st.session_state.seccion = "direccion"
    
    if st.button("🎒 Vista Alumno", use_container_width=True):
        st.session_state.seccion = "alumno"

# 4. Renderizado de Contenido
seccion = st.session_state.seccion

if seccion == "inicio":
    try:
        from secciones.landing import show_landing
        show_landing()
    except Exception as e:
        st.error(f"No se pudo cargar la Landing. Error: {e}")

elif seccion == "direccion":
    try:
        from secciones.direccion import render
        render()
    except Exception as e:
        st.error(f"No se pudo cargar Dirección. Error: {e}")

elif seccion == "alumno":
    try:
        from secciones.estudiantes import render
        render()
    except Exception as e:
        st.error(f"No se pudo cargar Alumnos. Error: {e}")
