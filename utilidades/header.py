import streamlit as st

def render_header():
    # Contenedor visual del Header
    st.markdown("""
        <div class="nav-container">
            <div class="logo">Con<em>Vivir</em></div>
        </div>
    """, unsafe_allow_html=True)

    # Botones de navegación (agrupados a la derecha)
    # Dejamos las primeras columnas vacías para empujar el menú
    cols = st.columns([4, 1, 1, 1, 1, 1, 1])
    
    with cols[1]:
        if st.button("Inicio", key="nav_inicio"):
            st.session_state.seccion = "inicio"
            st.rerun()
    with cols[2]:
        if st.button("Dirección", key="nav_dir"):
            st.session_state.seccion = "direccion"
            st.rerun()
    with cols[3]:
        if st.button("Docente", key="nav_doc"):
            st.session_state.seccion = "docente"
            st.rerun()
    with cols[4]:
        if st.button("Alumno", key="nav_alu"):
            st.session_state.seccion = "alumno"
            st.rerun()
    with cols[5]:
        if st.button("Moderador", key="nav_mod"):
            st.session_state.seccion = "moderador"
            st.rerun()
    with cols[6]:
        if st.button("Admin", key="nav_adm"):
            st.session_state.seccion = "admin"
            st.rerun()
