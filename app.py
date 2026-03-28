import streamlit as st

st.set_page_config(
    page_title="ConVivir — v1.1",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar CSS
with open("utilidades/desktop.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inicializar sección
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"

# ── SIDEBAR ESTRUCTURADO ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<h1 style="color:white; font-size:28px; margin-bottom:0;">ConVivir</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.5); margin-bottom:20px;">v1.1 · 2026</p>', unsafe_allow_html=True)
    
    # --- Landing ---
    if st.button("📋 Landing", use_container_width=True):
        st.session_state.seccion = "inicio"
    
    st.divider() # Línea
    
    # --- Institución ---
    st.markdown('<p style="color:rgba(255,255,255,0.4); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-left:15px;">Institución</p>', unsafe_allow_html=True)
    if st.button("🏢 Dirección", use_container_width=True):
        st.session_state.seccion = "direccion"
    if st.button("👨‍🏫 Docentes", use_container_width=True):
        st.session_state.seccion = "docente"
    if st.button("🎒 Alumnos", use_container_width=True):
        st.session_state.seccion = "alumno"
    
    st.divider() # Línea
    
    # --- Familia ---
    st.markdown('<p style="color:rgba(255,255,255,0.4); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-left:15px;">Familia</p>', unsafe_allow_html=True)
    if st.button("👨‍👩‍👧 Tutores", use_container_width=True):
        st.session_state.seccion = "familia"
    if st.button("👦 Alumnos (Fam)", key="nav_fam_alu", use_container_width=True):
        st.session_state.seccion = "alumno_familia"
    
    st.divider() # Línea
    
    # --- Animar ---
    st.markdown('<p style="color:rgba(255,255,255,0.4); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-left:15px;">Animar</p>', unsafe_allow_html=True)
    if st.button("🛡️ Moderadores", use_container_width=True):
        st.session_state.seccion = "moderador"
    if st.button("⚙️ Administradores", use_container_width=True):
        st.session_state.seccion = "admin"

    st.markdown('<br><br><div style="color:rgba(255,255,255,0.2); font-size:10px; padding-left:15px;">Confidencial · 2026</div>', unsafe_allow_html=True)

# ── RENDERIZADO DE CONTENIDO ──────────────────────────────────────────────
# Usamos un div para el fondo crema general
st.markdown('<div class="main-content">', unsafe_allow_html=True)

seccion = st.session_state.seccion

if seccion == "inicio":
    from secciones.landing import show_landing
    show_landing()
elif seccion == "direccion":
    from secciones.direccion import render
    render()
elif seccion == "alumno":
    from secciones.estudiantes import render
    render()
# (Agregar el resto de los elif a medida que creemos los archivos)
else:
    st.title(f"Sección: {seccion.capitalize()}")
    st.info("Esta pantalla está en desarrollo.")

st.markdown('</div>', unsafe_allow_html=True)
