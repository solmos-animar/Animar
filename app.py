import streamlit as st

# Configuración inicial
st.set_page_config(
    page_title="Gestión de Convivencia Escolar",
    page_icon="🛡️",
    layout="wide",
)

# Estilos CSS para recuperar la apariencia anterior
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #1a2634;
        color: white;
    }
    .main {
        background-color: #f5f7f9;
    }
    .stCard {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e6e9ef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #1a2634;
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.session_state.logged_in = True

def logout():
    st.session_state.logged_in = False

# --- PANTALLA DE LOGIN ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("# 🛡️ Acceso al Sistema")
        st.write("Ingrese sus credenciales para gestionar la convivencia.")
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        if st.button("Iniciar Sesión", use_container_width=True):
            login()
            st.rerun()

# --- PANEL PRINCIPAL (DASHBOARD) ---
else:
    # Sidebar anterior
    st.sidebar.title("Menú Principal")
    st.sidebar.write(f"Usuario: **Administrador**")
    
    menu = st.sidebar.radio(
        "Navegación",
        ["Panel General", "Sociogramas", "Reportes de Alerta", "Configuración"]
    )
    
    if st.sidebar.button("Cerrar Sesión"):
        logout()
        st.rerun()

    # Contenido según el menú
    if menu == "Panel General":
        st.title("Dashboard de Convivencia")
        
        # Métricas rápidas
        col1, col2, col3, col4 = st.columns(4)
        col
