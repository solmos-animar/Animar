# secciones/encuesta_docente.py
"""
Módulo de encuestas sociométricas para docentes.
Se usa embebido dentro del tab "Encuesta y Sociograma" de secciones/docente.py:

    from secciones.encuesta_docente import render_tab_encuesta
    render_tab_encuesta(conn, colegio_id, docente_id, grado_sel, rol)
"""
import streamlit as st
import pandas as pd
from sqlalchemy import text
from utilidades.sociograma import verificar_y_generar, cargar_sociograma, get_participacion

PREGUNTAS_DEFAULT = [
    {"orden": 1, "tipo": "eleccion_positiva",  "texto": "¿Con quién te gustaría hacer un trabajo grupal?",       "max_opciones": 3},
    {"orden": 2, "tipo": "eleccion_positiva",  "texto": "¿Con quién te gustaría sentarte en clase?",             "max_opciones": 3},
    {"orden": 3, "tipo": "eleccion_negativa",  "texto": "¿Con quién preferirías NO hacer un trabajo grupal?",    "max_opciones": 2},
    {"orden": 4, "tipo": "likert",             "texto": "Me siento bien en esta clase",                          "max_opciones": 5},
    {"orden": 5, "tipo": "likert",             "texto": "Me siento aceptado/a por mis compañeros",               "max_opciones": 5},
    {"orden": 6, "tipo": "likert",             "texto": "Hay situaciones de maltrato en mi grupo",               "max_opciones": 5},
    {"orden": 7, "tipo": "texto_libre",        "texto": "¿Hay algo que quieras contarle al docente? (opcional)", "max_opciones": 0},
]

ESTADO_BADGE = {
    "borrador":         ("⚪", "Borrador",         "#9a9690", "#f5f4f1"),
    "activa":           ("🟢", "Activa",            "#1d7a55", "#e6f4ee"),
    "cerrada":          ("🔴", "Cerrada",           "#c0392b", "#fde8e8"),
    "sociograma_listo": ("🕸️", "Sociograma listo", "#1a56a0", "#e0edff"),
}

ROLES_ES = {
    "estrella":       "⭐ Estrella",
    "bien_integrado": "🤝 Bien integrado",
    "controvertido":  "⚡ Controvertido",
    "ignorado":       "👻 Ignorado",
    "rechazado":      "🚫 Rechazado",
}

ROLES_INFO = {
    "estrella":       ("⭐", "#1d7a55", "#e6f4ee"),
    "bien_integrado": ("🤝", "#1a56a0", "#e0edff"),
    "controvertido":  ("⚡", "#5b3fa0", "#ede8fe"),
    "ignorado":       ("👻", "#9a9690", "#f5f4f1"),
    "rechazado":      ("🚫", "#c0392b", "#fde8e8"),
}


def render_tab_encuesta(conn, colegio_id, docente_id, grado_sel, rol):
    """Punto de entrada. Llamar desde el tab del docente."""
    st.subheader(f"Encuesta Sociométrica — {grado_sel}")
    enc = _get_encuesta(conn, colegio_id, docente_id, grado_sel, rol)
    if enc is None:
        _vista_sin_encuesta(conn, colegio_id, docente_id, grado_sel, rol)
    else:
        _vista_encuesta(conn, enc, colegio_id, grado_sel)


# ================================================================
# VISTAS
# ================================================================

def _vista_sin_encuesta(conn, colegio_id, docente_id, grado_sel, rol):
    st.markdown("""
        <div style="background:#fef9f0; border:1.5px dashed #d4580a;
                    border-radius:12px; padding:24px; text-align:center; margin:16px 0;">
            <div style="font-size:32px; margin-bottom:8px;">🕸️</div>
            <div style="font-size:15px; font-weight:600; color:#0f2240; margin-bottom:4px;">
                No hay encuesta para este grado
            </div>
            <div style="font-size:13px; color:#9a9690;">
                Creá una nueva encuesta sociométrica para comenzar.
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("➕ Crear encuesta para este grado", expanded=True):
        with st.form(f"form_nueva_enc_{grado_sel}", clear_on_submit=True):
            titulo_enc = st.text_input(
                "Título (opcional)",
                placeholder=f"Ej: Encuesta de convivencia — {grado_sel} — 1er trimestre"
            )
            umbral = st.slider(
                "Umbral de participación para generar el sociograma",
                min_value=40, max_value=100, value=60, step=5, format="%d%%"
            )
            st.markdown("""
                <div style="background:#f0f4ff; border-left:4px solid #1a56a0;
                            border-radius:0 10px 10px 0; padding:14px 18px; margin:12px 0;">
                    <strong style="color:#0f2240; font-size:13px;">📋 Preguntas incluidas</strong><br>
                    <span style="font-size:12px; color:#5c5852;">
                        Conjunto estándar de preguntas sociométricas validadas.
                    </span>
                </div>
            """, unsafe_allow_html=True)
            for i, p in enumerate(PREGUNTAS_DEFAULT, 1):
                tipo_label = {
                    "eleccion_positiva": "✅ Elección positiva",
                    "eleccion_negativa": "❌ Elección negativa",
                    "likert":            "📊 Likert (1-5)",
                    "texto_libre":       "💬 Texto libre",
                }.get(p["tipo"], p["tipo"])
                st.markdown(f"""
                    <div style="display:flex; gap:10px; padding:7px 0;
                                border-bottom:1px solid #f0f0f0;">
                        <span style="font-size:11px; font-weight:700; color:#9a9690; min-width:20px;">{i}.</span>
                        <div>
                            <span style="font-size:11px; font-weight:600; color:#1a56a0;">{tipo_label}</span><br>
                            <span style="font-size:13px; color:#1a1815;">{p['texto']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            if st.form_submit_button("Crear encuesta en borrador",
                                     type="primary", use_container_width=True):
                _crear_encuesta(conn, colegio_id, docente_id, grado_sel,
                                titulo_enc or f"Encuesta {grado_sel}", umbral, rol)
                st.success("✅ Encuesta creada. Lanzala cuando estés listo/a.")
                st.rerun()


def _vista_encuesta(conn, enc, colegio_id, grado_sel):
    eid, titulo, estado, umbral_pct, creada_por = enc
    icono, label, color, bg = ESTADO_BADGE.get(estado, ("⚪", estado, "#9a9690", "#f5f4f1"))
    respondieron, total, pct = get_participacion(conn, eid)

    # Card de estado
    st.markdown(f"""
        <div style="background:white; border:1px solid #ebe9e4; border-radius:14px;
                    padding:20px 24px; margin-bottom:16px;
                    box-shadow:0 2px 8px rgba(15,34,64,0.06);">
            <div style="margin-bottom:10px;">
                <span style="background:{bg}; color:{color}; font-size:11px; font-weight:700;
                             padding:3px 10px; border-radius:20px; text-transform:uppercase;
                             letter-spacing:1px;">{icono} {label}</span>
            </div>
            <div style="font-size:17px; font-weight:700; color:#0f2240; margin-bottom:6px;">{titulo}</div>
            <div style="font-size:13px; color:#9a9690;">
                Participación: <strong style="color:#0f2240;">{respondieron}/{total} ({pct}%)</strong>
                &nbsp;·&nbsp; Umbral: {umbral_pct}%
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.progress(min(pct / 100, 1.0))
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Acciones
    if estado == "borrador":
        col1, col2, _ = st.columns([1, 1, 2])
        if col1.button("🚀 Lanzar encuesta", type="primary",
                       use_container_width=True, key=f"lanzar_{eid}"):
            _lanzar_encuesta(conn, eid)
            st.success("✅ Encuesta lanzada. Los alumnos ya pueden responderla.")
            st.rerun()
        if col2.button("🗑️ Eliminar", use_container_width=True, key=f"eliminar_{eid}"):
            _eliminar_encuesta(conn, eid)
            st.rerun()

    elif estado == "activa":
        col1, col2, _ = st.columns([1, 1, 2])
        if col1.button("⏹️ Cerrar encuesta",
                       use_container_width=True, key=f"cerrar_{eid}"):
            _cerrar_encuesta(conn, eid)
            st.rerun()
        if pct >= umbral_pct:
            if col2.button("🕸️ Generar Sociograma", type="primary",
                           use_container_width=True, key=f"generar_{eid}"):
                ok = verificar_y_generar(conn, eid)
                if ok:
                    st.success("✅ Sociograma generado.")
                    st.rerun()
        else:
            st.info(f"Faltan {umbral_pct - pct:.1f}% más de participación para generar el sociograma.")

    elif estado in ("cerrada", "sociograma_listo"):
        if estado == "cerrada" and pct >= umbral_pct:
            if st.button("🕸️ Generar Sociograma", type="primary",
                         use_container_width=True, key=f"gen_cerrada_{eid}"):
                ok = verificar_y_generar(conn, eid)
                if ok:
                    st.success("✅ Sociograma generado.")
                    st.rerun()

    # Sociograma
    if estado == "sociograma_listo":
        st.markdown("---")
        _mostrar_sociograma(conn, eid)

    # Participación
    if estado in ("activa", "cerrada", "sociograma_listo"):
        with st.expander("👁️ Ver participación por alumno", expanded=False):
            _tabla_participacion(conn, eid, colegio_id, grado_sel)


# ================================================================
# SOCIOGRAMA
# ================================================================

def _mostrar_sociograma(conn, enc_id):
    datos = cargar_sociograma(conn, enc_id)
    if not datos:
        st.warning("El sociograma todavía no fue generado.")
        return

    grupo   = datos.get("grupo", {})
    alumnos = datos.get("alumnos", {})

    st.markdown("### 🕸️ Resultados del Sociograma")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Participantes",   grupo.get("n_participantes", 0))
    c2.metric("🤝 Cohesión grupal", f"{grupo.get('cohesion', 0):.0%}")
    c3.metric("📊 Reciprocidad",    f"{grupo.get('reciprocidad_media', 0):.0%}")
    c4.metric("🚨 Alertas",         grupo.get("n_alertas", 0))

    st.markdown("#### Distribución de roles")
    roles = grupo.get("roles_resumen", {})
    cols  = st.columns(5)
    for i, (rol_key, (icono, color, bg)) in enumerate(ROLES_INFO.items()):
        cols[i].markdown(f"""
            <div style="background:{bg}; border-radius:12px; padding:14px;
                        text-align:center; border:1px solid {color}22;">
                <div style="font-size:22px;">{icono}</div>
                <div style="font-size:20px; font-weight:700; color:{color};">
                    {roles.get(rol_key, 0)}
                </div>
                <div style="font-size:11px; color:{color}; text-transform:capitalize;">
                    {rol_key.replace('_', ' ')}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Índices individuales")

    filas, alertas_list = [], []
    for aid, a in alumnos.items():
        filas.append({
            "Alumno":       f"{a['apellido']}, {a['nombre']}",
            "Rol":          ROLES_ES.get(a["rol"], a["rol"]),
            "Popularidad":  a["idx_popularidad"],
            "Rechazo":      a["idx_rechazo"],
            "Integración":  a["idx_integracion"],
            "Reciprocidad": a["idx_reciprocidad"],
            "Bienestar":    a["likert_prom"] if a["likert_prom"] else "—",
            "⚠️":           "Sí" if a["alertas"] else "",
        })
        if a["alertas"]:
            alertas_list.append((f"{a['apellido']}, {a['nombre']}",
                                  a["alertas"], a.get("mensaje_conf")))

    st.dataframe(
        pd.DataFrame(filas),
        use_container_width=True, hide_index=True,
        column_config={
            "Popularidad":  st.column_config.ProgressColumn("Popularidad",  min_value=0, max_value=1, format="%.2f"),
            "Rechazo":      st.column_config.ProgressColumn("Rechazo",      min_value=0, max_value=1, format="%.2f"),
            "Integración":  st.column_config.ProgressColumn("Integración",  min_value=0, max_value=1, format="%.2f"),
            "Reciprocidad": st.column_config.ProgressColumn("Reciprocidad", min_value=0, max_value=1, format="%.2f"),
        }
    )

    if alertas_list:
        st.markdown("#### 🚨 Alumnos que requieren atención")
        for nombre, alertas, mensaje in alertas_list:
            with st.expander(f"⚠️ {nombre}", expanded=True):
                for alerta in alertas:
                    st.markdown(f"""
                        <div style="background:#fde8d0; border-left:4px solid #d4580a;
                                    border-radius:0 8px 8px 0; padding:10px 14px;
                                    margin-bottom:6px; font-size:13px; color:#6b3000;">
                            {alerta}
                        </div>
                    """, unsafe_allow_html=True)
                if mensaje:
                    st.markdown(f"""
                        <div style="background:#fde8e8; border-left:4px solid #c0392b;
                                    border-radius:0 8px 8px 0; padding:10px 14px;
                                    margin-top:8px; font-size:13px; color:#6b0a0a;">
                            <strong>Mensaje confidencial:</strong> {mensaje}
                        </div>
                    """, unsafe_allow_html=True)


def _tabla_participacion(conn, enc_id, colegio_id, grado_sel):
    try:
        with conn.session as s:
            res = s.execute(text("""
                SELECT a.apellido, a.nombre,
                       CASE WHEN er.alumno_id IS NOT NULL
                            THEN '✅ Respondió' ELSE '⏳ Pendiente' END AS estado
                FROM alumnos a
                LEFT JOIN (
                    SELECT DISTINCT alumno_id FROM encuesta_respuestas
                    WHERE encuesta_id = :eid
                ) er ON er.alumno_id = a.id
                WHERE a.colegio_id = :cid AND a.grado = :grado AND a.activo = TRUE
                ORDER BY estado DESC, a.apellido
            """), {"eid": enc_id, "cid": colegio_id, "grado": grado_sel})
            df = pd.DataFrame(res.fetchall(), columns=["Apellido", "Nombre", "Estado"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Error: {e}")


# ================================================================
# HELPERS DB
# ================================================================

def _get_encuesta(conn, colegio_id, docente_id, grado, rol):
    try:
        with conn.session as s:
            params = {"cid": colegio_id, "grado": grado}
            q = """
                SELECT id, titulo, estado, umbral_pct, creada_por_rol
                FROM encuestas
                WHERE colegio_id = :cid AND grado = :grado
            """
            if rol == "docente" and docente_id:
                q += " AND docente_id = :did"
                params["did"] = docente_id
            q += " ORDER BY creado_en DESC LIMIT 1"
            return s.execute(text(q), params).fetchone()
    except Exception:
        return None


def _crear_encuesta(conn, colegio_id, docente_id, grado, titulo, umbral_pct, creada_por_rol):
    with conn.session as s:
        res = s.execute(text("""
            INSERT INTO encuestas
                (colegio_id, docente_id, grado, titulo, estado, umbral_pct, creada_por_rol)
            VALUES (:cid, :did, :grado, :titulo, 'borrador', :umbral, :cpr)
            RETURNING id
        """), {"cid": colegio_id, "did": docente_id, "grado": grado,
               "titulo": titulo, "umbral": umbral_pct, "cpr": creada_por_rol})
        enc_id = res.fetchone()[0]
        for p in PREGUNTAS_DEFAULT:
            s.execute(text("""
                INSERT INTO encuesta_preguntas
                    (encuesta_id, orden, tipo, texto, max_opciones)
                VALUES (:eid, :orden, :tipo, :texto, :max_op)
            """), {"eid": enc_id, "orden": p["orden"], "tipo": p["tipo"],
                   "texto": p["texto"], "max_op": p["max_opciones"]})
        s.commit()


def _lanzar_encuesta(conn, enc_id):
    with conn.session as s:
        s.execute(text("UPDATE encuestas SET estado='activa', activada_en=NOW() WHERE id=:eid"),
                  {"eid": enc_id})
        s.commit()


def _cerrar_encuesta(conn, enc_id):
    with conn.session as s:
        s.execute(text("UPDATE encuestas SET estado='cerrada', cerrada_en=NOW() WHERE id=:eid"),
                  {"eid": enc_id})
        s.commit()


def _eliminar_encuesta(conn, enc_id):
    with conn.session as s:
        s.execute(text("DELETE FROM encuestas WHERE id=:eid AND estado='borrador'"),
                  {"eid": enc_id})
        s.commit()
