import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import ALERTAS, ALUMNOS


def render():
    st.title("🚨 Alertas")
    st.markdown("Alumnos identificados en riesgo a partir del análisis sociométrico.")

    filtro = st.selectbox("Filtrar por prioridad", ["Todas", "Alta", "Media", "Baja"])
    alertas = ALERTAS if filtro == "Todas" else [a for a in ALERTAS if a["prioridad"] == filtro]

    if not alertas:
        st.success("No hay alertas para el filtro seleccionado.")
        return

    for alerta in alertas:
        prioridad = alerta["prioridad"]
        css = {"Alta": "alert-high", "Media": "alert-medium", "Baja": "alert-low"}.get(prioridad, "")
        icon = {"Alta": "🔴", "Media": "🟡", "Baja": "🟢"}.get(prioridad, "")

        with st.expander(f"{icon} **{alerta['alumno']}** — {alerta['tipo']} ({alerta['estado']})"):
            # Buscar datos del alumno
            alumno_data = next((a for a in ALUMNOS if a["nombre"] == alerta["alumno"]), None)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Prioridad",  alerta["prioridad"])
            col2.metric("Estado",     alerta["estado"])
            col3.metric("Fecha",      alerta["fecha"])
            col4.metric("Aula",       alerta["aula"])

            if alumno_data:
                st.markdown("**Indicadores sociométricos:**")
                c1, c2, c3 = st.columns(3)
                c1.metric("Perfil",           alumno_data["perfil"])
                c2.metric("Índice aceptación", f"{alumno_data['indice_aceptacion']:.0%}" if alumno_data["indice_aceptacion"] else "N/D")
                c3.metric("Índice rechazo",    f"{alumno_data['indice_rechazo']:.0%}" if alumno_data["indice_rechazo"] else "N/D")

            st.markdown("**Recomendaciones automáticas:**")
            if alerta["tipo"] == "Rechazo elevado":
                st.info("💡 Revisá las dinámicas de grupo y considerá una actividad de integración. Reunite con el equipo de orientación.")
            elif alerta["tipo"] == "Aislamiento":
                st.info("💡 Facilitá espacios de participación para el alumno. Considerá comunicarte con la familia.")
            else:
                st.info("💡 Monitoreá la situación en las próximas semanas. El alumno recibe tanto elecciones positivas como negativas.")

            # Nota de seguimiento
            st.markdown("**Nota de seguimiento:**")
            nota = st.text_area("", value=alerta.get("nota", ""), key=f"nota_{alerta['id']}",
                                placeholder="Escribí tu nota de seguimiento aquí...")

            col_a, col_b, col_c = st.columns(3)
            if col_a.button("💾 Guardar nota", key=f"save_{alerta['id']}", type="primary"):
                st.success("Nota guardada (demo)")
            if col_b.button("✅ Marcar como resuelta", key=f"res_{alerta['id']}"):
                st.success("Alerta marcada como resuelta (demo)")
            if col_c.button("📄 Descargar reporte PDF", key=f"pdf_{alerta['id']}"):
                st.info("En la versión completa, esto genera un PDF descargable.")
