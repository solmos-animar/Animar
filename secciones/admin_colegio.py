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


                # --- FORMULARIO CARGA INDIVIDUAL ---
                st.markdown("---")
 
                with st.expander("➕ Agregar docente manualmente", expanded=False):
                    st.markdown("""
                        <div style="
                            background: linear-gradient(135deg, #f0f4ff 0%, #e8f4f0 100%);
                            border-left: 4px solid #1a56a0;
                            border-radius: 0 12px 12px 0;
                            padding: 14px 18px 6px;
                            margin-bottom: 18px;
                        ">
                            <span style="font-size:13px; color:#0f2240; font-weight:600;">
                                📋 Carga individual de docente
                            </span><br>
                            <span style="font-size:12px; color:#5c5852;">
                                Completá todos los campos para agregar un docente al colegio seleccionado.
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
 
                    with st.form("form_docente_individual", clear_on_submit=True):
 
                        col_a, col_b = st.columns([1, 2])
                        with col_a:
                            dni_ind = st.text_input(
                                "DNI *",
                                placeholder="Ej: 28456789",
                                help="Sin puntos ni espacios."
                            )
                        with col_b:
                            st.empty()  # espacio visual intencional
 
                        col_c, col_d = st.columns(2)
                        with col_c:
                            apellido_ind = st.text_input(
                                "Apellido *",
                                placeholder="Ej: García"
                            )
                        with col_d:
                            nombre_ind = st.text_input(
                                "Nombre *",
                                placeholder="Ej: Lucía"
                            )
 
                        col_e, col_f = st.columns(2)
                        with col_e:
                            grado_ind = st.selectbox(
                                "Grado *",
                                options=["1°", "2°", "3°", "4°", "5°", "6°", "7°"],
                                index=0
                            )
                        with col_f:
                            division_ind = st.selectbox(
                                "División *",
                                options=["A", "B", "C", "D", "E"],
                                index=0
                            )
 
                        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
 
                        submitted_ind = st.form_submit_button(
                            "✅ Agregar Docente",
                            type="primary",
                            use_container_width=True
                        )
 
                        if submitted_ind:
                            if dni_ind and apellido_ind and nombre_ind:
                                grados_y_div_ind = f"{grado_ind} {division_ind}"
                                try:
                                    with conn.session as s:
                                        s.execute(text("""
                                            INSERT INTO docentes (colegio_id, dni, apellido, nombre, grados_divisiones)
                                            VALUES (:cid, :dni, :ape, :nom, :gd)
                                            ON CONFLICT (dni) DO UPDATE SET
                                                apellido = EXCLUDED.apellido,
                                                nombre = EXCLUDED.nombre,
                                                grados_divisiones = EXCLUDED.grados_divisiones
                                        """), {
                                            "cid": col_destino,
                                            "dni": dni_ind.strip(),
                                            "ape": apellido_ind.strip().capitalize(),
                                            "nom": nombre_ind.strip().capitalize(),
                                            "gd": grados_y_div_ind
                                        })
                                        s.commit()
                                    st.success(
                                        f"✅ Docente **{apellido_ind.capitalize()}, {nombre_ind.capitalize()}** "
                                        f"agregado a **{nombre_institucion}** ({grados_y_div_ind})."
                                    )
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error al guardar: {e}")
                            else:
                                st.warning("⚠️ Completá todos los campos obligatorios antes de guardar.")
                
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

    # --- TAB 4: ALUMNOS ---
    with tab4:
        st.markdown('<h3 style="color:#0f2240;">🎒 Gestión de Alumnos</h3>', unsafe_allow_html=True)

        try:
            with conn.session as s:
                res_col_al = s.execute(text("SELECT id, nombre FROM colegios"))
                df_col_al = pd.DataFrame(res_col_al.fetchall(), columns=res_col_al.keys())

            if df_col_al.empty:
                st.warning("No hay colegios creados. Primero registrá una institución.")
                st.stop()

            colegio_al = st.selectbox(
                "Seleccionar Colegio",
                options=df_col_al['id'].tolist(),
                format_func=lambda x: df_col_al[df_col_al['id'] == x]['nombre'].iloc[0],
                key="sel_colegio_alumnos"
            )
            nombre_colegio_al = df_col_al[df_col_al['id'] == colegio_al]['nombre'].iloc[0]

            st.markdown("---")

            # ================================================================
            # BLOQUE 1 — CARGA MASIVA POR EXCEL
            # ================================================================
            st.subheader("📤 Carga masiva por Excel")

            with st.expander("Ver formato esperado del archivo", expanded=False):
                st.markdown("""
                    <div style="background:#f0f4ff; border-radius:10px; padding:14px 18px; font-size:13px; color:#0f2240;">
                        El archivo Excel debe tener <strong>exactamente estas columnas</strong> (los nombres no distinguen mayúsculas):
                    </div>
                """, unsafe_allow_html=True)
                st.dataframe(
                    pd.DataFrame([
                        {"DNI": "28456789", "Apellido": "García", "Nombre": "Lucía",
                         "Grado": "4°", "División": "B", "Fecha_nacimiento": "2012-05-14"},
                        {"DNI": "31234567", "Apellido": "López", "Nombre": "Mateo",
                         "Grado": "4°", "División": "B", "Fecha_nacimiento": "2011-11-03"},
                    ]),
                    use_container_width=True, hide_index=True
                )
                st.caption("La columna Fecha_nacimiento puede ir en formato YYYY-MM-DD o DD/MM/YYYY.")

            archivo_al = st.file_uploader(
                "Subir archivo Excel de alumnos",
                type=["xlsx"],
                key="uploader_alumnos"
            )

            if archivo_al:
                df_al_raw = pd.read_excel(archivo_al)
                df_al_raw.columns = [c.strip().capitalize() for c in df_al_raw.columns]
                columnas_esp = ['Dni', 'Apellido', 'Nombre', 'Grado', 'División', 'Fecha_nacimiento']
                # Permitir también "Fecha nacimiento" con espacio
                df_al_raw.columns = [c.replace(" ", "_") for c in df_al_raw.columns]

                if all(c in df_al_raw.columns for c in columnas_esp):
                    df_al_raw['Grados_y_div'] = (
                        df_al_raw['Grado'].astype(str) + " " + df_al_raw['División'].astype(str)
                    )
                    # Normalizar fecha
                    df_al_raw['Fecha_nacimiento'] = pd.to_datetime(
                        df_al_raw['Fecha_nacimiento'], dayfirst=True, errors='coerce'
                    ).dt.date

                    fechas_invalidas = df_al_raw['Fecha_nacimiento'].isna().sum()

                    st.markdown("**📋 Vista previa:**")
                    st.dataframe(
                        df_al_raw[['Dni', 'Apellido', 'Nombre', 'Grados_y_div', 'Fecha_nacimiento']].head(10),
                        use_container_width=True, hide_index=True
                    )

                    col_info1, col_info2, col_info3 = st.columns(3)
                    col_info1.metric("Total de filas", len(df_al_raw))
                    col_info2.metric("Colegio destino", nombre_colegio_al)
                    col_info3.metric(
                        "Fechas con error",
                        fechas_invalidas,
                        delta=None if fechas_invalidas == 0 else f"{fechas_invalidas} se guardarán como nulas",
                        delta_color="off" if fechas_invalidas == 0 else "inverse"
                    )

                    st.warning(
                        f"⚠️ Estás por cargar **{len(df_al_raw)} alumnos** al colegio: **{nombre_colegio_al}**. "
                        "Si un DNI ya existe, se actualizarán sus datos."
                    )

                    if st.button("🚀 Confirmar y Guardar alumnos", type="primary", use_container_width=True):
                        exitos, errores = 0, 0
                        with conn.session as s:
                            for _, row in df_al_raw.iterrows():
                                try:
                                    s.execute(text("""
                                        INSERT INTO alumnos
                                            (colegio_id, dni, apellido, nombre, grados_divisiones, fecha_nacimiento)
                                        VALUES
                                            (:cid, :dni, :ape, :nom, :gd, :fn)
                                        ON CONFLICT (dni) DO UPDATE SET
                                            apellido          = EXCLUDED.apellido,
                                            nombre            = EXCLUDED.nombre,
                                            grados_divisiones = EXCLUDED.grados_divisiones,
                                            fecha_nacimiento  = EXCLUDED.fecha_nacimiento
                                    """), {
                                        "cid": colegio_al,
                                        "dni": str(row['Dni']).strip(),
                                        "ape": str(row['Apellido']).strip().capitalize(),
                                        "nom": str(row['Nombre']).strip().capitalize(),
                                        "gd":  str(row['Grados_y_div']),
                                        "fn":  row['Fecha_nacimiento'] if pd.notna(row['Fecha_nacimiento']) else None,
                                    })
                                    exitos += 1
                                except Exception as e:
                                    errores += 1
                                    st.error(f"Error en DNI {row['Dni']}: {e}")
                            s.commit()

                        if exitos:
                            st.success(f"✅ Se procesaron **{exitos} alumnos** correctamente en {nombre_colegio_al}.")
                        if errores:
                            st.error(f"❌ {errores} filas tuvieron errores y no fueron guardadas.")
                        st.rerun()

                else:
                    faltantes = [c for c in columnas_esp if c not in df_al_raw.columns]
                    st.error(f"El Excel no tiene el formato correcto.")
                    st.info(f"Columnas detectadas: `{list(df_al_raw.columns)}`")
                    st.warning(f"Columnas faltantes: `{faltantes}`")

            # ================================================================
            # BLOQUE 2 — FORMULARIO INDIVIDUAL
            # ================================================================
            st.markdown("---")

            with st.expander("➕ Agregar alumno manualmente", expanded=False):
                st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, #f0f4ff 0%, #fef9f0 100%);
                        border-left: 4px solid #d4580a;
                        border-radius: 0 12px 12px 0;
                        padding: 14px 18px 6px;
                        margin-bottom: 18px;
                    ">
                        <span style="font-size:13px; color:#0f2240; font-weight:600;">
                            📋 Carga individual de alumno
                        </span><br>
                        <span style="font-size:12px; color:#5c5852;">
                            Completá todos los campos para agregar un alumno a <strong>{}</strong>.
                        </span>
                    </div>
                """.format(nombre_colegio_al), unsafe_allow_html=True)

                with st.form("form_alumno_individual", clear_on_submit=True):

                    # Fila 1: DNI (ancho reducido) + espacio
                    col_dni, col_esp = st.columns([1, 2])
                    dni_al = col_dni.text_input(
                        "DNI *",
                        placeholder="Ej: 45123456",
                        help="Sin puntos ni espacios."
                    )

                    # Fila 2: Apellido + Nombre
                    col_ape, col_nom = st.columns(2)
                    apellido_al = col_ape.text_input("Apellido *", placeholder="Ej: Ramírez")
                    nombre_al   = col_nom.text_input("Nombre *",   placeholder="Ej: Valentina")

                    # Fila 3: Grado + División + Fecha de nacimiento
                    col_gr, col_div, col_fn = st.columns([1, 1, 2])
                    grado_al   = col_gr.selectbox(
                        "Grado *",
                        ["1°", "2°", "3°", "4°", "5°", "6°", "7°"]
                    )
                    division_al = col_div.selectbox(
                        "División *",
                        ["A", "B", "C", "D", "E"]
                    )
                    fecha_al = col_fn.date_input(
                        "Fecha de nacimiento *",
                        value=None,
                        min_value=pd.Timestamp("2000-01-01").date(),
                        max_value=pd.Timestamp("today").date(),
                        format="DD/MM/YYYY",
                        help="Seleccioná la fecha de nacimiento del alumno."
                    )

                    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

                    submitted_al = st.form_submit_button(
                        "✅ Agregar Alumno",
                        type="primary",
                        use_container_width=True
                    )

                    if submitted_al:
                        if dni_al and apellido_al and nombre_al and fecha_al:
                            gd_al = f"{grado_al} {division_al}"
                            try:
                                with conn.session as s:
                                    s.execute(text("""
                                        INSERT INTO alumnos
                                            (colegio_id, dni, apellido, nombre, grados_divisiones, fecha_nacimiento)
                                        VALUES
                                            (:cid, :dni, :ape, :nom, :gd, :fn)
                                        ON CONFLICT (dni) DO UPDATE SET
                                            apellido          = EXCLUDED.apellido,
                                            nombre            = EXCLUDED.nombre,
                                            grados_divisiones = EXCLUDED.grados_divisiones,
                                            fecha_nacimiento  = EXCLUDED.fecha_nacimiento
                                    """), {
                                        "cid": colegio_al,
                                        "dni": dni_al.strip(),
                                        "ape": apellido_al.strip().capitalize(),
                                        "nom": nombre_al.strip().capitalize(),
                                        "gd":  gd_al,
                                        "fn":  fecha_al,
                                    })
                                    s.commit()
                                st.success(
                                    f"✅ **{apellido_al.capitalize()}, {nombre_al.capitalize()}** "
                                    f"agregado/a a **{nombre_colegio_al}** — {gd_al}."
                                )
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error al guardar: {e}")
                        else:
                            st.warning("⚠️ Completá todos los campos obligatorios antes de guardar.")

            # ================================================================
            # BLOQUE 3 — TABLA DE VISUALIZACIÓN Y EDICIÓN
            # ================================================================
            st.markdown("---")
            st.subheader(f"📊 Padrón: {nombre_colegio_al}")

            # Filtros rápidos por grado/división
            with conn.session as s:
                res_al = s.execute(text("""
                    SELECT id, dni, apellido, nombre, grados_divisiones, fecha_nacimiento, activo
                    FROM alumnos
                    WHERE colegio_id = :cid
                    ORDER BY grados_divisiones, apellido
                """), {"cid": colegio_al})
                df_alumnos = pd.DataFrame(res_al.fetchall(), columns=res_al.keys())

            if not df_alumnos.empty:
                # Filtro por grado/división
                opciones_grado = ["Todos"] + sorted(df_alumnos['grados_divisiones'].dropna().unique().tolist())
                col_f1, col_f2 = st.columns([2, 4])
                filtro_grado = col_f1.selectbox("Filtrar por grado/división", opciones_grado, key="filtro_grado_al")
                col_f2.markdown(
                    f"<div style='padding-top:28px; font-size:13px; color:#5c5852;'>"
                    f"Total: <strong>{len(df_alumnos)}</strong> alumnos registrados</div>",
                    unsafe_allow_html=True
                )

                df_vista = df_alumnos if filtro_grado == "Todos" else df_alumnos[df_alumnos['grados_divisiones'] == filtro_grado]

                df_editado_al = st.data_editor(
                    df_vista,
                    column_config={
                        "id":                None,
                        "activo":            st.column_config.CheckboxColumn("Activo"),
                        "fecha_nacimiento":  st.column_config.DateColumn("Fecha Nac.", format="DD/MM/YYYY"),
                        "dni":               st.column_config.TextColumn("DNI", disabled=True),
                        "apellido":          st.column_config.TextColumn("Apellido"),
                        "nombre":            st.column_config.TextColumn("Nombre"),
                        "grados_divisiones": st.column_config.TextColumn("Grado / Div."),
                    },
                    use_container_width=True,
                    hide_index=True,
                    key="edit_al_table"
                )

                if st.button("💾 Guardar cambios en el padrón", use_container_width=True):
                    with conn.session as s:
                        for _, r in df_editado_al.iterrows():
                            s.execute(text("""
                                UPDATE alumnos
                                SET apellido=:a, nombre=:n, grados_divisiones=:g,
                                    fecha_nacimiento=:fn, activo=:ac
                                WHERE id=:id
                            """), {
                                "a":  r['apellido'],
                                "n":  r['nombre'],
                                "g":  r['grados_divisiones'],
                                "fn": r['fecha_nacimiento'],
                                "ac": r['activo'],
                                "id": r['id']
                            })
                        s.commit()
                    st.success("✅ Padrón actualizado correctamente.")
                    st.rerun()

            else:
                st.info(f"No hay alumnos cargados para {nombre_colegio_al} todavía.")

        except Exception as e:
            st.error(f"Error en módulo de alumnos: {e}")
