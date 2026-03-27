
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import ALUMNOS

# ---------------------------------------------------------------------------
# Datos locales
# ---------------------------------------------------------------------------

COMPAÑEROS = [a["nombre"] for a in ALUMNOS if a["nombre"] != "Lucas Martínez"]

ARTICULOS = [
    {
        "titulo": "¿Qué es el bullying y cómo reconocerlo?",
        "tipo": "Artículo",
        "tiempo": "4 min",
        "contenido": """
El **bullying** es cualquier comportamiento agresivo y repetido que una persona usa para 
lastimar a otra. Puede ser físico, verbal o por redes sociales (cyberbullying).

**Señales de que alguien puede estar siendo víctima:**
- Evita ir al colegio
- Está triste, nervioso o asustado sin razón aparente
- Le desaparecen cosas o llega a casa con cosas rotas
- Tiene pocos amigos o se aísla

**¿Qué podés hacer si ves o vivís bullying?**
- Hablá con tu docente o algún adulto de confianza
- No te quedes solo/a con esto
- Usá el mensaje confidencial de esta plataforma para contarle a tu docente
        """,
    },
    {
        "titulo": "Cómo pedir ayuda si estás pasando mal",
        "tipo": "Guía",
        "tiempo": "3 min",
        "contenido": """
Pedir ayuda **no es de débiles** — es lo más valiente que podés hacer.

**Pasos para pedir ayuda:**
1. Identificá a alguien de confianza (docente, familiar, preceptor)
2. Buscá un momento tranquilo para hablar
3. Contá lo que está pasando, aunque sea difícil
4. Si no te animás a hablar, escribilo — usá el mensaje confidencial de esta app

Recordá: **merecés estar bien**. Nadie tiene que aguantar el maltrato.
        """,
    },
    {
        "titulo": "Ser buen compañero/a",
        "tipo": "Artículo",
        "tiempo": "5 min",
        "contenido": """
Ser buen compañero/a no requiere grandes gestos. Las **pequeñas acciones** hacen la diferencia:

- Saludá a todos cuando llegás al aula
- Incluí a quien está solo en las actividades
- Si ves que alguien está triste, preguntale cómo está
- No te rías si alguien se equivoca
- Defendé a quien está siendo maltratado

**El efecto del testigo:** cuando alguien interviene o busca ayuda, el bullying se detiene 
más rápido. Vos podés ser ese alguien.
        """,
    },
    {
        "titulo": "Emociones difíciles: está bien sentirse así",
        "tipo": "Artículo",
        "tiempo": "4 min",
        "contenido": """
Enojo, tristeza, miedo, vergüenza... todas estas emociones son **normales** y válidas.

Lo importante no es no sentirlas, sino aprender a reconocerlas y expresarlas de forma sana.

**Técnicas que pueden ayudar:**
- Respirá profundo y contá hasta 10 cuando estés enojado/a
- Escribí en un diario lo que sentís
- Hablá con alguien de confianza
- Hacé actividad física para liberar tensión

Si sentís que las emociones te desbordan con frecuencia, pedile ayuda a tu docente 
o al equipo de orientación escolar.
        """,
    },
]

# ---------------------------------------------------------------------------
# Sub-páginas
# ---------------------------------------------------------------------------

def render_home():
    """Página de bienvenida del estudiante."""
    user = st.session_state.user
    st.title(f"👋 Hola, {user['name'].split()[0]}!")
    st.markdown("Bienvenido/a a ConVivir — tu espacio para mejorar la convivencia en el aula.")

    # Estado del aula
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 🚪 Tu aula: 3° A Primaria")
            st.markdown("**Estado:** 🟢 Habilitada")
            st.markdown("**Encuesta sociométrica:** Disponible")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📝 Completar encuesta", type="primary", use_container_width=True):
                st.session_state.current_page = "student_encuesta"
                st.rerun()

    st.markdown("---")

    # Secciones disponibles
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("### 📝 Encuesta")
            st.markdown("Respondé la encuesta sobre tus compañeros de forma anónima y confidencial.")
            if st.button("Ir a la encuesta", use_container_width=True):
                st.session_state.current_page = "student_encuesta"
                st.rerun()
    with col2:
        with st.container(border=True):
            st.markdown("### 📚 Contenido")
            st.markdown("Artículos y guías sobre convivencia, bullying y cómo pedir ayuda.")
            if st.button("Ver contenido", use_container_width=True):
                st.session_state.current_page = "student_contenido"
                st.rerun()
    with col3:
        with st.container(border=True):
            st.markdown("### 💬 Mensaje al docente")
            st.markdown("Enviá un mensaje confidencial a tu docente si necesitás hablar de algo.")
            if st.button("Enviar mensaje", use_container_width=True):
                st.session_state.show_mensaje = True
                st.rerun()

    # Panel de mensaje confidencial (se muestra inline si está activo)
    if st.session_state.get("show_mensaje"):
        st.markdown("---")
        st.subheader("💬 Mensaje confidencial al docente")
        st.info("Este mensaje solo lo va a ver tu docente. Es completamente confidencial.")
        mensaje = st.text_area(
            "Escribí tu mensaje aquí:",
            placeholder="Podés contar lo que está pasando...",
        )
        if st.button("Enviar", type="primary"):
            if mensaje:
                st.success("✅ Tu mensaje fue enviado. Tu docente lo va a recibir en privado.")
                st.session_state.show_mensaje = False
            else:
                st.error("Escribí algo antes de enviar.")


def render_encuesta():
    """Encuesta sociométrica del estudiante."""
    st.title("📝 Encuesta Sociométrica")

    with st.container(border=True):
        st.markdown(
            """
            <div style='background:#e8f0fe;border-left:4px solid #1a56a0;border-radius:8px;padding:14px 18px;'>
              <strong>🔒 Tu respuesta es completamente confidencial</strong><br>
              <span style='font-size:14px;color:#1a3a7a;'>Ningún compañero puede ver tus elecciones. 
              Solo tu docente puede ver los resultados agregados del aula.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    if "encuesta_enviada" not in st.session_state:
        st.session_state.encuesta_enviada = False

    if st.session_state.encuesta_enviada:
        st.success("✅ ¡Gracias! Ya enviaste tu encuesta.")
        st.balloons()
        st.markdown("Tus respuestas fueron registradas de forma confidencial.")
        if st.button("Ver mis respuestas (solo esta sesión)"):
            st.session_state.encuesta_enviada = False
            st.rerun()
        return

    with st.form("encuesta_sociometrica"):
        st.markdown("### 🌟 Elecciones positivas")
        st.markdown("¿Con cuáles compañeros te gusta trabajar en el aula?")
        pos1 = st.selectbox("1ª opción positiva", ["— Seleccioná —"] + COMPAÑEROS, key="pos1")
        pos2 = st.selectbox("2ª opción positiva", ["— Seleccioná —"] + COMPAÑEROS, key="pos2")
        pos3 = st.selectbox("3ª opción positiva (opcional)", ["— Seleccioná —"] + COMPAÑEROS, key="pos3")

        st.markdown("---")
        st.markdown("### 💭 Elecciones negativas")
        st.markdown("¿Con cuáles compañeros preferís NO trabajar? (esto es confidencial)")
        neg1 = st.selectbox("1ª opción negativa", ["— Seleccioná —"] + COMPAÑEROS, key="neg1")
        neg2 = st.selectbox("2ª opción negativa (opcional)", ["— Seleccioná —"] + COMPAÑEROS, key="neg2")

        st.markdown("---")
        st.markdown("### 💬 Mensaje para tu docente (opcional)")
        mensaje = st.text_area(
            "¿Querés contarle algo a tu docente? Solo lo/a va a ver él/ella.",
            placeholder="Si estás pasando algo difícil en el aula, podés escribirlo acá...",
        )

        enviado = st.form_submit_button("✅ Enviar encuesta", type="primary", use_container_width=True)

        if enviado:
            if pos1 == "— Seleccioná —" or pos2 == "— Seleccioná —":
                st.error("Completá al menos las dos primeras elecciones positivas.")
            elif neg1 == "— Seleccioná —":
                st.error("Completá al menos la primera elección negativa.")
            elif len({pos1, pos2, pos3} - {"— Seleccioná —"}) < 2:
                st.error("No podés elegir al mismo compañero/a más de una vez.")
            else:
                st.session_state.encuesta_enviada = True
                st.rerun()


def render_contenido():
    """Sección de contenido educativo."""
    st.title("📚 Contenido Educativo")
    st.markdown("Información sobre convivencia y bullying pensada para vos.")

    for articulo in ARTICULOS:
        tipo_icon = {"Artículo": "📄", "Guía": "📋", "Video": "🎬"}.get(articulo["tipo"], "📄")
        with st.expander(f"{tipo_icon} **{articulo['titulo']}** · {articulo['tiempo']} de lectura"):
            st.markdown(articulo["contenido"])
            col1, col2 = st.columns(2)
            if col1.button("👍 Me fue útil", key=f"util_{articulo['titulo']}"):
                st.success("¡Gracias por tu feedback!")
            if col2.button("💬 Quiero hablar con mi docente", key=f"hablar_{articulo['titulo']}"):
                st.session_state.current_page = "student_home"
                st.session_state.show_mensaje = True
                st.rerun()

    st.markdown("---")
    st.markdown("### 🆘 ¿Necesitás ayuda urgente?")
    st.warning(
        """
Si estás en una situación de riesgo o necesitás hablar con alguien ahora:
- **Usá el mensaje confidencial** de esta app para contactar a tu docente
- **Hablá con un adulto de confianza** en tu escuela o en casa
- **Línea de ayuda:** 102 (Consejo Nacional de la Niñez)
        """
    )


# ---------------------------------------------------------------------------
# Punto de entrada principal
# ---------------------------------------------------------------------------

def render():
    """
    Enrutador principal del módulo de estudiantes.

    Rutas soportadas en st.session_state.current_page:
      - "student_home"      → pantalla de bienvenida
      - "student_encuesta"  → encuesta sociométrica
      - "student_contenido" → contenido educativo
    """
    page = st.session_state.get("current_page", "student_home")

    if page == "student_encuesta":
        render_encuesta()
    elif page == "student_contenido":
        render_contenido()
    else:
        render_home()
