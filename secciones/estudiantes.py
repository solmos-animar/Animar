import streamlit as st

# Intentamos cargar datos, si no, usamos genéricos
try:
    from data.mock_data import ALUMNOS
    COMPAÑEROS = [a["nombre"] for a in ALUMNOS if a["nombre"] != st.session_state.user.get("name", "Lucas Martínez")]
except:
    COMPAÑEROS = ["Mateo García", "Sofía Rodríguez", "Valentina López", "Bautista Pérez", "Martina Gómez"]

ARTICULOS = [
    {"titulo": "¿Qué es el bullying?", "contenido": "El bullying es agresión repetida..."},
    {"titulo": "Cómo pedir ayuda", "contenido": "Hablá con un adulto de confianza..."},
    {"titulo": "Ser buen compañero", "contenido": "Saludá y escuchá a los demás..."}
]

def render_home():
    user = st.session_state.user
    nombre = user['name'].split()[0]
    st.title(f"👋 ¡Hola, {nombre}!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 📝 Encuesta\nDisponible para responder.")
        if st.button("Ir a la encuesta"):
            st.session_state.current_page = "student_encuesta"
            st.rerun()
    with col2:
        st.success("### 📚 Contenido\nArtículos de interés.")
        if st.button("Ver contenido"):
            st.session_state.current_page = "student_contenido"
            st.rerun()
    with col3:
        st.warning("### 💬 Mensaje\nEscribí a tu docente.")
        if st.button("Enviar mensaje"):
            st.session_state.show_mensaje = True
            st.rerun()

def render():
    # Enrutador interno
    page = st.session_state.get("current_page", "student_home")
    
    st.markdown('<div style="padding: 40px;">', unsafe_allow_html=True)
    if page == "student_encuesta":
        if st.button("← Volver"): 
            st.session_state.current_page = "student_home"
            st.rerun()
        st.title("Encuesta")
    elif page == "student_contenido":
        if st.button("← Volver"): 
            st.session_state.current_page = "student_home"
            st.rerun()
        st.title("Contenido")
    else:
        render_home()
    st.markdown('</div>', unsafe_allow_html=True)
