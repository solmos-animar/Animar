import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import AULAS, ALUMNOS, ALERTAS


def render():
    user = st.session_state.user
    st.title(f"📊 Dashboard — {user['name']}")

    # KPIs del docente
    mis_aulas = [a for a in AULAS if a["docente"] == "María García"]
    total_alumnos = sum(a["alumnos"] for a in mis_aulas)
    alertas_pend  = sum(1 for a in ALERTAS if a["estado"] == "Pendiente")
    completadas   = sum(1 for a in mis_aulas if a["sociograma"] == "Completado")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🚪 Mis Aulas",           len(mis_aulas))
    col2.metric("👩‍🎓 Total alumnos",       total_alumnos)
    col3.metric("🚨 Alertas pendientes",   alertas_pend,  delta_color="inverse")
    col4.metric("✅ Sociogramas completos", completadas)

    st.markdown("---")
    col_a, col_b = st.columns(2)

    # Gauge de participación
    with col_a:
        st.subheader("Participación — 3° A Primaria")
        encuestados = sum(1 for a in ALUMNOS if a["encuesta"])
        total = len(ALUMNOS)
        pct = round(encuestados / total * 100)

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pct,
            delta={"reference": 60, "suffix": "%"},
            number={"suffix": "%"},
            title={"text": f"{encuestados} de {total} alumnos respondieron"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#1d7a55"},
                "steps": [
                    {"range": [0, 60],  "color": "#fde8d0"},
                    {"range": [60, 80], "color": "#e6f4ee"},
                    {"range": [80, 100],"color": "#b8e8d0"},
                ],
                "threshold": {"line": {"color": "#d4580a", "width": 3}, "thickness": 0.75, "value": 60},
            }
        ))
        fig.update_layout(margin=dict(t=40,b=20,l=20,r=20), height=260)
        st.plotly_chart(fig, use_container_width=True)

    # Distribución de perfiles
    with col_b:
        st.subheader("Distribución de perfiles sociométricos")
        perfiles = [a["perfil"] for a in ALUMNOS if a["perfil"] != "—"]
        from collections import Counter
        counts = Counter(perfiles)
        colores = {
            "Popular": "#1d7a55", "Integrado": "#1a56a0",
            "Aislado": "#d4580a", "Rechazado": "#c0392b", "Controvertido": "#5b3fa0"
        }
        fig2 = go.Figure(go.Bar(
            x=list(counts.keys()),
            y=list(counts.values()),
            marker_color=[colores.get(k, "#9a9690") for k in counts.keys()],
            text=list(counts.values()),
            textposition="outside",
        ))
        fig2.update_layout(showlegend=False, margin=dict(t=20,b=20,l=0,r=0), height=260,
                           xaxis_title="", yaxis_title="Cantidad")
        st.plotly_chart(fig2, use_container_width=True)

    # Alertas recientes
    st.subheader("🚨 Alertas recientes")
    for alerta in ALERTAS:
        prioridad = alerta["prioridad"]
        css_class = {"Alta": "alert-high", "Media": "alert-medium", "Baja": "alert-low"}.get(prioridad, "")
        icon = {"Alta": "🔴", "Media": "🟡", "Baja": "🟢"}.get(prioridad, "")
        st.markdown(f"""
        <div class='{css_class}'>
          <strong>{icon} {alerta['alumno']}</strong> — {alerta['tipo']}<br>
          <small>Aula: {alerta['aula']} · {alerta['fecha']} · Estado: {alerta['estado']}</small>
        </div>
        """, unsafe_allow_html=True)
