import streamlit as st

# 1. Configuración de página
st.set_page_config(
    page_title="Prevención del Bullying — Plataforma de Gestión",
    page_icon="🛡️",
    layout="wide",
)

# 2. Estilos CSS Originales (Barra lateral oscura y métricas limpias)
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #1a2634;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .main {
        background-color: #f5f7f9;
    }
    div[data-testid="metric-container"] {
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

# 3. Encabezado con la leyenda original
st.title("🛡️ Prevención del Bullying")
st.write("Plataforma de monitoreo, detección temprana y gestión de convivencia escolar.")

st.divider()

# 4. Panel de Métricas (Dashboard)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Alumnos Registrados", value="840", delta="12")
with col2:
    st.metric(label="Alertas Activas", value="5", delta="-2", delta_color="inverse")
with col3:
    st.metric(label="Clima Escolar", value="8.4/10", delta="0.2")
with col4:
    st.metric(label="Intervenciones", value="14", delta="3")

st.write("###")

# 5. Secciones de Alerta y Gráficos
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⚠️ Alertas de Riesgo Detectadas")
    st.error("**Exclusión Social:** Detectada en 2° Año B")
    st.warning("**Variación en Sociograma:** 4° Año A presenta cambios críticos.")
    st.info("**Taller Preventivo:** Programado para el Viernes 27/03")

with col_right:
    st.subheader("📊 Reportes por Nivel Institucional")
    # Gráfico de barras simple
    st.bar_chart({
        "Primaria": 8,
        "Secundaria": 15,
        "Terciaria": 4
    })

st.divider()

# 6. Sidebar con identificación clara
st.sidebar.title("Menú Principal")
st.sidebar.markdown("---")
st.sidebar.write("Usuario: **Administrador**")
st.sidebar.write("Rol: **Gestión Institucional**")

st.sidebar.info("Seleccione una vista en el menú inferior para ver detalles específicos de Sociogramas o Reportes.")

# Nota: Las páginas de la carpeta /pages aparecerán automáticamente debajo de esto en la barra lateral.
