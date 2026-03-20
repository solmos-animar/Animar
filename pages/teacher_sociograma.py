import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import math
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import ALUMNOS, SOCIOGRAMA_EDGES


PERFIL_COLOR = {
    "Popular":       "#1d7a55",
    "Integrado":     "#1a56a0",
    "Aislado":       "#d4580a",
    "Rechazado":     "#c0392b",
    "Controvertido": "#5b3fa0",
    "—":             "#9a9690",
}


def render():
    st.title("🕸️ Sociograma — 3° A Primaria")
    st.markdown("Mapa de relaciones sociales generado a partir de la encuesta sociométrica.")

    # ── Leyenda ───────────────────────────────────────────────────────────────
    col1, col2, col3, col4, col5 = st.columns(5)
    for col, (perfil, color) in zip(
        [col1, col2, col3, col4, col5],
        PERFIL_COLOR.items()
    ):
        if perfil != "—":
            col.markdown(f"<span style='background:{color};color:white;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:700'>{perfil}</span>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Opciones ──────────────────────────────────────────────────────────────
    col_a, col_b = st.columns([2, 1])
    with col_a:
        mostrar = st.radio("Mostrar relaciones:", ["Todas", "Solo positivas", "Solo negativas"], horizontal=True)
    with col_b:
        alumno_foco = st.selectbox("Enfocar alumno:", ["Ninguno"] + [a["nombre"] for a in ALUMNOS])

    # ── Construcción del grafo ────────────────────────────────────────────────
    G = nx.DiGraph()
    for a in ALUMNOS:
        G.add_node(a["id"], nombre=a["nombre"], perfil=a["perfil"])

    for (src, dst, tipo) in SOCIOGRAMA_EDGES:
        if mostrar == "Solo positivas" and tipo != "positivo":
            continue
        if mostrar == "Solo negativas" and tipo != "negativo":
            continue
        G.add_edge(src, dst, tipo=tipo)

    # Layout circular
    pos = nx.spring_layout(G, seed=42, k=2.5)

    # Resaltar nodo foco
    foco_id = None
    if alumno_foco != "Ninguno":
        foco_id = next((a["id"] for a in ALUMNOS if a["nombre"] == alumno_foco), None)

    # ── Trazado ───────────────────────────────────────────────────────────────
    edge_traces = []
    for src, dst, data in G.edges(data=True):
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        color = "#1d7a55" if data["tipo"] == "positivo" else "#c0392b"
        opacity = 0.8
        if foco_id and src != foco_id and dst != foco_id:
            opacity = 0.1

        # Flecha
        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode="lines",
            line=dict(width=1.8, color=color),
            opacity=opacity,
            hoverinfo="none",
        ))

    # Nodos
    node_x, node_y, node_text, node_color, node_size, node_hover = [], [], [], [], [], []
    for node in G.nodes():
        alumno = next((a for a in ALUMNOS if a["id"] == node), None)
        if not alumno:
            continue
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        nombre  = alumno["nombre"].split()[0]  # solo nombre
        node_text.append(nombre)
        color   = PERFIL_COLOR.get(alumno["perfil"], "#9a9690")
        node_color.append(color)
        size = 28 if alumno["perfil"] == "Popular" else 20
        if foco_id and node == foco_id:
            size = 36
        node_size.append(size)
        alerta = f" 🚨 Alerta: {alumno['alerta']}" if alumno["alerta"] else ""
        node_hover.append(f"<b>{alumno['nombre']}</b><br>Perfil: {alumno['perfil']}<br>"
                          f"Aceptación: {alumno['indice_aceptacion'] or 'N/D'}<br>"
                          f"Rechazo: {alumno['indice_rechazo'] or 'N/D'}{alerta}")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        textfont=dict(size=11, color="#0f2240"),
        marker=dict(size=node_size, color=node_color,
                    line=dict(width=2, color="white")),
        hovertext=node_hover,
        hoverinfo="text",
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        showlegend=False,
        height=560,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="rgba(249,246,240,0.5)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Tabla de perfiles ─────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Tabla de perfiles")
    import pandas as pd
    df = pd.DataFrame([
        {
            "Alumno": a["nombre"],
            "Perfil": a["perfil"],
            "Índice Aceptación": a["indice_aceptacion"] if a["indice_aceptacion"] is not None else "—",
            "Índice Rechazo":    a["indice_rechazo"]    if a["indice_rechazo"]    is not None else "—",
            "Alerta":            a["alerta"] or "—",
        }
        for a in ALUMNOS
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
