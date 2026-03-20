import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import DOCENTES


def render():
    st.title("👨‍🏫 Gestión de Docentes")

    filtro_kyc = st.selectbox("Filtrar por estado KYC", ["Todos", "Aprobado", "Pendiente", "En revisión"])
    docentes = DOCENTES if filtro_kyc == "Todos" else [d for d in DOCENTES if d["kyc"] == filtro_kyc]

    st.markdown(f"**{len(docentes)} docente(s)**")

    for d in docentes:
        kyc_icon = {"Aprobado": "✅", "Pendiente": "⏳", "En revisión": "🔍"}.get(d["kyc"], "❓")
        with st.expander(f"{kyc_icon} **{d['nombre']}** — {d['colegio']}"):
            col1, col2, col3 = st.columns(3)
            col1.markdown(f"📧 {d['email']}")
            col2.metric("Aulas asignadas", d["aulas"])
            col3.metric("KYC", d["kyc"])

            if d["kyc"] in ("Pendiente", "En revisión"):
                col_a, col_b = st.columns(2)
                if col_a.button("✅ Aprobar KYC", key=f"ok_{d['id']}", type="primary"):
                    st.success(f"KYC aprobado para {d['nombre']} (demo)")
                if col_b.button("❌ Rechazar", key=f"rej_{d['id']}"):
                    st.error(f"KYC rechazado para {d['nombre']} (demo)")
