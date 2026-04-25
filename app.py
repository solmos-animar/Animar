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

# 3. Ocultar sidebar nativa y el botón de colapsar
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# 4. Inicializar estado
if "seccion" not in st.session_state:
    st.session_state.seccion = "inicio"

# ============================================================
# NAVBAR SUPERIOR
# ============================================================
def nav_button(label, seccion_key):
    """Botón de navegación que marca la sección activa."""
    activo = st.session_state.seccion == seccion_key
    estilo_extra = "font-weight:700; border-bottom: 2px solid white;" if activo else "opacity:0.7;"
    if st.button(label, key=f"nav_{seccion_key}"):
        st.session_state.seccion = seccion_key
        st.rerun()

# CSS del navbar
st.markdown("""
<style>
.navbar-wrapper {
    position: sticky;
    top: 0;
    z-index: 999;
    background: #1a1a2e;
    padding: 8px 16px;
    margin-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.navbar-wrapper button {
    background: transparent !important;
    color: white !important;
    border: none !important;
    padding: 4px 10px !important;
    font-size: 13px !important;
    white-space: nowrap;
}
.navbar-wrapper button:hover {
    background: rgba(255,255,255,0.1) !important;
    border-radius: 6px !important;
}
/* Separador vertical entre grupos */
.nav-sep {
    color: rgba(255,255,255,0.2);
    font-size: 18px;
    align-self: center;
    padding: 0 2px;
    user-select: none;
}
/* Etiqueta de grupo */
.nav-group-label {
    color: rgba(255,255,255,0.35);
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    align-self: flex-end;
    padding-bottom: 2px;
    white-space: nowrap;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="navbar-wrapper">', unsafe_allow_html=True)

# Construir columnas dinámicamente según permisos
items = []  # lista de (tipo, label, key)  tipo = "btn" | "sep" | "label"

# Logo
items.append(("logo", "ConVivir", None))
items.append(("sep", None, None))

# Landing siempre visible
items.append(("btn", "📋 Landing", "inicio"))

if is_logged_in():
    usuario = get_session()
    rol = get_rol()

    # --- INSTITUCIÓN ---
    secs_inst = [("direccion", "🏢 Dirección"), ("docente", "👨‍🏫 Docentes"), ("alumno", "🎒 Alumnos")]
    vis_inst = [(k, l) for k, l in secs_inst if puede_ver(k)]
    if vis_inst:
        items.append(("sep", None, None))
        items.append(("label", "Institución", None))
        for k, l in vis_inst:
            items.append(("btn", l, k))

    # --- FAMILIA ---
    secs_fam = [("familia", "👪 Tutores"), ("alumno_familia", "👦 Alumnos (Fam)")]
    vis_fam = [(k, l) for k, l in secs_fam if puede_ver(k)]
    if vis_fam:
        items.append(("sep", None, None))
        items.append(("label", "Familia", None))
        for k, l in vis_fam:
            items.append(("btn", l, k))

    # --- ANIMAR ---
    secs_anim = [("moderador", "🛡️ Moderadores"), ("admin", "⚙️ Admin")]
    vis_anim = [(k, l) for k, l in secs_anim if puede_ver(k)]
    if vis_anim:
        items.append(("sep", None, None))
        items.append(("label", "Animar", None))
        for k, l in vis_anim:
            items.append(("btn", l, k))

    # --- Usuario + logout ---
    items.append(("sep", None, None))
    items.append(("user", usuario, None))
    items.append(("btn", "🚪 Salir", "__logout__"))

else:
    items.append(("sep", None, None))
    items.append(("btn", "🔑 Iniciar sesión", "login"))

# Calcular proporciones de columnas
col_sizes = []
for tipo, label, key in items:
    if tipo == "logo":
        col_sizes.append(1.8)
    elif tipo == "sep":
        col_sizes.append(0.15)
    elif tipo == "label":
        col_sizes.append(0.9)
    elif tipo == "user":
        col_sizes.append(2)
    else:
        col_sizes.append(1)

cols = st.columns(col_sizes)

for i, (tipo, label, key) in enumerate(items):
    with cols[i]:
        if tipo == "logo":
            st.markdown(
                '<span style="color:white; font-size:20px; font-weight:700; letter-spacing:0.5px;">🕸️ ConVivir</span>',
                unsafe_allow_html=True
            )
        elif tipo == "sep":
            st.markdown('<span class="nav-sep">|</span>', unsafe_allow_html=True)
        elif tipo == "label":
            st.markdown(f'<span class="nav-group-label">{label}</span>', unsafe_allow_html=True)
        elif tipo == "user":
            st.markdown(
                f'<div style="color:rgba(255,255,255,0.75); font-size:11px; line-height:1.4; padding-top:4px;">'
                f'<b style="color:white;">{label["email"]}</b><br>'
                f'{label["rol"].replace("_"," ").capitalize()}'
                f'</div>',
                unsafe_allow_html=True
            )
        elif tipo == "btn":
            if key == "__logout__":
                if st.button(label, key="nav___logout__"):
                    logout()
                    st.rerun()
            else:
                nav_button(label, key)

st.markdown('</div>', unsafe_allow_html=True)

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
