# app.py
import streamlit as st
from utilidades.auth import (
    is_logged_in, get_rol, get_session, logout, puede_ver
)

# 1. Configuración de página
st.set_page_config(
    page_title="ConVivir — v1.1",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Cargar CSS
try:
    with open("utilidades/desktop.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("No se encontró el archivo utilidades/desktop.css")

# 3. Inicializar estado
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<h1 style="color:white; font-size:28px; margin-bottom:0;">ConVivir</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.4); margin-bottom:20px; font-size:12px;">v1.1 · 2026</p>', unsafe_allow_html=True)

    # Landing siempre visible
    if st.button("📋 Landing", use_container_width=True):
        st.session_state.seccion = "inicio"
        st.rerun()

    if is_logged_in():
        usuario = get_session()
        rol     = get_rol()

        st.divider()

        # --- INSTITUCIÓN ---
        if any(puede_ver(s) for s in ["direccion", "docente", "alumno"]):
            st.markdown('<p style="color:rgba(255,255,255,0.4); font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-left:6px; margin-bottom:4px;">Institución</p>', unsafe_allow_html=True)
            if puede_ver("direccion"):
                if st.button("🏢 Dirección", use_container_width=True):
                    st.session_state.seccion = "direccion"
                    st.rerun()
            if puede_ver("docente"):
                if st.button("👨‍🏫 Docentes", use_container_width=True):
                    st.session_state.seccion = "docente"
                    st.rerun()
            if puede_ver("alumno"):
                if st.button("🎒 Alumnos", use_container_width=True):
                    st.session_state.seccion = "alumno"
                    st.rerun()

        # --- FAMILIA ---
        if any(puede_ver(s) for s in ["familia", "alumno_familia"]):
            st.divider()
            st.markdown('<p style="color:rgba(255,255,255,0.4); font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-left:6px; margin-bottom:4px;">Familia</p>', unsafe_allow_html=True)
            if puede_ver("familia"):
                if st.button("👦 Tutores", use_container_width=True):
                    st.session_state.seccion = "familia"
                    st.rerun()
            if puede_ver("alumno_familia"):
                if st.button("👦 Alumnos (Fam)", key="nav_fam_alu", use_container_width=True):
                    st.session_state.seccion = "alumno_familia"
                    st.rerun()

        # --- ANIMAR ---
        if any(puede_ver(s) for s in ["moderador", "admin"]):
            st.divider()
            st.markdown('<p style="color:rgba(255,255,255,0.4); font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-left:6px; margin-bottom:4px;">Animar</p>', unsafe_allow_html=True)
            if puede_ver("moderador"):
                if st.button("🛡️ Moderadores", use_container_width=True):
                    st.session_state.seccion = "moderador"
                    st.rerun()
            if puede_ver("admin"):
                if st.button("⚙️ Admin Institución", use_container_width=True):
                    st.session_state.seccion = "admin"
                    st.rerun()

        # --- Usuario + logout ---
        st.divider()
        st.markdown(
            f'<div style="padding:0 6px; font-size:12px; color:rgba(255,255,255,0.5);">'
            f'<span style="color:rgba(255,255,255,0.85); font-weight:600;">{usuario["email"]}</span><br>'
            f'<span style="font-size:11px; text-transform:capitalize;">{usuario["rol"].replace("_", " ")}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            logout()
            st.rerun()

    else:
        # No logueado
        st.divider()
        if st.button("🔑 Iniciar sesión", use_container_width=True, type="primary"):
            st.session_state.seccion = "login"
            st.rerun()

    st.markdown('<br><div style="color:rgba(255,255,255,0.2); font-size:10px; padding-left:6px;">Confidencial · 2026</div>', unsafe_allow_html=True)

# ============================================================
# GUARD — secciones protegidas
# ============================================================
seccion = st.session_state.seccion

SECCIONES_PROTEGIDAS = [
    "direccion", "docente", "alumno",
    "familia", "alumno_familia",
    "moderador", "admin"
]

# Sin login → redirigir a login
if seccion in SECCIONES_PROTEGIDAS and not is_logged_in():
    st.session_state.seccion = "login"
    seccion = "login"

# Logueado pero sin permiso → error
if seccion in SECCIONES_PROTEGIDAS and is_logged_in() and not puede_ver(seccion):
    st.error("⛔ No tenés permisos para acceder a esta sección.")
    st.stop()

# ============================================================
# RENDERIZADO
# ============================================================
if seccion != "inicio":
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

try:
    if seccion == "inicio":
        from secciones.landing import show_landing
        show_landing()

    elif seccion == "login":
        from secciones.login import render
        render()

    elif seccion == "direccion":
        from secciones.direccion import render
        render()

    elif seccion == "alumno":
        from secciones.estudiantes import render
        render()

    elif seccion == "admin":
        from secciones.admin_colegio import render
        render()

    elif seccion == "docente":
        from secciones.docente import render
        render()

    else:
        st.title(f"Sección: {seccion.replace('_', ' ').capitalize()}")
        st.info("Esta pantalla está siendo preparada para el despliegue.")

except ModuleNotFoundError as e:
    st.warning(f"Todavía no has creado el archivo para la sección '{seccion}'.")
    st.info(f"Detalle: {e}")
except Exception as e:
    st.error(f"Ocurrió un error al cargar la sección: {e}")

if seccion != "inicio":
    st.markdown('</div>', unsafe_allow_html=True)
