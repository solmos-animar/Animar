import streamlit as st
import pandas as pd
import os

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

DATA_PATH = "data/alumnos.csv"

# -------------------------------------------------------------------
# FUNCIONES DE DATOS
# -------------------------------------------------------------------

def cargar_alumnos():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["nombre", "fecha_nac", "grado"])

def guardar_alumnos(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

# -------------------------------------------------------------------
# UI PRINCIPAL
# -------------------------------------------------------------------

def render():
    st.title("🏫 Panel de Dirección")

    # Cargar datos
    df = cargar_alumnos()

    # -------------------------------
    # FILTRO
    # -------------------------------
    st.markdown("### 🔍 Filtros")

    if not df.empty:
        grados = ["Todos"] + sorted(df["grado"].dropna().unique().tolist())
    else:
        grados = ["Todos"]

    filtro_grado = st.selectbox("Filtrar por grado", grados)

    if filtro_grado != "Todos":
        df_filtrado = df[df["grado"] == filtro_grado]
    else:
        df_filtrado = df

    # -------------------------------
    # TABLA
    # -------------------------------
    st.markdown("### 📋 Listado de alumnos")

    if df_filtrado.empty:
        st.info("No hay alumnos cargados todavía.")
    else:
        st.dataframe(df_filtrado, use_container_width=True)

    st.markdown("---")

    # -------------------------------
    # FORMULARIO NUEVO ALUMNO
    # -------------------------------
    st.markdown("### ➕ Agregar nuevo alumno")

    with st.form("form_nuevo_alumno"):
        nombre = st.text_input("Nombre completo")
        fecha_nac = st.date_input("Fecha de nacimiento")
        grado = st.text_input("Grado / División (ej: 3° A)")

        submitted = st.form_submit_button("Guardar alumno")

        if submitted:
            if not nombre or not grado:
                st.error("Completá todos los campos")
            else:
                nuevo = pd.DataFrame([{
                    "nombre": nombre,
                    "fecha_nac": fecha_nac.strftime("%d/%m/%Y"),
                    "grado": grado
                }])

                df = pd.concat([df, nuevo], ignore_index=True)
                guardar_alumnos(df)

                st.success("✅ Alumno agregado correctamente")
                st.rerun()
