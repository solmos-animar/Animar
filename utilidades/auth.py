# utilidades/auth.py
import hashlib
import secrets
import streamlit as st
from sqlalchemy import text

# ============================================================
# HASHING DE CONTRASEÑAS
# ============================================================

def hash_password(password: str) -> str:
    """Genera un hash seguro con salt aleatorio. Formato: salt$hash"""
    salt = secrets.token_hex(32)
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(password: str, stored_hash: str) -> bool:
    """Verifica una contraseña contra el hash almacenado."""
    try:
        salt, hashed = stored_hash.split("$", 1)
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest() == hashed
    except Exception:
        return False

# ============================================================
# SESIÓN
# ============================================================

def get_session() -> dict | None:
    """Devuelve el usuario logueado o None."""
    return st.session_state.get("usuario", None)

def is_logged_in() -> bool:
    return get_session() is not None

def get_rol() -> str | None:
    u = get_session()
    return u["rol"] if u else None

def get_colegio_id() -> int | None:
    u = get_session()
    return u.get("colegio_id") if u else None

def logout():
    st.session_state.pop("usuario", None)
    st.session_state.seccion = "inicio"

# ============================================================
# PERMISOS POR ROL
# ============================================================

# Secciones habilitadas por rol
SECCIONES_POR_ROL = {
    "animar_admin": [
        "inicio", "login", "admin", "direccion", "docente", "alumno",
        "familia", "alumno_familia", "moderador"
    ],
    "animar_moderador": [
        "inicio", "login", "moderador", "familia", "alumno_familia",
        "alumno", "docente", "direccion"
    ],
    "directivo": [
        "inicio", "login", "direccion", "docente", "alumno"
    ],
    "docente": [
        "inicio", "login", "docente", "alumno"
    ],
    "alumno": [
        "inicio", "login", "alumno"
    ],
    "tutor": [
        "inicio", "login", "familia", "alumno_familia"
    ],
}

# Sección de destino al hacer login según rol
DESTINO_POR_ROL = {
    "animar_admin":      "admin",
    "animar_moderador":  "moderador",
    "directivo":         "direccion",
    "docente":           "docente",
    "alumno":            "alumno",
    "tutor":             "familia",
}

def puede_ver(seccion: str) -> bool:
    """Devuelve True si el usuario logueado puede acceder a esa sección."""
    rol = get_rol()
    if rol is None:
        return seccion == "inicio"
    return seccion in SECCIONES_POR_ROL.get(rol, ["inicio"])

def destino_post_login() -> str:
    """Sección a la que redirigir después de un login exitoso."""
    rol = get_rol()
    return DESTINO_POR_ROL.get(rol, "inicio")

# ============================================================
# GUARD — usar al inicio de cada sección protegida
# ============================================================

def require_login(seccion: str = None):
    """
    Llama esto al inicio de cada sección.
    Si el usuario no tiene permiso, muestra error y detiene la ejecución.
    """
    if not is_logged_in():
        st.warning("🔒 Necesitás iniciar sesión para acceder a esta sección.")
        if st.button("Ir al Login"):
            st.switch_page("pages/login.py")
        st.stop()

    if seccion and not puede_ver(seccion):
        st.error("⛔ No tenés permisos para acceder a esta sección.")
        st.stop()

# ============================================================
# CREAR USUARIO (para usar desde el backoffice)
# ============================================================

def crear_usuario(conn, email: str, password: str, rol: str,
                  colegio_id: int = None, persona_id: int = None) -> tuple[bool, str]:
    """
    Crea un usuario nuevo en la base de datos.
    Retorna (éxito: bool, mensaje: str)
    """
    if rol not in SECCIONES_POR_ROL:
        return False, f"Rol inválido: {rol}"

    password_hash = hash_password(password)
    try:
        with conn.session as s:
            s.execute(text("""
                INSERT INTO usuarios (email, password_hash, rol, colegio_id, persona_id)
                VALUES (:email, :hash, :rol, :cid, :pid)
            """), {
                "email": email.strip().lower(),
                "hash":  password_hash,
                "rol":   rol,
                "cid":   colegio_id,
                "pid":   persona_id,
            })
            s.commit()
        return True, "Usuario creado correctamente."
    except Exception as e:
        if "unique" in str(e).lower():
            return False, f"El email {email} ya existe en el sistema."
        return False, str(e)

def cambiar_password(conn, usuario_id: int, nueva_password: str) -> tuple[bool, str]:
    """Actualiza el hash de contraseña de un usuario."""
    try:
        with conn.session as s:
            s.execute(text("""
                UPDATE usuarios SET password_hash = :hash WHERE id = :id
            """), {"hash": hash_password(nueva_password), "id": usuario_id})
            s.commit()
        return True, "Contraseña actualizada."
    except Exception as e:
        return False, str(e)
