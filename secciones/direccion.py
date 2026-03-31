# secciones/direccion.py
import streamlit as st
import pandas as pd
from sqlalchemy import text
from utilidades.auth import require_login, get_colegio_id, get_rol, get_session

conn = st.connection("postgresql", type="sql")

def render():
    require_login("direccion")

    rol        = get_rol()
    usuario    = get_session()

    # ============================================================
    # RESOLUCIÓN DEL COLEGIO
    # Admin puede elegir cualquier colegio. Resto: fijo por sesión.
    # ============================================================
    if rol == "animar_admin":
        try:
            with conn.session as s:
                res = s.execute(text("SELECT id, nombre FROM colegios ORDER BY nombre"))
                df_cols = pd.DataFrame(res.fetchall(), columns=res.keys())
            if df_cols.empty:
                st.warning("No hay colegios registrados.")
                st.stop()
            colegio_id = st.selectbox(
                "Ver colegio",
                options=df_cols['id'].tolist(),
                format_func=lambda x: df_cols[df_cols['id'] == x]['nombre'].iloc[0],
                key="admin_sel_colegio_dir"
            )
            nombre_colegio = df_cols[df_cols['id'] == colegio_id]['nombre'].iloc[0]
        except Exception as e:
            st.error(f"Error al cargar colegios: {e}")
            st.stop()
    else:
        colegio_id = get_colegio_id()
        if not colegio_id:
            st.error("Tu usuario no tiene un colegio asignado. Contactá al administrador.")
            st.stop()
        try:
            with conn.session as s:
                res = s.execute(text("SELECT nombre FROM colegios WHERE id = :id"),
                                {"id": colegio_id})
                row = res.fetchone()
            nombre_colegio = row[0] if row else f"Colegio #{colegio_id}"
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    # ============================================================
    # HEADER
    # ============================================================
    st.markdown(f"""
        <div style="margin-bottom:24px;">
            <div style="font-size:11px; font-weight:700; text-transform:uppercase;
                        letter-spacing:1.5px; color:#9a9690; margin-bottom:4px;">Panel de Dirección</div>
            <h2 style="font-family:'Georgia',serif; font-size:28px; color:#0f2240;
                       margin:0; letter-spacing:-0.5px;">{nombre_colegio}</h2>
        </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # TABS
    # ============================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Resumen",
        "👨‍🏫 Docentes",
        "🎒 Alumnos",
        "🕸️ Sociogramas",
        "🚨 Alertas",
    ])

    # ================================================================
    # TAB 1 — RESUMEN GENERAL
    # ================================================================
    with tab1:
        try:
            with conn.session as s:
                # Conteos principales
                r = s.execute(text("""
                    SELECT
                        (SELECT COUNT(*) FROM docentes  WHERE colegio_id = :cid AND activo = TRUE)  AS docentes,
                        (SELECT COUNT(*) FROM alumnos   WHERE colegio_id = :cid AND activo = TRUE)  AS alumnos,
                        (SELECT COUNT(*) FROM tutores   t
                            INNER JOIN alumno_tutores at2 ON at2.tutor_id = t.id
                            INNER JOIN alumnos a          ON a.id = at2.alumno_id
                            WHERE a.colegio_id = :cid)                                              AS tutores,
                        (SELECT COUNT(*) FROM alumnos   WHERE colegio_id = :cid AND activo = FALSE) AS inactivos
                """), {"cid": colegio_id})
                counts = r.fetchone()

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("👨‍🏫 Docentes activos",  counts.docentes)
            c2.metric("🎒 Alumnos activos",    counts.alumnos)
            c3.metric("👨‍👩‍👧 Tutores vinculados", counts.tutores)
            c4.metric("❌ Alumnos inactivos",  counts.inactivos)

        except Exception as e:
            st.error(f"Error al cargar resumen: {e}")

        st.markdown("---")

        # Distribución por grado
        st.subheader("Distribución de alumnos por grado")
        try:
            with conn.session as s:
                res = s.execute(text("""
                    SELECT grado, COUNT(*) AS cantidad
                    FROM alumnos
                    WHERE colegio_id = :cid AND activo = TRUE
                    GROUP BY grado
                    ORDER BY grado
                """), {"cid": colegio_id})
                df_dist = pd.DataFrame(res.fetchall(), columns=res.keys())

            if not df_dist.empty:
                st.bar_chart(df_dist.set_index("grado")["cantidad"])
            else:
                st.info("No hay alumnos cargados todavía.")
        except Exception as e:
            st.error(f"Error: {e}")

    # ================================================================
    # TAB 2 — DOCENTES
    # ================================================================
    with tab2:
        st.subheader(f"Docentes — {nombre_colegio}")
        try:
            with conn.session as s:
                res = s.execute(text("""
                    SELECT id, dni, apellido, nombre, grados_divisiones, activo
                    FROM docentes
                    WHERE colegio_id = :cid
                    ORDER BY apellido
                """), {"cid": colegio_id})
                df_doc = pd.DataFrame(res.fetchall(), columns=res.keys())

            if not df_doc.empty:
                col_f1, col_f2 = st.columns([2, 4])
                filtro_activo_doc = col_f1.selectbox(
                    "Estado", ["Todos", "Activos", "Inactivos"], key="dir_filtro_doc"
                )
                col_f2.markdown(
                    f"<div style='padding-top:28px; font-size:13px; color:#5c5852;'>"
                    f"Total: <strong>{len(df_doc)}</strong> docentes</div>",
                    unsafe_allow_html=True
                )

                if filtro_activo_doc == "Activos":
                    df_doc = df_doc[df_doc['activo'] == True]
                elif filtro_activo_doc == "Inactivos":
                    df_doc = df_doc[df_doc['activo'] == False]

                # Dirección puede editar activo, no puede editar DNI
                df_edit_doc = st.data_editor(
                    df_doc,
                    column_config={
                        "id":                None,
                        "dni":               st.column_config.TextColumn("DNI", disabled=True),
                        "apellido":          st.column_config.TextColumn("Apellido", disabled=True),
                        "nombre":            st.column_config.TextColumn("Nombre", disabled=True),
                        "grados_divisiones": st.column_config.TextColumn("Grados / Div.", disabled=True),
                        "activo":            st.column_config.CheckboxColumn("Activo"),
                    },
                    use_container_width=True,
                    hide_index=True,
                    key="dir_edit_doc"
                )

                if st.button("💾 Guardar cambios de estado", key="dir_save_doc"):
                    with conn.session as s:
                        for i, r in df_edit_doc.iterrows():
                            uid = df_doc.iloc[i]['id']
                            s.execute(text("UPDATE docentes SET activo=:a WHERE id=:id AND colegio_id=:cid"),
                                      {"a": r['activo'], "id": uid, "cid": colegio_id})
                        s.commit()
                    st.success("✅ Estados actualizados.")
                    st.rerun()
            else:
                st.info("No hay docentes cargados para este colegio.")
        except Exception as e:
            st.error(f"Error: {e}")

    # ================================================================
    # TAB 3 — ALUMNOS
    # ================================================================
    with tab3:
        st.subheader(f"Alumnos — {nombre_colegio}")
        try:
            with conn.session as s:
                res = s.execute(text("""
                    SELECT
                        a.id, a.dni, a.apellido, a.nombre, a.grado,
                        a.fecha_nacimiento, a.activo,
                        COUNT(at2.tutor_id) AS cant_tutores,
                        STRING_AGG(
                            at2.relacion || ': ' || t.apellido || ' ' || t.nombre ||
                            CASE WHEN at2.es_principal THEN ' ★' ELSE '' END,
                            ' | ' ORDER BY at2.es_principal DESC
                        ) AS tutores_resumen
                    FROM alumnos a
                    LEFT JOIN alumno_tutores at2 ON at2.alumno_id = a.id
                    LEFT JOIN tutores t          ON t.id = at2.tutor_id
                    WHERE a.colegio_id = :cid
                    GROUP BY a.id, a.dni, a.apellido, a.nombre,
                             a.grado, a.fecha_nacimiento, a.activo
                    ORDER BY a.grado, a.apellido
                """), {"cid": colegio_id})
                df_al = pd.DataFrame(res.fetchall(), columns=res.keys())

            if not df_al.empty:
                opciones_grado = ["Todos"] + sorted(df_al['grado'].dropna().unique().tolist())
                col_f1, col_f2, col_f3 = st.columns([2, 2, 3])
                filtro_grado = col_f1.selectbox("Grado", opciones_grado, key="dir_filtro_grado")
                sin_tutor = (df_al['cant_tutores'] == 0).sum()
                if sin_tutor > 0:
                    col_f2.markdown(
                        f"<div style='padding-top:26px;'>"
                        f"<span style='background:#fde8d0; color:#6b3000; padding:4px 10px;"
                        f"border-radius:20px; font-size:12px; font-weight:600;'>"
                        f"⚠️ {sin_tutor} sin tutor</span></div>",
                        unsafe_allow_html=True
                    )
                col_f3.markdown(
                    f"<div style='padding-top:28px; font-size:13px; color:#5c5852;'>"
                    f"Total: <strong>{len(df_al)}</strong> alumnos</div>",
                    unsafe_allow_html=True
                )

                df_vista = df_al if filtro_grado == "Todos" \
                    else df_al[df_al['grado'] == filtro_grado]

                # Solo lectura para dirección
                st.dataframe(
                    df_vista[['dni','apellido','nombre','grado',
                              'fecha_nacimiento','cant_tutores','tutores_resumen','activo']],
                    column_config={
                        "dni":              st.column_config.TextColumn("DNI"),
                        "apellido":         st.column_config.TextColumn("Apellido"),
                        "nombre":           st.column_config.TextColumn("Nombre"),
                        "grado":            st.column_config.TextColumn("Grado / Div."),
                        "fecha_nacimiento": st.column_config.DateColumn("Fecha Nac.", format="DD/MM/YYYY"),
                        "cant_tutores":     st.column_config.NumberColumn("# Tutores", format="%d"),
                        "tutores_resumen":  st.column_config.TextColumn("Tutores (★ = principal)", width="large"),
                        "activo":           st.column_config.CheckboxColumn("Activo"),
                    },
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No hay alumnos cargados para este colegio.")
        except Exception as e:
            st.error(f"Error: {e}")

    # ================================================================
    # TAB 4 — SOCIOGRAMAS (placeholder hasta que esté el módulo)
    # ================================================================
    with tab4:
        st.subheader(f"Estado de Sociogramas — {nombre_colegio}")
        st.info("🕸️ El módulo de sociogramas está en desarrollo. Próximamente verás aquí el estado de cada grado/división.")

        # Preview de estructura por grado
        try:
            with conn.session as s:
                res = s.execute(text("""
                    SELECT grado, COUNT(*) AS total_alumnos
                    FROM alumnos
                    WHERE colegio_id = :cid AND activo = TRUE
                    GROUP BY grado ORDER BY grado
                """), {"cid": colegio_id})
                df_grados = pd.DataFrame(res.fetchall(), columns=res.keys())

            if not df_grados.empty:
                df_grados['estado']       = "⏳ Pendiente"
                df_grados['participacion'] = "—"
                st.dataframe(
                    df_grados.rename(columns={
                        "grado": "Grado / Div.",
                        "total_alumnos": "Total alumnos",
                        "estado": "Estado sociograma",
                        "participacion": "% Participación"
                    }),
                    use_container_width=True,
                    hide_index=True,
                )
        except Exception as e:
            st.error(f"Error: {e}")

    # ================================================================
    # TAB 5 — ALERTAS (placeholder)
    # ================================================================
    with tab5:
        st.subheader(f"Alertas — {nombre_colegio}")
        st.info("🚨 Las alertas se generarán automáticamente una vez que los sociogramas estén activos.")

        st.markdown("""
            <div style="background:#fde8d0; border-left:4px solid #d4580a;
                        border-radius:0 12px 12px 0; padding:16px 20px; margin-top:16px;">
                <span style="font-size:13px; color:#6b3000; font-weight:600;">
                    ¿Qué verás aquí?
                </span><br>
                <span style="font-size:13px; color:#6b3000;">
                    Alumnos con alto índice de rechazo · Alumnos aislados ·
                    Mensajes confidenciales al docente · Alertas sin gestionar
                </span>
            </div>
        """, unsafe_allow_html=True)
