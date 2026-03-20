import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import COLEGIOS


def render():
    st.title("🏫 Gestión de Colegios")

    col_search, col_filter = st.columns([3, 1])
    with col_search:
        busqueda = st.text_input("🔍 Buscar colegio", placeholder="Nombre o ciudad...")
    with col_filter:
        filtro = st.selectbox("Estado", ["Todos", "Activo", "Pendiente KYC", "Suspendido"])

    colegios = COLEGIOS
    if busqueda:
        colegios = [c for c in colegios if busqueda.lower() in c["nombre"].lower() or busqueda.lower() in c["ciudad"].lower()]
    if filtro != "Todos":
        colegios = [c for c in colegios if c["estado"] == filtro]

    st.markdown(f"**{len(colegios)} colegio(s) encontrado(s)**")

    for c in colegios:
        estado_color = {"Activo": "🟢", "Pendiente KYC": "🟡", "Suspendido": "🔴"}.get(c["estado"], "⚪")
        with st.expander(f"{estado_color} **{c['nombre']}** — {c['ciudad']}"):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Docentes",  c["docentes"])
            col2.metric("Aulas",     c["aulas"])
            col3.metric("Estado",    c["estado"])
            col4.metric("Ciudad",    c["ciudad"])

            col_a, col_b, col_c = st.columns(3)
            if c["estado"] == "Activo":
                if col_a.button("🔴 Suspender", key=f"susp_{c['id']}"):
                    st.warning(f"Acción de suspensión sobre {c['nombre']} (demo)")
            elif c["estado"] == "Suspendido":
                if col_a.button("🟢 Reactivar", key=f"react_{c['id']}"):
                    st.success(f"Colegio reactivado (demo)")
            if col_b.button("📋 Ver docentes", key=f"doc_{c['id']}"):
                st.info("Navegá a la sección Docentes para filtrar por colegio.")

    st.markdown("---")
    st.subheader("➕ Registrar nuevo colegio")
    with st.form("nuevo_colegio"):
        col1, col2 = st.columns(2)
        nombre  = col1.text_input("Nombre del colegio")
        ciudad  = col2.text_input("Ciudad")
        col3, col4 = st.columns(2)
        email   = col3.text_input("Email institucional")
        tel     = col4.text_input("Teléfono")
        if st.form_submit_button("Registrar colegio", type="primary"):
            if nombre and ciudad:
                st.success(f"✅ Colegio '{nombre}' registrado. Quedará pendiente de KYC.")
            else:
                st.error("Completá nombre y ciudad.")
