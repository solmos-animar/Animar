# pages/login.py
import streamlit as st
from sqlalchemy import text
from utilidades.auth import verify_password, destino_post_login, is_logged_in

st.set_page_config(
    page_title="ConVivir — Iniciar sesión",
    page_icon="🕸️",
    layout="centered",
)

# Cargar CSS
try:
    with open("utilidades/desktop.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Si ya está logueado, redirigir directo
if is_logged_in():
    destino = destino_post_login()
    st.session_state.seccion = destino
    st.switch_page("app.py")

conn = st.connection("postgresql", type="sql")

# ---- UI ----
st.markdown("""
    <div style="text-align:center; padding: 40px 0 24px;">
        <div style="font-size:42px; margin-bottom:8px;">🕸️</div>
        <h1 style="font-family:'Georgia',serif; font-size:36px; color:#0f2240;
                   margin:0; letter-spacing:-1px;">ConVivir</h1>
        <p style="color:#9a9690; font-size:14px; margin-top:6px;">
            Plataforma de Convivencia Escolar
        </p>
    </div>
""", unsafe_allow_html=True)

with st.form("form_login", clear_on_submit=False):
    st.markdown("""
        <div style="background:white; border:1px solid #ebe9e4; border-radius:16px;
                    padding:28px 32px; box-shadow:0 4px 16px rgba(15,34,64,0.08);">
    """, unsafe_allow_html=True)

    email = st.text_input(
        "Email",
        placeholder="tu@email.com",
        label_visibility="visible"
    )
    password = st.text_input(
        "Contraseña",
        type="password",
        placeholder="••••••••"
    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    submitted = st.form_submit_button(
        "Iniciar sesión →",
        type="primary",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not email or not password:
            st.warning("Completá email y contraseña.")
        else:
            try:
                with conn.session as s:
                    res = s.execute(text("""
                        SELECT id, email, password_hash, rol, colegio_id, persona_id, activo
                        FROM usuarios
                        WHERE email = :email
                        LIMIT 1
                    """), {"email": email.strip().lower()})
                    usuario = res.fetchone()

                if usuario is None:
                    st.error("Email o contraseña incorrectos.")
                elif not usuario.activo:
                    st.error("Tu cuenta está desactivada. Contactá al administrador.")
                elif not verify_password(password, usuario.password_hash):
                    st.error("Email o contraseña incorrectos.")
                else:
                    # Guardar sesión
                    st.session_state.usuario = {
                        "id":         usuario.id,
                        "email":      usuario.email,
                        "rol":        usuario.rol,
                        "colegio_id": usuario.colegio_id,
                        "persona_id": usuario.persona_id,
                    }
                    destino = destino_post_login()
                    st.session_state.seccion = destino
                    st.success(f"¡Bienvenido/a! Redirigiendo...")
                    st.switch_page("app.py")

            except Exception as e:
                st.error(f"Error al conectar con la base de datos: {e}")

# Link para volver a la landing
st.markdown("""
    <div style="text-align:center; margin-top:24px;">
        <a href="/" style="color:#9a9690; font-size:13px; text-decoration:none;">
            ← Volver a la página principal
        </a>
    </div>
""", unsafe_allow_html=True)
