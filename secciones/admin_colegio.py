import streamlit as st
import pandas as pd
from sqlalchemy import text

# Inicializamos la conexión con el conector de SQL de Streamlit
conn = st.connection("postgresql", type="sql")

def render():
    st.markdown('<h2 style="color: #0f2240;">🛡️ Administración de Instituciones</h2>', unsafe_allow_html=True)
    st.markdown("Panel global de Animar para la gestión de la estructura educativa.")
    
    # Tabs para organizar la navegación
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
                            s.execute(
                                text("INSERT INTO colegios (nombre, cuit, plan) VALUES (:nom, :cuit, :plan)"),
                                {"nom": nombre_col, "cuit": cuit_col, "plan": plan_tipo}
                            )
                            s.commit()
                        st.success(f"✅ Colegio '{nombre_col}' guardado exitosamente.")
                        st.rerun() 
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                else:
                    st.warning("Completa los campos obligatorios.")

        # --- VISUALIZACIÓN DE COLEGIOS (Usando Session para evitar error de Hash) ---
        st.markdown("---")
        st.subheader("Colegios Registrados")
        try:
            with conn.session as s:
                # Ejecutamos la consulta directamente sobre la sesión
                result = s.execute(text("SELECT nombre, cuit, plan, fecha_alta FROM colegios ORDER BY fecha_alta DESC"))
                # Construimos el DataFrame con los resultados y las columnas
                df_colegios = pd.DataFrame(result.fetchall(), columns=result.keys())
            
            if not df_colegios.empty:
                # Limpiamos la visualización de la fecha
                df_colegios['fecha_alta'] = pd.to_datetime(df_colegios['fecha_alta']).dt.date
                st.dataframe(df_colegios, use_container_width=True)
            else:
                st.info("No hay colegios en la base de datos.")
        except Exception as e:
            st.error(f"Error al cargar la lista: {e}")

    # --- TAB 4: CARGA DE ALUMNOS (Lógica de Inserción Masiva) ---
    with tab4:
        st.subheader("Gestión de Alumnos")
        try:
            with conn.session as s:
                res = s.execute(text("SELECT id, nombre FROM colegios"))
                df_lista_col = pd.DataFrame(res.fetchall(), columns=res.keys())
            
            if not df_lista_col.empty:
                colegio_sel = st.selectbox(
                    "Seleccionar Colegio para la carga", 
                    options=df_lista_col['id'].tolist(), 
                    format_func=lambda x: df_lista_col[df_lista_col['id']==x]['nombre'].iloc[0],
                    key="sel_col_alu"
                )
                
                archivo = st.file_uploader("Subir Excel de alumnos (.xlsx)", type=["xlsx"])
                
                if archivo:
                    df_alumnos = pd.read_excel(archivo)
                    st.write("📋 Vista previa del archivo:")
                    st.dataframe(df_alumnos.head(), use_container_width=True)
                    
                    # Verificamos que el Excel tenga las columnas necesarias
                    columnas_req = ['Nombre', 'Apellido', 'DNI', 'Grado']
                    if all(col in df_alumnos.columns for col in columnas_req):
                        
                        if st.button("🚀 Confirmar Carga Masiva", type="primary"):
                            exitos = 0
                            errores = 0
                            
                            with conn.session as s:
                                for _, row in df_alumnos.iterrows():
                                    try:
                                        s.execute(
                                            text("""INSERT INTO alumnos (colegio_id, nombre, apellido, dni, grado) 
                                                 VALUES (:col, :nom, :ape, :dni, :gra)"""),
                                            {
                                                "col": colegio_sel,
                                                "nom": str(row['Nombre']),
                                                "ape": str(row['Apellido']),
                                                "dni": str(row['DNI']),
                                                "gra": str(row['Grado'])
                                            }
                                        )
                                        exitos += 1
                                    except Exception as e:
                                        errores += 1
                                s.commit()
                            
                            st.success(f"✅ Proceso finalizado. Alumnos cargados: {exitos}")
                            if errores > 0:
                                st.error(f"❌ No se pudieron cargar {errores} alumnos (posible DNI duplicado).")
                    else:
                        st.error(f"El Excel debe contener las columnas: {', '.join(columnas_req)}")
            else:
                st.warning("Primero debes registrar un colegio.")
        except Exception as e:
            st.error(f"Error: {e}")

    # --- TABS EN DESARROLLO ---
    with tab2:
        st.info("Próximamente: Carga y asignación de Docentes.")
    with tab3:
        st.info("Próximamente: Gestión de Tutores y vinculación familiar.")
