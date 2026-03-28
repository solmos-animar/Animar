import streamlit as st
from utilidades.header import render_header
from secciones.landing import show_landing
from secciones.estudiantes import render as render_estudiantes
# ... resto de las importaciones

st.set_page_config(
    page_title="ConVivir",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 1. Inicializar el estado de la sección si no existe
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"

# 2. Cargar CSS global
with open("utilidades/desktop.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Renderizar el Header (desde el archivo separado)
render_header()

# 4. Espaciador para que el contenido no quede bajo el menú fijo
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)

# 5. Lógica de renderizado basada en session_state (Carga instantánea)
seccion = st.session_state.seccion

if seccion == "inicio":
    show_landing()
elif seccion == "alumno":
    render_estudiantes()
elif seccion == "direccion":
    # render_direccion()
    st.write("Sección Dirección")
# ... resto de las secciones
