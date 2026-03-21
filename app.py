import streamlit as st
import json, io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="ConVivir",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# MOTOR DE DATOS (JSON local)
# ══════════════════════════════════════════════════════════════════════════════
DATA_DIR   = Path(__file__).parent
AULAS_FILE = DATA_DIR / "aulas.json"
RESP_FILE  = DATA_DIR / "respuestas.json"

def _load(path):
    if path.exists():
        try: return json.loads(path.read_text(encoding="utf-8"))
        except: return {}
    return {}

def _save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def get_aulas():
    data = _load(AULAS_FILE)
    if not data:
        data = {"DEMO2025": {"nombre":"3° A Primaria","docente":"Prof. María García","creada":"2025-01-01",
            "alumnos":[{"id":1,"nombre":"Lucas Martínez","genero":"M"},{"id":2,"nombre":"Sofía Rodríguez","genero":"F"},
                {"id":3,"nombre":"Mateo González","genero":"M"},{"id":4,"nombre":"Valentina Torres","genero":"F"},
                {"id":5,"nombre":"Benjamín López","genero":"M"},{"id":6,"nombre":"Camila Díaz","genero":"F"},
                {"id":7,"nombre":"Nicolás Pérez","genero":"M"},{"id":8,"nombre":"Isabella Moreno","genero":"F"},
                {"id":9,"nombre":"Santiago Romero","genero":"M"},{"id":10,"nombre":"Emma Álvarez","genero":"F"},
                {"id":11,"nombre":"Joaquín Ramírez","genero":"M"},{"id":12,"nombre":"Martina Castro","genero":"F"}]}}
        _save(AULAS_FILE, data)
    return data

def get_aula(codigo): return get_aulas().get(codigo.upper())

def crear_aula(codigo, nombre, docente, alumnos):
    aulas = get_aulas()
    aulas[codigo.upper()] = {"nombre":nombre,"docente":docente,"creada":datetime.now().strftime("%Y-%m-%d"),
        "alumnos":[{"id":i+1,"nombre":a["nombre"],"genero":a.get("genero","?")} for i,a in enumerate(alumnos)]}
    _save(AULAS_FILE, aulas)

def get_alumno_by_numero(codigo, numero):
    aula = get_aula(codigo)
    if not aula: return None
    return next((a for a in aula["alumnos"] if a["id"]==numero), None)

def get_respuestas(): return _load(RESP_FILE)

def ya_respondio(codigo, alumno_id):
    return f"{codigo.upper()}_{alumno_id}" in get_respuestas()

def guardar_respuesta(codigo, alumno_id, respuesta):
    resp = get_respuestas()
    respuesta.update({"alumno_id":alumno_id,"codigo_aula":codigo.upper(),"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")})
    resp[f"{codigo.upper()}_{alumno_id}"] = respuesta
    _save(RESP_FILE, resp)

def get_respuestas_aula(codigo):
    return [v for k,v in get_respuestas().items() if k.startswith(codigo.upper()+"_")]

DIM_META = {
    "me_gusta":("positivo",1.0),"mis_amigos":("positivo",1.2),"ayuda":("positivo",0.8),"anima":("positivo",0.8),
    "no_me_gusta":("negativo",-1.0),"no_deja_participar":("negativo",-0.8),"insulta":("negativo",-0.7),
}

def calcular_sociograma(codigo):
    aula = get_aula(codigo)
    if not aula: return {}
    alumnos = {a["id"]:a for a in aula["alumnos"]}
    respuestas = get_respuestas_aula(codigo)
    stats = {aid:{"nombre":a["nombre"],"genero":a["genero"],"score_social":0.0,
                  "votos_positivos":0,"votos_negativos":0,"respondio":False,"perfil":"Sin datos","alerta":None}
             for aid,a in alumnos.items()}
    edges = []
    for r in respuestas:
        oid = r["alumno_id"]
        if oid in stats: stats[oid]["respondio"] = True
        for dim,(tipo,peso) in DIM_META.items():
            for did in (r.get(dim) or []):
                if did not in stats or did==oid: continue
                stats[did]["score_social"] += peso
                if tipo=="positivo": stats[did]["votos_positivos"]+=1; edges.append((oid,did,"positivo"))
                else:                stats[did]["votos_negativos"]+=1; edges.append((oid,did,"negativo"))
    n = len(respuestas)
    for s in stats.values():
        vp,vn = s["votos_positivos"],s["votos_negativos"]
        if n==0 or (vp==0 and vn==0): perfil,alerta="Sin datos",None
        elif vp>=4 and vn<=1:          perfil,alerta="Popular",None
        elif vn>=4 and vp<=1:          perfil,alerta="Rechazado","Alta"
        elif vp<=1 and vn<=1:          perfil,alerta="Aislado","Alta" if vp==0 else "Media"
        elif vp>=2 and vn>=2:          perfil,alerta="Controvertido","Media"
        else:                           perfil,alerta="Integrado",None
        s["perfil"],s["alerta"] = perfil,alerta
    stats["_edges"]=edges; stats["_n"]=n; stats["_total"]=len(alumnos)
    return stats

# Mock data admin
COLEGIOS_MOCK = [
    {"id":1,"nombre":"Instituto San Martín","ciudad":"Buenos Aires","docentes":4,"aulas":6,"estado":"Activo"},
    {"id":2,"nombre":"Colegio del Valle","ciudad":"Córdoba","docentes":2,"aulas":3,"estado":"Activo"},
    {"id":3,"nombre":"Escuela Belgrano","ciudad":"Rosario","docentes":1,"aulas":2,"estado":"Pendiente KYC"},
    {"id":4,"nombre":"Colegio Las Flores","ciudad":"Mendoza","docentes":3,"aulas":4,"estado":"Activo"},
]
DOCENTES_MOCK = [
    {"id":1,"nombre":"María García","email":"docente@colegio.ar","colegio":"Instituto San Martín","kyc":"Aprobado"},
    {"id":2,"nombre":"Carlos López","email":"clopez@colegio.ar","colegio":"Instituto San Martín","kyc":"Aprobado"},
    {"id":3,"nombre":"Ana Fernández","email":"afernandez@valle.ar","colegio":"Colegio del Valle","kyc":"Pendiente"},
    {"id":4,"nombre":"Roberto Soria","email":"rsoria@belgrano.ar","colegio":"Escuela Belgrano","kyc":"En revisión"},
]
ALERTAS_MOCK = [
    {"id":1,"alumno":"Valentina Torres","aula":"3° A","tipo":"Rechazo elevado","prioridad":"Alta","fecha":"2025-05-10","estado":"Pendiente","nota":""},
    {"id":2,"alumno":"Mateo González","aula":"3° A","tipo":"Aislamiento","prioridad":"Alta","fecha":"2025-05-10","estado":"En gestión","nota":"Se habló con la familia."},
    {"id":3,"alumno":"Nicolás Pérez","aula":"3° A","tipo":"Perfil controvertido","prioridad":"Media","fecha":"2025-05-10","estado":"Pendiente","nota":""},
]

# ── Estado de sesión ──────────────────────────────────────────────────────────
for k,v in [("logged_in",False),("user",None),("page","home")]:
    if k not in st.session_state: st.session_state[k] = v

def go(page): st.session_state.page = page; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PANTALLA DE LOGIN — limpia, centrada, sin landing
# ══════════════════════════════════════════════════════════════════════════════
def show_login():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;700;800&display=swap');
    body, .main { background:#f0f4ff !important; }
    header[data-testid="stHeader"] { display:none; }
    [data-testid="stSidebar"] { display:none !important; }
    .block-container { padding:0 !important; }
    .login-page { min-height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; background:linear-gradient(135deg,#e8f0fe 0%,#f0f4ff 50%,#e0ecff 100%); padding:32px 16px; }
    .login-logo { display:flex; align-items:center; gap:12px; margin-bottom:8px; }
    .login-logo-txt { font-family:'Sora',sans-serif; font-size:32px; font-weight:800; color:#0a1f5c; letter-spacing:-1px; }
    .login-logo-txt em { font-style:normal; color:#1a6fff; }
    .login-sub { color:#5c6e8a; font-size:15px; margin-bottom:40px; text-align:center; }
    .login-title { font-family:'Sora',sans-serif; font-size:22px; font-weight:800; color:#0a1f5c; margin-bottom:6px; text-align:center; }
    .login-subtitle { font-size:14px; color:#7a8aaa; margin-bottom:28px; text-align:center; }
    .profile-grid { display:grid; grid-template-columns:1fr 1fr; gap:14px; width:100%; max-width:460px; margin-bottom:16px; }
    .profile-grid-3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; width:100%; max-width:460px; margin-bottom:16px; }
    .pcard { background:white; border:2px solid #e0e8ff; border-radius:18px; padding:28px 16px 22px; text-align:center; cursor:pointer; transition:all .18s; box-shadow:0 2px 12px rgba(26,111,255,0.07); }
    .pcard:hover { border-color:#1a6fff; transform:translateY(-3px); box-shadow:0 8px 24px rgba(26,111,255,0.15); }
    .pcard-ico { font-size:42px; margin-bottom:10px; }
    .pcard-name { font-family:'Sora',sans-serif; font-size:15px; font-weight:800; color:#0a1f5c; margin-bottom:4px; }
    .pcard-desc { font-size:12px; color:#7a8aaa; line-height:1.5; }
    .back-btn { color:#7a8aaa; font-size:13px; cursor:pointer; margin-top:8px; }
    </style>
    <div class="login-page">
      <div class="login-logo">
        <svg width="42" height="42" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <rect width="100" height="100" rx="16" fill="#1a6fff"/>
          <path d="M11,92 L35,20 L50,20 L50,92 Z" fill="#0a2a6e"/>
          <path d="M89,92 L65,20 L50,20 L50,92 Z" fill="#0a2a6e"/>
          <circle cx="50" cy="45" r="9" fill="#93c5fd"/>
          <path d="M50,54 Q37,47 29,35" stroke="#93c5fd" stroke-width="7" stroke-linecap="round" fill="none"/>
          <path d="M50,54 Q63,47 71,35" stroke="#93c5fd" stroke-width="7" stroke-linecap="round" fill="none"/>
          <line x1="50" y1="54" x2="50" y2="73" stroke="#93c5fd" stroke-width="7" stroke-linecap="round"/>
          <line x1="50" y1="73" x2="42" y2="88" stroke="#93c5fd" stroke-width="6" stroke-linecap="round"/>
          <line x1="50" y1="73" x2="58" y2="88" stroke="#93c5fd" stroke-width="6" stroke-linecap="round"/>
        </svg>
        <span class="login-logo-txt">Con<em>Vivir</em></span>
      </div>
      <p class="login-sub">Plataforma de Convivencia Escolar</p>
    </div>
    """, unsafe_allow_html=True)

    if "login_step" not in st.session_state: st.session_state.login_step = "choose"

    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        if st.session_state.login_step == "choose":
            st.markdown("<p class='login-title'>¿Cómo querés ingresar?</p>", unsafe_allow_html=True)

            st.markdown("""
            <div class="profile-grid">
              <div class="pcard"><div class="pcard-ico">🏛️</div>
                <div class="pcard-name">Administrador</div>
                <div class="pcard-desc">Gestión de colegios, docentes y KYC</div></div>
              <div class="pcard"><div class="pcard-ico">🏫</div>
                <div class="pcard-name">Colegio</div>
                <div class="pcard-desc">Docentes, familias y alumnos</div></div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Entrar como\nAdministrador", use_container_width=True, type="primary", key="btn_admin"):
                    st.session_state.logged_in = True
                    st.session_state.user = {"role":"admin","name":"Administrador","email":"admin@convivir.ar"}
                    st.session_state.page = "home"
                    st.rerun()
            with c2:
                if st.button("Entrar al\nColegio →", use_container_width=True, key="btn_colegio"):
                    st.session_state.login_step = "colegio"
                    st.rerun()

        elif st.session_state.login_step == "colegio":
            st.markdown("<p class='login-title'>Colegio — ¿Quién sos?</p>", unsafe_allow_html=True)

            st.markdown("""
            <div class="profile-grid-3">
              <div class="pcard"><div class="pcard-ico">👨‍🏫</div>
                <div class="pcard-name">Docente</div>
                <div class="pcard-desc">Sociograma, alertas y reportes</div></div>
              <div class="pcard"><div class="pcard-ico">👨‍👩‍👧</div>
                <div class="pcard-name">Familia</div>
                <div class="pcard-desc">Contenido y seguimiento</div></div>
              <div class="pcard"><div class="pcard-ico">🎒</div>
                <div class="pcard-name">Alumno</div>
                <div class="pcard-desc">Encuesta y contenido</div></div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Soy Docente", use_container_width=True, type="primary", key="btn_teacher"):
                    st.session_state.logged_in = True
                    st.session_state.user = {"role":"teacher","name":"Prof. María García","email":"docente@colegio.ar"}
                    st.session_state.page = "home"
                    st.rerun()
            with c2:
                if st.button("Soy Familia", use_container_width=True, type="primary", key="btn_family"):
                    st.session_state.logged_in = True
                    st.session_state.user = {"role":"student","name":"Carlos Martínez (Padre)","email":"familia@colegio.ar"}
                    st.session_state.page = "home"
                    st.rerun()
            with c3:
                if st.button("Soy Alumno", use_container_width=True, type="primary", key="btn_student"):
                    st.session_state.logged_in = True
                    st.session_state.user = {"role":"student","name":"Lucas Martínez","email":"alumno@colegio.ar"}
                    st.session_state.page = "home"
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("← Volver", key="btn_back", use_container_width=True):
                st.session_state.login_step = "choose"
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TOPBAR  (reemplaza el sidebar)
# ══════════════════════════════════════════════════════════════════════════════
def topbar():
    user = st.session_state.user
    role = user["role"]

    # CSS topbar
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&display=swap');
    [data-testid="stSidebar"] { display:none !important; }
    header[data-testid="stHeader"] { display:none; }
    .block-container { padding-top:80px !important; padding-left:2rem; padding-right:2rem; }
    .topbar { position:fixed; top:0; left:0; right:0; height:62px; background:white;
              border-bottom:1px solid #e0e8ff; z-index:999;
              display:flex; align-items:center; padding:0 28px; gap:20px;
              box-shadow:0 2px 12px rgba(26,111,255,0.07); }
    .tb-logo { display:flex; align-items:center; gap:8px; margin-right:16px; }
    .tb-logo-txt { font-family:'Sora',sans-serif; font-size:18px; font-weight:800; color:#0a1f5c; }
    .tb-logo-txt em { font-style:normal; color:#1a6fff; }
    .tb-nav { display:flex; gap:4px; flex:1; overflow-x:auto; }
    .tb-user { margin-left:auto; display:flex; align-items:center; gap:10px; font-size:13px; color:#5c6e8a; white-space:nowrap; }
    </style>
    """, unsafe_allow_html=True)

    # Logo en topbar (HTML puro)
    logo_svg = ('<svg width="30" height="30" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
                '<rect width="100" height="100" rx="12" fill="#1a6fff"/>'
                '<path d="M11,92 L35,20 L50,20 L50,92 Z" fill="#0a2a6e"/>'
                '<path d="M89,92 L65,20 L50,20 L50,92 Z" fill="#0a2a6e"/>'
                '<circle cx="50" cy="45" r="9" fill="#93c5fd"/>'
                '<path d="M50,54 Q37,47 29,35" stroke="#93c5fd" stroke-width="7" stroke-linecap="round" fill="none"/>'
                '<path d="M50,54 Q63,47 71,35" stroke="#93c5fd" stroke-width="7" stroke-linecap="round" fill="none"/>'
                '<line x1="50" y1="54" x2="50" y2="73" stroke="#93c5fd" stroke-width="7" stroke-linecap="round"/>'
                '<line x1="50" y1="73" x2="42" y2="88" stroke="#93c5fd" stroke-width="6" stroke-linecap="round"/>'
                '<line x1="50" y1="73" x2="58" y2="88" stroke="#93c5fd" stroke-width="6" stroke-linecap="round"/>'
                '</svg>')
    st.markdown(
        '<div class="topbar"><div class="tb-logo">' + logo_svg +
        '<span class="tb-logo-txt">Con<em>Vivir</em></span></div></div>',
        unsafe_allow_html=True
    )

    # Botones de navegación según rol
    if role == "admin":
        navs = [("🏠 Inicio","home"),("🏫 Colegios","admin_colegios"),
                ("👨‍🏫 Docentes","admin_docentes"),("✅ KYC","admin_kyc")]
    elif role == "teacher":
        navs = [("🏠 Inicio","home"),("🕸️ Sociograma","sociograma"),
                ("🚪 Mis Aulas","aulas"),("🚨 Alertas","alertas"),
                ("📋 Reportes","reportes"),("📝 Encuesta alumnos","encuesta_info")]
    else:
        navs = [("🏠 Inicio","home"),("📝 Encuesta","encuesta"),("📚 Contenido","contenido")]

    cur = st.session_state.page
    cols = st.columns(len(navs) + 1)
    for i, (label, key) in enumerate(navs):
        is_active = (cur == key)
        btn_type = "primary" if is_active else "secondary"
        if cols[i].button(label, key="nav_"+key, use_container_width=True, type=btn_type):
            go(key)

    # Cerrar sesión al final
    if cols[-1].button("🚪 Salir", key="nav_logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "home"
        st.session_state.login_step = "choose"
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# HOME DOCENTE — tarjetas grandes
# ══════════════════════════════════════════════════════════════════════════════
def page_teacher_home():
    user = st.session_state.user
    nombre = user["name"].replace("Prof. ","")
    hora = datetime.now().hour
    saludo = "Buenos días" if hora < 12 else ("Buenas tardes" if hora < 19 else "Buenas noches")

    st.markdown(f"""
    <style>
    .home-greeting {{ font-family:'Sora',sans-serif; font-size:28px; font-weight:800;
        color:#0a1f5c; margin-bottom:4px; }}
    .home-sub {{ color:#7a8aaa; font-size:15px; margin-bottom:32px; }}
    .hcard {{ background:white; border-radius:20px; padding:28px 24px; border:2px solid #e8eeff;
        box-shadow:0 4px 20px rgba(26,111,255,0.07); cursor:pointer;
        transition:all .2s; text-align:center; height:100%; }}
    .hcard:hover {{ border-color:#1a6fff; transform:translateY(-4px);
        box-shadow:0 12px 32px rgba(26,111,255,0.15); }}
    .hcard-ico {{ font-size:52px; margin-bottom:14px; }}
    .hcard-title {{ font-family:'Sora',sans-serif; font-size:17px; font-weight:800;
        color:#0a1f5c; margin-bottom:6px; }}
    .hcard-desc {{ font-size:13px; color:#7a8aaa; line-height:1.6; }}
    .hcard-badge {{ display:inline-block; margin-top:12px; padding:4px 14px;
        border-radius:100px; font-size:11px; font-weight:700; }}
    .badge-blue  {{ background:#e8f0fe; color:#1a56a0; }}
    .badge-green {{ background:#e6f4ee; color:#1d7a55; }}
    .badge-red   {{ background:#fdeaea; color:#c0392b; }}
    .badge-orange{{ background:#fef3e2; color:#d4580a; }}
    .badge-purple{{ background:#ede8fe; color:#5b3fa0; }}
    .stat-row {{ display:flex; gap:16px; margin-bottom:32px; }}
    .stat-box {{ background:white; border-radius:14px; padding:20px 24px; flex:1;
        border:1px solid #e8eeff; box-shadow:0 2px 8px rgba(26,111,255,0.05); }}
    .stat-num {{ font-family:'Sora',sans-serif; font-size:32px; font-weight:800; color:#0a1f5c; }}
    .stat-lbl {{ font-size:13px; color:#7a8aaa; margin-top:2px; }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<p class="home-greeting">👋 {saludo}, {nombre.split()[0]}</p>'
                '<p class="home-sub">¿Qué querés hacer hoy?</p>', unsafe_allow_html=True)

    # Stats rápidas
    aulas = get_aulas()
    total_alumnos = sum(len(a["alumnos"]) for a in aulas.values())
    total_resp    = sum(len(get_respuestas_aula(c)) for c in aulas)
    alertas_pend  = sum(1 for a in ALERTAS_MOCK if a["estado"]=="Pendiente")

    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-box"><div class="stat-num">{len(aulas)}</div><div class="stat-lbl">🚪 Aulas activas</div></div>
      <div class="stat-box"><div class="stat-num">{total_alumnos}</div><div class="stat-lbl">👩‍🎓 Alumnos registrados</div></div>
      <div class="stat-box"><div class="stat-num">{total_resp}</div><div class="stat-lbl">📝 Encuestas respondidas</div></div>
      <div class="stat-box"><div class="stat-num" style="color:{'#c0392b' if alertas_pend>0 else '#1d7a55'}">{alertas_pend}</div><div class="stat-lbl">🚨 Alertas pendientes</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Tarjetas principales
    cards = [
        ("sociograma",   "🕸️", "Sociograma del Aula",
         "Visualizá el mapa de relaciones sociales generado a partir de las encuestas.",
         "badge-blue",   "Ver sociograma →"),
        ("aulas",        "🚪", "Gestión de Aulas",
         "Cargá el listado de alumnos desde Excel y generá el código de acceso para la encuesta.",
         "badge-green",  "Gestionar aulas →"),
        ("alertas",      "🚨", "Alertas de Riesgo",
         "Revisá los alumnos identificados en riesgo de aislamiento, rechazo o acoso.",
         "badge-red",    f"{alertas_pend} alertas pendientes →"),
        ("reportes",     "📊", "Reportes",
         "Descargá informes individuales o grupales con perfiles sociométricos completos.",
         "badge-purple", "Ver reportes →"),
        ("encuesta_info","📝", "Encuesta para alumnos",
         "Compartí el código con tus alumnos para que respondan la encuesta de convivencia.",
         "badge-orange", "Ver código del aula →"),
        ("denuncias",    "🆘", "Denuncias de Acoso",
         "Registrá y gestioná situaciones de bullying reportadas por alumnos o familias.",
         "badge-red",    "Ver denuncias →"),
    ]

    row1 = st.columns(3)
    row2 = st.columns(3)
    rows = [row1, row2]

    for i, (page_key, ico, title, desc, badge_cls, cta) in enumerate(cards):
        with rows[i//3][i%3]:
            st.markdown(f"""
            <div class="hcard">
              <div class="hcard-ico">{ico}</div>
              <div class="hcard-title">{title}</div>
              <div class="hcard-desc">{desc}</div>
              <span class="hcard-badge {badge_cls}">{cta}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Abrir {title}", key="home_"+page_key, use_container_width=True, type="primary"):
                go(page_key)

# ══════════════════════════════════════════════════════════════════════════════
# HOME ALUMNO
# ══════════════════════════════════════════════════════════════════════════════
def page_student_home():
    user = st.session_state.user
    st.markdown(f"""
    <style>
    .hcard {{ background:white; border-radius:20px; padding:28px 24px; border:2px solid #e8eeff;
        box-shadow:0 4px 20px rgba(26,111,255,0.07); text-align:center; }}
    .hcard-ico {{ font-size:52px; margin-bottom:14px; }}
    .hcard-title {{ font-family:'Sora',sans-serif; font-size:17px; font-weight:800; color:#0a1f5c; margin-bottom:6px; }}
    .hcard-desc  {{ font-size:13px; color:#7a8aaa; line-height:1.6; }}
    </style>
    <h1 style="font-family:Sora,sans-serif;color:#0a1f5c;">👋 Hola, {user['name'].split()[0]}!</h1>
    <p style="color:#7a8aaa;margin-bottom:32px;">Bienvenido/a a ConVivir</p>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="hcard"><div class="hcard-ico">📝</div>'
                    '<div class="hcard-title">Encuesta de Convivencia</div>'
                    '<div class="hcard-desc">Respondé la encuesta de tu aula. Es confidencial y anónima.</div></div>',
                    unsafe_allow_html=True)
        if st.button("Ir a la encuesta", key="s_enc", use_container_width=True, type="primary"):
            go("encuesta")
    with c2:
        st.markdown('<div class="hcard"><div class="hcard-ico">📚</div>'
                    '<div class="hcard-title">Contenido Educativo</div>'
                    '<div class="hcard-desc">Artículos y guías sobre convivencia y cómo pedir ayuda.</div></div>',
                    unsafe_allow_html=True)
        if st.button("Ver contenido", key="s_cont", use_container_width=True, type="primary"):
            go("contenido")
    with c3:
        st.markdown('<div class="hcard"><div class="hcard-ico">💬</div>'
                    '<div class="hcard-title">Mensaje al Docente</div>'
                    '<div class="hcard-desc">Enviá un mensaje privado y confidencial a tu docente.</div></div>',
                    unsafe_allow_html=True)
        if st.button("Enviar mensaje", key="s_msg", use_container_width=True, type="primary"):
            go("mensaje")

# ══════════════════════════════════════════════════════════════════════════════
# HOME ADMIN
# ══════════════════════════════════════════════════════════════════════════════
def page_admin_home():
    st.markdown("""
    <style>
    .hcard { background:white; border-radius:20px; padding:28px 24px; border:2px solid #e8eeff;
        box-shadow:0 4px 20px rgba(26,111,255,0.07); text-align:center; }
    .hcard-ico { font-size:52px; margin-bottom:14px; }
    .hcard-title { font-family:'Sora',sans-serif; font-size:17px; font-weight:800; color:#0a1f5c; margin-bottom:6px; }
    .hcard-desc  { font-size:13px; color:#7a8aaa; line-height:1.6; }
    </style>
    <h1 style="font-family:Sora,sans-serif;color:#0a1f5c;">🏛️ Panel Administrador</h1>
    <p style="color:#7a8aaa;margin-bottom:32px;">Gestión del ecosistema ConVivir</p>
    """, unsafe_allow_html=True)

    activos   = sum(1 for c in COLEGIOS_MOCK if c["estado"]=="Activo")
    pendientes = sum(1 for c in COLEGIOS_MOCK if c["estado"]=="Pendiente KYC")
    validados  = sum(1 for d in DOCENTES_MOCK if d["kyc"]=="Aprobado")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("🏫 Colegios activos", activos)
    c2.metric("⏳ Pendientes KYC",  pendientes, delta_color="inverse")
    c3.metric("✅ Docentes validados", validados)
    c4.metric("🚨 Alertas pendientes", sum(1 for a in ALERTAS_MOCK if a["estado"]=="Pendiente"), delta_color="inverse")

    st.markdown("---")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="hcard"><div class="hcard-ico">🏫</div>'
                    '<div class="hcard-title">Colegios</div>'
                    '<div class="hcard-desc">Registrá y gestioná las instituciones educativas.</div></div>',
                    unsafe_allow_html=True)
        if st.button("Ver colegios", key="a_col", use_container_width=True, type="primary"): go("admin_colegios")
    with c2:
        st.markdown('<div class="hcard"><div class="hcard-ico">👨‍🏫</div>'
                    '<div class="hcard-title">Docentes</div>'
                    '<div class="hcard-desc">Gestioná el acceso de docentes a la plataforma.</div></div>',
                    unsafe_allow_html=True)
        if st.button("Ver docentes", key="a_doc", use_container_width=True, type="primary"): go("admin_docentes")
    with c3:
        st.markdown('<div class="hcard"><div class="hcard-ico">✅</div>'
                    '<div class="hcard-title">Validación KYC</div>'
                    '<div class="hcard-desc">Aprobá la documentación de docentes pendientes.</div></div>',
                    unsafe_allow_html=True)
        if st.button("Ver KYC", key="a_kyc", use_container_width=True, type="primary"): go("admin_kyc")

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: DENUNCIAS
# ══════════════════════════════════════════════════════════════════════════════
def page_denuncias():
    st.title("🆘 Denuncias de Acoso Escolar")
    st.markdown("Registrá situaciones de bullying reportadas por alumnos, familias o docentes.")

    tab1, tab2 = st.tabs(["📋 Denuncias registradas", "➕ Nueva denuncia"])

    with tab1:
        if "denuncias" not in st.session_state or not st.session_state.denuncias:
            st.info("No hay denuncias registradas todavía.")
        else:
            for i, d in enumerate(st.session_state.denuncias):
                urgencia_color = {"Alta":"🔴","Media":"🟡","Baja":"🟢"}.get(d["urgencia"],"⚪")
                with st.expander(f"{urgencia_color} **{d['victima']}** — {d['tipo']} · {d['fecha']}"):
                    c1,c2,c3 = st.columns(3)
                    c1.metric("Urgencia",d["urgencia"])
                    c2.metric("Estado",d["estado"])
                    c3.metric("Aula",d["aula"])
                    st.markdown(f"**Descripción:** {d['descripcion']}")
                    if d.get("testigos"): st.markdown(f"**Testigos:** {d['testigos']}")
                    ca,cb = st.columns(2)
                    if ca.button("✅ Marcar en gestión", key=f"gest_{i}"):
                        st.session_state.denuncias[i]["estado"] = "En gestión"
                        st.success("Estado actualizado.")
                    if cb.button("📄 Generar reporte", key=f"rep_{i}"):
                        st.info("Función de reporte PDF disponible en versión completa.")

    with tab2:
        st.markdown("### Registrar nueva situación")
        with st.form("nueva_denuncia"):
            c1,c2 = st.columns(2)
            victima    = c1.text_input("Nombre del alumno/a afectado/a")
            aula       = c2.text_input("Aula", placeholder="Ej: 3° A")
            c3,c4 = st.columns(2)
            tipo = c3.selectbox("Tipo de situación", [
                "Agresión verbal (insultos, burlas)",
                "Agresión física (golpes, empujones)",
                "Exclusión social (no lo/a dejan participar)",
                "Cyberbullying",
                "Difusión de rumores",
                "Otro"
            ])
            urgencia = c4.selectbox("Urgencia", ["Alta","Media","Baja"])
            descripcion = st.text_area("Descripción de la situación", placeholder="Describí lo que pasó con la mayor cantidad de detalle posible...")
            testigos    = st.text_input("Testigos (opcional)", placeholder="Nombres de alumnos que presenciaron")
            reportado_por = st.selectbox("Reportado por", ["Alumno/a afectado/a","Familiar","Otro docente","Yo lo observé"])

            if st.form_submit_button("📋 Registrar denuncia", type="primary", use_container_width=True):
                if victima and descripcion:
                    if "denuncias" not in st.session_state: st.session_state.denuncias = []
                    st.session_state.denuncias.append({
                        "victima":victima, "aula":aula, "tipo":tipo, "urgencia":urgencia,
                        "descripcion":descripcion, "testigos":testigos,
                        "reportado_por":reportado_por, "estado":"Pendiente",
                        "fecha":datetime.now().strftime("%d/%m/%Y")
                    })
                    st.success(f"✅ Denuncia registrada para **{victima}**. Se notificará al equipo.")
                    st.balloons()
                else:
                    st.error("Completá al menos el nombre del alumno/a y la descripción.")

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: INFO ENCUESTA (para el docente)
# ══════════════════════════════════════════════════════════════════════════════
def page_encuesta_info():
    st.title("📝 Encuesta para Alumnos")
    st.markdown("Compartí el código de tu aula con los alumnos para que respondan la encuesta.")

    aulas = get_aulas()
    if not aulas:
        st.info("Primero tenés que crear un aula en **Gestión de Aulas**.")
        if st.button("Ir a Gestión de Aulas"): go("aulas")
        return

    for codigo, aula in aulas.items():
        resp  = get_respuestas_aula(codigo)
        total = len(aula["alumnos"])
        n     = len(resp)
        pct   = round(n/total*100) if total else 0

        with st.container(border=True):
            st.markdown(f"### {aula['nombre']}")
            c1,c2 = st.columns([2,1])
            with c1:
                st.markdown("#### 📢 Código para los alumnos:")
                st.markdown(
                    f"<div style='background:#e8f0fe;border-radius:12px;padding:20px;"
                    f"font-size:36px;font-weight:800;letter-spacing:6px;color:#0a1f5c;"
                    f"text-align:center;border:2px solid #1a6fff;'>{codigo}</div>",
                    unsafe_allow_html=True)
                st.caption("Los alumnos van a **Encuesta Sociométrica**, escriben este código y su número de lista.")
            with c2:
                st.metric("Participación", f"{pct}%")
                st.metric("Respondieron", f"{n} de {total}")
                st.progress(pct/100)

        st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: SOCIOGRAMA
# ══════════════════════════════════════════════════════════════════════════════
def page_sociograma():
    st.title("🕸️ Sociograma del Aula")
    PERFIL_COLOR = {"Popular":"#1d7a55","Integrado":"#1a56a0","Controvertido":"#5b3fa0",
                    "Aislado":"#d4580a","Rechazado":"#c0392b","Sin datos":"#9a9690"}
    aulas = get_aulas()
    if not aulas: st.warning("No hay aulas."); return
    codigos = list(aulas.keys())
    idx = st.selectbox("Seleccioná el aula", range(len(codigos)),
                       format_func=lambda i: f"{aulas[codigos[i]]['nombre']} ({codigos[i]})")
    codigo = codigos[idx]; aula = aulas[codigo]
    resp = get_respuestas_aula(codigo)
    total = len(aula["alumnos"]); n = len(resp)
    pct   = round(n/total*100) if total else 0

    c1,c2,c3 = st.columns(3)
    c1.metric("Alumnos",total); c2.metric("Respondieron",n)
    c3.metric("Participación",f"{pct}%", delta="Suficiente ✅" if pct>=60 else "Necesitás más ⚠️")

    if n == 0:
        st.info(f"Todavía no hay respuestas. Código del aula: **`{codigo}`**")
        if st.button("Ver código para compartir"): go("encuesta_info")
        return

    datos = calcular_sociograma(codigo)
    edges = datos.pop("_edges",[]); datos.pop("_n",None); datos.pop("_total",None)

    col_a,col_b = st.columns([3,1])
    with col_a: mostrar = st.radio("Vínculos:", ["Todos","Solo positivos","Solo negativos"], horizontal=True)
    with col_b: solo_alertas = st.checkbox("Solo alertas 🚨")

    cols_ley = st.columns(len(PERFIL_COLOR))
    for col,(p,color) in zip(cols_ley,PERFIL_COLOR.items()):
        col.markdown(f"<span style='background:{color};color:white;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:700'>{p}</span>",unsafe_allow_html=True)
    st.markdown("---")

    G = nx.DiGraph()
    for aid in datos: G.add_node(aid)
    ef = []
    for (s,d,t) in edges:
        if mostrar=="Solo positivos" and t!="positivo": continue
        if mostrar=="Solo negativos" and t!="negativo": continue
        ef.append((s,d,t)); G.add_edge(s,d,tipo=t)
    pos = nx.spring_layout(G, seed=42, k=2.8)
    traces = []
    for (s,d,t) in ef:
        if s not in pos or d not in pos: continue
        x0,y0=pos[s]; x1,y1=pos[d]
        op = 0.75
        if solo_alertas and datos.get(d,{}).get("alerta") is None: op=0.05
        traces.append(go.Scatter(x=[x0,x1,None],y=[y0,y1,None],mode="lines",
            line=dict(width=1.6,color="#1d7a55" if t=="positivo" else "#c0392b"),
            opacity=op,hoverinfo="none",showlegend=False))
    nx_l,ny_l,nt,nc,ns,nh=[],[],[],[],[],[]
    for aid,info in datos.items():
        if aid not in pos: continue
        if solo_alertas and info["alerta"] is None: continue
        x,y=pos[aid]; nx_l.append(x); ny_l.append(y)
        nt.append(info["nombre"].split()[0])
        nc.append(PERFIL_COLOR.get(info["perfil"],"#9a9690"))
        ns.append(32 if info["perfil"]=="Popular" else 22)
        nh.append(f"<b>{info['nombre']}</b><br>Perfil: {info['perfil']}<br>"
                  f"Votos ✅:{info['votos_positivos']} ❌:{info['votos_negativos']}"
                  f"{'<br>🚨 '+info['alerta'] if info['alerta'] else ''}")
    fig = go.Figure(data=traces+[go.Scatter(x=nx_l,y=ny_l,mode="markers+text",text=nt,
        textposition="top center",textfont=dict(size=11,color="#0f2240"),
        marker=dict(size=ns,color=nc,line=dict(width=2,color="white")),
        hovertext=nh,hoverinfo="text",showlegend=False)])
    fig.update_layout(height=540,margin=dict(l=20,r=20,t=20,b=20),
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
        plot_bgcolor="rgba(248,250,255,0.8)",paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---"); st.subheader("Tabla de perfiles")
    rows=[{"Nombre":v["nombre"],"Perfil":v["perfil"],"Votos ✅":v["votos_positivos"],
           "Votos ❌":v["votos_negativos"],"Respondió":"✅" if v["respondio"] else "❌",
           "Alerta":v["alerta"] or "—"} for v in datos.values() if isinstance(v,dict)]
    st.dataframe(pd.DataFrame(rows).sort_values("Votos ✅",ascending=False),use_container_width=True,hide_index=True)
    mensajes=[(r["alumno_id"],r["mensaje_docente"]) for r in resp if r.get("mensaje_docente","").strip()]
    if mensajes:
        st.markdown("---"); st.subheader("💌 Mensajes privados de alumnos")
        for aid,msg in mensajes:
            n2=next((v["nombre"] for k,v in datos.items() if k==aid),f"Alumno #{aid}")
            with st.expander(f"Mensaje de {n2}"): st.markdown(f"> {msg}")

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: AULAS
# ══════════════════════════════════════════════════════════════════════════════
def page_aulas():
    st.title("🚪 Gestión de Aulas")
    tab1,tab2 = st.tabs(["📋 Mis aulas","➕ Crear nueva aula"])
    with tab1:
        aulas = get_aulas()
        for codigo,aula in aulas.items():
            resp=get_respuestas_aula(codigo); n=len(resp); total=len(aula["alumnos"])
            pct=round(n/total*100) if total else 0
            icon="🟢" if pct>=60 else ("🟡" if pct>0 else "⚪")
            with st.expander(f"{icon} **{aula['nombre']}** · `{codigo}` · {n}/{total} respondieron ({pct}%)"):
                c1,c2,c3=st.columns(3); c1.metric("Alumnos",total); c2.metric("Respondieron",n); c3.metric("Participación",f"{pct}%")
                st.markdown("**Código para alumnos:**")
                st.markdown(f"<div style='background:#e8f0fe;border-radius:10px;padding:14px;font-size:28px;"
                            f"font-weight:800;letter-spacing:5px;color:#0a1f5c;text-align:center;'>{codigo}</div>",
                            unsafe_allow_html=True)
                respondieron={r["alumno_id"] for r in resp}
                st.markdown("**Alumnos:**"); cols=st.columns(4)
                for i,a in enumerate(aula["alumnos"]):
                    cols[i%4].markdown(f"{'✅' if a['id'] in respondieron else '⏳'} {a['id']}. {a['nombre']}")
    with tab2:
        st.markdown("### Cargá el listado de alumnos")
        metodo=st.radio("Método",["📄 Subir Excel","✏️ Cargar manualmente"],horizontal=True)
        c1,c2=st.columns(2)
        nombre_aula=c1.text_input("Nombre del aula",placeholder="Ej: 4° B Primaria")
        codigo_aula=c2.text_input("Código de acceso",placeholder="Ej: CUARTOB2025",help="Sin espacios, mayúsculas").upper().replace(" ","")
        alumnos_lista=[]
        if metodo=="📄 Subir Excel":
            plantilla=pd.DataFrame({"Nombre":["Juan García","María López"],"Genero":["M","F"]})
            buf=io.BytesIO(); plantilla.to_excel(buf,index=False)
            st.download_button("⬇️ Descargar plantilla Excel",data=buf.getvalue(),
                file_name="plantilla_alumnos.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            archivo=st.file_uploader("Subí el Excel con el listado",type=["xlsx","xls","csv"])
            if archivo:
                try:
                    df=pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
                    df.columns=[c.strip().lower() for c in df.columns]
                    col_n=next((c for c in df.columns if "nombre" in c),None)
                    col_g=next((c for c in df.columns if "gen" in c or "sex" in c),None)
                    if col_n:
                        df=df.dropna(subset=[col_n])
                        for _,row in df.iterrows():
                            g=str(row[col_g]).upper()[0] if col_g else "?"
                            alumnos_lista.append({"nombre":row[col_n].strip(),"genero":g})
                        st.success(f"✅ {len(alumnos_lista)} alumnos cargados.")
                        st.dataframe(pd.DataFrame(alumnos_lista),use_container_width=True,hide_index=True)
                except Exception as e: st.error(f"Error: {e}")
        else:
            texto=st.text_area("Lista (Nombre, M/F — una por línea)",placeholder="Juan García, M\nMaría López, F",height=180)
            if texto:
                for l in texto.strip().split("\n"):
                    p=l.strip().split(",")
                    if p[0].strip(): alumnos_lista.append({"nombre":p[0].strip(),"genero":p[1].strip().upper()[0] if len(p)>1 else "?"})
                if alumnos_lista: st.info(f"{len(alumnos_lista)} alumnos listos.")
        st.markdown("---")
        if st.button("🚀 Crear aula",type="primary",use_container_width=True):
            if not nombre_aula: st.error("Ingresá el nombre del aula.")
            elif len(codigo_aula)<4: st.error("El código debe tener al menos 4 caracteres.")
            elif not alumnos_lista: st.error("Cargá al menos un alumno.")
            elif get_aula(codigo_aula): st.error(f"Ya existe el código {codigo_aula}.")
            else:
                crear_aula(codigo_aula,nombre_aula,st.session_state.user["name"],alumnos_lista)
                st.success(f"✅ Aula **{nombre_aula}** creada con {len(alumnos_lista)} alumnos.")
                st.markdown(f"<div style='background:#e8f0fe;border-radius:10px;padding:16px;font-size:32px;"
                            f"font-weight:800;letter-spacing:5px;color:#0a1f5c;text-align:center;'>{codigo_aula}</div>",
                            unsafe_allow_html=True)
                st.balloons()

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: ALERTAS
# ══════════════════════════════════════════════════════════════════════════════
def page_alertas():
    st.title("🚨 Alertas de Riesgo")
    st.markdown("Alumnos identificados en riesgo a partir del análisis sociométrico.")
    filtro=st.selectbox("Filtrar por prioridad",["Todas","Alta","Media","Baja"])
    alertas=[a for a in ALERTAS_MOCK if filtro=="Todas" or a["prioridad"]==filtro]
    for alerta in alertas:
        icon={"Alta":"🔴","Media":"🟡","Baja":"🟢"}.get(alerta["prioridad"],"⚪")
        with st.expander(f"{icon} **{alerta['alumno']}** — {alerta['tipo']} · {alerta['estado']}"):
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Prioridad",alerta["prioridad"]); c2.metric("Estado",alerta["estado"])
            c3.metric("Fecha",alerta["fecha"]);         c4.metric("Aula",alerta["aula"])
            if alerta["tipo"]=="Rechazo elevado": st.info("💡 Revisá las dinámicas del grupo. Considerá actividades de integración y hablar con el equipo de orientación.")
            elif alerta["tipo"]=="Aislamiento":   st.info("💡 Facilitá espacios de participación. Considerá comunicarte con la familia.")
            else:                                  st.info("💡 Monitoreá la situación. El alumno recibe elecciones tanto positivas como negativas.")
            nota=st.text_area("Nota de seguimiento",value=alerta.get("nota",""),key="nota_"+str(alerta["id"]),placeholder="Escribí tu observación aquí...")
            ca,cb,cc=st.columns(3)
            if ca.button("💾 Guardar nota",key="save_"+str(alerta["id"]),type="primary"): st.success("Nota guardada.")
            if cb.button("✅ Marcar resuelta",key="res_"+str(alerta["id"])): st.success("Alerta resuelta.")
            if cc.button("📄 Ver perfil completo",key="perfil_"+str(alerta["id"])): go("sociograma")

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: REPORTES
# ══════════════════════════════════════════════════════════════════════════════
def page_reportes():
    st.title("📊 Reportes")
    aulas=get_aulas()
    if not aulas: st.info("No hay aulas con datos todavía."); return
    codigos=list(aulas.keys())
    idx=st.selectbox("Aula",range(len(codigos)),format_func=lambda i:f"{aulas[codigos[i]]['nombre']} ({codigos[i]})")
    codigo=codigos[idx]
    datos=calcular_sociograma(codigo)
    datos.pop("_edges",None); datos.pop("_n",None); datos.pop("_total",None)
    resp=get_respuestas_aula(codigo); total=len(aulas[codigo]["alumnos"]); n_resp=len(resp)
    en_riesgo=sum(1 for v in datos.values() if isinstance(v,dict) and v.get("alerta"))
    c1,c2,c3=st.columns(3)
    c1.metric("Encuestados",f"{n_resp}/{total}"); c2.metric("En riesgo",en_riesgo,delta_color="inverse"); c3.metric("Participación",f"{round(n_resp/total*100) if total else 0}%")
    perfiles=[v["perfil"] for v in datos.values() if isinstance(v,dict) and v["perfil"]!="Sin datos"]
    if perfiles:
        df_p=pd.Series(perfiles).value_counts().reset_index(); df_p.columns=["Perfil","Cantidad"]
        color_map={"Popular":"#1d7a55","Integrado":"#1a56a0","Aislado":"#d4580a","Rechazado":"#c0392b","Controvertido":"#5b3fa0"}
        fig=px.bar(df_p,x="Perfil",y="Cantidad",color="Perfil",color_discrete_map=color_map,text="Cantidad")
        fig.update_traces(textposition="outside"); fig.update_layout(showlegend=False,margin=dict(t=20,b=20,l=0,r=0))
        st.plotly_chart(fig,use_container_width=True)
    rows=[{"Nombre":v["nombre"],"Perfil":v["perfil"],"Votos ✅":v["votos_positivos"],
           "Votos ❌":v["votos_negativos"],"Respondió":"✅" if v["respondio"] else "❌","Alerta":v["alerta"] or "—"}
          for v in datos.values() if isinstance(v,dict)]
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    if st.button("📄 Generar reporte PDF",type="primary"): st.info("Función de PDF disponible en versión completa.")

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: ENCUESTA ALUMNO
# ══════════════════════════════════════════════════════════════════════════════
def page_encuesta():
    st.title("📝 Encuesta de Convivencia")
    for k,v in [("enc_alumno_id",None),("enc_codigo_aula",None),("enc_alumno_nombre",""),("enc_enviada",False),("enc_paso",1)]:
        if k not in st.session_state: st.session_state[k]=v

    if st.session_state.enc_paso==1:
        st.markdown("### 👋 Identificate para empezar")
        st.info("🔒 Tus respuestas son **completamente confidenciales**.")
        with st.form("id_form"):
            codigo=st.text_input("Código de aula",placeholder="Ej: DEMO2025").upper()
            numero=st.number_input("Tu número de lista",min_value=1,max_value=60,step=1)
            if st.form_submit_button("Continuar →",type="primary",use_container_width=True):
                aula=get_aula(codigo)
                if not aula: st.error("Código incorrecto."); return
                alumno=get_alumno_by_numero(codigo,int(numero))
                if not alumno: st.error(f"No encontré el número {int(numero)}."); return
                if ya_respondio(codigo,alumno["id"]): st.warning(f"¡Hola {alumno['nombre']}! Ya respondiste. ¡Gracias! 🎉"); return
                st.session_state.enc_alumno_id=alumno["id"]; st.session_state.enc_codigo_aula=codigo
                st.session_state.enc_alumno_nombre=alumno["nombre"]; st.session_state.enc_paso=2; st.rerun()
        return

    if st.session_state.enc_enviada:
        st.balloons()
        st.markdown("<div style='text-align:center;padding:60px 24px;'>"
                    "<div style='font-size:72px;'>✅</div>"
                    "<h2 style='color:#0a1f5c;font-family:Sora,sans-serif;'>¡Gracias por responder!</h2>"
                    "<p style='color:#7a8aaa;font-size:16px;'>Tus respuestas fueron guardadas de forma confidencial.</p>"
                    "</div>",unsafe_allow_html=True)
        if st.button("← Volver al inicio"):
            for k in ["enc_enviada","enc_paso","enc_alumno_id","enc_codigo_aula","enc_alumno_nombre"]:
                st.session_state[k]=(False if k=="enc_enviada" else(1 if k=="enc_paso" else None))
            st.rerun()
        return

    codigo=st.session_state.enc_codigo_aula; alumno_id=st.session_state.enc_alumno_id
    nombre=st.session_state.enc_alumno_nombre; aula=get_aula(codigo)
    companeros=[a for a in aula["alumnos"] if a["id"]!=alumno_id]
    id_por_nombre={a["nombre"]:a["id"] for a in companeros}
    lista=list(id_por_nombre.keys())

    st.markdown(f"### Hola, **{nombre}** 👋")
    st.markdown(f"Aula: **{aula['nombre']}**")
    st.markdown("<div style='background:#e8f0fe;border-left:4px solid #1a56a0;border-radius:8px;padding:14px 18px;margin:12px 0 20px;'>"
                "<strong>🔒 Confidencial:</strong> Ningún compañero/a puede ver tus respuestas. "
                "Solo tu docente ve resultados generales del aula.</div>",unsafe_allow_html=True)

    with st.form("enc_form"):
        st.markdown("## 🌟 Tus relaciones")
        st.markdown("**1. ¿Quiénes te caen mejor o con quiénes te gusta más estar?**")
        me_gusta=st.multiselect("Elegí hasta 3",lista,max_selections=3,key="f1")
        st.markdown("**2. ¿Con quiénes preferís no estar o trabajar?**")
        no_me_gusta=st.multiselect("Elegí hasta 3",lista,max_selections=3,key="f2")
        st.markdown("**3. ¿Quiénes son tus mejores amigos/as del aula?**")
        mis_amigos=st.multiselect("Elegí hasta 3",lista,max_selections=3,key="f3")
        st.markdown("---")
        st.markdown("## 🤝 ¿Quiénes se portan bien?")
        st.markdown("**4. ¿Quiénes ayudan a sus compañeros cuando los necesitan?**")
        ayuda=st.multiselect("Elegí hasta 3",lista,max_selections=3,key="f4")
        st.markdown("**5. ¿Quiénes animan o consuelan cuando alguien está triste?**")
        anima=st.multiselect("Elegí hasta 3",lista,max_selections=3,key="f5")
        st.markdown("---")
        st.markdown("## ⚠️ Situaciones que no están bien")
        st.caption("Esto es confidencial y ayuda al docente a mejorar la convivencia.")
        st.markdown("**6. ¿Hay alguien que insulte, se burle o se ría de sus compañeros?**")
        insulta=st.multiselect("Elegí hasta 3",lista,max_selections=3,key="f6")
        st.markdown("**7. ¿Hay alguien que no deje participar o excluya a otros?**")
        no_deja=st.multiselect("Elegí hasta 3",lista,max_selections=3,key="f7")
        st.markdown("---")
        st.markdown("## 💬 Sobre vos")
        acoso=st.radio("**8. ¿Algún compañero/a te hizo sentir mal de forma repetida en los últimos meses?**",
            ["No, no me pasó nada de eso","Sí, me pasó una o dos veces",
             "Sí, me pasa seguido","Sí, me pasa casi todas las semanas"],key="f8")
        st.markdown("---")
        st.markdown("#### 💌 Mensaje privado para tu docente (opcional)")
        mensaje=st.text_area("Solo lo/la ve él/ella.",placeholder="Podés escribir lo que sea.",key="f9")
        if st.form_submit_button("✅ Enviar mi encuesta",type="primary",use_container_width=True):
            def ids(lst): return [id_por_nombre[n] for n in lst if n in id_por_nombre]
            guardar_respuesta(codigo,alumno_id,{"me_gusta":ids(me_gusta),"no_me_gusta":ids(no_me_gusta),
                "mis_amigos":ids(mis_amigos),"ayuda":ids(ayuda),"anima":ids(anima),
                "insulta":ids(insulta),"no_deja_participar":ids(no_deja),
                "acoso_sufrido":acoso,"mensaje_docente":mensaje})
            st.session_state.enc_enviada=True; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: CONTENIDO ALUMNO
# ══════════════════════════════════════════════════════════════════════════════
def page_contenido():
    st.title("📚 Contenido Educativo")
    ARTS=[
        ("¿Qué es el bullying?","📄","4 min",
         "El **bullying** es un comportamiento agresivo y repetido para lastimar a otra persona.\n\n**Señales:** evita el colegio, está triste o asustado, tiene pocos amigos.\n\n**¿Qué hacer?** Hablá con tu docente o un adulto de confianza. No te quedes solo/a con esto."),
        ("Cómo pedir ayuda","📋","3 min",
         "Pedir ayuda **no es de débiles** — es lo más valiente que podés hacer.\n\n1. Identificá a alguien de confianza\n2. Buscá un momento tranquilo\n3. Contá lo que pasó\n\nRecordá: **merecés estar bien**."),
        ("Ser buen compañero/a","📄","5 min",
         "Las **pequeñas acciones** hacen la diferencia:\n- Saludá a todos cuando llegás\n- Incluí a quien está solo\n- No te rías si alguien se equivoca\n- Si ves que alguien está mal, preguntale cómo está"),
    ]
    for titulo,ico,tiempo,contenido in ARTS:
        with st.expander(f"{ico} **{titulo}** · {tiempo} de lectura"):
            st.markdown(contenido)
    st.markdown("---")
    st.warning("**🆘 ¿Necesitás ayuda urgente?**\n\n- Hablá con un adulto de confianza\n- **Línea de ayuda:** 102 (Consejo Nacional de la Niñez)")

# PÁGINA: MENSAJE AL DOCENTE
def page_mensaje():
    st.title("💬 Mensaje al Docente")
    st.info("Este mensaje es **privado y confidencial**. Solo lo ve tu docente.")
    with st.form("msg_form"):
        mensaje=st.text_area("Escribí tu mensaje:",placeholder="Podés contar lo que está pasando...",height=180)
        if st.form_submit_button("Enviar →",type="primary",use_container_width=True):
            if mensaje: st.success("✅ Mensaje enviado. Tu docente lo va a leer en privado."); st.balloons()
            else: st.error("Escribí algo antes de enviar.")

# PÁGINAS ADMIN
def page_admin_colegios():
    st.title("🏫 Gestión de Colegios")
    for c in COLEGIOS_MOCK:
        icon={"Activo":"🟢","Pendiente KYC":"🟡","Suspendido":"🔴"}.get(c["estado"],"⚪")
        with st.expander(f"{icon} **{c['nombre']}** — {c['ciudad']}"):
            c1,c2,c3,c4=st.columns(4); c1.metric("Docentes",c["docentes"]); c2.metric("Aulas",c["aulas"]); c3.metric("Estado",c["estado"]); c4.metric("Ciudad",c["ciudad"])

def page_admin_docentes():
    st.title("👨‍🏫 Gestión de Docentes")
    for d in DOCENTES_MOCK:
        icon={"Aprobado":"✅","Pendiente":"⏳","En revisión":"🔍"}.get(d["kyc"],"❓")
        with st.expander(f"{icon} **{d['nombre']}** — {d['colegio']}"):
            c1,c2=st.columns(2); c1.markdown(f"📧 {d['email']}"); c2.metric("KYC",d["kyc"])
            if d["kyc"] in ("Pendiente","En revisión"):
                ca,cb=st.columns(2)
                if ca.button("✅ Aprobar",key="ok_"+str(d["id"]),type="primary"): st.success("Aprobado (demo)")
                if cb.button("❌ Rechazar",key="rej_"+str(d["id"])): st.error("Rechazado (demo)")

def page_admin_kyc():
    st.title("✅ KYC — Validación de Docentes")
    pend=[d for d in DOCENTES_MOCK if d["kyc"] in ("Pendiente","En revisión")]
    if not pend: st.success("🎉 No hay validaciones pendientes."); return
    for d in pend:
        with st.container(border=True):
            c1,c2=st.columns([3,1])
            with c1: st.markdown(f"### {d['nombre']}"); st.markdown(f"📧 {d['email']} · 🏫 {d['colegio']}")
            with c2:
                if st.button("✅ Aprobar",key="kyc_"+str(d["id"]),type="primary",use_container_width=True): st.success("Aprobado")
                if st.button("❌ Rechazar",key="krej_"+str(d["id"]),use_container_width=True): st.error("Rechazado")

# ══════════════════════════════════════════════════════════════════════════════
# ROUTER PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
def route():
    role = st.session_state.user["role"]
    page = st.session_state.page

    topbar()

    if role == "admin":
        if page in ("home","admin_home"): page_admin_home()
        elif page == "admin_colegios":    page_admin_colegios()
        elif page == "admin_docentes":    page_admin_docentes()
        elif page == "admin_kyc":         page_admin_kyc()
        else: page_admin_home()

    elif role == "teacher":
        if page in ("home","teacher_home"): page_teacher_home()
        elif page == "sociograma":          page_sociograma()
        elif page == "aulas":               page_aulas()
        elif page == "alertas":             page_alertas()
        elif page == "reportes":            page_reportes()
        elif page == "encuesta_info":       page_encuesta_info()
        elif page == "denuncias":           page_denuncias()
        else: page_teacher_home()

    else:  # student / family
        if page in ("home","student_home"): page_student_home()
        elif page == "encuesta":            page_encuesta()
        elif page == "contenido":           page_contenido()
        elif page == "mensaje":             page_mensaje()
        else: page_student_home()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    show_login()
else:
    route()
