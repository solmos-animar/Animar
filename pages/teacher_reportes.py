import streamlit as st
import plotly.express as px
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import ALUMNOS


def render():
    st.title("📋 Reportes")
    st.markdown("Resúmenes del estado sociométrico del aula.")

    tab1, tab2 = st.tabs(["📊 Reporte del aula", "👤 Perfil individual"])

    with tab1:
        st.subheader("Reporte — 3° A Primaria")

        col1, col2, col3 = st.columns(3)
        encuestados = sum(1 for a in ALUMNOS if a["encuesta"])
        en_riesgo   = sum(1 for a in ALUMNOS if a["alerta"])
        col1.metric("Alumnos encuestados", f"{encuestados}/{len(ALUMNOS)}")
        col2.metric("Alumnos en riesgo",    en_riesgo, delta_color="inverse")
        col3.metric("Participación",        f"{encuestados/len(ALUMNOS):.0%}")

        # Gráfico de barras de perfiles
        perfiles = [a["perfil"] for a in ALUMNOS if a["perfil"] != "—"]
        df_perfiles = pd.Series(perfiles).value_counts().reset_index()
        df_perfiles.columns = ["Perfil", "Cantidad"]
        color_map = {
            "Popular": "#1d7a55", "Integrado": "#1a56a0",
            "Aislado": "#d4580a", "Rechazado": "#c0392b", "Controvertido": "#5b3fa0"
        }
        fig = px.bar(df_perfiles, x="Perfil", y="Cantidad",
                     color="Perfil", color_discrete_map=color_map, text="Cantidad")
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, margin=dict(t=20,b=20,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Todos los alumnos:**")
        df = pd.DataFrame([{
            "Nombre": a["nombre"],
            "Perfil": a["perfil"],
            "Aceptación": f"{a['indice_aceptacion']:.0%}" if a["indice_aceptacion"] else "—",
            "Rechazo":    f"{a['indice_rechazo']:.0%}"    if a["indice_rechazo"]    else "—",
            "Encuesta":   "✅" if a["encuesta"] else "❌",
            "Alerta":     a["alerta"] or "—",
        } for a in ALUMNOS])
        st.dataframe(df, use_container_width=True, hide_index=True)

        if st.button("📄 Descargar reporte completo PDF", type="primary"):
            st.info("En la versión completa, esto genera y descarga un PDF del reporte.")

    with tab2:
        st.subheader("Perfil individual de alumno")
        alumno_sel = st.selectbox("Seleccioná un alumno",
                                  [a["nombre"] for a in ALUMNOS if a["encuesta"]])
        alumno = next((a for a in ALUMNOS if a["nombre"] == alumno_sel), None)
        if alumno:
            col1, col2, col3 = st.columns(3)
            col1.metric("Perfil sociométrico", alumno["perfil"])
            col2.metric("Índice de aceptación", f"{alumno['indice_aceptacion']:.0%}" if alumno["indice_aceptacion"] else "—")
            col3.metric("Índice de rechazo",    f"{alumno['indice_rechazo']:.0%}"    if alumno["indice_rechazo"] else "—")

            if alumno["alerta"]:
                st.markdown(f"""
                <div class='alert-high'>
                  <strong>🚨 Alerta {alumno['alerta']} detectada</strong><br>
                  Este alumno requiere atención prioritaria.
                </div>
                """, unsafe_allow_html=True)

            # Gauge de aceptación
            import plotly.graph_objects as go
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round((alumno["indice_aceptacion"] or 0) * 100),
                title={"text": "Índice de Aceptación"},
                number={"suffix": "%"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#1a56a0"},
                    "steps": [
                        {"range": [0, 30],  "color": "#fdeaea"},
                        {"range": [30, 60], "color": "#fef3e2"},
                        {"range": [60, 100],"color": "#e6f4ee"},
                    ],
                }
            ))
            fig_gauge.update_layout(height=220, margin=dict(t=40,b=10,l=20,r=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

            if st.button("📄 Generar reporte individual PDF", type="primary"):
                st.info("En la versión completa, esto genera el reporte PDF individual descargable.")
