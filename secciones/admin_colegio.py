import streamlit as st
import pandas as pd
from sqlalchemy import text  # IMPORTANTE: Para que no de el error de declaración explícita

# Inicializamos la conexión con Supabase (Configurada en Secrets)
conn = st.connection("postgresql", type="sql")

def render():
    st.markdown('<h2 style="color: #0f2240;">🛡️ Administración de Instituciones</h2>', unsafe_allow_html=True)
    st.markdown("Gestión global de colegios, docentes, alumnos y tutores para el ecosistema Animar.")
    
    # Tabs para organizar la carga por entidad
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏢 Nuevo Colegio", 
        "👨‍🏫 Docentes", 
        "👪 Tutores/Padres", 
        "🎒 Alumnos"
    ])

    # --- TAB 1: GESTIÓN DE COLEGIO ---
    with tab1:
        st.subheader("Registrar Institución")
        with st.form("form_nuevo_colegio", clear_on_submit=True):
            col1, col2 = st.columns(2)
            nombre_col = col1.text_input("Nombre del Colegio")
            cuit_col = col2.text_input("Identificación Fiscal (CUIT/RUT)")
            
            c3, c4 = st.columns(2)
            plan_tipo = c3.selectbox("Plan de Suscripción", ["Básico", "Estándar", "Premium"])
            
            if st.form_submit_button("Guardar Colegio"):
                if nombre_col and cuit_col:
                    try:
                        with conn.session as s:
                            # Usamos text() para declarar explícitamente la consulta SQL
                            s.execute(
                                text("INSERT INTO colegios (nombre, cuit, plan) VALUES (:nom, :cuit, :plan)"),
                                {"nom": nombre_col, "cuit": cuit_col, "plan": plan_tipo}
                            )
                            s.commit()
                        st.success(f"✅ Colegio '{nombre_col}' guardado exitosamente.")
                        st.rerun() # Refrescamos para ver los cambios en la tabla
                    except Exception as e:
                        st.error(f"Error al guardar en la base de datos: {e}")
                else:
                    st.warning("Por favor completa los campos obligatorios (Nombre y CUIT).")

        # --- VISUALIZACIÓN DE COLEGIOS ---
        st.markdown("---")
        st.subheader("Colegios Registrados")
        try:
            # Consultamos la lista de colegios
            df_colegios = conn.query(text("SELECT nombre, cuit, plan, fecha_alta FROM colegios ORDER BY fecha_alta DESC"), ttl=0)
            if not df_colegios.empty:
                st.dataframe(df_colegios, use_container_width=True)
            else:
                st.info("Aún no hay instituciones registradas.")
        except Exception as e:
            st.error(f"No se pudo cargar la lista: {e}")

    # --- TAB 4: CARGA DE ALUMNOS (DINÁMICA) ---
    with tab4:
        st.subheader("Gestión de Alumnos")
        
        try:
            # Traemos los colegios para el selector
            res_colegios = conn.query(text("SELECT id, nombre FROM colegios"), ttl=0)
            
            if not res_colegios.empty:
                colegio_sel = st.selectbox(
                    "Seleccionar Colegio para la carga", 
                    options=res_colegios['id'], 
                    format_func=lambda x: res_colegios[res_colegios['id']==x]['nombre'].iloc[0]
                )
                
                st.info(f"Has seleccionado: {res_colegios[res_colegios['id']==colegio_sel]['nombre'].iloc[0]}")
                
                # Aquí podrías agregar el file_uploader para el Excel de alumnos más adelante
                archivo = st.file_uploader("Subir archivo Excel de alumnos", type=["xlsx"])
                if archivo:
                    st.success("Archivo detectado. ¿Quieres que programemos la lógica de guardado masivo?")
            else:
                st.warning("⚠️ No puedes cargar alumnos si no existe al menos un colegio registrado en la Tab 1.")
        
        except Exception as e:
            st.error(f"Error al conectar con la tabla de colegios: {e}")

    # --- TABS VACÍAS (POR AHORA) ---
    with tab2:
        st.info("Módulo de carga de Docentes en desarrollo.")
    with tab3:
        st.info("Módulo de carga de Tutores en desarrollo.")
