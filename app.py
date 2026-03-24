import streamlit as st

# 1. Configuración de página
st.set_page_config(
    page_title="Sistema de Gestión de Convivencia",
    page_icon="🛡️",
    layout="wide",
)

# 2. Estilos CSS (Versión Institucional Anterior)
st.markdown("""
<style>
    /* Barra lateral profesional */
    [data-testid="stSidebar"] {
        background-color: #1a2634;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Fondo y contenedores */
    .main {
        background-color: #f8f9fa;
    }
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    h1, h2, h3 {
        color: #1a2634;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# 3. Encabezado Principal
st.title("🛡️ Panel de Control de Convivencia")
st.write("Bienvenido al sistema de monitoreo y prevención institucional.")

st.divider()

# 4. Métricas en Tiempo Real (Resumen Ejecutivo)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Alumnos en Sistema", value="840", delta="12")
with col2:
    st.metric(label="Alertas Críticas", value="5", delta="-2", delta_color="inverse")
with col3:
    st.metric(label="Índice de Clima", value="8.4/10", delta="0.2")
with col4:
    st.metric(label="Intervenciones Mes", value="14", delta="3")

st.write("###") # Espaciador

# 5. Secciones de Información Rápida
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("⚠️ Alertas Recientes")
    st.error("**Caso de Exclusión:** Detectado en 2° Año B (Nivel Secundario)")
    st.warning("**Variación de Vínculos:** 4° Año A presenta cambios en la red social.")
    st.info("**Próximo Taller:** Convivencia digital - Viernes 27/03")

with col_b:
    st.subheader("📊 Distribución por Nivel")
