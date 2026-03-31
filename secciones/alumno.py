# secciones/alumno.py
import streamlit as st
import pandas as pd
from datetime import date
from sqlalchemy import text
from utilidades.auth import require_login, get_session

conn = st.connection("postgresql", type="sql")

def calcular_edad(fecha_nac):
    if not fecha_nac:
        return None
    corte = date(date.today().year, 6, 30)
    return corte.year - fecha_nac.year - (
        (corte.month, corte.day) < (fecha_nac.month, fecha_nac.day)
    )

def es_primaria(edad):
    if edad is None:
        return True
    return (edad - 5) <= 7

PRIMARIA_CSS = """<style>
.saludo { font-size: 32px; font-weight: 800; color: #e05c00; }
</style>"""

SECUNDARIA_CSS = """<style>
.saludo { font-size: 24px; font-weight: 700; color: #0f2240; }
</style>"""

def render():
    require_login("alumno")
    usuario    = get_session()
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
                res = s.execute(text("""
                    SELECT a.id, a.nombre, a.apellido, a.grado,
                           a.fecha_nacimiento, a.colegio_id
                    FROM alumnos a WHERE a.colegio_id = :cid LIMIT 1
                """), {"cid": colegio_id})
            row = res.fetchone()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}"); st.stop()

    if not row:
        st.warning("No encontramos tu perfil de alumno. Contactá a tu docente.")
        st.stop()

    alumno = {
        "id": row[0], "nombre": row[1], "apellido": row[2],
        "grado": row[3], "fecha_nac": row[4], "colegio_id": row[5],
    }
    edad     = calcular_edad(alumno["fecha_nac"])
    primaria = es_primaria(edad)

    st.markdown(PRIMARIA_CSS if primaria else SECUNDARIA_CSS, unsafe_allow_html=True)

    if primaria:
        render_primaria(alumno, edad)
    else:
        render_secundaria(alumno, edad)


# ============================================================
# PRIMARIA
# ============================================================
def render_primaria(alumno, edad):
    st.markdown(f"""
        <div style="background:linear-gradient(135deg,#fff8f0,#fff0e8);
                    border-radius:24px; padding:28px 32px; margin-bottom:24px;
                    border:2px solid #ffd4b8;">
            <div style="font-size:48px; margin-bottom:8px;">👋</div>
            <div class="saludo">¡Hola, {alumno['nombre']}!</div>
            <div style="font-size:16px; color:#9a5c00; margin-top:6px;">
                Este es tu espacio seguro 🌟 Grado: <strong>{alumno['grado']}</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "😊 ¿Cómo estoy?",
        "📝 Mi Encuesta",
        "📣 Quiero contar algo",
        "📚 Aprendo",
        "🆘 Pedir ayuda",
        "👤 Mis datos",
    ])

    with tab1:
        _tab_bienestar_primaria(alumno)

    with tab2:
        from secciones.encuesta_alumno import render_tab_encuesta_alumno
        render_tab_encuesta_alumno(conn, alumno, primaria=True)

    with tab3:
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
            texto_rep = st.text_area("Contame qué pasó 👇",
                placeholder="Podés escribir lo que quieras. Nadie más lo va a ver...", height=140)
            if st.form_submit_button("📣 Enviar mensaje secreto",
                                     type="primary", use_container_width=True):
                if not texto_rep.strip():
                    st.warning("¡Escribí algo antes de enviar! 😊")
                else:
                    _guardar_reporte(alumno, texto_rep)

    with tab4:
        _contenido_primaria()

    with tab5:
        _recursos_ayuda(primaria=True)

    with tab6:
        _mis_datos(alumno, edad)


# ============================================================
# SECUNDARIA
# ============================================================
def render_secundaria(alumno, edad):
    st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f2240,#1a3560);
                    border-radius:16px; padding:28px 32px; margin-bottom:24px; color:white;">
            <div style="font-size:13px; text-transform:uppercase; letter-spacing:2px;
                        color:rgba(255,255,255,0.5); margin-bottom:6px;">Mi espacio</div>
            <div class="saludo" style="color:white;">Hola, {alumno['nombre']}</div>
            <div style="font-size:14px; color:rgba(255,255,255,0.6); margin-top:4px;">
                {alumno['grado']} · Este es tu espacio seguro y confidencial.
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💬 Mi bienestar",
        "📝 Mi Encuesta",
        "📣 Reportar situación",
        "📚 Informarme",
        "🆘 Buscar ayuda",
        "👤 Mi perfil",
    ])

    with tab1:
        _tab_bienestar_secundaria(alumno)

    with tab2:
        from secciones.encuesta_alumno import render_tab_encuesta_alumno
        render_tab_encuesta_alumno(conn, alumno, primaria=False)

    with tab3:
        st.subheader("Reportar una situación")
        st.markdown("""
            <div style="background:#f0f4ff; border-left:4px solid #1a56a0;
                        border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:20px;">
                <strong style="color:#0f2240;">🔒 Tu reporte es confidencial</strong><br>
                <span style="font-size:13px; color:#5c5852;">
                    Lo que escribas acá solo lo van a leer tu docente y el/la director/a.
                    Podés reportar algo que te pasó a vos o que viste que le pasó a otro.
                </span>
            </div>
        """, unsafe_allow_html=True)
        with st.form("form_reporte_sec", clear_on_submit=True):
            texto_rep = st.text_area("Describí la situación",
                placeholder="Contá qué pasó, cuándo, y si podés, quiénes estuvieron involucrados...",
                height=160)
            anonimo = st.checkbox("Prefiero que no sepan que fui yo quien reportó", value=False)
            if st.form_submit_button("📣 Enviar reporte confidencial",
                                     type="primary", use_container_width=True):
                if not texto_rep.strip():
                    st.warning("⚠️ Escribí algo antes de enviar.")
                else:
                    _guardar_reporte(alumno, ("[ANÓNIMO] " if anonimo else "") + texto_rep)

    with tab4:
        _contenido_secundaria()

    with tab5:
        _recursos_ayuda(primaria=False)

    with tab6:
        _mis_datos(alumno, edad)


# ============================================================
# BIENESTAR
# ============================================================
def _tab_bienestar_primaria(alumno):
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

    CARITAS = {1:("😢","Muy mal"), 2:("😕","No tan bien"), 3:("😐","Más o menos"),
               4:("🙂","Bien"), 5:("😄","¡Muy bien!")}
    cols = st.columns(5)
    puntaje_sel = None
    for i, (puntaje, (emoji, label)) in enumerate(CARITAS.items()):
        with cols[i]:
            st.markdown(f'<div style="text-align:center; font-size:48px;">{emoji}</div>'
                        f'<div style="text-align:center; font-size:12px; color:#5c5852;">{label}</div>',
                        unsafe_allow_html=True)
            if st.button("Elegir", key=f"carita_{puntaje}", use_container_width=True):
                puntaje_sel = puntaje

    if puntaje_sel:
        emoji_sel, label_sel = CARITAS[puntaje_sel]
        try:
            with conn.session as s:
                s.execute(text("INSERT INTO bienestar_alumnos (alumno_id, puntaje) VALUES (:aid,:p)"),
                          {"aid": alumno["id"], "p": puntaje_sel})
                s.commit()
            st.markdown(f"""
                <div style="text-align:center; background:#e8f4f0; border-radius:16px; padding:20px; margin-top:16px;">
                    <div style="font-size:48px;">{emoji_sel}</div>
                    <div style="font-size:18px; font-weight:700; color:#1d7a55;">¡Gracias! {label_sel}</div>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("**¿Cómo me sentí últimamente?**")
    _mostrar_historial_bienestar(alumno["id"], primaria=True)


def _tab_bienestar_secundaria(alumno):
    st.subheader("¿Cómo te sentís en el aula?")
    OPCIONES = {
        1: "😢  Muy incómodo/a", 2: "😕  Algo incómodo/a",
        3: "😐  Regular",        4: "🙂  Bien",
        5: "😄  Muy bien",
    }
    with st.form("form_bienestar_sec", clear_on_submit=True):
        puntaje = st.radio("Seleccioná cómo te sentís hoy:",
                           options=list(OPCIONES.keys()),
                           format_func=lambda x: OPCIONES[x],
                           horizontal=False, index=2)
        if st.form_submit_button("Registrar", type="primary", use_container_width=True):
            try:
                with conn.session as s:
                    s.execute(text("INSERT INTO bienestar_alumnos (alumno_id, puntaje) VALUES (:aid,:p)"),
                              {"aid": alumno["id"], "p": puntaje})
                    s.commit()
                st.success(f"✅ Registrado.")
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Mi historial de bienestar")
    st.caption("Mostramos la tendencia, no los valores exactos.")
    _mostrar_historial_bienestar(alumno["id"], primaria=False)


# ============================================================
# FUNCIONES COMPARTIDAS
# ============================================================
def _guardar_reporte(alumno, texto):
    try:
        with conn.session as s:
            s.execute(text("INSERT INTO reportes_alumnos (alumno_id, colegio_id, texto) VALUES (:aid,:cid,:txt)"),
                      {"aid": alumno["id"], "cid": alumno["colegio_id"], "txt": texto.strip()})
            s.commit()
        st.success("✅ Tu mensaje fue enviado. Un adulto de confianza lo va a leer pronto.")
        st.balloons()
    except Exception as e:
        st.error(f"Error: {e}")


def _mostrar_historial_bienestar(alumno_id, primaria):
    try:
        with conn.session as s:
            res = s.execute(text("""
                SELECT DATE(creado_en) AS fecha, ROUND(AVG(puntaje),1) AS promedio
                FROM bienestar_alumnos
                WHERE alumno_id = :aid AND creado_en >= NOW() - INTERVAL '30 days'
                GROUP BY DATE(creado_en) ORDER BY fecha
            """), {"aid": alumno_id})
            df_b = pd.DataFrame(res.fetchall(), columns=res.keys())

        if df_b.empty:
            msg = "Todavía no tenés registros. ¡Empezá hoy!" if primaria else "No hay registros de los últimos 30 días."
            st.info(msg); return

        df_b['fecha'] = pd.to_datetime(df_b['fecha'])
        df_b = df_b.set_index('fecha')

        if primaria:
            EMOJI_MAP = {1:"😢", 2:"😕", 3:"😐", 4:"🙂", 5:"😄"}
            cols = st.columns(min(len(df_b), 7))
            for i, (fecha, row) in enumerate(df_b.tail(7).iterrows()):
                emoji = EMOJI_MAP.get(round(row['promedio']), "😐")
                with cols[i % len(cols)]:
                    st.markdown(f"""
                        <div style="text-align:center; background:white; border-radius:12px;
                                    padding:10px; border:1px solid #ebe9e4;">
                            <div style="font-size:28px;">{emoji}</div>
                            <div style="font-size:10px; color:#9a9690;">{fecha.strftime('%d/%m')}</div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.line_chart(df_b['promedio'], height=160)
            st.caption("Escala: 1 = Muy mal · 5 = Muy bien")
    except Exception as e:
        st.error(f"Error: {e}")


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

    try:
        with conn.session as s:
            res = s.execute(text("""
                SELECT t.nombre, t.apellido, t.telefono, t.email, at2.relacion
                FROM tutores t
                INNER JOIN alumno_tutores at2 ON at2.tutor_id = t.id
                WHERE at2.alumno_id = :aid ORDER BY at2.es_principal DESC
            """), {"aid": alumno["id"]})
            df_tut = pd.DataFrame(res.fetchall(), columns=res.keys())

        with col2:
            st.markdown("""
                <div style="background:white; border:1px solid #ebe9e4; border-radius:14px; padding:20px;">
                    <div style="font-size:11px; text-transform:uppercase; letter-spacing:1px;
                                color:#9a9690; margin-bottom:12px;">Mis tutores</div>
            """, unsafe_allow_html=True)
            if not df_tut.empty:
                for _, t in df_tut.iterrows():
                    st.markdown(f"""
                        <div style="margin-bottom:10px;">
                            <strong style="color:#0f2240;">{t['relacion']}: {t['apellido']}, {t['nombre']}</strong><br>
                            <span style="font-size:13px; color:#5c5852;">
                                📞 {t['telefono'] or '—'} &nbsp;·&nbsp; ✉️ {t['email'] or '—'}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#9a9690;'>No hay tutores vinculados.</span>",
                            unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")

    st.markdown("---")
    from utilidades.cambiar_pass_widget import render_cambiar_password
    render_cambiar_password()


def _contenido_primaria():
    st.markdown('<div style="font-size:22px; font-weight:800; color:#e05c00; text-align:center; margin-bottom:20px;">📚 ¿Qué es el bullying?</div>',
                unsafe_allow_html=True)
    tarjetas = [
        ("🤜","¿Qué es el bullying?","Es cuando alguien molesta, golpea o se burla de otra persona muchas veces. ¡No está bien!"),
        ("🆘","¿Qué hago si me pasa?","Contale a un adulto de confianza: tu maestra, tus papás o el director. ¡No estás solo/a!"),
        ("👀","¿Y si le pasa a otro?","Si ves que molestan a alguien, podés ayudar: avisale a un adulto o acompañá a esa persona."),
        ("📵","En internet también pasa","Si alguien te molesta por WhatsApp o redes, guardá el mensaje y contáselo a un adulto."),
    ]
    col1, col2 = st.columns(2)
    for i, (icono, titulo, texto) in enumerate(tarjetas):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
                <div style="background:white; border-radius:20px; padding:20px;
                            margin-bottom:16px; border:2px solid #ffd4b8;">
                    <div style="font-size:36px; margin-bottom:8px;">{icono}</div>
                    <div style="font-size:16px; font-weight:800; color:#e05c00; margin-bottom:8px;">{titulo}</div>
                    <div style="font-size:14px; color:#5c5852; line-height:1.6;">{texto}</div>
                </div>
            """, unsafe_allow_html=True)


def _contenido_secundaria():
    st.subheader("Informarme sobre bullying")
    recursos = [
        ("🔍","¿Qué es el bullying y qué no?","Entendé la diferencia entre un conflicto puntual y el acoso sistemático.","#1a56a0"),
        ("🛡️","Si estoy siendo acosado/a","Pasos concretos y seguros para pedir ayuda sin exponerte más.","#1d7a55"),
        ("👥","El rol del testigo","Cómo actuar si ves que acosan a alguien sin ponerte en riesgo.","#5b3fa0"),
        ("📱","Ciberbullying","Qué hacer si el acoso pasa en redes, cómo bloquear y reportar.","#d4580a"),
    ]
    col1, col2 = st.columns(2)
    for i, (icono, titulo, desc, color) in enumerate(recursos):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
                <div style="background:white; border:1px solid #ebe9e4; border-radius:14px;
                            padding:20px; margin-bottom:16px;">
                    <div style="font-size:28px; margin-bottom:10px;">{icono}</div>
                    <div style="font-size:15px; font-weight:700; color:#0f2240; margin-bottom:6px;">{titulo}</div>
                    <div style="font-size:13px; color:#5c5852; line-height:1.6; margin-bottom:12px;">{desc}</div>
                    <span style="background:{color}18; color:{color}; font-size:11px;
                                 font-weight:700; padding:3px 10px; border-radius:20px;">Próximamente →</span>
                </div>
            """, unsafe_allow_html=True)


def _recursos_ayuda(primaria):
    if primaria:
        st.markdown("""
            <div style="text-align:center; margin-bottom:20px;">
                <div style="font-size:48px;">🆘</div>
                <div style="font-size:22px; font-weight:800; color:#e05c00;">¿Necesitás ayuda ahora?</div>
                <div style="font-size:14px; color:#9a5c00; margin-top:4px;">Hablá con alguna de estas personas 👇</div>
            </div>
        """, unsafe_allow_html=True)
        for icono, nombre, desc in [
            ("👩‍🏫","Tu docente","La persona que da clases en tu grado"),
            ("🏫","El director/a","El/la responsable de tu escuela"),
            ("👨‍👩‍👧","Tus papás o tutor","Un adulto de confianza en tu casa"),
        ]:
            st.markdown(f"""
                <div style="background:white; border-radius:20px; padding:20px;
                            margin-bottom:12px; border:2px solid #ffd4b8;">
                    <div style="font-size:40px;">{icono}</div>
                    <div style="font-size:18px; font-weight:800; color:#e05c00;">{nombre}</div>
                    <div style="font-size:13px; color:#9a5c00;">{desc}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.subheader("Recursos y líneas de ayuda")
        st.markdown('<div style="background:#fde8d0; border-left:4px solid #d4580a; border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:20px;"><strong style="color:#6b3000;">Si estás en peligro inmediato, llamá al 911.</strong></div>',
                    unsafe_allow_html=True)
        for icono, nombre, desc in [
            ("👩‍🏫","Tu docente o tutor/a","Primera línea de apoyo dentro de la escuela."),
            ("🏫","Gabinete o equipo de orientación","Profesionales de tu institución."),
            ("📞","Línea 102 — Infancia y Adolescencia","Llamada gratuita, disponible las 24hs en Argentina."),
            ("💬","Centro de Asistencia al Suicida — 135","Si sentís que no podés más, hay alguien que escucha. Gratis, 24hs."),
        ]:
            st.markdown(f"""
                <div style="background:white; border:1px solid #ebe9e4; border-radius:14px;
                            padding:18px 20px; margin-bottom:12px;">
                    <div style="font-size:28px;">{icono}</div>
                    <div style="font-size:15px; font-weight:700; color:#0f2240;">{nombre}</div>
                    <div style="font-size:13px; color:#5c5852; margin-top:2px;">{desc}</div>
                </div>
            """, unsafe_allow_html=True)
