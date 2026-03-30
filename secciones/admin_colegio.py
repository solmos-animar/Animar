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

   # --- TAB 4: ALUMNOS + TUTORES ---
    with tab4:
        st.markdown('<h3 style="color:#0f2240;">🎒 Gestión de Alumnos y Tutores</h3>', unsafe_allow_html=True)

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
                    <div style="background:#f0f4ff; border-radius:10px; padding:14px 18px; font-size:13px; color:#0f2240; margin-bottom:10px;">
                        El archivo debe tener los datos del alumno primero, y luego los tutores con prefijo
                        <code>Tutor1_</code>, <code>Tutor2_</code>, <code>Tutor3_</code>.<br>
                        <strong>Solo Tutor1 es obligatorio.</strong> Los campos de Tutor2 y Tutor3 pueden dejarse vacíos.
                    </div>
                """, unsafe_allow_html=True)

                ejemplo = pd.DataFrame([{
                    "Dni": "45123456", "Apellido": "García", "Nombre": "Lucía",
                    "Grado": "4°", "División": "B", "Fecha_nacimiento": "2012-05-14",
                    "Tutor1_relacion": "Madre", "Tutor1_apellido": "García",
                    "Tutor1_nombre": "Ana", "Tutor1_dni": "28456789",
                    "Tutor1_telefono": "1156781234", "Tutor1_email": "ana@email.com",
                    "Tutor1_principal": "SI",
                    "Tutor2_relacion": "Padre", "Tutor2_apellido": "López",
                    "Tutor2_nombre": "Carlos", "Tutor2_dni": "27123456",
                    "Tutor2_telefono": "1143219876", "Tutor2_email": "carlos@email.com",
                    "Tutor2_principal": "NO",
                }])
                st.dataframe(ejemplo, use_container_width=True, hide_index=True)
                st.caption("Tutor1_principal y Tutor2_principal: escribir SI o NO. Los campos de Tutor3 siguen el mismo patrón.")

            archivo_al = st.file_uploader(
                "Subir archivo Excel de alumnos con tutores",
                type=["xlsx"],
                key="uploader_alumnos"
            )

            if archivo_al:
                df_al_raw = pd.read_excel(archivo_al)
                # Normalizar columnas
                df_al_raw.columns = [c.strip().replace(" ", "_") for c in df_al_raw.columns]
                # Capitalizar solo la primera letra de cada segmento para manejar Tutor1_apellido, etc.
                def normalizar_col(c):
                    partes = c.split("_")
                    return "_".join([p.capitalize() for p in partes])
                df_al_raw.columns = [normalizar_col(c) for c in df_al_raw.columns]

                cols_alumno = ['Dni', 'Apellido', 'Nombre', 'Grado', 'División', 'Fecha_nacimiento']
                cols_tutor1 = ['Tutor1_relacion', 'Tutor1_apellido', 'Tutor1_nombre',
                               'Tutor1_dni', 'Tutor1_telefono', 'Tutor1_email', 'Tutor1_principal']

                faltantes_al = [c for c in cols_alumno if c not in df_al_raw.columns]
                faltantes_t1 = [c for c in cols_tutor1 if c not in df_al_raw.columns]

                if faltantes_al or faltantes_t1:
                    st.error("El Excel no tiene el formato correcto.")
                    if faltantes_al:
                        st.warning(f"Columnas de alumno faltantes: `{faltantes_al}`")
                    if faltantes_t1:
                        st.warning(f"Columnas de Tutor1 faltantes: `{faltantes_t1}`")
                else:
                    df_al_raw['Grados_y_div'] = (
                        df_al_raw['Grado'].astype(str) + " " + df_al_raw['División'].astype(str)
                    )
                    df_al_raw['Fecha_nacimiento'] = pd.to_datetime(
                        df_al_raw['Fecha_nacimiento'], dayfirst=True, errors='coerce'
                    ).dt.date

                    fechas_invalidas = df_al_raw['Fecha_nacimiento'].isna().sum()
                    sin_tutor = df_al_raw['Tutor1_dni'].isna().sum()

                    st.markdown("**📋 Vista previa (primeras 5 filas):**")
                    st.dataframe(
                        df_al_raw[['Dni', 'Apellido', 'Nombre', 'Grados_y_div',
                                   'Fecha_nacimiento', 'Tutor1_nombre', 'Tutor1_apellido']].head(5),
                        use_container_width=True, hide_index=True
                    )

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Total alumnos", len(df_al_raw))
                    c2.metric("Colegio destino", nombre_colegio_al)
                    c3.metric("Fechas con error", fechas_invalidas,
                              delta=None if fechas_invalidas == 0 else "se guardan como nulas",
                              delta_color="off" if fechas_invalidas == 0 else "inverse")
                    c4.metric("Sin Tutor1", sin_tutor,
                              delta=None if sin_tutor == 0 else "filas serán rechazadas",
                              delta_color="off" if sin_tutor == 0 else "inverse")

                    if sin_tutor > 0:
                        st.error(f"❌ {sin_tutor} filas no tienen Tutor1 y serán omitidas. Corregí el Excel antes de continuar.")
                    else:
                        st.warning(
                            f"⚠️ Estás por cargar **{len(df_al_raw)} alumnos** con sus tutores "
                            f"al colegio **{nombre_colegio_al}**. Si un DNI ya existe se actualizarán sus datos."
                        )

                        if st.button("🚀 Confirmar y Guardar", type="primary", use_container_width=True):
                            exitos, errores = 0, 0
                            PREFIJOS_TUTOR = ["Tutor1", "Tutor2", "Tutor3"]

                            with conn.session as s:
                                for _, row in df_al_raw.iterrows():
                                    try:
                                        # Insertar alumno
                                        res_ins = s.execute(text("""
                                            INSERT INTO alumnos
                                                (colegio_id, dni, apellido, nombre, grados_divisiones, fecha_nacimiento)
                                            VALUES (:cid, :dni, :ape, :nom, :gd, :fn)
                                            ON CONFLICT (dni) DO UPDATE SET
                                                apellido=EXCLUDED.apellido, nombre=EXCLUDED.nombre,
                                                grados_divisiones=EXCLUDED.grados_divisiones,
                                                fecha_nacimiento=EXCLUDED.fecha_nacimiento
                                            RETURNING id
                                        """), {
                                            "cid": colegio_al,
                                            "dni": str(row['Dni']).strip(),
                                            "ape": str(row['Apellido']).strip().capitalize(),
                                            "nom": str(row['Nombre']).strip().capitalize(),
                                            "gd":  str(row['Grados_y_div']),
                                            "fn":  row['Fecha_nacimiento'] if pd.notna(row.get('Fecha_nacimiento')) else None,
                                        })
                                        alumno_id = res_ins.fetchone()[0]

                                        # Borrar tutores previos del alumno para re-insertar limpios
                                        s.execute(text("DELETE FROM tutores WHERE alumno_id = :aid"), {"aid": alumno_id})

                                        # Insertar tutores
                                        for pref in PREFIJOS_TUTOR:
                                            col_dni_t = f"{pref}_dni"
                                            if col_dni_t not in df_al_raw.columns:
                                                continue
                                            dni_t = row.get(col_dni_t)
                                            if pd.isna(dni_t) or str(dni_t).strip() == "":
                                                continue
                                            principal_raw = str(row.get(f"{pref}_principal", "NO")).strip().upper()
                                            s.execute(text("""
                                                INSERT INTO tutores
                                                    (alumno_id, relacion, apellido, nombre, dni, telefono, email, es_principal)
                                                VALUES
                                                    (:aid, :rel, :ape, :nom, :dni, :tel, :email, :esp)
                                            """), {
                                                "aid":   alumno_id,
                                                "rel":   str(row.get(f"{pref}_relacion", "")).strip().capitalize(),
                                                "ape":   str(row.get(f"{pref}_apellido", "")).strip().capitalize(),
                                                "nom":   str(row.get(f"{pref}_nombre", "")).strip().capitalize(),
                                                "dni":   str(dni_t).strip(),
                                                "tel":   str(row.get(f"{pref}_telefono", "")).strip(),
                                                "email": str(row.get(f"{pref}_email", "")).strip().lower(),
                                                "esp":   principal_raw == "SI",
                                            })
                                        exitos += 1
                                    except Exception as e:
                                        errores += 1
                                        st.error(f"Error en DNI {row.get('Dni', '?')}: {e}")
                                s.commit()

                            if exitos:
                                st.success(f"✅ Se procesaron **{exitos} alumnos** con sus tutores en {nombre_colegio_al}.")
                            if errores:
                                st.error(f"❌ {errores} filas tuvieron errores.")
                            st.rerun()

            # ================================================================
            # BLOQUE 2 — FORMULARIO INDIVIDUAL CON TUTORES
            # ================================================================
            st.markdown("---")

            with st.expander("➕ Agregar alumno manualmente", expanded=False):

                st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, #f0f4ff 0%, #fef9f0 100%);
                        border-left: 4px solid #d4580a;
                        border-radius: 0 12px 12px 0;
                        padding: 14px 18px 8px; margin-bottom: 20px;">
                        <span style="font-size:13px; color:#0f2240; font-weight:600;">📋 Datos del alumno</span><br>
                        <span style="font-size:12px; color:#5c5852;">
                            Completá los datos del alumno y al menos un tutor para poder guardar.
                        </span>
                    </div>
                """, unsafe_allow_html=True)

                # Usamos session_state para manejar la cantidad de tutores dinámica
                if "n_tutores" not in st.session_state:
                    st.session_state.n_tutores = 1

                with st.form("form_alumno_completo", clear_on_submit=True):

                    # ---- SECCIÓN ALUMNO ----
                    col_dni, _ = st.columns([1, 2])
                    dni_al = col_dni.text_input("DNI del alumno *", placeholder="Ej: 45123456", help="Sin puntos ni espacios.")

                    col_ape, col_nom = st.columns(2)
                    apellido_al = col_ape.text_input("Apellido *", placeholder="Ej: Ramírez")
                    nombre_al   = col_nom.text_input("Nombre *",   placeholder="Ej: Valentina")

                    col_gr, col_div, col_fn = st.columns([1, 1, 2])
                    grado_al    = col_gr.selectbox("Grado *",    ["1°","2°","3°","4°","5°","6°","7°"])
                    division_al = col_div.selectbox("División *", ["A","B","C","D","E"])
                    fecha_al    = col_fn.date_input(
                        "Fecha de nacimiento *", value=None,
                        min_value=pd.Timestamp("2000-01-01").date(),
                        max_value=pd.Timestamp("today").date(),
                        format="DD/MM/YYYY"
                    )

                    # ---- SECCIÓN TUTORES ----
                    st.markdown("""
                        <div style="
                            margin: 24px 0 14px;
                            padding: 12px 18px;
                            background: linear-gradient(135deg, #e8f4f0 0%, #f0f9f4 100%);
                            border-left: 4px solid #1d7a55;
                            border-radius: 0 10px 10px 0;">
                            <span style="font-size:13px; color:#0f2240; font-weight:600;">
                                👨‍👩‍👧 Tutores / Referentes del alumno
                            </span><br>
                            <span style="font-size:12px; color:#5c5852;">
                                Al menos un tutor es obligatorio. Podés cargar hasta 3.
                            </span>
                        </div>
                    """, unsafe_allow_html=True)

                    tutores_data = []
                    RELACIONES = ["Madre", "Padre", "Tutor/a legal", "Abuelo/a", "Otro"]

                    for i in range(st.session_state.n_tutores):
                        numero = i + 1
                        color_borde = ["#1d7a55", "#1a56a0", "#d4580a"][i]
                        label_default = ["Tutor 1 (principal)", "Tutor 2", "Tutor 3"][i]

                        st.markdown(f"""
                            <div style="
                                border: 1.5px solid {color_borde}22;
                                border-left: 4px solid {color_borde};
                                border-radius: 0 10px 10px 0;
                                padding: 14px 16px 6px;
                                margin-bottom: 14px;
                                background: white;">
                                <span style="font-size:12px; font-weight:700;
                                    text-transform:uppercase; letter-spacing:1px; color:{color_borde};">
                                    {label_default}
                                </span>
                            </div>
                        """, unsafe_allow_html=True)

                        t_col1, t_col2 = st.columns([1, 2])
                        t_relacion = t_col1.selectbox(
                            f"Relación {numero} *" if numero == 1 else f"Relación {numero}",
                            RELACIONES, key=f"t{i}_rel"
                        )
                        t_principal = t_col2.checkbox(
                            "Es el contacto principal",
                            value=(i == 0),
                            key=f"t{i}_principal"
                        )

                        t_c1, t_c2 = st.columns(2)
                        t_apellido = t_c1.text_input(
                            f"Apellido {'*' if numero==1 else ''}",
                            placeholder="Ej: García", key=f"t{i}_ape"
                        )
                        t_nombre = t_c2.text_input(
                            f"Nombre {'*' if numero==1 else ''}",
                            placeholder="Ej: Ana", key=f"t{i}_nom"
                        )

                        t_c3, t_c4 = st.columns(2)
                        t_dni = t_c3.text_input(
                            f"DNI {'*' if numero==1 else ''}",
                            placeholder="Ej: 28456789", key=f"t{i}_dni"
                        )
                        t_tel = t_c4.text_input(
                            "Teléfono", placeholder="Ej: 1156781234", key=f"t{i}_tel"
                        )

                        t_email = st.text_input(
                            "Email", placeholder="Ej: contacto@email.com", key=f"t{i}_email"
                        )

                        tutores_data.append({
                            "relacion":    t_relacion,
                            "apellido":    t_apellido,
                            "nombre":      t_nombre,
                            "dni":         t_dni,
                            "telefono":    t_tel,
                            "email":       t_email,
                            "es_principal": t_principal,
                        })

                    # Botones fuera del loop pero dentro del form
                    col_btn1, col_btn2 = st.columns([1, 3])
                    agregar = col_btn1.form_submit_button(
                        f"＋ Tutor {st.session_state.n_tutores + 1}",
                        disabled=st.session_state.n_tutores >= 3
                    )
                    guardar = col_btn2.form_submit_button(
                        "✅ Guardar Alumno con Tutores",
                        type="primary",
                        use_container_width=True
                    )

                    # Acción: agregar tutor
                    if agregar and st.session_state.n_tutores < 3:
                        st.session_state.n_tutores += 1
                        st.rerun()

                    # Acción: guardar
                    if guardar:
                        # Validaciones
                        t1 = tutores_data[0]
                        errores_val = []
                        if not dni_al.strip():         errores_val.append("DNI del alumno")
                        if not apellido_al.strip():    errores_val.append("Apellido del alumno")
                        if not nombre_al.strip():      errores_val.append("Nombre del alumno")
                        if not fecha_al:               errores_val.append("Fecha de nacimiento")
                        if not t1['apellido'].strip(): errores_val.append("Apellido del Tutor 1")
                        if not t1['nombre'].strip():   errores_val.append("Nombre del Tutor 1")
                        if not t1['dni'].strip():      errores_val.append("DNI del Tutor 1")

                        if errores_val:
                            st.warning(f"⚠️ Campos obligatorios faltantes: **{', '.join(errores_val)}**")
                        else:
                            try:
                                with conn.session as s:
                                    # Insertar alumno
                                    res_ins = s.execute(text("""
                                        INSERT INTO alumnos
                                            (colegio_id, dni, apellido, nombre, grados_divisiones, fecha_nacimiento)
                                        VALUES (:cid, :dni, :ape, :nom, :gd, :fn)
                                        ON CONFLICT (dni) DO UPDATE SET
                                            apellido=EXCLUDED.apellido, nombre=EXCLUDED.nombre,
                                            grados_divisiones=EXCLUDED.grados_divisiones,
                                            fecha_nacimiento=EXCLUDED.fecha_nacimiento
                                        RETURNING id
                                    """), {
                                        "cid": colegio_al,
                                        "dni": dni_al.strip(),
                                        "ape": apellido_al.strip().capitalize(),
                                        "nom": nombre_al.strip().capitalize(),
                                        "gd":  f"{grado_al} {division_al}",
                                        "fn":  fecha_al,
                                    })
                                    alumno_id = res_ins.fetchone()[0]

                                    # Borrar tutores previos y reinsertar
                                    s.execute(text("DELETE FROM tutores WHERE alumno_id = :aid"), {"aid": alumno_id})

                                    for t in tutores_data:
                                        if not t['dni'].strip():
                                            continue
                                        s.execute(text("""
                                            INSERT INTO tutores
                                                (alumno_id, relacion, apellido, nombre, dni,
                                                 telefono, email, es_principal)
                                            VALUES
                                                (:aid, :rel, :ape, :nom, :dni,
                                                 :tel, :email, :esp)
                                        """), {
                                            "aid":   alumno_id,
                                            "rel":   t['relacion'],
                                            "ape":   t['apellido'].strip().capitalize(),
                                            "nom":   t['nombre'].strip().capitalize(),
                                            "dni":   t['dni'].strip(),
                                            "tel":   t['telefono'].strip(),
                                            "email": t['email'].strip().lower(),
                                            "esp":   t['es_principal'],
                                        })
                                    s.commit()

                                st.success(
                                    f"✅ **{apellido_al.capitalize()}, {nombre_al.capitalize()}** "
                                    f"guardado/a en **{nombre_colegio_al}** — {grado_al} {division_al} "
                                    f"con {len([t for t in tutores_data if t['dni'].strip()])} tutor/es."
                                )
                                st.session_state.n_tutores = 1
                                st.rerun()

                            except Exception as e:
                                st.error(f"Error al guardar: {e}")

            # ================================================================
            # BLOQUE 3 — PADRÓN CON DETALLE DE TUTORES
            # ================================================================
            st.markdown("---")
            st.subheader(f"📊 Padrón: {nombre_colegio_al}")

            with conn.session as s:
                res_al = s.execute(text("""
                    SELECT
                        a.id, a.dni, a.apellido, a.nombre,
                        a.grados_divisiones, a.fecha_nacimiento, a.activo,
                        COUNT(t.id) AS cant_tutores,
                        STRING_AGG(
                            t.relacion || ': ' || t.apellido || ' ' || t.nombre ||
                            CASE WHEN t.es_principal THEN ' ★' ELSE '' END,
                            ' | ' ORDER BY t.es_principal DESC
                        ) AS tutores_resumen
                    FROM alumnos a
                    LEFT JOIN tutores t ON t.alumno_id = a.id
                    WHERE a.colegio_id = :cid
                    GROUP BY a.id, a.dni, a.apellido, a.nombre,
                             a.grados_divisiones, a.fecha_nacimiento, a.activo
                    ORDER BY a.grados_divisiones, a.apellido
                """), {"cid": colegio_al})
                df_alumnos = pd.DataFrame(res_al.fetchall(), columns=res_al.keys())

            if not df_alumnos.empty:
                opciones_grado = ["Todos"] + sorted(df_alumnos['grados_divisiones'].dropna().unique().tolist())
                col_f1, col_f2, col_f3 = st.columns([2, 2, 3])
                filtro_grado = col_f1.selectbox("Filtrar por grado", opciones_grado, key="filtro_grado_al")

                # Alerta de alumnos sin tutores
                sin_tutores = (df_alumnos['cant_tutores'] == 0).sum()
                if sin_tutores > 0:
                    col_f2.markdown(
                        f"<div style='padding-top:26px;'>"
                        f"<span style='background:#fde8d0; color:#6b3000; padding:4px 10px; "
                        f"border-radius:20px; font-size:12px; font-weight:600;'>"
                        f"⚠️ {sin_tutores} sin tutor</span></div>",
                        unsafe_allow_html=True
                    )
                col_f3.markdown(
                    f"<div style='padding-top:28px; font-size:13px; color:#5c5852;'>"
                    f"Total: <strong>{len(df_alumnos)}</strong> alumnos registrados</div>",
                    unsafe_allow_html=True
                )

                df_vista = df_alumnos if filtro_grado == "Todos" \
                    else df_alumnos[df_alumnos['grados_divisiones'] == filtro_grado]

                st.dataframe(
                    df_vista[[
                        'dni', 'apellido', 'nombre', 'grados_divisiones',
                        'fecha_nacimiento', 'cant_tutores', 'tutores_resumen', 'activo'
                    ]],
                    column_config={
                        "dni":               st.column_config.TextColumn("DNI"),
                        "apellido":          st.column_config.TextColumn("Apellido"),
                        "nombre":            st.column_config.TextColumn("Nombre"),
                        "grados_divisiones": st.column_config.TextColumn("Grado / Div."),
                        "fecha_nacimiento":  st.column_config.DateColumn("Fecha Nac.", format="DD/MM/YYYY"),
                        "cant_tutores":      st.column_config.NumberColumn("# Tutores", format="%d"),
                        "tutores_resumen":   st.column_config.TextColumn("Tutores (★ = principal)", width="large"),
                        "activo":            st.column_config.CheckboxColumn("Activo"),
                    },
                    use_container_width=True,
                    hide_index=True,
                )

            else:
                st.info(f"No hay alumnos cargados para {nombre_colegio_al} todavía.")

        except Exception as e:
            st.error(f"Error en módulo de alumnos: {e}")
