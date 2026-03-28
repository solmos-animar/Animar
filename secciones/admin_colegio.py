import streamlit as st
import pandas as pd

# Conexión a Supabase
conn = st.connection("postgresql", type="sql")

def render():
    st.markdown('<h2 style="color: #0f2240;">🛡️ Administración de Instituciones</h2>', unsafe_allow_html=True)
    
    # --- TABS DE GESTIÓN ---
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Nuevo Colegio", "👨‍🏫 Docentes", "👪 Tutores", "🎒 Alumnos"])

    with tab1:
        st.subheader("Registrar Institución")
        with st.form("form_nuevo_colegio", clear_on_submit=True):
            col1, col2 = st.columns(2)
            nombre_col = col1.text_input("Nombre del Colegio")
            cuit_col = col2.text_input("Identificación Fiscal (CUIT/RUT)")
            plan_tipo = st.selectbox("Plan", ["Básico", "Estándar", "Premium"])
            
            if st.form_submit_button("Guardar Colegio"):
                if nombre_col and cuit_col:
                    try:
                        with conn.session as s:
                            s.execute(
                                "INSERT INTO colegios (nombre, cuit, plan) VALUES (:nom, :cuit, :plan)",
                                {"nom": nombre_col, "cuit": cuit_col, "plan": plan_tipo}
                            )
                            s.commit()
                        st.success(f"✅ '{nombre_col}' guardado correctamente.")
                        st.rerun() # Refrescamos para que aparezca en la lista
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                else:
                    st.warning("Completa los campos obligatorios.")

        # --- LISTADO DE COLEGIO (VISUALIZACIÓN) ---
        st.markdown("---")
        st.subheader("Colegios Registrados")
        try:
            df_colegios = conn.query("SELECT nombre, cuit, plan, fecha_alta FROM colegios ORDER BY fecha_alta DESC", ttl=0)
            if not df_colegios.empty:
                st.dataframe(df_colegios, use_container_width=True)
            else:
                st.info("Aún no hay colegios registrados.")
        except Exception as e:
            st.error("No se pudo cargar la lista de colegios.")

    with tab4:
        st.subheader("Gestión de Alumnos")
        # Aquí ya podemos usar los colegios de la base de datos para el selectbox
        try:
            lista_colegios = conn.query("SELECT id, nombre FROM colegios", ttl=0)
            if not lista_colegios.empty:
                colegio_destino = st.selectbox(
                    "Seleccionar Colegio", 
                    options=lista_colegios['id'], 
                    format_func=lambda x: lista_colegios[lista_colegios['id']==x]['nombre'].iloc[0]
                )
                
                # ... (Aquí iría tu lógica de carga masiva que definimos antes) ...
                st.info(f"Listo para cargar alumnos en ID: {colegio_destino}")
            else:
                st.warning("Primero debes cargar un colegio en la pestaña anterior.")
        except:
            st.error("Error al conectar con la tabla de colegios.")
