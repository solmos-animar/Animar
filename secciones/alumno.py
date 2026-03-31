# secciones/alumno.py
import streamlit as st
import pandas as pd
from datetime import date
from sqlalchemy import text
from utilidades.auth import require_login, get_session

conn = st.connection("postgresql", type="sql")

# ============================================================
# HELPERS
# ============================================================
def calcular_edad(fecha_nac):
    if not fecha_nac:
        return None
    corte = date(date.today().year, 6, 30)
    edad = corte.year - fecha_nac.year - (
        (corte.month, corte.day) < (fecha_nac.month, fecha_nac.day)
    )
    return edad

def es_primaria(edad):
    if edad is None:
        return True
    grado_escolar = edad - 5      # 6 años → 1°, 12 años → 7°
    return grado_escolar <= 7     # 1° a 7° = primaria, 8° en adelante = secundaria
# ============================================================
# ESTILOS POR NIVEL
# ============================================================
PRIMARIA_CSS = """
<style>
.nivel-card {
    border-radius: 20px !important;
    font-family: 'Comic Sans MS', 'Chalkboard SE', cursive !important;
}
.saludo { font-size: 32px; font-weight: 800; color: #e05c00; }
.emoji-big { font-size: 48px; }
.btn-ayuda {
    background: #ff6b35 !important;
    color: white !important;
    font-size: 18px !important;
    border-radius: 30px !important;
    padding: 16px 32px !important;
}
</style>"""

SECUNDARIA_CSS = """
<style>
.saludo { font-size: 24px; font-weight: 700; color: #0f2240; }
.emoji-big { font-size: 32px; }
</style>"""

# ============================================================
# RENDER PRINCIPAL
# ============================================================
def render():
    require_login("alumno")
    usuario = get_session()

    # Buscar datos del alumno por persona_id o por email como fallback
    alumno_id  = usuario.get("persona_id")
    colegio_id = usuario.get("colegio_id")

    try:
        with conn.session as s:
            if alumno_id:
                res = s.execute(text("""
                    SELECT a.id, a.nombre, a.apellido, a.grado,
                           a.fecha_nacimiento, a.colegio_id
                    FROM alumnos a WHERE a.id = :id
                """), {"id": alumno_id})
            else:
                # Fallback: buscar por colegio (demo)
                res = s.execute(text("""
                    SELECT a.id, a.nombre, a.apellido, a.grado,
                           a.fecha_nacimiento, a.colegio_id
                    FROM alumnos a WHERE a.colegio_id = :cid LIMIT 1
                """), {"cid": colegio_id})
            row = res.fetchone()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        st.stop()

    if not row:
        st.warning("No encontramos tu perfil de alumno. Contactá a tu docente.")
        st.stop()

    alumno = {
        "id":        row[0],
        "nombre":    row[1],
        "apellido":  row[2],
        "grado":     row[3],
        "fecha_nac": row[4],
        "colegio_id":row[5],
    }
    edad    = calcular_edad(alumno["fecha_nac"])
    primaria = es_primaria(edad)

    # Inyectar CSS según nivel
    st.markdown(PRIMARIA_CSS if primaria else SECUNDARIA_CSS, unsafe_allow_html=True)

    # ============================================================
    # RENDER SEGÚN NIVEL
    # ============================================================
    if primaria:
        render_primaria(alumno, edad)
    else:
        render_secundaria(alumno, edad)


# ============================================================
# VERSIÓN PRIMARIA (≤ 12 años)
# ============================================================
def render_primaria(alumno, edad):
    nombre = alumno["nombre"]

    st.markdown(f"""
        <div style="background:linear-gradient(135deg,#fff8f0,#fff0e8);
                    border-radius:24px; padding:28px 32px; margin-bottom:24px;
                    border:2px solid #ffd4b8;">
            <div style="font-size:48px; margin-bottom:8px;">👋</div>
            <div class="saludo">¡Hola, {nombre}!</div>
            <div style="font-size:16px; color:#9a5c00; margin-top:6px;">
                Este es tu espacio seguro 🌟 Grado: <strong>{alumno['grado']}</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "😊 ¿Cómo estoy?",
        "📣 Quiero contar algo",
        "📚 Aprendo",
        "🆘 Pedir ayuda",
        "👤 Mis datos",
    ])

    # ---- TAB 1: BIENESTAR ----
    with tab1:
        st.markdown("""
            <div style="text-align:center; padding:16px 0 8px;">
                <div style="font-size:24px; font-weight:800; color:#e05c00;">
                    ¿Cómo te sentís hoy en la escuela?
                </div>
                <div style="font-size:15px; color:#9a5c00; margin-top:4px;">
                    Tocá la carita que mejor te representa 👇
                </div>
            </div>
        """, unsafe_allow_html=True)

        CARITAS = {
            1: ("😢", "Muy mal"),
            2: ("😕", "No tan bien"),
            3: ("😐", "Más o menos"),
            4: ("🙂", "Bien"),
            5: ("😄", "¡Muy bien!"),
        }

        cols = st.columns(5)
        puntaje_sel = None
        for i, (puntaje, (emoji, label)) in enumerate(CARITAS.items()):
            with cols[i]:
                st.markdown(f"""
                    <div style="text-align:center; font-size:48px; margin-bottom:4px;">
                        {emoji}
                    </div>
                    <div style="text-align:center; font-size:12px; color:#5c5852;">
                        {label}
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Elegir", key=f"carita_{puntaje}",
                             use_container_width=True):
                    puntaje_sel = puntaje

        if puntaje_sel:
            emoji_sel, label_sel = CARITAS[puntaje_sel]
            try:
                with conn.session as s:
                    s.execute(text("""
                        INSERT INTO bienestar_alumnos (alumno_id, puntaje)
                        VALUES (:aid, :p)
                    """), {"aid": alumno["id"], "p": puntaje_sel})
                    s.commit()
                st.markdown(f"""
                    <div style="text-align:center; background:#e8f4f0;
                                border-radius:16px; padding:20px; margin-top:16px;">
                        <div style="font-size:48px;">{emoji_sel}</div>
                        <div style="font-size:18px; font-weight:700; color:#1d7a55;">
                            ¡Gracias por contarnos! {label_sel}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"No pudimos guardar tu respuesta: {e}")

        # Historial visual (sin valores exactos)
        st.markdown("---")
        st.markdown("**¿Cómo me sentí últimamente?**")
        _mostrar_historial_bienestar(alumno["id"], primaria=True)

    # ---- TAB 2: REPORTE ----
    with tab2:
        st.markdown("""
            <div style="background:#fff0e8; border-radius:20px; padding:24px;
                        text-align:center; margin-bottom:20px;">
                <div style="font-size:48px;">🤫</div>
                <div style="font-size:20px; font-weight:800; color:#e05c00; margin:8px 0;">
                    ¿Querés contarle algo a un adulto?
                </div>
                <div style="font-size:14px; color:#9a5c00;">
                    Lo que escribas acá es <strong>secreto</strong>.<br>
                    Solo lo va a leer tu docente y el director/a. ¡Nadie más!
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.form("form_reporte_pri", clear_on_submit=True):
            texto_rep = st.text_area(
                "Contame qué pasó 👇",
                placeholder="Podés escribir lo que quieras. Nadie más lo va a ver...",
                height=140
            )
            enviado = st.form_submit_button(
                "📣 Enviar mensaje secreto",
                type="primary",
                use_container_width=True
            )
            if enviado:
                if not texto_rep.strip():
                    st.warning("¡Escribí algo antes de enviar! 😊")
                else:
                    _guardar_reporte(alumno, texto_rep)

    # ---- TAB 3: CONTENIDO ----
    with tab3:
        _contenido_primaria()

    # ---- TAB 4: AYUDA ----
    with tab4:
        _recursos_ayuda(primaria=True)

    # ---- TAB 5: MIS DATOS ----
    with tab5:
        _mis_datos(alumno, edad)


# ============================================================
# VERSIÓN SECUNDARIA (> 12 años)
# ============================================================
def render_secundaria(alumno, edad):
    nombre = alumno["nombre"]

    st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f2240,#1a3560);
                    border-radius:16px; padding:28px 32px; margin-bottom:24px; color:white;">
            <div style="font-size:13px; text-transform:uppercase; letter-spacing:2px;
                        color:rgba(255,255,255,0.5); margin-bottom:6px;">Mi espacio</div>
            <div class="saludo" style="color:white;">Hola, {nombre}</div>
            <div style="font-size:14px; color:rgba(255,255,255,0.6); margin-top:4px;">
                {alumno['grado']} · Este es tu espacio seguro y confidencial.
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 Mi bienestar",
        "📣 Reportar situación",
        "📚 Informarme",
        "🆘 Buscar ayuda",
        "👤 Mi perfil",
    ])

    # ---- TAB 1: BIENESTAR ----
    with tab1:
        st.subheader("¿Cómo te sentís en el aula?")
        st.markdown("""
            <p style="color:#5c5852; font-size:14px;">
                Registrá cómo te sentís hoy. Esta información es confidencial
                y ayuda a tu docente a entender el clima del grupo.
            </p>
        """, unsafe_allow_html=True)

        OPCIONES = {
            1: "😢  Muy incómodo/a — me siento excluido/a o mal",
            2: "😕  Algo incómodo/a — hay tensión o situaciones que no me gustan",
            3: "😐  Regular — ni bien ni mal",
            4: "🙂  Bien — me siento cómodo/a con mis compañeros",
            5: "😄  Muy bien — me siento integrado/a y a gusto",
        }

        with st.form("form_bienestar_sec", clear_on_submit=True):
            puntaje = st.radio(
                "Seleccioná cómo te sentís hoy en el aula:",
                options=list(OPCIONES.keys()),
                format_func=lambda x: OPCIONES[x],
                horizontal=False,
                index=2
            )
            enviado_b = st.form_submit_button("Registrar cómo me siento",
                                               type="primary",
                                               use_container_width=True)
            if enviado_b:
                try:
                    with conn.session as s:
                        s.execute(text("""
                            INSERT INTO bienestar_alumnos (alumno_id, puntaje)
                            VALUES (:aid, :p)
                        """), {"aid": alumno["id"], "p": puntaje})
                        s.commit()
                    st.success(f"✅ Registrado. {OPCIONES[puntaje]}")
                except Exception as e:
                    st.error(f"Error: {e}")

        st.markdown("---")
        st.subheader("Mi historial de bienestar")
        st.caption("Mostramos la tendencia, no los valores exactos.")
        _mostrar_historial_bienestar(alumno["id"], primaria=False)

    # ---- TAB 2: REPORTE ----
    with tab2:
        st.subheader("Reportar una situación")
        st.markdown("""
            <div style="background:#f0f4ff; border-left:4px solid #1a56a0;
                        border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:20px;">
                <strong style="color:#0f2240;">🔒 Tu reporte es confidencial</strong><br>
                <span style="font-size:13px; color:#5c5852;">
                    Lo que escribas acá solo lo van a leer tu docente y el/la director/a.
                    Nunca se va a compartir con otros alumnos.
                    Podés reportar algo que te pasó a vos o que viste que le pasó a otro.
                </span>
            </div>
        """, unsafe_allow_html=True)

        with st.form("form_reporte_sec", clear_on_submit=True):
            texto_rep = st.text_area(
                "Describí la situación",
                placeholder="Contá qué pasó, cuándo, y si podés, quiénes estuvieron involucrados...",
                height=160
            )
            anonimo = st.checkbox(
                "Prefiero que no sepan que fui yo quien reportó",
                value=False,
                help="Si marcás esta opción, el docente verá el reporte pero no tu nombre."
            )
            enviado_r = st.form_submit_button("📣 Enviar reporte confidencial",
                                               type="primary",
                                               use_container_width=True)
            if enviado_r:
                if not texto_rep.strip():
                    st.warning("⚠️ Escribí algo antes de enviar.")
                else:
                    texto_final = texto_rep
                    if anonimo:
                        texto_final = "[ANÓNIMO] " + texto_rep
                    _guardar_reporte(alumno, texto_final)

    # ---- TAB 3: CONTENIDO ----
    with tab3:
        _contenido_secundaria()

    # ---- TAB 4: AYUDA ----
    with tab4:
        _recursos_ayuda(primaria=False)

    # ---- TAB 5: MI PERFIL ----
    with tab5:
        _mis_datos(alumno, edad)


# ============================================================
# FUNCIONES COMPARTIDAS
# ============================================================

def _guardar_reporte(alumno, texto):
    try:
        with conn.session as s:
            s.execute(text("""
                INSERT INTO reportes_alumnos (alumno_id, colegio_id, texto)
                VALUES (:aid, :cid, :txt)
            """), {
                "aid": alumno["id"],
                "cid": alumno["colegio_id"],
                "txt": texto.strip()
            })
            s.commit()
        st.success("✅ Tu mensaje fue enviado. Un adulto de confianza lo va a leer pronto.")
        st.balloons()
    except Exception as e:
        st.error(f"No pudimos enviar tu mensaje: {e}")


def _mostrar_historial_bienestar(alumno_id, primaria):
    try:
        with conn.session as s:
            res = s.execute(text("""
                SELECT DATE(creado_en) AS fecha, ROUND(AVG(puntaje),1) AS promedio
                FROM bienestar_alumnos
                WHERE alumno_id = :aid
                  AND creado_en >= NOW() - INTERVAL '30 days'
                GROUP BY DATE(creado_en)
                ORDER BY fecha
            """), {"aid": alumno_id})
            df_b = pd.DataFrame(res.fetchall(), columns=res.keys())

        if df_b.empty:
            if primaria:
                st.markdown("""
                    <div style="text-align:center; padding:20px; color:#9a9690;">
                        <div style="font-size:36px;">📊</div>
                        Todavía no tenés registros. ¡Empezá hoy!
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Todavía no hay registros de los últimos 30 días.")
            return

        df_b['fecha'] = pd.to_datetime(df_b['fecha'])
        df_b = df_b.set_index('fecha')

        if primaria:
            # Versión con emojis por valor promedio
            EMOJI_MAP = {1:"😢", 2:"😕", 3:"😐", 4:"🙂", 5:"😄"}
            cols = st.columns(min(len(df_b), 7))
            for i, (fecha, row) in enumerate(df_b.tail(7).iterrows()):
                prom = round(row['promedio'])
                emoji = EMOJI_MAP.get(prom, "😐")
                with cols[i % len(cols)]:
                    st.markdown(f"""
                        <div style="text-align:center; background:white;
                                    border-radius:12px; padding:10px; border:1px solid #ebe9e4;">
                            <div style="font-size:28px;">{emoji}</div>
                            <div style="font-size:10px; color:#9a9690;">
                                {fecha.strftime('%d/%m')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            # Gráfico de línea para secundaria
            st.line_chart(df_b['promedio'], height=160)
            st.caption("Escala: 1 = Muy mal · 5 = Muy bien")

    except Exception as e:
        st.error(f"Error al cargar historial: {e}")


def _mis_datos(alumno, edad):
    st.subheader("Mis datos")

    col1, col2 = st.columns(2)
    col1.markdown(f"""
        <div style="background:white; border:1px solid #ebe9e4; border-radius:14px; padding:20px;">
            <div style="font-size:11px; text-transform:uppercase; letter-spacing:1px;
                        color:#9a9690; margin-bottom:12px;">Mi información</div>
            <div style="font-size:22px; font-weight:700; color:#0f2240;">
                {alumno['apellido']}, {alumno['nombre']}
            </div>
            <div style="font-size:14px; color:#5c5852; margin-top:8px;">
                📚 Grado: <strong>{alumno['grado']}</strong><br>
                🎂 Edad: <strong>{edad} años</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Tutores vinculados
    try:
        with conn.session as s:
            res = s.execute(text("""
                SELECT t.nombre, t.apellido, t.telefono, t.email, at2.relacion
                FROM tutores t
                INNER JOIN alumno_tutores at2 ON at2.tutor_id = t.id
                WHERE at2.alumno_id = :aid
                ORDER BY at2.es_principal DESC
            """), {"aid": alumno["id"]})
            df_tut = pd.DataFrame(res.fetchall(), columns=res.keys())

        with col2:
            st.markdown("""
                <div style="background:white; border:1px solid #ebe9e4;
                            border-radius:14px; padding:20px;">
                    <div style="font-size:11px; text-transform:uppercase; letter-spacing:1px;
                                color:#9a9690; margin-bottom:12px;">Mis tutores</div>
            """, unsafe_allow_html=True)
            if not df_tut.empty:
                for _, t in df_tut.iterrows():
                    st.markdown(f"""
                        <div style="margin-bottom:10px;">
                            <strong style="color:#0f2240;">
                                {t['relacion']}: {t['apellido']}, {t['nombre']}
                            </strong><br>
                            <span style="font-size:13px; color:#5c5852;">
                                📞 {t['telefono'] or '—'} &nbsp;·&nbsp;
                                ✉️ {t['email'] or '—'}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#9a9690;'>No hay tutores vinculados.</span>",
                            unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")


def _contenido_primaria():
    st.markdown("""
        <div style="font-size:22px; font-weight:800; color:#e05c00;
                    text-align:center; margin-bottom:20px;">
            📚 ¿Qué es el bullying?
        </div>
    """, unsafe_allow_html=True)

    tarjetas = [
        ("🤜", "¿Qué es el bullying?",
         "Es cuando alguien molesta, golpea o se burla de otra persona muchas veces. ¡No está bien!"),
        ("🆘", "¿Qué hago si me pasa?",
         "Contale a un adulto de confianza: tu maestra, tus papás o el director. ¡No estás solo/a!"),
        ("👀", "¿Y si le pasa a otro?",
         "Si ves que molestan a alguien, podés ayudar: avisale a un adulto o acompañá a esa persona."),
        ("📵", "En internet también pasa",
         "Si alguien te molesta por WhatsApp o redes, guardá el mensaje y contáselo a un adulto."),
    ]

    col1, col2 = st.columns(2)
    for i, (icono, titulo, texto) in enumerate(tarjetas):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
                <div style="background:white; border-radius:20px; padding:20px;
                            margin-bottom:16px; border:2px solid #ffd4b8;
                            box-shadow:0 4px 12px rgba(224,92,0,0.08);">
                    <div style="font-size:36px; margin-bottom:8px;">{icono}</div>
                    <div style="font-size:16px; font-weight:800; color:#e05c00;
                                margin-bottom:8px;">{titulo}</div>
                    <div style="font-size:14px; color:#5c5852; line-height:1.6;">{texto}</div>
                </div>
            """, unsafe_allow_html=True)


def _contenido_secundaria():
    st.subheader("Informarme sobre bullying")

    recursos = [
        ("🔍", "¿Qué es el bullying y qué no?",
         "Entendé la diferencia entre un conflicto puntual y el acoso sistemático.",
         "#1a56a0"),
        ("🛡️", "Si estoy siendo acosado/a",
         "Pasos concretos y seguros para pedir ayuda sin exponerte más.",
         "#1d7a55"),
        ("👥", "El rol del testigo",
         "Cómo actuar si ves que acosan a alguien sin ponerte en riesgo.",
         "#5b3fa0"),
        ("📱", "Ciberbullying",
         "Qué hacer si el acoso pasa en redes, cómo bloquear y reportar.",
         "#d4580a"),
    ]

    col1, col2 = st.columns(2)
    for i, (icono, titulo, desc, color) in enumerate(recursos):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
                <div style="background:white; border:1px solid #ebe9e4; border-radius:14px;
                            padding:20px; margin-bottom:16px;
                            box-shadow:0 2px 8px rgba(15,34,64,0.06);">
                    <div style="font-size:28px; margin-bottom:10px;">{icono}</div>
                    <div style="font-size:15px; font-weight:700; color:#0f2240;
                                margin-bottom:6px;">{titulo}</div>
                    <div style="font-size:13px; color:#5c5852; line-height:1.6;
                                margin-bottom:12px;">{desc}</div>
                    <span style="background:{color}18; color:{color}; font-size:11px;
                                 font-weight:700; padding:3px 10px; border-radius:20px;">
                        Próximamente →
                    </span>
                </div>
            """, unsafe_allow_html=True)


def _recursos_ayuda(primaria):
    if primaria:
        st.markdown("""
            <div style="text-align:center; margin-bottom:20px;">
                <div style="font-size:48px;">🆘</div>
                <div style="font-size:22px; font-weight:800; color:#e05c00;">
                    ¿Necesitás ayuda ahora?
                </div>
                <div style="font-size:14px; color:#9a5c00; margin-top:4px;">
                    Hablá con alguna de estas personas 👇
                </div>
            </div>
        """, unsafe_allow_html=True)

        contactos = [
            ("👩‍🏫", "Tu docente", "La persona que da clases en tu grado"),
            ("🏫", "El director/a", "El/la responsable de tu escuela"),
            ("👨‍👩‍👧", "Tus papás o tutor", "Un adulto de confianza en tu casa"),
        ]
        for icono, nombre, desc in contactos:
            st.markdown(f"""
                <div style="background:white; border-radius:20px; padding:20px;
                            margin-bottom:12px; border:2px solid #ffd4b8;
                            display:flex; align-items:center; gap:16px;">
                    <div style="font-size:40px;">{icono}</div>
                    <div>
                        <div style="font-size:18px; font-weight:800; color:#e05c00;">
                            {nombre}
                        </div>
                        <div style="font-size:13px; color:#9a5c00;">{desc}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    else:
        st.subheader("Recursos y líneas de ayuda")
        st.markdown("""
            <div style="background:#fde8d0; border-left:4px solid #d4580a;
                        border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:20px;">
                <strong style="color:#6b3000;">Si estás en peligro inmediato, llamá al 911.</strong>
            </div>
        """, unsafe_allow_html=True)

        recursos = [
            ("👩‍🏫", "Tu docente o tutor/a", "Primera línea de apoyo dentro de la escuela."),
            ("🏫", "Gabinete o equipo de orientación", "Profesionales de tu institución."),
            ("📞", "Línea 102 — Infancia y Adolescencia",
             "Llamada gratuita, disponible las 24hs en Argentina."),
            ("💬", "Centro de Asistencia al Suicida — 135",
             "Si sentís que no podés más, hay alguien que escucha. Gratis, 24hs."),
        ]

        for icono, nombre, desc in recursos:
            st.markdown(f"""
                <div style="background:white; border:1px solid #ebe9e4; border-radius:14px;
                            padding:18px 20px; margin-bottom:12px;
                            display:flex; align-items:flex-start; gap:16px;">
                    <div style="font-size:28px; flex-shrink:0;">{icono}</div>
                    <div>
                        <div style="font-size:15px; font-weight:700; color:#0f2240;">
                            {nombre}
                        </div>
                        <div style="font-size:13px; color:#5c5852; margin-top:2px;">
                            {desc}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
