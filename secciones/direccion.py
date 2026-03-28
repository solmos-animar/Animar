import streamlit as st
from auth.session import require_role

# Mock de alumnos (después lo conectamos a DB o CSV)
ALUMNOS = [
    {"nombre": "Juan Pérez", "fecha_nac": "12/05/2013", "grado": "3° A"},
    {"nombre": "María López", "fecha_nac": "22/09/2012", "grado": "4° B"},
    {"nombre": "Tomás García", "fecha_nac": "03/11/2013", "grado": "3° A"},
]

def render():
    require_role("admin")  # o "direccion" si después separás roles

    st.title("🏫 Dirección - Alumnos")

    st.markdown("### 📋 Listado de alumnos")

    for alumno in ALUMNOS:
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**👤 Nombre**")
                st.write(alumno["nombre"])

            with col2:
                st.markdown("**🎂 Fecha de nacimiento**")
                st.write(alumno["fecha_nac"])

            with col3:
                st.markdown("**🏫 Grado / División**")
                st.write(alumno["grado"])
