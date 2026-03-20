import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import AULAS, ALUMNOS


def render():
    st.title("🚪 Gestión de Aulas")

    mis_aulas = [a for a in AULAS if a["docente"] == "María García"]

    for aula in mis_aulas:
        estado_icon = "🟢" if aula["estado"] == "Habilitada" else "🔴"
        soc_icon = {"Completado": "✅", "En progreso": "🔄", "Sin iniciar": "⏳"}.get(aula["sociograma"], "")

        with st.expander(f"{estado_icon} **{aula['nombre']}** — {aula['alumnos']} alumnos · Sociograma: {soc_icon} {aula['sociograma']}"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Alumnos", aula["alumnos"])
            col2.metric("Estado del aula", aula["estado"])
            col3.metric("Sociograma", aula["sociograma"])

            alumnos_aula = [a for a in ALUMNOS if a["aula"] == aula["nombre"]]
            if alumnos_aula:
                st.markdown("**Alumnos del aula:**")
                cols = st.columns(3)
                for i, alumno in enumerate(alumnos_aula):
                    enc = "✅" if alumno["encuesta"] else "❌"
                    alerta = f" 🚨" if alumno["alerta"] else ""
                    cols[i % 3].markdown(f"{enc} {alumno['nombre']}{alerta}")

            col_a, col_b = st.columns(2)
            if aula["estado"] == "Habilitada":
                if col_a.button("🔴 Deshabilitar aula", key=f"dis_{aula['id']}"):
                    st.warning("Aula deshabilitada (demo)")
                if aula["sociograma"] == "Sin iniciar":
                    if col_b.button("▶️ Iniciar encuesta", key=f"ini_{aula['id']}", type="primary"):
                        st.success("Encuesta iniciada — se notificó a los alumnos (demo)")
            else:
                if col_a.button("🟢 Habilitar aula", key=f"en_{aula['id']}", type="primary"):
                    st.success("Aula habilitada (demo)")

    st.markdown("---")
    st.subheader("➕ Crear nueva aula")
    with st.form("nueva_aula"):
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre del aula", placeholder="Ej: 4° C Primaria")
        grado  = col2.selectbox("Nivel", ["Primaria", "Secundaria"])
        codigo = st.text_input("Código de acceso para alumnos", placeholder="Ej: AULA-2025-XK")
        if st.form_submit_button("Crear aula", type="primary"):
            if nombre:
                st.success(f"✅ Aula '{nombre}' creada. Código: {codigo or 'AULA-AUTO-001'}")
            else:
                st.error("Completá el nombre del aula.")
