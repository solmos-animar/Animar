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
    # --- TAB 2: DOCENTES (CORREGIDA) ---
    with tab2:
        st.subheader("Gestión de Personal Docente")
        
        try:
            with conn.session as s:
                res_col = s.execute(text("SELECT id, nombre FROM colegios"))
                df_col_list = pd.DataFrame(res_col.fetchall(), columns=res_col.keys())

            if not df_col_list.empty:
                col_destino = st.selectbox("Seleccionar Colegio para Docentes", 
                                          options=df_col_list['id'].tolist(), 
                                          format_func=lambda x: df_col_list[df_col_list['id']==x]['nombre'].iloc[0])
                
                nombre_institucion = df_col_list[df_col_list['id']==col_destino]['nombre'].iloc[0]

                # Subida de archivo
                archivo_doc = st.file_uploader("Subir Excel de Docentes", type=["xlsx"])
                
                if archivo_doc:
                    df_doc_raw = pd.read_excel(archivo_doc)
                    
                    # Normalizamos nombres de columnas para evitar errores de mayúsculas/espacios
                    df_doc_raw.columns = [c.strip().capitalize() for c in df_doc_raw.columns]
                    columnas_esperadas = ['Dni', 'Apellido', 'Nombre', 'Grado', 'División']
                    
                    # Verificamos si están todas
                    if all(c in df_doc_raw.columns for c in columnas_esperadas):
                        # Creamos la columna combinada
                        df_doc_raw['Grados_y_div'] = df_doc_raw['Grado'].astype(str) + " " + df_doc_raw['División'].astype(str)
                        
                        st.write("📋 **Vista previa de los datos a importar:**")
                        st.dataframe(df_doc_raw[['Dni', 'Apellido', 'Nombre', 'Grados_y_div']].head(), use_container_width=True)

                        # EL BOTÓN DE GUARDADO DENTRO DE UN WARNING DE CONFIRMACIÓN
                        st.warning(f"⚠️ Estás por cargar estos docentes al colegio: **{nombre_institucion}**")
                        
                        if st.button("🚀 Confirmar y Guardar en Base de Datos", type="primary", use_container_width=True):
                            exitos = 0
                            with conn.session as s:
                                for _, row in df_doc_raw.iterrows():
                                    try:
                                        s.execute(text("""
                                            INSERT INTO docentes (colegio_id, dni, apellido, nombre, grados_divisiones)
                                            VALUES (:cid, :dni, :ape, :nom, :gd)
                                            ON CONFLICT (dni) DO UPDATE SET 
                                            grados_divisiones = EXCLUDED.grados_divisiones,
                                            apellido = EXCLUDED.apellido,
                                            nombre = EXCLUDED.nombre
                                        """), {
                                            "cid": col_destino, 
                                            "dni": str(row['Dni']), 
                                            "ape": str(row['Apellido']), 
                                            "nom": str(row['Nombre']), 
                                            "gd": str(row['Grados_y_div'])
                                        })
                                        exitos += 1
                                    except Exception as e:
                                        st.error(f"Error en DNI {row['Dni']}: {e}")
                                s.commit()
                            st.success(f"✅ ¡Hecho! Se procesaron {exitos} docentes en {nombre_institucion}.")
                            st.rerun()
                    else:
                        st.error(f"El Excel no tiene el formato correcto. Columnas detectadas: {list(df_doc_raw.columns)}")
                        st.info(f"Se esperan exactamente: {columnas_esperadas}")

                # --- TABLA DE EDICIÓN ---
                st.markdown("---")
                with conn.session as s:
                    res_d = s.execute(text("SELECT id, dni, apellido, nombre, grados_divisiones, activo FROM docentes WHERE colegio_id = :cid"), {"cid": col_destino})
                    df_docentes = pd.DataFrame(res_d.fetchall(), columns=res_d.keys())

                if not df_docentes.empty:
                    st.subheader(f"Listado de Docentes: {nombre_institucion}")
                    # Editor dinámico
                    df_editado = st.data_editor(
                        df_docentes,
                        column_config={"activo": st.column_config.CheckboxColumn("Activo"), "id": None},
                        disabled=["dni"],
                        use_container_width=True,
                        key="edit_doc_table"
                    )
                    
                    if st.button("💾 Guardar cambios realizados en la tabla"):
                        with conn.session as s:
                            for _, r in df_editado.iterrows():
                                s.execute(text("""
                                    UPDATE docentes SET apellido=:a, nombre=:n, grados_divisiones=:g, activo=:ac WHERE id=:id
                                """), {"a": r['apellido'], "n": r['nombre'], "g": r['grados_divisiones'], "ac": r['activo'], "id": r['id']})
                            s.commit()
                        st.success("Cambios actualizados.")
                        st.rerun()
            else:
                st.warning("No hay colegios creados.")
        except Exception as e: st.error(f"Error: {e}")

    # --- TAB 4: ALUMNOS (Tu código anterior...) ---
    with tab4:
        st.info("Módulo de alumnos operativo.")
