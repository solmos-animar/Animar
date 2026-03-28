import streamlit as st

def render_header():
    # Detectamos la sección activa para el estilo visual
    seccion_actual = st.session_state.get("seccion", "inicio")
    
    # Contenedor principal del Header
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    # Creamos un layout de columnas: 
    # c1: Logo | c2: Espacio flexible | c3-c8: Botones del menú
    c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([2, 3, 1, 1, 1, 1, 1, 1])
    
    with c1:
        # El logo ahora es un botón invisible que lleva al inicio
        if st.button("ConVivir", key="logo_home"):
            st.session_state.seccion = "inicio"
            st.rerun()
            
    # c2 queda vacío para empujar el resto a la derecha
    
    with c3:
        if st.button("Inicio", key="nav_inicio"):
            st.session_state.seccion = "inicio"
            st.rerun()
    with c4:
        if st.button("Dirección", key="nav_dir"):
            st.session_state.seccion = "direccion"
            st.rerun()
    with c5:
        if st.button("Docente", key="nav_doc"):
            st.session_state.seccion = "docente"
            st.rerun()
    with c6:
        if st.button("Alumno", key="nav_alu"):
            st.session_state.seccion = "alumno"
            st.rerun()
    with c7:
        if st.button("Moderador", key="nav_mod"):
            st.session_state.seccion = "moderador"
            st.rerun()
    with c8:
        if st.button("Admin", key="nav_adm"):
            st.session_state.seccion = "admin"
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
