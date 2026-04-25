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
    initial_sidebar_state="collapsed"
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
# NAVBAR SUPERIOR
# ============================================================

# Construir lista de ítems visibles
# Cada ítem: (tipo, label, key)
# tipos: "logo" | "sep" | "group" | "btn" | "user" | "logout"
items = []

items.append(("logo",  "🕸️ ConVivir", None))
items.append(("btn",   "📋 Landing",  "inicio"))

if is_logged_in():
    usuario = get_session()

    # Institución
    secs_inst = [
        ("direccion",  "🏢 Dirección"),
        ("docente",    "👨‍🏫 Docentes"),
        ("alumno",     "🎒 Alumnos"),
    ]
    vis_inst = [(k, l) for k, l in secs_inst if puede_ver(k)]
    if vis_inst:
        items.append(("sep",   "|",            None))
        items.append(("group", "Institución",  None))
        for k, l in vis_inst:
            items.append(("btn", l, k))

    # Familia
    secs_fam = [
        ("familia",        "👪 Tutores"),
        ("alumno_familia", "👦 Alumnos Fam"),
    ]
    vis_fam = [(k, l) for k, l in secs_fam if puede_ver(k)]
    if vis_fam:
        items.append(("sep",   "|",       None))
        items.append(("group", "Familia", None))
        for k, l in vis_fam:
            items.append(("btn", l, k))

    # Animar
    secs_anim = [
        ("moderador", "🛡️ Moderadores"),
        ("admin",     "⚙️ Admin"),
    ]
    vis_anim = [(k, l) for k, l in secs_anim if puede_ver(k)]
    if vis_anim:
        items.append(("sep",   "|",      None))
        items.append(("group", "Animar", None))
        for k, l in vis_anim:
            items.append(("btn", l, k))

    # Usuario y logout
    items.append(("sep",    "|",      None))
    items.append(("user",   usuario,  None))
    items.append(("logout", "🚪 Salir", None))

else:
    items.append(("sep", "|",               None))
    items.append(("btn", "🔑 Iniciar sesión", "login"))

# Asignar anchos de columna por tipo
ANCHOS = {
    "logo":   2.0,
    "sep":    0.1,
    "group":  1.0,
    "btn":    1.0,
    "user":   2.2,
    "logout": 0.9,
}
col_sizes = [ANCHOS.get(tipo, 1.0) for tipo, _, _ in items]
cols = st.columns(col_sizes, gap="small")

for col, (tipo, label, key) in zip(cols, items):
    with col:
        if tipo == "logo":
            st.markdown(
                f'<div style="color:white;font-size:16px;font-weight:700;'
                f'padding-top:6px;white-space:nowrap;">{label}</div>',
                unsafe_allow_html=True
            )
        elif tipo == "sep":
            st.markdown(
                '<div style="color:rgba(255,255,255,0.15);font-size:18px;'
                'text-align:center;padding-top:4px;">|</div>',
                unsafe_allow_html=True
            )
        elif tipo == "group":
            st.markdown(
                f'<div style="color:rgba(255,255,255,0.35);font-size:9px;'
                f'font-weight:700;text-transform:uppercase;letter-spacing:1.2px;'
                f'padding-top:10px;white-space:nowrap;">{label}</div>',
                unsafe_allow_html=True
            )
        elif tipo == "btn":
            if st.button(label, key=f"nav_{key}"):
                st.session_state.seccion = key
                st.rerun()
        elif tipo == "user":
            st.markdown(
                f'<div style="color:rgba(255,255,255,0.55);font-size:11px;'
                f'line-height:1.35;padding-top:4px;white-space:nowrap;">'
                f'<b style="color:rgba(255,255,255,0.9);">{label["email"]}</b><br>'
                f'{label["rol"].replace("_"," ").capitalize()}'
                f'</div>',
                unsafe_allow_html=True
            )
        elif tipo == "logout":
            if st.button(label, key="nav_logout"):
                logout()
                st.rerun()

# ============================================================
# GUARD
# ============================================================
seccion = st.session_state.seccion

SECCIONES_PROTEGIDAS = [
    "direccion", "docente", "alumno",
    "familia", "alumno_familia",
    "moderador", "admin"
]

if seccion in SECCIONES_PROTEGIDAS and not is_logged_in():
    st.session_state.seccion = "login"
    seccion = "login"

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

    elif seccion == "docente":
        from secciones.docente import render
        render()

    elif seccion == "alumno":
        from secciones.alumno import render
        render()

    elif seccion == "admin":
        from secciones.admin_colegio import render
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
