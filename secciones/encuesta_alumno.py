# secciones/encuesta_alumno.py
"""
Módulo de encuesta para el alumno.
Se usa embebido dentro del tab correspondiente de secciones/alumno.py:

    from secciones.encuesta_alumno import render_tab_encuesta_alumno
    render_tab_encuesta_alumno(conn, alumno, primaria)
"""
import streamlit as st
from sqlalchemy import text
from utilidades.sociograma import verificar_y_generar


def render_tab_encuesta_alumno(conn, alumno, primaria):
    """
    Punto de entrada. Llamar desde el tab del alumno.
    alumno: dict con id, nombre, apellido, grado, colegio_id
    primaria: bool
    """
    # Buscar encuesta activa para el grado
    try:
        with conn.session as s:
            res = s.execute(text("""
                SELECT id, titulo, umbral_pct
                FROM encuestas
                WHERE colegio_id = :cid AND grado = :grado AND estado = 'activa'
                ORDER BY activada_en DESC LIMIT 1
            """), {"cid": alumno["colegio_id"], "grado": alumno["grado"]})
            enc_row = res.fetchone()
    except Exception as e:
        st.error(f"Error: {e}"); return

    if not enc_row:
        _sin_encuesta(alumno, primaria)
        return

    enc_id, enc_titulo, umbral_pct = enc_row

    # ¿Ya respondió?
    try:
        with conn.session as s:
            res = s.execute(text("""
                SELECT COUNT(DISTINCT pregunta_id) FROM encuesta_respuestas
                WHERE encuesta_id = :eid AND alumno_id = :aid
            """), {"eid": enc_id, "aid": alumno["id"]})
            ya_respondio = res.fetchone()[0] > 0
    except Exception as e:
        st.error(f"Error: {e}"); return

    if ya_respondio:
        _ya_respondio(alumno, primaria)
        return

    # Cargar preguntas y compañeros
    try:
        with conn.session as s:
            res = s.execute(text("""
                SELECT id, orden, tipo, texto, max_opciones
                FROM encuesta_preguntas WHERE encuesta_id = :eid ORDER BY orden
            """), {"eid": enc_id})
            preguntas = res.fetchall()

            res = s.execute(text("""
                SELECT id, nombre, apellido FROM alumnos
                WHERE colegio_id = :cid AND grado = :grado
                  AND activo = TRUE AND id != :aid
                ORDER BY apellido
            """), {"cid": alumno["colegio_id"], "grado": alumno["grado"], "aid": alumno["id"]})
            companeros = res.fetchall()
    except Exception as e:
        st.error(f"Error: {e}"); return

    # Estado de la navegación en session_state
    key_paso = f"enc_paso_{enc_id}"
    key_resp = f"enc_resp_{enc_id}"
    if key_paso not in st.session_state:
        st.session_state[key_paso] = 0
    if key_resp not in st.session_state:
        st.session_state[key_resp] = {}

    paso_actual = st.session_state[key_paso]
    total_pasos = len(preguntas)

    # Pantalla de bienvenida
    if paso_actual == 0:
        _bienvenida(alumno, enc_titulo, total_pasos, primaria, key_paso)
        return

    # Finalizar
    if paso_actual > total_pasos:
        _guardar_y_finalizar(conn, enc_id, alumno["id"],
                             st.session_state[key_resp], primaria)
        verificar_y_generar(conn, enc_id)
        del st.session_state[key_paso]
        del st.session_state[key_resp]
        st.rerun()
        return

    # Pregunta actual
    pregunta = preguntas[paso_actual - 1]
    pid, orden, tipo, texto, max_opciones = pregunta

    _header_progreso(paso_actual, total_pasos, primaria)

    if tipo in ("eleccion_positiva", "eleccion_negativa"):
        _pregunta_eleccion(pid, texto, tipo, max_opciones,
                           companeros, paso_actual, key_paso, key_resp, primaria)
    elif tipo == "likert":
        _pregunta_likert(pid, texto, paso_actual, key_paso, key_resp, primaria)
    elif tipo == "texto_libre":
        _pregunta_texto_libre(pid, texto, paso_actual, key_paso, key_resp, primaria)


# ================================================================
# PANTALLAS DE ESTADO
# ================================================================

def _sin_encuesta(alumno, primaria):
    if primaria:
        st.markdown(f"""
            <div style="text-align:center; padding:40px 24px;
                        background:linear-gradient(135deg,#fff8f0,#fff0e8);
                        border-radius:24px; border:2px solid #ffd4b8;">
                <div style="font-size:48px; margin-bottom:12px;">😴</div>
                <div style="font-size:22px; font-weight:800; color:#e05c00; margin-bottom:8px;">
                    ¡Hola, {alumno['nombre']}!
                </div>
                <div style="font-size:15px; color:#9a5c00;">
                    Todavía no hay encuesta disponible para tu grado.<br>
                    Cuando tu docente la active, vas a poder responderla acá 🌟
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background:white; border:1px solid #ebe9e4; border-radius:16px;
                        padding:40px; text-align:center;">
                <div style="font-size:40px; margin-bottom:12px;">📋</div>
                <div style="font-size:18px; font-weight:700; color:#0f2240; margin-bottom:6px;">
                    No hay encuestas activas
                </div>
                <div style="font-size:14px; color:#5c5852;">
                    Tu docente todavía no activó ninguna encuesta. Volvé a consultar pronto.
                </div>
            </div>
        """, unsafe_allow_html=True)


def _ya_respondio(alumno, primaria):
    if primaria:
        st.markdown(f"""
            <div style="text-align:center; padding:40px 24px;
                        background:linear-gradient(135deg,#e8f4f0,#f0f9f4);
                        border-radius:24px; border:2px solid #b8e8d4;">
                <div style="font-size:48px; margin-bottom:12px;">🎉</div>
                <div style="font-size:22px; font-weight:800; color:#1d7a55; margin-bottom:8px;">
                    ¡Ya la respondiste!
                </div>
                <div style="font-size:15px; color:#0d4a30;">
                    Muchas gracias {alumno['nombre']}. Tu respuesta fue guardada ✅
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.success(f"✅ Ya completaste la encuesta, {alumno['nombre']}. ¡Gracias por participar!")
        st.info("Tus respuestas son confidenciales y contribuyen a mejorar la convivencia del grupo.")


def _bienvenida(alumno, titulo, total_pasos, primaria, key_paso):
    if primaria:
        st.markdown(f"""
            <div style="text-align:center; padding:36px 24px;
                        background:linear-gradient(135deg,#fff8f0,#fff0e8);
                        border-radius:24px; border:2px solid #ffd4b8; margin-bottom:20px;">
                <div style="font-size:44px; margin-bottom:10px;">📝</div>
                <div style="font-size:24px; font-weight:800; color:#e05c00; margin-bottom:8px;">
                    ¡Hola, {alumno['nombre']}!
                </div>
                <div style="font-size:15px; color:#9a5c00;">
                    Te vamos a hacer <strong>{total_pasos} preguntas</strong>
                    sobre tus compañeros y cómo te sentís en clase.<br>
                    ¡Nadie más va a ver tus respuestas! 🤫
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f2240,#1a3560);
                        border-radius:14px; padding:28px 32px; color:white; margin-bottom:20px;">
                <div style="font-size:11px; text-transform:uppercase; letter-spacing:2px;
                            color:rgba(255,255,255,0.5); margin-bottom:6px;">Encuesta Sociométrica</div>
                <div style="font-size:22px; font-weight:700; margin-bottom:6px;">{titulo}</div>
                <div style="font-size:13px; color:rgba(255,255,255,0.65);">
                    {total_pasos} preguntas · Tus respuestas son completamente confidenciales.
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div style="background:#f0f4ff; border-left:4px solid #1a56a0;
                        border-radius:0 12px 12px 0; padding:14px 18px; margin-bottom:20px;">
                <strong style="color:#0f2240; font-size:13px;">🔒 ¿Cómo funciona?</strong><br>
                <span style="font-size:13px; color:#5c5852;">
                    Esta encuesta ayuda a entender la dinámica del grupo para mejorar la convivencia.
                    Nadie va a poder ver tus respuestas individuales.
                </span>
            </div>
        """, unsafe_allow_html=True)

    if st.button("¡Empezar! 🚀" if primaria else "Comenzar →",
                 type="primary", use_container_width=True, key=f"start_{key_paso}"):
        st.session_state[key_paso] = 1
        st.rerun()


# ================================================================
# PREGUNTAS
# ================================================================

def _header_progreso(paso, total, primaria):
    st.progress(paso / total)
    st.markdown(
        f"<div style='font-size:12px; color:#9a9690; margin-bottom:12px;'>"
        f"Pregunta {paso} de {total}</div>",
        unsafe_allow_html=True
    )


def _pregunta_eleccion(pid, texto, tipo, max_opciones,
                        companeros, paso, key_paso, key_resp, primaria):
    es_pos = tipo == "eleccion_positiva"
    color  = "#1d7a55" if es_pos else "#c0392b"
    bg     = "#e6f4ee" if es_pos else "#fde8e8"
    icono  = "✅" if es_pos else "❌"

    st.markdown(f"""
        <div style="background:{bg}; border-left:4px solid {color};
                    border-radius:0 12px 12px 0; padding:18px 22px; margin-bottom:16px;">
            <div style="font-size:17px; font-weight:700; color:{color};">{icono} {texto}</div>
            <div style="font-size:12px; color:{color}; margin-top:4px; opacity:0.8;">
                Podés elegir hasta {max_opciones} compañeros
            </div>
        </div>
    """, unsafe_allow_html=True)

    opciones = {r[0]: f"{r[2]}, {r[1]}" for r in companeros}
    seleccionados = st.multiselect(
        "Seleccioná tus compañeros:",
        options=list(opciones.keys()),
        format_func=lambda x: opciones[x],
        max_selections=max_opciones,
        key=f"ms_{pid}_{paso}"
    )

    col1, col2 = st.columns([1, 3])
    if paso > 1:
        if col1.button("← Atrás", key=f"atras_{pid}_{paso}"):
            st.session_state[key_paso] -= 1
            st.rerun()
    if col2.button("Siguiente →" if not primaria else "¡Siguiente! ➡️",
                   type="primary", use_container_width=True, key=f"sig_{pid}_{paso}"):
        st.session_state[key_resp][pid] = {"tipo": tipo, "elegidos": seleccionados}
        st.session_state[key_paso] += 1
        st.rerun()


def _pregunta_likert(pid, texto, paso, key_paso, key_resp, primaria):
    CARITAS = ["😢 Muy en desacuerdo", "😕 En desacuerdo", "😐 Neutral",
               "🙂 De acuerdo", "😄 Muy de acuerdo"]

    st.markdown(f"""
        <div style="background:#f0f4ff; border-left:4px solid #1a56a0;
                    border-radius:0 12px 12px 0; padding:18px 22px; margin-bottom:16px;">
            <div style="font-size:17px; font-weight:700; color:#0f2240;">📊 {texto}</div>
        </div>
    """, unsafe_allow_html=True)

    valor_sel = None

    if primaria:
        st.markdown("**¿Cómo te sentís?**")
        cols = st.columns(5)
        emojis = ["😢", "😕", "😐", "🙂", "😄"]
        for i, (col, emoji) in enumerate(zip(cols, emojis)):
            if col.button(emoji, key=f"likert_{pid}_{i}_{paso}", use_container_width=True):
                valor_sel = i + 1
    else:
        valor_sel = st.radio(
            "Tu respuesta:",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: CARITAS[x-1],
            horizontal=True,
            index=2,
            key=f"radio_{pid}_{paso}"
        )

    col1, col2 = st.columns([1, 3])
    if paso > 1:
        if col1.button("← Atrás", key=f"atras_l_{pid}_{paso}"):
            st.session_state[key_paso] -= 1
            st.rerun()
    if col2.button("¡Siguiente! ➡️" if primaria else "Siguiente →",
                   type="primary", use_container_width=True, key=f"sig_l_{pid}_{paso}"):
        st.session_state[key_resp][pid] = {"tipo": "likert", "valor": valor_sel or 3}
        st.session_state[key_paso] += 1
        st.rerun()


def _pregunta_texto_libre(pid, texto, paso, key_paso, key_resp, primaria):
    st.markdown(f"""
        <div style="background:#fef9f0; border-left:4px solid #d4580a;
                    border-radius:0 12px 12px 0; padding:18px 22px; margin-bottom:16px;">
            <div style="font-size:17px; font-weight:700; color:#6b3000;">💬 {texto}</div>
            <div style="font-size:12px; color:#9a5c00; margin-top:4px;">
                {'Esta pregunta es opcional 😊' if primaria else 'Podés dejarla en blanco si querés.'}
            </div>
        </div>
    """, unsafe_allow_html=True)

    texto_resp = st.text_area(
        "Tu mensaje (opcional):",
        placeholder="Podés escribir algo acá si querés... 🤫" if primaria
                    else "Escribí lo que quieras contarle al docente...",
        height=120,
        key=f"txt_{pid}_{paso}"
    )

    col1, col2 = st.columns([1, 3])
    if paso > 1:
        if col1.button("← Atrás", key=f"atras_t_{pid}_{paso}"):
            st.session_state[key_paso] -= 1
            st.rerun()
    if col2.button("¡Terminar! 🎉" if primaria else "Finalizar encuesta →",
                   type="primary", use_container_width=True, key=f"sig_t_{pid}_{paso}"):
        st.session_state[key_resp][pid] = {"tipo": "texto_libre", "texto": texto_resp}
        st.session_state[key_paso] += 1
        st.rerun()


# ================================================================
# GUARDAR RESPUESTAS
# ================================================================

def _guardar_y_finalizar(conn, enc_id, alumno_id, respuestas, primaria):
    try:
        with conn.session as s:
            for pid, resp in respuestas.items():
                tipo = resp.get("tipo")
                if tipo in ("eleccion_positiva", "eleccion_negativa"):
                    elegidos = resp.get("elegidos", [])
                    if elegidos:
                        for elid in elegidos:
                            s.execute(text("""
                                INSERT INTO encuesta_respuestas
                                    (encuesta_id, alumno_id, pregunta_id, elegido_id)
                                VALUES (:eid, :aid, :pid, :elid)
                                ON CONFLICT (encuesta_id, alumno_id, pregunta_id) DO NOTHING
                            """), {"eid": enc_id, "aid": alumno_id, "pid": pid, "elid": elid})
                    else:
                        s.execute(text("""
                            INSERT INTO encuesta_respuestas
                                (encuesta_id, alumno_id, pregunta_id)
                            VALUES (:eid, :aid, :pid)
                            ON CONFLICT DO NOTHING
                        """), {"eid": enc_id, "aid": alumno_id, "pid": pid})

                elif tipo == "likert":
                    s.execute(text("""
                        INSERT INTO encuesta_respuestas
                            (encuesta_id, alumno_id, pregunta_id, valor_likert)
                        VALUES (:eid, :aid, :pid, :val)
                        ON CONFLICT (encuesta_id, alumno_id, pregunta_id) DO NOTHING
                    """), {"eid": enc_id, "aid": alumno_id, "pid": pid,
                           "val": resp.get("valor", 3)})

                elif tipo == "texto_libre":
                    txt = resp.get("texto", "").strip()
                    if txt:
                        s.execute(text("""
                            INSERT INTO encuesta_respuestas
                                (encuesta_id, alumno_id, pregunta_id, texto_libre)
                            VALUES (:eid, :aid, :pid, :txt)
                            ON CONFLICT (encuesta_id, alumno_id, pregunta_id) DO NOTHING
                        """), {"eid": enc_id, "aid": alumno_id, "pid": pid, "txt": txt})
            s.commit()

        if primaria:
            st.markdown("""
                <div style="text-align:center; padding:40px 24px;
                            background:linear-gradient(135deg,#e8f4f0,#f0f9f4);
                            border-radius:24px; border:2px solid #b8e8d4;">
                    <div style="font-size:56px; margin-bottom:12px;">🎉</div>
                    <div style="font-size:24px; font-weight:800; color:#1d7a55; margin-bottom:8px;">
                        ¡Muchas gracias!
                    </div>
                    <div style="font-size:15px; color:#0d4a30;">
                        Tus respuestas fueron guardadas. ¡Sos el mejor! ⭐
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.success("✅ Encuesta completada. ¡Gracias por tu participación!")
            st.info("Tus respuestas son confidenciales y contribuyen a mejorar la convivencia.")

    except Exception as e:
        st.error(f"Error al guardar las respuestas: {e}")
