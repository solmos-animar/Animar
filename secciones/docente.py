# secciones/docente.py
import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import text
from utilidades.auth import require_login, get_colegio_id, get_rol, get_session

conn = st.connection("postgresql", type="sql")

def render():
    require_login("docente")

    rol     = get_rol()
    usuario = get_session()

    # ============================================================
    # RESOLUCIÓN DE COLEGIO
    # ============================================================
    if rol == "animar_admin":
        try:
            with conn.session as s:
                res = s.execute(text("SELECT id, nombre FROM colegios ORDER BY nombre"))
                df_cols = pd.DataFrame(res.fetchall(), columns=res.keys())
            colegio_id = st.selectbox(
                "Ver colegio",
                options=df_cols['id'].tolist(),
                format_func=lambda x: df_cols[df_cols['id'] == x]['nombre'].iloc[0],
                key="admin_sel_colegio_doc"
            )
            nombre_colegio = df_cols[df_cols['id'] == colegio_id]['nombre'].iloc[0]
            # Admin no tiene docente_id propio — usamos None
            docente_id = None
        except Exception as e:
            st.error(f"Error: {e}"); st.stop()
    else:
        colegio_id = get_colegio_id()
        if not colegio_id:
            st.error("Tu usuario no tiene un colegio asignado. Contactá al administrador.")
            st.stop()
        try:
            with conn.session as s:
                res = s.execute(text("SELECT nombre FROM colegios WHERE id = :id"), {"id": colegio_id})
                nombre_colegio = res.fetchone()[0]
                # Obtener docente_id desde persona_id del usuario
                docente_id = usuario.get("persona_id")
        except Exception as e:
            st.error(f"Error: {e}"); st.stop()

    # ============================================================
    # SELECTOR DE GRADO
    # ============================================================
    try:
        with conn.session as s:
            if docente_id and rol == "docente":
                # Solo los grados del docente logueado
                res = s.execute(text("""
                    SELECT DISTINCT grado FROM alumnos
                    WHERE colegio_id = :cid AND activo = TRUE
                    AND grado IN (
                        SELECT UNNEST(STRING_TO_ARRAY(grados_divisiones, ','))
                        FROM docentes WHERE id = :did
                    )
                    ORDER BY grado
                """), {"cid": colegio_id, "did": docente_id})
            else:
                # Admin o directivo ven todos los grados
                res = s.execute(text("""
                    SELECT DISTINCT grado FROM alumnos
                    WHERE colegio_id = :cid AND activo = TRUE
                    ORDER BY grado
                """), {"cid": colegio_id})
            grados = [r[0] for r in res.fetchall()]
    except Exception:
        # Fallback: todos los grados del colegio
        try:
            with conn.session as s:
                res = s.execute(text("""
                    SELECT DISTINCT grado FROM alumnos
                    WHERE colegio_id = :cid AND activo = TRUE ORDER BY grado
                """), {"cid": colegio_id})
                grados = [r[0] for r in res.fetchall()]
        except Exception as e:
            st.error(f"Error al cargar grados: {e}"); st.stop()

    if not grados:
        st.warning("No hay alumnos cargados para este colegio todavía.")
        st.stop()

    # ============================================================
    # HEADER
    # ============================================================
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"""
            <div style="margin-bottom:8px;">
                <div style="font-size:11px; font-weight:700; text-transform:uppercase;
                            letter-spacing:1.5px; color:#9a9690; margin-bottom:4px;">Panel Docente</div>
                <h2 style="font-family:'Georgia',serif; font-size:28px; color:#0f2240;
                           margin:0; letter-spacing:-0.5px;">{nombre_colegio}</h2>
            </div>
        """, unsafe_allow_html=True)
    with col_h2:
        grado_sel = st.selectbox("Grado / División", grados, key="doc_grado_sel")

    st.markdown("---")

    # Alumnos del grado seleccionado
    try:
        with conn.session as s:
            res = s.execute(text("""
                SELECT a.id, a.dni, a.apellido, a.nombre, a.fecha_nacimiento, a.activo
                FROM alumnos a
                WHERE a.colegio_id = :cid AND a.grado = :grado AND a.activo = TRUE
                ORDER BY a.apellido
            """), {"cid": colegio_id, "grado": grado_sel})
            df_alumnos = pd.DataFrame(res.fetchall(), columns=res.keys())
    except Exception as e:
        st.error(f"Error al cargar alumnos: {e}"); st.stop()

    # ============================================================
    # TABS
    # ============================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Resumen del Grado",
        "🕸️ Encuesta y Sociograma",
        "🚨 Alertas",
        "📝 Seguimiento de Alumnos",
        "📚 Contenido Educativo",
    ])

    # ================================================================
    # TAB 1 — RESUMEN DEL GRADO
    # ================================================================
    with tab1:
        st.subheader(f"Grado: {grado_sel}")

        c1, c2, c3 = st.columns(3)
        c1.metric("🎒 Alumnos en el grado", len(df_alumnos))

        try:
            with conn.session as s:
                res = s.execute(text("""
                    SELECT COUNT(*) FROM comentarios_alumnos ca
                    INNER JOIN alumnos a ON a.id = ca.alumno_id
                    WHERE a.colegio_id = :cid AND a.grado = :grado
                """), {"cid": colegio_id, "grado": grado_sel})
                cant_comentarios = res.fetchone()[0]
            c2.metric("📝 Comentarios registrados", cant_comentarios)
        except Exception:
            c2.metric("📝 Comentarios registrados", "—")

        c3.metric("🕸️ Sociograma", "⏳ Pendiente")

        st.markdown("---")
        st.subheader("Listado del grado")

        if not df_alumnos.empty:
            st.dataframe(
                df_alumnos[['dni', 'apellido', 'nombre', 'fecha_nacimiento']],
                column_config={
                    "dni":              st.column_config.TextColumn("DNI"),
                    "apellido":         st.column_config.TextColumn("Apellido"),
                    "nombre":           st.column_config.TextColumn("Nombre"),
                    "fecha_nacimiento": st.column_config.DateColumn("Fecha Nac.", format="DD/MM/YYYY"),
                },
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(f"No hay alumnos en {grado_sel}.")

    # ================================================================
    # TAB 2 — ENCUESTA Y SOCIOGRAMA
    # ================================================================
    with tab2:
        st.subheader(f"Encuesta Sociométrica — {grado_sel}")

        col_e1, col_e2 = st.columns([2, 1])
        with col_e1:
            st.markdown("""
                <div style="background:#f0f4ff; border-left:4px solid #1a56a0;
                            border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:20px;">
                    <span style="font-size:13px; color:#0f2240; font-weight:600;">
                        ¿Cómo funciona?
                    </span><br>
                    <span style="font-size:13px; color:#5c5852;">
                        Al lanzar la encuesta, todos los alumnos del grado reciben acceso.
                        Una vez que alcanza el 60% de participación, el sociograma
                        se genera automáticamente.
                    </span>
                </div>
            """, unsafe_allow_html=True)

        with col_e2:
            total = len(df_alumnos)
            st.metric("Alumnos en el grado", total)
            st.metric("Mínimo para generar sociograma",
                      f"{max(1, int(total * 0.6))} alumnos (60%)")

        # Estado de la encuesta (placeholder hasta tener tabla encuestas)
        st.markdown("""
            <div style="background:#fef9f0; border:1.5px dashed #d4580a;
                        border-radius:12px; padding:24px; text-align:center; margin:20px 0;">
                <div style="font-size:32px; margin-bottom:8px;">🕸️</div>
                <div style="font-size:15px; font-weight:600; color:#0f2240; margin-bottom:4px;">
                    Encuesta no iniciada
                </div>
                <div style="font-size:13px; color:#9a9690;">
                    El módulo de encuestas estará disponible en la próxima versión.
                </div>
            </div>
        """, unsafe_allow_html=True)

        col_b1, col_b2, _ = st.columns([1, 1, 2])
        col_b1.button("🚀 Lanzar encuesta", type="primary",
                      use_container_width=True, disabled=True)
        col_b2.button("⏹️ Cerrar encuesta",
                      use_container_width=True, disabled=True)

    # ================================================================
    # TAB 3 — ALERTAS
    # ================================================================
    with tab3:
        st.subheader(f"Alertas — {grado_sel}")
        st.info("🚨 Las alertas se activarán automáticamente cuando el sociograma esté generado.")
        st.markdown("""
            <div style="background:#fde8d0; border-left:4px solid #d4580a;
                        border-radius:0 12px 12px 0; padding:16px 20px;">
                <span style="font-size:13px; color:#6b3000; font-weight:600;">
                    ¿Qué verás aquí?
                </span><br>
                <span style="font-size:13px; color:#6b3000;">
                    🔴 Alumnos con alto índice de rechazo ·
                    👻 Alumnos aislados ·
                    ✉️ Mensajes confidenciales al docente
                </span>
            </div>
        """, unsafe_allow_html=True)

    # ================================================================
    # TAB 4 — SEGUIMIENTO / COMENTARIOS
    # ================================================================
    with tab4:
        st.subheader(f"Seguimiento de Alumnos — {grado_sel}")

        if df_alumnos.empty:
            st.info("No hay alumnos en este grado.")
        else:
            # Selector de alumno
            opciones_al = {
                row['id']: f"{row['apellido']}, {row['nombre']}"
                for _, row in df_alumnos.iterrows()
            }
            alumno_sel_id = st.selectbox(
                "Seleccionar alumno",
                options=list(opciones_al.keys()),
                format_func=lambda x: opciones_al[x],
                key="doc_alumno_comentario"
            )
            alumno_nombre = opciones_al[alumno_sel_id]

            # Historial de comentarios del alumno
            st.markdown(f"#### 📋 Historial de {alumno_nombre}")
            try:
                with conn.session as s:
                    res = s.execute(text("""
                        SELECT
                            ca.texto,
                            ca.creado_en,
                            d.apellido || ', ' || d.nombre AS docente
                        FROM comentarios_alumnos ca
                        INNER JOIN docentes d ON d.id = ca.docente_id
                        WHERE ca.alumno_id = :aid
                        ORDER BY ca.creado_en DESC
                    """), {"aid": alumno_sel_id})
                    df_com = pd.DataFrame(res.fetchall(), columns=res.keys())

                if not df_com.empty:
                    for _, row in df_com.iterrows():
                        fecha = pd.to_datetime(row['creado_en']).strftime("%d/%m/%Y %H:%M")
                        st.markdown(f"""
                            <div style="background:white; border:1px solid #ebe9e4;
                                        border-left:4px solid #1a56a0; border-radius:0 10px 10px 0;
                                        padding:14px 18px; margin-bottom:10px;">
                                <div style="font-size:12px; color:#9a9690; margin-bottom:6px;">
                                    📅 {fecha} &nbsp;·&nbsp;
                                    👨‍🏫 {row['docente']}
                                </div>
                                <div style="font-size:14px; color:#1a1815; line-height:1.6;">
                                    {row['texto']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No hay comentarios registrados para este alumno todavía.")

            except Exception as e:
                st.error(f"Error al cargar comentarios: {e}")

            # Nuevo comentario
            st.markdown("#### ✍️ Agregar comentario")

            # Necesitamos el docente_id real para guardar
            # Si es docente logueado, usamos persona_id. Si es admin/directivo, buscamos por colegio
            if rol == "docente" and docente_id:
                docente_id_guardar = docente_id
            else:
                # Admin o directivo: buscar primer docente del colegio como fallback
                # En producción se debería pedir selección
                try:
                    with conn.session as s:
                        res = s.execute(text("""
                            SELECT id FROM docentes
                            WHERE colegio_id = :cid LIMIT 1
                        """), {"cid": colegio_id})
                        row_d = res.fetchone()
                        docente_id_guardar = row_d[0] if row_d else None
                except Exception:
                    docente_id_guardar = None

            with st.form("form_comentario", clear_on_submit=True):
                texto_com = st.text_area(
                    "Comentario",
                    placeholder=f"Escribí tu observación sobre {alumno_nombre}...",
                    height=120,
                    help="Este comentario será visible para todos los docentes que tengan a este alumno y para el directivo."
                )
                submitted_com = st.form_submit_button(
                    "💾 Guardar comentario",
                    type="primary",
                    use_container_width=True
                )

                if submitted_com:
                    if not texto_com.strip():
                        st.warning("⚠️ El comentario no puede estar vacío.")
                    elif not docente_id_guardar:
                        st.error("No se pudo identificar el docente. Contactá al administrador.")
                    else:
                        try:
                            with conn.session as s:
                                s.execute(text("""
                                    INSERT INTO comentarios_alumnos
                                        (alumno_id, docente_id, colegio_id, texto)
                                    VALUES (:aid, :did, :cid, :txt)
                                """), {
                                    "aid": alumno_sel_id,
                                    "did": docente_id_guardar,
                                    "cid": colegio_id,
                                    "txt": texto_com.strip(),
                                })
                                s.commit()
                            st.success(f"✅ Comentario guardado para {alumno_nombre}.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al guardar: {e}")

    # ================================================================
    # TAB 5 — CONTENIDO EDUCATIVO
    # ================================================================
    with tab5:
        st.subheader("Recursos para Docentes")

        recursos = [
            {
                "titulo": "¿Cómo interpretar un sociograma?",
                "desc":   "Guía práctica para leer los mapas de relaciones y entender los roles sociométricos.",
                "tag":    "Sociograma",
                "color":  "#1a56a0",
                "icono":  "🕸️",
            },
            {
                "titulo": "Señales de alerta en el aula",
                "desc":   "Indicadores conductuales y sociales que pueden señalar situaciones de bullying.",
                "tag":    "Prevención",
                "color":  "#d4580a",
                "icono":  "🚨",
            },
            {
                "titulo": "Dinámicas de integración grupal",
                "desc":   "Actividades concretas para mejorar el clima de convivencia en el grado.",
                "tag":    "Actividades",
                "color":  "#1d7a55",
                "icono":  "🤝",
            },
            {
                "titulo": "Protocolo de intervención ante bullying",
                "desc":   "Pasos a seguir cuando se detecta una situación de acoso. Marco legal y derivación.",
                "tag":    "Protocolo",
                "color":  "#5b3fa0",
                "icono":  "📋",
            },
        ]

        col_r1, col_r2 = st.columns(2)
        for i, rec in enumerate(recursos):
            col = col_r1 if i % 2 == 0 else col_r2
            with col:
                st.markdown(f"""
                    <div style="background:white; border:1px solid #ebe9e4; border-radius:14px;
                                padding:20px; margin-bottom:16px;
                                box-shadow:0 2px 8px rgba(15,34,64,0.06);">
                        <div style="font-size:28px; margin-bottom:10px;">{rec['icono']}</div>
                        <span style="background:{rec['color']}18; color:{rec['color']};
                                     font-size:11px; font-weight:700; text-transform:uppercase;
                                     letter-spacing:1px; padding:3px 10px; border-radius:20px;">
                            {rec['tag']}
                        </span>
                        <div style="font-size:15px; font-weight:700; color:#0f2240;
                                    margin:10px 0 6px;">{rec['titulo']}</div>
                        <div style="font-size:13px; color:#5c5852; line-height:1.6;">
                            {rec['desc']}
                        </div>
                        <div style="margin-top:14px; font-size:12px; color:{rec['color']};
                                    font-weight:600;">Próximamente disponible →</div>
                    </div>
                """, unsafe_allow_html=True)
