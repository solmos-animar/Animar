import streamlit as st
import pandas as pd
from sqlalchemy import text

conn = st.connection("postgresql", type="sql")

def render():
    st.markdown('<h2 style="color: #0f2240;">🛡️ Administración de Instituciones</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Nuevo Colegio", "👨‍🏫 Docentes", "👪 Tutores", "🎒 Alumnos"])

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
    # --- TAB 2: DOCENTES (NUEVA LÓGICA) ---
    with tab2:
        st.subheader("Gestión de Personal Docente")
        
        try:
            with conn.session as s:
                res = s.execute(text("SELECT id, nombre FROM colegios"))
                df_col = pd.DataFrame(res.fetchall(), columns=res.keys())

            if not df_col.empty:
                col_destino = st.selectbox("Seleccionar Colegio para Docentes", 
                                          options=df_col['id'].tolist(), 
                                          format_func=lambda x: df_col[df_col['id']==x]['nombre'].iloc[0],
                                          key="sel_col_doc")
                nombre_colegio = df_col[df_col['id']==col_destino]['nombre'].iloc[0]

                # --- CARGA MASIVA ---
                archivo_doc = st.file_uploader("Subir Excel de Docentes (DNI, Apellido, Nombre, Grado, División)", type=["xlsx"])
                
                if archivo_doc:
                    df_doc_raw = pd.read_excel(archivo_doc)
                    # Unificamos Grado y División en una sola columna para la base de datos
                    if all(c in df_doc_raw.columns for c in ['DNI', 'Apellido', 'Nombre', 'Grado', 'División']):
                        df_doc_raw['Grados_y_Div'] = df_doc_raw['Grado'].astype(str) + " " + df_doc_raw['División'].astype(str)
                        st.write("📋 Vista previa de carga:")
                        st.dataframe(df_doc_raw[['DNI', 'Apellido', 'Nombre', 'Grados_y_Div']], use_container_width=True)

                        # RECUADRO DE CONFIRMACIÓN
                        st.warning(f"⚠️ **CONFIRMACIÓN**: Estás por cargar {len(df_doc_raw)} docentes al **{nombre_colegio}**. ¿Confirmas la operación?")
                        col_conf1, col_conf2 = st.columns(2)
                        
                        if col_conf1.button("✅ Sí, proceder con la carga", use_container_width=True):
                            exitos = 0
                            with conn.session as s:
                                for _, row in df_doc_raw.iterrows():
                                    try:
                                        s.execute(text("""
                                            INSERT INTO docentes (colegio_id, dni, apellido, nombre, grados_divisiones)
                                            VALUES (:cid, :dni, :ape, :nom, :gd)
                                            ON CONFLICT (dni) DO UPDATE SET grados_divisiones = EXCLUDED.grados_divisiones
                                        """), {"cid": col_destino, "dni": str(row['DNI']), "ape": row['Apellido'], "nom": row['Nombre'], "gd": row['Grados_y_Div']})
                                        exitos += 1
                                    except: pass
                                s.commit()
                            st.success(f"Se cargaron/actualizaron {exitos} docentes.")
                            st.rerun()

                # --- EDICIÓN Y LISTADO ---
                st.markdown("---")
                st.subheader(f"Docentes de {nombre_colegio}")
                with conn.session as s:
                    res_d = s.execute(text("SELECT id, dni, apellido, nombre, grados_divisiones, activo FROM docentes WHERE colegio_id = :cid"), {"cid": col_destino})
                    df_docentes = pd.DataFrame(res_d.fetchall(), columns=res_d.keys())

                if not df_docentes.empty:
                    st.write("💡 Puedes editar nombres, grados o el estado directamente en la tabla.")
                    # TABLA EDITABLE
                    edited_df = st.data_editor(
                        df_docentes, 
                        column_config={
                            "activo": st.column_config.CheckboxColumn("Habilitado"),
                            "grados_divisiones": "Grados/Div (ej: 1A, 2B)",
                            "id": None # Ocultamos el ID
                        },
                        disabled=["dni"], # El DNI no se debería editar por seguridad
                        use_container_width=True,
                        key="editor_docentes"
                    )

                    if st.button("💾 Guardar cambios en la tabla"):
                        # Aquí detectamos cambios y actualizamos en lote
                        with conn.session as s:
                            for _, row in edited_df.iterrows():
                                s.execute(text("""
                                    UPDATE docentes SET 
                                    apellido = :ape, nombre = :nom, grados_divisiones = :gd, activo = :act
                                    WHERE id = :id
                                """), {"ape": row['apellido'], "nom": row['nombre'], "gd": row['grados_divisiones'], "act": row['activo'], "id": row['id']})
                            s.commit()
                        st.success("Cambios guardados correctamente.")
                else:
                    st.info("No hay docentes cargados para este colegio.")

        except Exception as e:
            st.error(f"Error en módulo docentes: {e}")

    # --- TAB 4: ALUMNOS (Tu código anterior...) ---
    with tab4:
        st.info("Módulo de alumnos operativo.")
