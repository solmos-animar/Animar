import streamlit as st
import pandas as pd

def render():
    st.markdown('<h2 style="color: #0f2240;">🛡️ Administración de Instituciones</h2>', unsafe_allow_html=True)
    st.markdown("Gestión global de colegios, docentes, alumnos y tutores para el ecosistema Animar.")
    
    # Tabs para organizar la carga por entidad
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏢 Nuevo Colegio", 
        "👨‍🏫 Docentes", 
        "👪 Tutores/Padres", 
        "🎒 Alumnos"
    ])

    # --- TAB 1: CARGA DE COLEGIO ---
    with tab1:
        st.subheader("Registrar Institución")
        with st.form("form_nuevo_colegio", clear_on_submit=True):
            c1, c2 = st.columns(2)
            nombre_col = c1.text_input("Nombre del Colegio")
            cuit_col = c2.text_input("Identificación Fiscal (CUIT/RUT)")
            
            c3, c4 = st.columns(2)
            contacto_mail = c3.text_input("Email de contacto oficial")
            plan_tipo = c4.selectbox("Plan de Suscripción", ["Básico", "Estándar", "Premium"])
            
            if st.form_submit_button("Crear Colegio"):
                if nombre_col and cuit_col:
                    # Aquí iría la lógica de guardado en base de datos
                    st.success(f"✅ Colegio '{nombre_col}' creado exitosamente.")
                else:
                    st.error("Por favor completa los campos obligatorios.")

    # --- TAB 2, 3 y 4: LÓGICA DE CARGA MASIVA ---
    # Usaremos una función auxiliar para no repetir código en los tabs
    def seccion_carga_masiva(entidad):
        st.subheader(f"Carga de {entidad}")
        
        # Selección del colegio destino (Esto vendría de tu BD)
        colegio_sel = st.selectbox(f"Seleccionar Colegio para asignar {entidad}", 
                                  ["Colegio San José", "Instituto Belgrano", "Escuela Técnica N°1"],
                                  key=f"sel_{entidad}")
        
        col_btn1, col_btn2 = st.columns([1, 2])
        with col_btn1:
            st.button(f"📥 Descargar Plantilla {entidad}", use_container_width=True)
        
        archivo = st.file_uploader(f"Subir archivo Excel/CSV de {entidad}", type=["xlsx", "csv"], key=f"up_{entidad}")
        
        if archivo:
            df = pd.read_excel(archivo) if archivo.name.endswith('xlsx') else pd.read_csv(archivo)
            st.write("Vista previa de los datos:")
            st.dataframe(df.head(5), use_container_width=True)
            
            if st.button(f"🚀 Procesar Alta de {len(df)} {entidad}", type="primary"):
                st.success(f"Procesando carga en {colegio_sel}...")

    with tab2: seccion_carga_masiva("Docentes")
    with tab3: seccion_carga_masiva("Tutores")
    with tab4: seccion_carga_masiva("Alumnos")
