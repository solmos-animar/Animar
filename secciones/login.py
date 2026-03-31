# secciones/login.py
import streamlit as st
from sqlalchemy import text
from utilidades.auth import verify_password, destino_post_login

conn = st.connection("postgresql", type="sql")

def render():

    _, col_center, _ = st.columns([1, 1.2, 1])

    with col_center:
        st.markdown("""
            <div style="text-align:center; padding: 48px 0 28px;">
                <div style="font-size:44px; margin-bottom:10px;">🕸️</div>
                <h1 style="font-family:'Georgia',serif; font-size:34px; color:#0f2240;
                           margin:0; letter-spacing:-1px;">ConVivir</h1>
                <p style="color:#9a9690; font-size:14px; margin-top:6px;">
                    Plataforma de Convivencia Escolar
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div style="background:white; border:1px solid #ebe9e4; border-radius:16px;
                        padding:32px; box-shadow:0 4px 24px rgba(15,34,64,0.10);">
        """, unsafe_allow_html=True)

        with st.form("form_login", clear_on_submit=False):
            email_in = st.text_input(
                "Email",
                placeholder="tu@email.com",
            )
            pass_in = st.text_input(
                "Contraseña",
                type="password",
                placeholder="••••••••"
            )

            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

            submitted = st.form_submit_button(
                "Iniciar sesión →",
                type="primary",
                use_container_width=True
            )

            if submitted:
                if not email_in or not pass_in:
                    st.warning("⚠️ Completá email y contraseña.")
                else:
                    try:
                        with conn.session as s:
                            res = s.execute(text("""
                                SELECT id, email, password_hash, rol,
                                       colegio_id, persona_id, activo
                                FROM usuarios
                                WHERE email = :email
                                LIMIT 1
                            """), {"email": email_in.strip().lower()})
                            usuario = res.fetchone()

                        if usuario is None or not verify_password(pass_in, usuario.password_hash):
                            st.error("❌ Email o contraseña incorrectos.")
                        elif not usuario.activo:
                            st.error("❌ Tu cuenta está desactivada. Contactá al administrador.")
                        else:
                            # Guardar sesión
                            st.session_state.usuario = {
                                "id":         usuario.id,
                                "email":      usuario.email,
                                "rol":        usuario.rol,
                                "colegio_id": usuario.colegio_id,
                                "persona_id": usuario.persona_id,
                            }
                            # Redirigir según rol
                            destino = destino_post_login()
                            st.session_state.seccion = destino
                            st.rerun()

                    except Exception as e:
                        st.error(f"Error al conectar con la base de datos: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <div style="text-align:center; margin-top:20px;">
                <span style="color:#9a9690; font-size:13px;">
                    ¿No tenés cuenta? Contactá al administrador de tu institución.
                </span>
            </div>
        """, unsafe_allow_html=True)

        if st.button("← Volver a la página principal", use_container_width=True):
            st.session_state.seccion = "inicio"
            st.rerun()
