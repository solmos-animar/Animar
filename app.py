import streamlit as st

# Configuración de página
st.set_page_config(page_title="ConVivir en grande", layout="wide")

# Ocultar menús por defecto de Streamlit para que parezca una web profesional
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0rem;}
    </style>
    """, unsafe_allow_html=True)

# ── LOGOS Y ESTILOS ──────────────────────────────────────────────────────────
# Usamos una variable simple para el HTML de la landing
landing_html = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
    
    .main-hero {
        background: radial-gradient(circle at top right, #1a3a5a, #03091a);
        color: white;
        font-family: 'DM Sans', sans-serif;
        padding: 100px 50px;
        min-height: 80vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .tag {
        background: rgba(74, 158, 255, 0.2);
        color: #4a9eff;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    h1 {
        font-family: 'Sora', sans-serif;
        font-size: 60px;
        margin: 0;
        line-height: 1.1;
    }
    h1 em { color: #4db8a0; font-style: normal; }
    .sub {
        font-size: 20px;
        color: rgba(255,255,255,0.7);
        max-width: 700px;
        margin-top: 20px;
    }
</style>

<div class="main-hero">
    <div class="tag">PROPUESTA EDUCATIVA 2026</div>
    <h1>ConVivir<br><em>en grande</em></h1>
    <p class="sub">
        Transformamos la convivencia escolar fortaleciendo los vínculos. 
        Una plataforma diseñada para crear entornos seguros donde cada estudiante puede crecer con confianza.
    </p>
</div>
<div style="background: #03091a; padding: 20px; text-align: center; color: gray; font-size: 12px;">
    © 2026 ConVivir — Educar en grande es convivir mejor.
</div>
"""

# ── LÓGICA DE NAVEGACIÓN ──────────────────────────────────────────────────────

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Mostramos la landing
    st.markdown(landing_html, unsafe_allow_html=True)
    
    # Botón centrado usando columnas de Streamlit
    _, col, _ = st.columns([2,1,2])
    with col:
        if st.button("Ingresar a la Plataforma", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
else:
    # Dashboard simple para probar
    st.sidebar.title("ConVivir")
    st.title("Bienvenido al Panel de Gestión")
    st.write("Has ingresado correctamente a la plataforma.")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
