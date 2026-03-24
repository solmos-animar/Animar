import streamlit as st

# 1. Configuración de página (ESTO DEBE IR PRIMERO)
st.set_page_config(
    page_title="ConVivir en grande",
    page_icon="🛡️",
    layout="wide"
)

# 2. Estilo para la barra lateral (para que se vea profesional)
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #1a2634;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Contenido de Bienvenida
st.title("🛡️ Sistema ConVivir")
st.write("Bienvenido al panel central. Selecciona una opción en el menú de la izquierda para comenzar.")

st.info("← Usa el menú lateral para navegar entre las diferentes secciones (Sociogramas, Reportes, etc.)")

# 4. (Opcional) Resumen rápido
col1, col2 = st.columns(2)
with col1:
    st.metric("Estado General", "Saludable")
with col2:
    st.metric("Alertas Hoy", "0")
