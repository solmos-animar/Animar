import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import COLEGIOS, DOCENTES, AULAS, ALERTAS


def render():
    st.title("🏛️ Dashboard Administrador")
    st.markdown("Vista general del ecosistema ConVivir.")

    # ── KPIs ──────────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    activos   = sum(1 for c in COLEGIOS if c["estado"] == "Activo")
    pendientes = sum(1 for c in COLEGIOS if c["estado"] == "Pendiente KYC")
    doc_validados = sum(1 for d in DOCENTES if d["kyc"] == "Aprobado")
    alertas_altas = sum(1 for a in ALERTAS if a["prioridad"] == "Alta" and a["estado"] == "Pendiente")

    col1.metric("🏫 Colegios Activos",   activos,       f"+{activos} totales")
    col2.metric("⏳ Pendientes KYC",     pendientes,    "requieren acción")
    col3.metric("👨‍🏫 Docentes validados", doc_validados, f"de {len(DOCENTES)} totales")
    col4.metric("🚨 Alertas altas sin gestionar", alertas_altas, delta_color="inverse")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    # ── Gráfico colegios por estado ───────────────────────────────────────────
    with col_a:
        st.subheader("Estado de colegios")
        estado_counts = pd.Series([c["estado"] for c in COLEGIOS]).value_counts().reset_index()
        estado_counts.columns = ["Estado", "Cantidad"]
        colors = {"Activo": "#1d7a55", "Pendiente KYC": "#d4580a", "Suspendido": "#c0392b"}
        fig = px.pie(estado_counts, names="Estado", values="Cantidad",
                     color="Estado", color_discrete_map=colors,
                     hole=0.45)
        fig.update_layout(margin=dict(t=20,b=20,l=0,r=0), legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)

    # ── Gráfico docentes por estado KYC ──────────────────────────────────────
    with col_b:
        st.subheader("Estado KYC de docentes")
        kyc_counts = pd.Series([d["kyc"] for d in DOCENTES]).value_counts().reset_index()
        kyc_counts.columns = ["Estado KYC", "Cantidad"]
        colors_kyc = {"Aprobado": "#1d7a55", "Pendiente": "#d4580a", "En revisión": "#1a56a0"}
        fig2 = px.bar(kyc_counts, x="Estado KYC", y="Cantidad",
                      color="Estado KYC", color_discrete_map=colors_kyc,
                      text="Cantidad")
        fig2.update_layout(showlegend=False, margin=dict(t=20,b=20,l=0,r=0))
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tabla colegios ────────────────────────────────────────────────────────
    st.subheader("Colegios registrados")
    df = pd.DataFrame(COLEGIOS)
    df = df.rename(columns={"id":"ID","nombre":"Colegio","ciudad":"Ciudad","docentes":"Docentes","aulas":"Aulas","estado":"Estado"})
    st.dataframe(df.drop("ID", axis=1), use_container_width=True, hide_index=True)
