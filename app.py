import streamlit as st

# 1. Configuración de página (Debe ser lo primero)
st.set_page_config(
    page_title="ConVivir — v1.1",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Cargar CSS Institucional (Asegúrate de que desktop.css tenga el padding-top: 0)
try:
    with open("utilidades/desktop.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("No se encontró el archivo utilidades/desktop.css")

# 3. Inicializar Estado de Navegación
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"

# 4. SIDEBAR ESTRUCTURADO (Menú de la izquierda)
with st.sidebar:
    st.markdown('<h1 style="color:white; font-size:28px; margin-bottom:0;">ConVivir</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.5); margin-bottom:20px;">v1.1 · 2026</p>', unsafe_allow_html=True)
    
    # --- Landing ---
    if st.button("📋 Landing", use_container_width=True):
        st.session_state.seccion = "inicio"
        st.rerun()
    
    st.divider() 
    
    # --- Institución ---
    st.markdown('<p style="color:rgba(255,255,255,0.4); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-left:15px;">Institución</p>', unsafe_allow_html=True)
    if st.button("🏢 Dirección", use_container_width=True):
        st.session_state.seccion = "direccion"
        st.rerun()
    if st.button("👨‍🏫 Docentes", use_container_width=True):
        st.session_state.seccion = "docente"
        st.rerun()
    if st.button("🎒 Alumnos", use_container_width=True):
        st.session_state.seccion = "alumno"
        st.rerun()
    
    st.divider()
    
    # --- Familia ---
    st.markdown('<p style="color:rgba(255,255,255,0.4); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-left:15px;">Familia</p>', unsafe_allow_html=True)
    if st.button("👨‍准确‍♀️ Tutores", use_container_width=True):
        st.session_state.seccion = "familia"
        st.rerun()
    if st.button("👦 Alumnos (Fam)", key="nav_fam_alu", use_container_width=True):
        st.session_state.seccion = "alumno_familia"
        st.rerun()
    
    st.divider()
    
    # --- Animar ---
    st.markdown('<p style="color:rgba(255,255,255,0.4); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-left:15px;">Animar</p>', unsafe_allow_html=True)
    if st.button("🛡️ Moderadores", use_container_width=True):
        st.session_state.seccion = "moderador"
        st.rerun()
    if st.button("⚙️ Administradores", use_container_width=True):
        st.session_state.seccion = "admin"
        st.rerun()

    st.markdown('<br><br><div style="color:rgba(255,255,255,0.2); font-size:10px; padding-left:15px;">Confidencial · 2026</div>', unsafe_allow_html=True)

# 5. RENDERIZADO DE CONTENIDO (Área Principal)
seccion = st.session_state.seccion

# Contenedor para el resto de secciones que no son Landing (para aplicar fondo crema)
if seccion != "inicio":
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Lógica de ruteo
try:
    if seccion == "inicio":
        from secciones.landing import show_landing
        show_landing()
        
    elif seccion == "direccion":
        from secciones.direccion import render
        render()
        
    elif seccion == "alumno":
        from secciones.estudiantes import render
        render()
        
    # Agregaremos el resto de los módulos (docente, familia, etc.) aquí
    else:
        st.title(f"Sección: {seccion.replace('_', ' ').capitalize()}")
        st.info("Esta pantalla está siendo preparada para el despliegue.")

except ModuleNotFoundError as e:
    st.warning(f"Todavía no has creado el archivo para la sección '{seccion}'.")
    st.info("Crea el archivo correspondiente en la carpeta 'secciones/' para activarlo.")
except Exception as e:
    st.error(f"Ocurrió un error al cargar la sección: {e}")

if seccion != "inicio":
    st.markdown('</div>', unsafe_allow_html=True)
