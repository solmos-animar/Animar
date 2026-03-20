import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import CONTENIDO_EDUCATIVO

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


def render():
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
    st.warning("""
Si estás en una situación de riesgo o necesitás hablar con alguien ahora:
- **Usá el mensaje confidencial** de esta app para contactar a tu docente
- **Hablá con un adulto de confianza** en tu escuela o en casa
- **Línea de ayuda:** 102 (Consejo Nacional de la Niñez)
    """)
