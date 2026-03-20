import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def render():
    user = st.session_state.user
    st.title(f"👋 Hola, {user['name'].split()[0]}!")
    st.markdown("Bienvenido/a a ConVivir — tu espacio para mejorar la convivencia en el aula.")

    # Estado del aula
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 🚪 Tu aula: 3° A Primaria")
            st.markdown("**Estado:** 🟢 Habilitada")
            st.markdown("**Encuesta sociométrica:** Disponible")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📝 Completar encuesta", type="primary", use_container_width=True):
                st.session_state.current_page = "student_encuesta"
                st.rerun()

    st.markdown("---")

    # Secciones disponibles
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 📝 Encuesta")
            st.markdown("Respondé la encuesta sobre tus compañeros de forma anónima y confidencial.")
            if st.button("Ir a la encuesta", use_container_width=True):
                st.session_state.current_page = "student_encuesta"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 📚 Contenido")
            st.markdown("Artículos y guías sobre convivencia, bullying y cómo pedir ayuda.")
            if st.button("Ver contenido", use_container_width=True):
                st.session_state.current_page = "student_contenido"
                st.rerun()

    with col3:
        with st.container(border=True):
            st.markdown("### 💬 Mensaje al docente")
            st.markdown("Enviá un mensaje confidencial a tu docente si necesitás hablar de algo.")
            if st.button("Enviar mensaje", use_container_width=True):
                st.session_state.show_mensaje = True
                st.rerun()

    if st.session_state.get("show_mensaje"):
        st.markdown("---")
        st.subheader("💬 Mensaje confidencial al docente")
        st.info("Este mensaje solo lo va a ver tu docente. Es completamente confidencial.")
        mensaje = st.text_area("Escribí tu mensaje aquí:", placeholder="Podés contar lo que está pasando...")
        if st.button("Enviar", type="primary"):
            if mensaje:
                st.success("✅ Tu mensaje fue enviado. Tu docente lo va a recibir en privado.")
                st.session_state.show_mensaje = False
            else:
                st.error("Escribí algo antes de enviar.")
