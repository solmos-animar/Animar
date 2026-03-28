import streamlit as st
import pandas as pd

# Inicializamos la conexión (Streamlit la maneja automáticamente)
conn = st.connection("postgresql", type="sql")

def render():
    st.markdown('<h2 style="color: #0f2240;">🛡️ Administración de Instituciones</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Nuevo Colegio", "👨‍🏫 Docentes", "👪 Tutores", "🎒 Alumnos"])

    with tab1:
        st.subheader("Registrar Institución")
        with st.form("form_nuevo_colegio", clear_on_submit=True):
            col1, col2 = st.columns(2)
            nombre_col = col1.text_input("Nombre del Colegio")
            cuit_col = col2.text_input("Identificación Fiscal (CUIT/RUT)")
            plan_tipo = st.selectbox("Plan", ["Básico", "Estándar", "Premium"])
            
            if st.form_submit_button("Crear Colegio"):
                if nombre_col and cuit_col:
                    try:
                        # INSERTAMOS EN LA BASE DE DATOS
                        with conn.session as s:
                            s.execute(
                                "INSERT INTO colegios (nombre, cuit, plan) VALUES (:nom, :cuit, :plan)",
                                {"nom": nombre_col, "cuit": cuit_col, "plan": plan_tipo}
                            )
                            s.commit()
                        st.success(f"✅ '{nombre_col}' guardado en Supabase.")
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                else:
                    st.warning("Completa los campos obligatorios.")

    with tab4:
        st.subheader("Carga Masiva de Alumnos")
        # Leemos los colegios existentes para el dropdown
        df_colegios = conn.query("SELECT id, nombre FROM colegios", ttl="0")
        
        if not df_colegios.empty:
            colegio_sel = st.selectbox("Seleccionar Colegio", 
                                      options=df_colegios['id'], 
                                      format_func=lambda x: df_colegios[df_colegios['id']==x]['nombre'].iloc[0])
            
            archivo = st.file_uploader("Subir Excel de Alumnos", type=["xlsx"])
            if archivo:
                df_alumnos = pd.read_excel(archivo)
                st.dataframe(df_alumnos.head())
                
                if st.button("🚀 Confirmar Carga"):
                    # Aquí iría un loop para insertar cada fila del DF en la tabla 'alumnos'
                    st.info("Procesando carga masiva...")
        else:
            st.warning("Primero debes cargar un colegio en la Tab 1.")
