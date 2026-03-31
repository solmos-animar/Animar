# utilidades/cambiar_pass_widget.py
import streamlit as st
from utilidades.auth import verify_password, cambiar_password, get_session

conn = st.connection("postgresql", type="sql")

def render_cambiar_password():
    """
    Widget reutilizable para cambio de contraseña.
    Llamar desde cualquier sección de usuario con:
        from utilidades.cambiar_pass_widget import render_cambiar_password
        render_cambiar_password()
    """
    usuario = get_session()
    if not usuario:
        return

    with st.expander("🔑 Cambiar mi contraseña", expanded=False):
        st.markdown("""
            <div style="background:linear-gradient(135deg,#f0f4ff 0%,#fef9f0 100%);
                border-left:4px solid #1a56a0; border-radius:0 12px 12px 0;
                padding:14px 18px 8px; margin-bottom:16px;">
                <span style="font-size:13px; color:#0f2240; font-weight:600;">
                    🔒 Seguridad de la cuenta
                </span><br>
                <span style="font-size:12px; color:#5c5852;">
                    Tu contraseña actual es necesaria para confirmar el cambio.
                </span>
            </div>
        """, unsafe_allow_html=True)

        with st.form("form_cambio_pass_usuario", clear_on_submit=True):
            pass_actual = st.text_input(
                "Contraseña actual *",
                type="password",
                placeholder="Tu contraseña actual"
            )
            col1, col2 = st.columns(2)
            pass_nueva    = col1.text_input("Nueva contraseña *",    type="password", placeholder="Mínimo 8 caracteres")
            pass_confirmar = col2.text_input("Confirmar nueva contraseña *", type="password", placeholder="Repetir contraseña")

            submitted = st.form_submit_button(
                "Actualizar contraseña",
                type="primary",
                use_container_width=True
            )

            if submitted:
                errores = []
                if not pass_actual:                        errores.append("Ingresá tu contraseña actual")
                if not pass_nueva:                         errores.append("Ingresá la nueva contraseña")
                if len(pass_nueva or "") < 8:              errores.append("La nueva contraseña debe tener al menos 8 caracteres")
                if pass_nueva != pass_confirmar:           errores.append("Las contraseñas nuevas no coinciden")

                if errores:
                    st.warning(f"⚠️ {' · '.join(errores)}")
                else:
                    # Verificar contraseña actual
                    try:
                        from sqlalchemy import text
                        with conn.session as s:
                            res = s.execute(
                                text("SELECT password_hash FROM usuarios WHERE id = :id"),
                                {"id": usuario["id"]}
                            )
                            row = res.fetchone()

                        if not row or not verify_password(pass_actual, row[0]):
                            st.error("❌ La contraseña actual es incorrecta.")
                        else:
                            ok, msg = cambiar_password(conn, usuario["id"], pass_nueva)
                            if ok:
                                st.success("✅ Contraseña actualizada correctamente.")
                            else:
                                st.error(f"❌ {msg}")
                    except Exception as e:
                        st.error(f"Error: {e}")
