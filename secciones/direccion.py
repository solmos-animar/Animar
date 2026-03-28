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

    df = cargar_alumnos()

    # -------------------------------
    # BUSCADOR
    # -------------------------------
    st.markdown("### 📋 Alumnos")

    busqueda = st.text_input("🔍 Buscar alumno por nombre")

    if busqueda:
        df = df[
            df["nombre"].str.contains(busqueda, case=False, na=False) |
            df["grado"].str.contains(busqueda, case=False, na=False)
        ]

    # -------------------------------
    # LISTADO
    # -------------------------------
    if df.empty:
        st.info("No hay alumnos cargados.")
    else:
        for i, alumno in df.iterrows():
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3,2,2,2])

                with col1:
                    st.write(f"**{alumno['nombre']}**")
                with col2:
                    st.write(alumno["fecha_nac"])
                with col3:
                    st.write(alumno["grado"])

                with col4:
                    if st.button("✏️ Editar", key=f"edit_{i}"):
                        st.session_state.editando = i

                    if st.button("❌ Borrar", key=f"del_{i}"):
                        df = df.drop(i)
                        guardar_alumnos(df)
                        st.success("Alumno eliminado")
                        st.rerun()

    st.markdown("---")

    # -------------------------------
    # EDITAR
    # -------------------------------
    if "editando" in st.session_state:
        i = st.session_state.editando
        alumno = df.loc[i]

        st.markdown("### ✏️ Editar alumno")

        with st.form("form_editar"):
            nombre = st.text_input("Nombre", value=alumno["nombre"])
            fecha_nac = st.text_input("Fecha de nacimiento", value=alumno["fecha_nac"])
            grado = st.text_input("Grado", value=alumno["grado"])

            col1, col2 = st.columns(2)

            with col1:
                guardar = st.form_submit_button("Guardar cambios")
            with col2:
                cancelar = st.form_submit_button("Cancelar")

            if guardar:
                df.loc[i] = [nombre, fecha_nac, grado]
                guardar_alumnos(df)
                del st.session_state.editando
                st.success("Alumno actualizado")
                st.rerun()

            if cancelar:
                del st.session_state.editando
                st.rerun()

    # -------------------------------
    # AGREGAR
    # -------------------------------
    st.markdown("### ➕ Agregar nuevo alumno")

    with st.form("form_nuevo"):
        nombre = st.text_input("Nombre completo")
        fecha_nac = st.date_input("Fecha de nacimiento")
        grado = st.text_input("Grado / División")

        submitted = st.form_submit_button("Agregar")

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

                st.success("Alumno agregado")
                st.rerun()
