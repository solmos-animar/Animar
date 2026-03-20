import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import ALUMNOS

COMPAÑEROS = [a["nombre"] for a in ALUMNOS if a["nombre"] != "Lucas Martínez"]


def render():
    st.title("📝 Encuesta Sociométrica")

    with st.container(border=True):
        st.markdown("""
        <div style='background:#e8f0fe;border-left:4px solid #1a56a0;border-radius:8px;padding:14px 18px;'>
          <strong>🔒 Tu respuesta es completamente confidencial</strong><br>
          <span style='font-size:14px;color:#1a3a7a;'>Ningún compañero puede ver tus elecciones. 
          Solo tu docente puede ver los resultados agregados del aula.</span>
        </div>
        """, unsafe_allow_html=True)

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
        mensaje = st.text_area("¿Querés contarle algo a tu docente? Solo lo/a va a ver él/ella.",
                               placeholder="Si estás pasando algo difícil en el aula, podés escribirlo acá...")

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
