import streamlit as st
import sys, os

# Intentar importar mock_data. Si falla por estructura de carpetas, definimos un fallback
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from data.mock_data import ALUMNOS
    COMPAÑEROS = [a["nombre"] for a in ALUMNOS if a["nombre"] != st.session_state.user.get("name", "Lucas Martínez")]
except Exception:
    # Fallback por si no encuentra el archivo data/mock_data.py durante la prueba
    COMPAÑEROS = ["Mateo García", "Sofía Rodríguez", "Valentina López", "Bautista Pérez", "Martina Gómez"]

# ---------------------------------------------------------------------------
# Datos locales (Contenido Educativo)
# ---------------------------------------------------------------------------

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
]

# ---------------------------------------------------------------------------
# Sub-páginas
# ---------------------------------------------------------------------------

def render_home():
    """Página de bienvenida del estudiante."""
    user = st.session_state.user
    nombre_pila = user['name'].split()[0] if 'name' in user else "Estudiante"
    
    st.markdown(f"""
        <div style="margin-bottom: 25px;">
            <h1 style="font-family: 'Sora', sans-serif; color: #111; margin-bottom: 5px;">👋 ¡Hola, {nombre_pila}!</h1>
            <p style="color: #666; font-size: 16px;">Bienvenido/a a ConVivir — tu espacio para mejorar la convivencia en el aula.</p>
        </div>
    """, unsafe_allow_html=True)

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

    st.markdown("<br>", unsafe_allow_html=True)

    # Secciones disponibles
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("### 📝 Encuesta")
            st.markdown("Respondé sobre tus compañeros de forma anónima.")
            if st.button("Ir a la encuesta", use_container_width=True, key="btn_ir_encuesta"):
                st.session_state.current_page = "student_encuesta"
                st.rerun()
    with col2:
        with st.container(border=True):
            st.markdown("### 📚 Contenido")
            st.markdown("Artículos y guías sobre convivencia y bullying.")
            if st.button("Ver contenido", use_container_width=True, key="btn_ir_contenido"):
                st.session_state.current_page = "student_contenido"
                st.rerun()
    with col3:
        with st.container(border=True):
            st.markdown("### 💬 Mensaje")
            st.markdown("Enviá un mensaje confidencial a tu docente.")
            if st.button("Enviar mensaje", use_container_width=True, key="btn_ir_mensaje"):
                st.session_state.show_mensaje = True
                st.rerun()

    # Panel de mensaje confidencial
    if st.session_state.get("show_mensaje"):
        st.markdown("---")
        st.subheader("💬 Mensaje confidencial al docente")
        st.info("Este mensaje solo lo va a ver tu docente. Es completamente confidencial.")
        mensaje = st.text_area("Escribí tu mensaje aquí:", placeholder="Podés contar lo que está pasando...")
        
        c1, c2 = st.columns([1, 4])
        if c1.button("Enviar", type="primary"):
            if mensaje:
                st.success("✅ Mensaje enviado en privado.")
                st.session_state.show_mensaje = False
                st.rerun()
            else:
                st.error("Escribí algo.")
        if c2.button("Cancelar"):
            st.session_state.show_mensaje = False
            st.rerun()

def render_encuesta():
    """Encuesta sociométrica del estudiante."""
    if st.button("← Volver al inicio", key="back_home_enc"):
        st.session_state.current_page = "student_home"
        st.rerun()

    st.title("📝 Encuesta Sociométrica")
    
    st.info("🔒 **Tu respuesta es confidencial.** Solo tu docente verá los resultados del aula.")

    if st.session_state.get("encuesta_enviada"):
        st.success("✅ ¡Gracias! Ya enviaste tu encuesta.")
        st.balloons()
        if st.button("Volver a responder (demo)"):
            st.session_state.encuesta_enviada = False
            st.rerun()
        return

    with st.form("encuesta_sociometrica"):
        st.markdown("### 🌟 Elecciones positivas")
        st.write("¿Con quién te gusta trabajar?")
        pos1 = st.selectbox("1ª opción", ["— Seleccioná —"] + COMPAÑEROS)
        pos2 = st.selectbox("2ª opción", ["— Seleccioná —"] + COMPAÑEROS)

        st.markdown("### 💭 Elecciones negativas")
        st.write("¿Con quién preferís NO trabajar?")
        neg1 = st.selectbox("Opción negativa", ["— Seleccioná —"] + COMPAÑEROS)

        st.markdown("### 💬 Mensaje extra")
        mensaje = st.text_area("¿Querés decirle algo más a tu docente?")

        enviado = st.form_submit_button("✅ Enviar encuesta", type="primary", use_container_width=True)

        if enviado:
            if pos1 == "— Seleccioná —" or neg1 == "— Seleccioná —":
                st.error("Por favor completá las opciones.")
            else:
                st.session_state.encuesta_enviada = True
                st.rerun()

def render_contenido():
    """Sección de contenido educativo."""
    if st.button("← Volver al inicio", key="back_home_cont"):
        st.session_state.current_page = "student_home"
        st.rerun()

    st.title("📚 Contenido Educativo")
    
    for articulo in ARTICULOS:
        with st.expander(f"📄 **{articulo['titulo']}**"):
            st.markdown(articulo["contenido"])
            if st.button("👍 Útil", key=f"util_{articulo['titulo']}"):
                st.toast("¡Gracias!")

# ---------------------------------------------------------------------------
# Punto de entrada principal
# ---------------------------------------------------------------------------

def render():
    """
    Enrutador principal del módulo de estudiantes.
    Se asegura de envolver todo en un contenedor de padding consistente.
    """
    # Contenedor principal con estilo institucional
    st.markdown('<div style="padding: 0px 40px 40px 40px;">', unsafe_allow_html=True)
    
    page = st.session_state.get("current_page", "student_home")

    if page == "student_encuesta":
        render_encuesta()
    elif page == "student_contenido":
        render_contenido()
    else:
        render_home()
        
    st.markdown('</div>', unsafe_allow_html=True)
