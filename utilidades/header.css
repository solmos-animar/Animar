import streamlit as st

def render_header():
    # Recuperamos la sección actual del estado
    seccion_actual = st.session_state.get("seccion", "inicio")
    
    # CSS específico para que los botones de Streamlit parezcan links de navegación
    st.markdown("""
        <style>
        .nav-container {
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 60px;
            background: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 56px;
            border-bottom: 1px solid #e8e5df;
            z-index: 999999;
            box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        }
        .logo {
            font-family: 'Sora', sans-serif;
            font-size: 22px;
            font-weight: 800;
            color: #0f2240;
            cursor: pointer;
        }
        .logo em { font-style: normal; color: #1a56a0; }
        
        /* Estilo para los botones de Streamlit dentro del menú */
        div[data-testid="stHorizontalBlock"] .stButton button {
            background: transparent !important;
            border: none !important;
            color: #6b7280 !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            padding: 8px 16px !important;
            transition: all 0.2s ease !important;
            line-height: 1.5 !important;
        }
        div[data-testid="stHorizontalBlock"] .stButton button:hover {
            color: #0f2240 !important;
            background: #f3f4f6 !important;
        }
        /* Clase para el botón activo (la inyectamos vía JS o lógica de color) */
        </style>
    """, unsafe_allow_html=True)

    # HTML del Header (Logo y Estructura)
    st.markdown(f"""
        <div class="nav-container">
            <div class="logo">Con<em>Vivir</em></div>
            <div id="nav-placeholder"></div>
        </div>
    """, unsafe_allow_html=True)

    # Botones reales de Streamlit que disparan el cambio sin recargar la URL
    cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
    
    with cols[0]:
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
    # ... puedes agregar el resto de los botones aquí
