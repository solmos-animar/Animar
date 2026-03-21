import streamlit as st
import json
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from pathlib import Path
from datetime import datetime
from collections import Counter

st.set_page_config(
    page_title="ConVivir — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos globales ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #0a1f5c; }
  [data-testid="stSidebar"] * { color: white !important; }
  [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12); }
  .main .block-container { padding-top: 2rem; }
  h1 { color: #0a1f5c; }
  h2 { color: #0a1f5c; }
  h3 { color: #1a56a0; }
  .badge-admin   { background:#e8effe; color:#1a56a0; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-teacher { background:#e6f4ee; color:#1d7a55; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-student { background:#fde8d0; color:#d4580a; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .alert-high   { background:#fdeaea; border-left:4px solid #c0392b; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-medium { background:#fef3e2; border-left:4px solid #d4580a; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-low    { background:#e6f4ee; border-left:4px solid #1d7a55; border-radius:8px; padding:12px 16px; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MOTOR DE DATOS
# ══════════════════════════════════════════════════════════════════════════════
DATA_DIR   = Path(__file__).parent
AULAS_FILE = DATA_DIR / "aulas.json"
RESP_FILE  = DATA_DIR / "respuestas.json"

def _load(path):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def _save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def get_aulas():
    data = _load(AULAS_FILE)
    if not data:
        data = {
            "AULA2025": {
                "nombre": "3° A Primaria",
                "docente": "Prof. María García",
                "creada": "2025-01-01",
                "alumnos": [
                    {"id": 1,  "nombre": "Lucas Martínez",   "genero": "M"},
                    {"id": 2,  "nombre": "Sofía Rodríguez",  "genero": "F"},
                    {"id": 3,  "nombre": "Mateo González",   "genero": "M"},
                    {"id": 4,  "nombre": "Valentina Torres", "genero": "F"},
                    {"id": 5,  "nombre": "Benjamín López",   "genero": "M"},
                    {"id": 6,  "nombre": "Camila Díaz",      "genero": "F"},
                    {"id": 7,  "nombre": "Nicolás Pérez",    "genero": "M"},
                    {"id": 8,  "nombre": "Isabella Moreno",  "genero": "F"},
                    {"id": 9,  "nombre": "Santiago Romero",  "genero": "M"},
                    {"id": 10, "nombre": "Emma Álvarez",     "genero": "F"},
                    {"id": 11, "nombre": "Joaquín Ramírez",  "genero": "M"},
                    {"id": 12, "nombre": "Martina Castro",   "genero": "F"},
                ]
            }
        }
        _save(AULAS_FILE, data)
    return data

def get_aula(codigo):
    return get_aulas().get(codigo.upper())

def crear_aula(codigo, nombre, docente, alumnos):
    aulas = get_aulas()
    aulas[codigo.upper()] = {
        "nombre": nombre, "docente": docente,
        "creada": datetime.now().strftime("%Y-%m-%d"),
        "alumnos": [{"id": i+1, "nombre": a["nombre"], "genero": a.get("genero","?")} for i,a in enumerate(alumnos)],
    }
    _save(AULAS_FILE, aulas)

def get_alumno_by_numero(codigo_aula, numero):
    aula = get_aula(codigo_aula)
    if not aula: return None
    return next((a for a in aula["alumnos"] if a["id"] == numero), None)

def get_respuestas():
    return _load(RESP_FILE)

def ya_respondio(codigo_aula, alumno_id):
    return f"{codigo_aula.upper()}_{alumno_id}" in get_respuestas()

def guardar_respuesta(codigo_aula, alumno_id, respuesta):
    resp = get_respuestas()
    respuesta.update({"alumno_id": alumno_id, "codigo_aula": codigo_aula.upper(),
                      "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    resp[f"{codigo_aula.upper()}_{alumno_id}"] = respuesta
    _save(RESP_FILE, resp)

def get_respuestas_aula(codigo_aula):
    resp = get_respuestas()
    return [v for k,v in resp.items() if k.startswith(codigo_aula.upper()+"_")]

DIM_META = {
    "me_gusta": ("positivo", 1.0), "mis_amigos": ("positivo", 1.2),
    "ayuda": ("positivo", 0.8),    "anima": ("positivo", 0.8),
    "no_me_gusta": ("negativo", -1.0), "no_deja_participar": ("negativo", -0.8),
    "insulta": ("negativo", -0.7),
}

def calcular_sociograma(codigo_aula):
    aula = get_aula(codigo_aula)
    if not aula: return {}
    alumnos   = {a["id"]: a for a in aula["alumnos"]}
    respuestas = get_respuestas_aula(codigo_aula)
    stats = {
        aid: {"nombre": a["nombre"], "genero": a["genero"], "score_social": 0.0,
              "votos_positivos": 0, "votos_negativos": 0, "votos_victima": 0,
              "respondio": False, "perfil": "Sin datos", "alerta": None}
        for aid, a in alumnos.items()
    }
    edges = []
    for r in respuestas:
        origen_id = r["alumno_id"]
        if origen_id in stats: stats[origen_id]["respondio"] = True
        for dim, (tipo, peso) in DIM_META.items():
            for dest_id in (r.get(dim) or []):
                if dest_id not in stats or dest_id == origen_id: continue
                stats[dest_id]["score_social"] += peso
                if tipo == "positivo":
                    stats[dest_id]["votos_positivos"] += 1
                    edges.append((origen_id, dest_id, "positivo", dim))
                else:
                    stats[dest_id]["votos_negativos"] += 1
                    edges.append((origen_id, dest_id, "negativo", dim))
    n_resp = len(respuestas)
    for aid, s in stats.items():
        vp, vn = s["votos_positivos"], s["votos_negativos"]
        if n_resp == 0 or (vp == 0 and vn == 0):
            perfil, alerta = "Sin datos", None
        elif vp >= 4 and vn <= 1:  perfil, alerta = "Popular", None
        elif vn >= 4 and vp <= 1:  perfil, alerta = "Rechazado", "Alta"
        elif vp <= 1 and vn <= 1:  perfil, alerta = "Aislado", "Alta" if vp == 0 else "Media"
        elif vp >= 2 and vn >= 2:  perfil, alerta = "Controvertido", "Media"
        else:                       perfil, alerta = "Integrado", None
        s["perfil"], s["alerta"] = perfil, alerta
    stats["_edges"] = edges
    stats["_n_respuestas"] = n_resp
    stats["_total_alumnos"] = len(alumnos)
    return stats

# ── Mock data para Admin ──────────────────────────────────────────────────────
COLEGIOS = [
    {"id":1,"nombre":"Instituto San Martín","ciudad":"Buenos Aires","docentes":4,"aulas":6,"estado":"Activo"},
    {"id":2,"nombre":"Colegio del Valle","ciudad":"Córdoba","docentes":2,"aulas":3,"estado":"Activo"},
    {"id":3,"nombre":"Escuela Belgrano","ciudad":"Rosario","docentes":1,"aulas":2,"estado":"Pendiente KYC"},
    {"id":4,"nombre":"Colegio Las Flores","ciudad":"Mendoza","docentes":3,"aulas":4,"estado":"Activo"},
    {"id":5,"nombre":"Instituto Rivadavia","ciudad":"Tucumán","docentes":0,"aulas":0,"estado":"Suspendido"},
]
DOCENTES_MOCK = [
    {"id":1,"nombre":"María García","email":"docente@colegio.ar","colegio":"Instituto San Martín","aulas":2,"kyc":"Aprobado"},
    {"id":2,"nombre":"Carlos López","email":"clopez@colegio.ar","colegio":"Instituto San Martín","aulas":1,"kyc":"Aprobado"},
    {"id":3,"nombre":"Ana Fernández","email":"afernandez@valle.ar","colegio":"Colegio del Valle","aulas":2,"kyc":"Pendiente"},
    {"id":4,"nombre":"Roberto Soria","email":"rsoria@belgrano.ar","colegio":"Escuela Belgrano","aulas":0,"kyc":"En revisión"},
    {"id":5,"nombre":"Laura Vega","email":"lvega@flores.ar","colegio":"Colegio Las Flores","aulas":3,"kyc":"Aprobado"},
]
ALERTAS_MOCK = [
    {"id":1,"alumno":"Valentina Torres","aula":"3° A","tipo":"Rechazo elevado","prioridad":"Alta","fecha":"2025-05-10","estado":"Pendiente","nota":""},
    {"id":2,"alumno":"Mateo González","aula":"3° A","tipo":"Aislamiento","prioridad":"Alta","fecha":"2025-05-10","estado":"En gestión","nota":"Se habló con la familia."},
    {"id":3,"alumno":"Nicolás Pérez","aula":"3° A","tipo":"Perfil controvertido","prioridad":"Media","fecha":"2025-05-10","estado":"Pendiente","nota":""},
]

# ── SVGs del logo ─────────────────────────────────────────────────────────────
LOGO_NAV = (
    '<svg width="34" height="34" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="100" height="100" rx="13" fill="#1a6fff"/>'
    '<path d="M11,92 L35,20 L50,20 L50,92 Z" fill="#0a2a6e"/>'
    '<path d="M89,92 L65,20 L50,20 L50,92 Z" fill="#0a2a6e"/>'
    '<circle cx="50" cy="45" r="9" fill="#93c5fd"/>'
    '<path d="M50,54 Q37,47 29,35" stroke="#93c5fd" stroke-width="7" stroke-linecap="round" fill="none"/>'
    '<path d="M50,54 Q63,47 71,35" stroke="#93c5fd" stroke-width="7" stroke-linecap="round" fill="none"/>'
    '<line x1="50" y1="54" x2="50" y2="73" stroke="#93c5fd" stroke-width="7" stroke-linecap="round"/>'
    '<line x1="50" y1="73" x2="42" y2="88" stroke="#93c5fd" stroke-width="6" stroke-linecap="round"/>'
    '<line x1="50" y1="73" x2="58" y2="88" stroke="#93c5fd" stroke-width="6" stroke-linecap="round"/>'
    '</svg>'
)
LOGO_HERO = (
    '<svg width="130" height="130" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">'
    '<defs><radialGradient id="hg" cx="50%" cy="25%" r="75%">'
    '<stop offset="0%" stop-color="#2563eb"/><stop offset="100%" stop-color="#0a1f5c"/>'
    '</radialGradient><filter id="gl"><feGaussianBlur stdDeviation="3.5" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
    '<rect width="200" height="200" rx="30" fill="url(#hg)"/>'
    '<path d="M16,188 L62,28 L100,28 L100,188 Z" fill="#0a1840" opacity="0.85"/>'
    '<path d="M184,188 L138,28 L100,28 L100,188 Z" fill="#0a1840" opacity="0.85"/>'
    '<circle cx="100" cy="88" r="19" fill="#93c5fd" filter="url(#gl)"/>'
    '<path d="M100,107 Q78,95 60,70" stroke="#93c5fd" stroke-width="14" stroke-linecap="round" fill="none" filter="url(#gl)"/>'
    '<path d="M100,107 Q122,95 140,70" stroke="#93c5fd" stroke-width="14" stroke-linecap="round" fill="none" filter="url(#gl)"/>'
    '<line x1="100" y1="107" x2="100" y2="148" stroke="#93c5fd" stroke-width="14" stroke-linecap="round" filter="url(#gl)"/>'
    '<line x1="100" y1="148" x2="83" y2="178" stroke="#93c5fd" stroke-width="12" stroke-linecap="round" filter="url(#gl)"/>'
    '<line x1="100" y1="148" x2="117" y2="178" stroke="#93c5fd" stroke-width="12" stroke-linecap="round" filter="url(#gl)"/>'
    '</svg>'
)
LOGO_MOD = (
    '<svg width="40" height="40" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="100" height="100" rx="16" fill="rgba(26,111,255,0.15)"/>'
    '<path d="M12,92 L36,20 L50,20 L50,92 Z" fill="#1a6fff" opacity="0.75"/>'
    '<path d="M88,92 L64,20 L50,20 L50,92 Z" fill="#1a6fff" opacity="0.75"/>'
    '<circle cx="50" cy="45" r="8" fill="#93c5fd"/>'
    '<path d="M50,53 Q39,47 32,36" stroke="#93c5fd" stroke-width="6" stroke-linecap="round" fill="none"/>'
    '<path d="M50,53 Q61,47 68,36" stroke="#93c5fd" stroke-width="6" stroke-linecap="round" fill="none"/>'
    '<line x1="50" y1="53" x2="50" y2="70" stroke="#93c5fd" stroke-width="6" stroke-linecap="round"/>'
    '<line x1="50" y1="70" x2="43" y2="83" stroke="#93c5fd" stroke-width="5" stroke-linecap="round"/>'
    '<line x1="50" y1="70" x2="57" y2="83" stroke="#93c5fd" stroke-width="5" stroke-linecap="round"/>'
    '</svg>'
)

# ── CSS y HTML de la landing ──────────────────────────────────────────────────
LANDING_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
.block-container { padding:0!important; max-width:100%!important; }
header[data-testid="stHeader"] { display:none; }
[data-testid="stSidebar"] { display:none; }
.cv { font-family:'DM Sans',sans-serif; background:#03091a; color:#dde8f8; min-height:100vh; }
.cv-nav { position:fixed; top:0; left:0; right:0; z-index:100; display:flex; align-items:center; justify-content:space-between; padding:0 52px; height:66px; background:rgba(3,9,26,0.9); backdrop-filter:blur(20px); border-bottom:1px solid rgba(74,158,255,0.1); }
.cv-logo { display:flex; align-items:center; gap:10px; }
.cv-logo-txt { font-family:'Sora',sans-serif; font-size:20px; font-weight:800; color:#fff; letter-spacing:-0.4px; }
.cv-logo-txt em { font-style:normal; color:#4a9eff; }
.cv-nav-links { display:flex; gap:34px; font-size:13px; font-weight:500; color:rgba(221,232,248,0.4); }
.cv-hero { min-height:100vh; display:flex; flex-direction:column; justify-content:center; padding:120px 52px 80px; position:relative; overflow:hidden; background: radial-gradient(ellipse 90% 65% at 50% -5%, rgba(26,111,255,0.2) 0%, transparent 65%), radial-gradient(ellipse 45% 45% at 87% 38%, rgba(59,130,246,0.08) 0%, transparent 55%), #03091a; }
.cv-hero::before { content:''; position:absolute; inset:0; background-image: linear-gradient(rgba(74,158,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(74,158,255,0.035) 1px, transparent 1px); background-size:64px 64px; mask-image:radial-gradient(ellipse 80% 55% at 50% 0%, black, transparent 72%); }
.cv-hero-inner { display:grid; grid-template-columns:1fr auto; gap:72px; align-items:center; max-width:1200px; position:relative; z-index:1; }
.cv-tag { display:inline-flex; align-items:center; gap:7px; background:rgba(26,111,255,0.1); border:1px solid rgba(74,158,255,0.22); border-radius:100px; padding:5px 14px; font-size:10.5px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#60a5fa; margin-bottom:22px; }
.cv-hero h1 { font-family:'Sora',sans-serif; font-size:clamp(36px,5vw,66px); font-weight:800; line-height:1.07; letter-spacing:-2.5px; color:#fff; margin-bottom:20px; }
.cv-hero h1 em { font-style:normal; color:#4a9eff; }
.cv-hero-sub { font-size:16.5px; font-weight:300; line-height:1.75; color:rgba(221,232,248,0.52); max-width:510px; }
.cv-logo-hero { position:relative; width:210px; height:210px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.cv-logo-ring1 { position:absolute; inset:0; border-radius:50%; border:1px solid rgba(74,158,255,0.14); animation:spin1 20s linear infinite; }
.cv-logo-ring1::after { content:''; position:absolute; top:-5px; left:50%; transform:translateX(-50%); width:10px; height:10px; border-radius:50%; background:#4a9eff; box-shadow:0 0 14px 4px rgba(74,158,255,0.55); }
.cv-logo-ring2 { position:absolute; inset:22px; border-radius:50%; border:1px dashed rgba(74,158,255,0.07); animation:spin1 32s linear infinite reverse; }
@keyframes spin1 { to { transform:rotate(360deg); } }
.cv-logo-glow { position:absolute; inset:-30px; border-radius:50%; background:radial-gradient(circle, rgba(26,111,255,0.14) 0%, transparent 68%); animation:pulse1 3.5s ease-in-out infinite; }
@keyframes pulse1 { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.6;transform:scale(1.1)} }
.cv-stats { display:flex; gap:0; margin-top:56px; padding-top:40px; border-top:1px solid rgba(74,158,255,0.09); position:relative; z-index:1; }
.cv-stat { flex:1; padding-right:36px; margin-right:36px; border-right:1px solid rgba(74,158,255,0.07); }
.cv-stat:last-child { border-right:none; padding-right:0; margin-right:0; }
.cv-stat-n { font-family:'Sora',sans-serif; font-size:36px; font-weight:800; letter-spacing:-2px; line-height:1; color:#fff; margin-bottom:5px; }
.cv-stat-n b { color:#4a9eff; }
.cv-stat-l { font-size:12px; color:rgba(221,232,248,0.36); line-height:1.55; }
.cv-s  { padding:84px 52px; }
.cv-sa { padding:84px 52px; background:rgba(26,111,255,0.022); border-top:1px solid rgba(74,158,255,0.065); border-bottom:1px solid rgba(74,158,255,0.065); }
.cv-eyebrow { font-size:10px; font-weight:700; letter-spacing:2.8px; text-transform:uppercase; color:#4a9eff; margin-bottom:13px; }
.cv-s h2, .cv-sa h2 { font-family:'Sora',sans-serif; font-size:clamp(24px,2.7vw,38px); font-weight:800; letter-spacing:-1px; color:#fff; line-height:1.12; margin-bottom:12px; }
.cv-intro { font-size:16px; color:rgba(221,232,248,0.48); max-width:560px; line-height:1.72; margin-bottom:48px; }
.pg { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.pc { background:rgba(255,255,255,0.023); border:1px solid rgba(74,158,255,0.09); border-radius:18px; padding:26px; transition:all .2s; }
.pc:hover { border-color:rgba(74,158,255,0.28); background:rgba(26,111,255,0.055); transform:translateY(-3px); }
.pc-icon { font-size:24px; margin-bottom:12px; }
.pc h3 { font-family:'Sora',sans-serif; font-size:15px; font-weight:700; color:#fff; margin-bottom:9px; }
.pc p  { font-size:13px; color:rgba(221,232,248,0.46); line-height:1.65; }
.pc-stat { font-family:'Sora',sans-serif; font-size:28px; font-weight:800; color:#4a9eff; margin-top:16px; letter-spacing:-1px; }
.pc-sub  { font-size:10.5px; color:rgba(221,232,248,0.28); margin-top:2px; }
.mg { display:grid; grid-template-columns:repeat(5,1fr); gap:11px; }
.mc { background:rgba(255,255,255,0.02); border:1px solid rgba(74,158,255,0.08); border-radius:16px; padding:22px 14px 18px; text-align:center; transition:all .2s; }
.mc:hover { background:rgba(26,111,255,0.07); border-color:rgba(74,158,255,0.28); transform:translateY(-5px); box-shadow:0 12px 30px rgba(26,111,255,0.14); }
.mc-icon { font-size:26px; margin-bottom:8px; }
.mc-logo { width:40px; height:40px; margin:0 auto 8px; display:flex; align-items:center; justify-content:center; }
.mc-id   { font-family:'Sora',monospace; font-size:9px; color:#4a9eff; font-weight:700; letter-spacing:1.5px; margin-bottom:5px; }
.mc-name { font-family:'Sora',sans-serif; font-size:12px; font-weight:700; color:#fff; line-height:1.3; margin-bottom:6px; }
.mc-desc { font-size:10.5px; color:rgba(221,232,248,0.36); line-height:1.55; }
.ag { display:grid; grid-template-columns:repeat(4,1fr); gap:13px; }
.ac { border-radius:18px; padding:24px 20px; border:1px solid transparent; transition:transform .2s; }
.ac:hover { transform:translateY(-4px); }
.ac-adm { background:linear-gradient(145deg,rgba(26,86,160,.2),rgba(26,86,160,.05)); border-color:rgba(26,86,160,.3); }
.ac-tch { background:linear-gradient(145deg,rgba(29,122,85,.2),rgba(29,122,85,.05)); border-color:rgba(29,122,85,.3); }
.ac-stu { background:linear-gradient(145deg,rgba(212,88,10,.2),rgba(212,88,10,.05)); border-color:rgba(212,88,10,.3); }
.ac-fam { background:linear-gradient(145deg,rgba(91,63,160,.2),rgba(91,63,160,.05)); border-color:rgba(91,63,160,.3); }
.ac-emoji { font-size:28px; margin-bottom:11px; display:block; }
.ac-badge { display:inline-block; padding:2px 10px; border-radius:100px; font-size:9px; font-weight:700; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:8px; }
.ab-a { background:rgba(26,86,160,.28); color:#93b4e8; }
.ab-t { background:rgba(29,122,85,.28); color:#6dd9a8; }
.ab-s { background:rgba(212,88,10,.28); color:#f4a461; }
.ab-f { background:rgba(91,63,160,.28); color:#b39ddb; }
.ac-name { font-family:'Sora',sans-serif; font-size:14px; font-weight:700; color:#fff; margin-bottom:7px; }
.ac-desc { font-size:12.5px; color:rgba(221,232,248,0.46); line-height:1.65; }
.fg { display:flex; gap:0; position:relative; margin-top:44px; }
.fg::before { content:''; position:absolute; top:26px; left:26px; right:26px; height:2px; background:linear-gradient(90deg,#1a6fff,rgba(26,111,255,.12)); }
.fs { flex:1; text-align:center; padding:0 10px; }
.fs-n { width:52px; height:52px; border-radius:50%; margin:0 auto 12px; background:#03091a; border:2px solid #1a6fff; display:flex; align-items:center; justify-content:center; font-family:'Sora',sans-serif; font-size:16px; font-weight:800; color:#4a9eff; position:relative; z-index:1; }
.fs-t { font-family:'Sora',sans-serif; font-size:12px; font-weight:700; color:#fff; margin-bottom:5px; }
.fs-d { font-size:11px; color:rgba(221,232,248,0.36); line-height:1.6; }
.priv-g { display:grid; grid-template-columns:1fr 1fr; gap:13px; }
.priv-i { display:flex; gap:14px; align-items:flex-start; background:rgba(255,255,255,0.02); border:1px solid rgba(74,158,255,0.08); border-radius:14px; padding:18px; }
.priv-ico { font-size:18px; flex-shrink:0; margin-top:1px; }
.priv-t { font-family:'Sora',sans-serif; font-size:13px; font-weight:700; color:#fff; margin-bottom:3px; }
.priv-d { font-size:12px; color:rgba(221,232,248,0.42); line-height:1.6; }
.rm-g { display:grid; grid-template-columns:repeat(4,1fr); gap:13px; }
.rm-p { border-radius:16px; padding:24px 20px; background:rgba(255,255,255,0.02); border:1px solid rgba(74,158,255,0.08); position:relative; overflow:hidden; }
.rm-p::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.r1::before { background:#1a6fff; } .r2::before { background:#0ea5e9; }
.r3::before { background:#06b6d4; } .r4::before { background:#6366f1; }
.rm-tag { font-size:9px; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }
.r1 .rm-tag { color:#4a9eff; } .r2 .rm-tag { color:#38bdf8; }
.r3 .rm-tag { color:#22d3ee; } .r4 .rm-tag { color:#818cf8; }
.rm-title { font-family:'Sora',sans-serif; font-size:14.5px; font-weight:700; color:#fff; margin-bottom:12px; }
.rm-p ul { list-style:none; }
.rm-p ul li { font-size:11.5px; color:rgba(221,232,248,0.46); padding:4px 0; border-bottom:1px solid rgba(74,158,255,0.055); line-height:1.5; }
.rm-p ul li::before { content:'→ '; color:rgba(74,158,255,0.35); }
.cv-cta { padding:84px 52px; text-align:center; background:radial-gradient(ellipse 50% 65% at 50% 50%, rgba(26,111,255,0.09) 0%, transparent 65%); }
.cv-cta h2 { font-family:'Sora',sans-serif; font-size:42px; font-weight:800; letter-spacing:-2px; color:#fff; margin-bottom:14px; }
.cv-cta p { font-size:16px; color:rgba(221,232,248,0.42); }
.cv-ft { padding:22px 52px; border-top:1px solid rgba(74,158,255,0.07); display:flex; justify-content:space-between; align-items:center; font-size:11px; color:rgba(221,232,248,0.2); }
.cv-ft-logo { display:flex; align-items:center; gap:7px; }
</style>
"""

LANDING_HTML_1 = '<div class="cv"><nav class="cv-nav"><div class="cv-logo">'
LANDING_HTML_2 = '<span class="cv-logo-txt">Con<em>Vivir</em></span></div><div class="cv-nav-links"><span>El problema</span><span>Solución</span><span>Actores</span><span>Roadmap</span></div></nav><section class="cv-hero"><div class="cv-hero-inner"><div><div class="cv-tag">Plataforma de Convivencia Escolar</div><h1>Prevención del bullying<br><em>basada en datos</em><br>para colegios</h1><p class="cv-hero-sub">ConVivir combina sociogramas de aula, contenido educativo y gestión institucional para que docentes detecten situaciones de acoso antes de que escalen.</p></div><div class="cv-logo-hero"><div class="cv-logo-glow"></div><div class="cv-logo-ring1"></div><div class="cv-logo-ring2"></div>'
LANDING_HTML_3 = '</div></div><div class="cv-stats"><div class="cv-stat"><div class="cv-stat-n">1 de 3<b>.</b></div><div class="cv-stat-l">alumnos vive o presencia<br>situaciones de bullying</div></div><div class="cv-stat"><div class="cv-stat-n">24<b>+</b></div><div class="cv-stat-l">pantallas y flujos<br>diseñados en el MVP</div></div><div class="cv-stat"><div class="cv-stat-n">5<b>.</b></div><div class="cv-stat-l">módulos integrados:<br>Admin · Aulas · Sociograma · Contenido · Reportes</div></div><div class="cv-stat"><div class="cv-stat-n">4<b>.</b></div><div class="cv-stat-l">actores del sistema con<br>flujos completamente diferenciados</div></div></div></section><section class="cv-s"><div class="cv-eyebrow">El Problema</div><h2>El bullying existe.<br>El problema es que no lo vemos.</h2><p class="cv-intro">Sin herramientas adecuadas, los docentes actúan cuando el daño ya ocurrió.</p><div class="pg"><div class="pc"><div class="pc-icon">👁️</div><h3>Sin visibilidad de la dinámica grupal</h3><p>Los docentes no tienen forma objetiva de ver quién está aislado o en riesgo dentro del aula.</p><div class="pc-stat">70%</div><div class="pc-sub">de casos no son reportados al docente</div></div><div class="pc"><div class="pc-icon">⏱️</div><h3>Intervención tardía</h3><p>Cuando el problema se hace visible, ya generó daño psicológico y académico.</p><div class="pc-stat">6 meses</div><div class="pc-sub">tiempo promedio antes de una intervención</div></div><div class="pc"><div class="pc-icon">🧩</div><h3>Herramientas fragmentadas</h3><p>No existe una plataforma que integre diagnóstico, contenido y seguimiento en un solo lugar.</p><div class="pc-stat">0</div><div class="pc-sub">plataformas integrales disponibles en Argentina</div></div></div></section><section class="cv-sa"><div class="cv-eyebrow">La Solución</div><h2>5 módulos. Un ecosistema completo.</h2><p class="cv-intro">Cada módulo cubre una parte del ciclo: gestión institucional → diagnóstico → acción → seguimiento.</p><div class="mg"><div class="mc"><div class="mc-icon">🏛️</div><div class="mc-id">M1</div><div class="mc-name">Backoffice Admin</div><div class="mc-desc">Alta de colegios, KYC y auditoría</div></div><div class="mc"><div class="mc-icon">🚪</div><div class="mc-id">M2</div><div class="mc-name">Gestión de Aulas</div><div class="mc-desc">Creación y habilitación con código de acceso</div></div><div class="mc"><div class="mc-logo">'
LANDING_HTML_4 = '</div><div class="mc-id">M3</div><div class="mc-name">Sociograma</div><div class="mc-desc">Encuesta confidencial y mapa de relaciones</div></div><div class="mc"><div class="mc-icon">📚</div><div class="mc-id">M4</div><div class="mc-name">Contenido</div><div class="mc-desc">Guías adaptadas al rol del usuario</div></div><div class="mc"><div class="mc-icon">📊</div><div class="mc-id">M5</div><div class="mc-name">Reportes</div><div class="mc-desc">Alertas automáticas y PDF descargables</div></div></div></section><section class="cv-s"><div class="cv-eyebrow">Actores del Sistema</div><h2>Cuatro roles. Flujos completamente diferenciados.</h2><p class="cv-intro">Cada usuario accede únicamente a lo que necesita y está autorizado a ver.</p><div class="ag"><div class="ac ac-adm"><span class="ac-emoji">🏛️</span><div><span class="ac-badge ab-a">Administrador</span></div><div class="ac-name">Backoffice Admin</div><p class="ac-desc">Gestiona colegios, valida docentes mediante KYC y controla el acceso al ecosistema.</p></div><div class="ac ac-tch"><span class="ac-emoji">👨‍🏫</span><div><span class="ac-badge ab-t">Docente</span></div><div class="ac-name">Docente Validado</div><p class="ac-desc">Habilita aulas, visualiza el sociograma, gestiona alertas y descarga reportes completos.</p></div><div class="ac ac-stu"><span class="ac-emoji">🎒</span><div><span class="ac-badge ab-s">Alumno</span></div><div class="ac-name">Alumno Registrado</div><p class="ac-desc">Completa la encuesta de forma confidencial y accede a contenido adaptado a su edad.</p></div><div class="ac ac-fam"><span class="ac-emoji">👨‍👩‍👧</span><div><span class="ac-badge ab-f">Familia</span></div><div class="ac-name">Familia / Tutor</div><p class="ac-desc">Se vincula al alumno y accede a recursos orientados a prevención en el hogar.</p></div></div></section><section class="cv-sa"><div class="cv-eyebrow">Cómo Funciona</div><h2>Del registro al diagnóstico en 6 pasos.</h2><p class="cv-intro">El flujo principal del docente, desde el alta institucional hasta la intervención sobre una alerta.</p><div class="fg"><div class="fs"><div class="fs-n">1</div><div class="fs-t">Alta institucional</div><div class="fs-d">El colegio se registra y pasa el proceso KYC</div></div><div class="fs"><div class="fs-n">2</div><div class="fs-t">Habilitación del aula</div><div class="fs-d">El docente crea el aula y comparte el código</div></div><div class="fs"><div class="fs-n">3</div><div class="fs-t">Encuesta sociométrica</div><div class="fs-d">Los alumnos responden de forma confidencial</div></div><div class="fs"><div class="fs-n">4</div><div class="fs-t">Sociograma generado</div><div class="fs-d">El sistema genera el mapa de relaciones</div></div><div class="fs"><div class="fs-n">5</div><div class="fs-t">Alerta automática</div><div class="fs-d">El docente es notificado si hay alumno en riesgo</div></div><div class="fs"><div class="fs-n">6</div><div class="fs-t">Intervención y reporte</div><div class="fs-d">El docente actúa y descarga el reporte PDF</div></div></div></section><section class="cv-s"><div class="cv-eyebrow">Privacidad y Seguridad</div><h2>Los datos de los menores son intocables.</h2><p class="cv-intro">El diseño garantiza por arquitectura que ningún alumno pueda ver las respuestas de otro.</p><div class="priv-g"><div class="priv-i"><div class="priv-ico">🔒</div><div><div class="priv-t">Respuestas 100% confidenciales</div><div class="priv-d">Ningún compañero puede ver las elecciones de otro. Solo el docente accede a resultados agregados.</div></div></div><div class="priv-i"><div class="priv-ico">🛡️</div><div><div class="priv-t">Cumplimiento Ley 25.326</div><div class="priv-d">Protección de Datos Personales de Argentina. Consentimiento digital de tutores para datos de menores.</div></div></div><div class="priv-i"><div class="priv-ico">🔑</div><div><div class="priv-t">Autenticación robusta</div><div class="priv-d">JWT con refresh tokens. 2FA obligatorio para el Admin. Roles validados en cada endpoint.</div></div></div><div class="priv-i"><div class="priv-ico">📋</div><div><div class="priv-t">Auditoría inmutable</div><div class="priv-d">Log de acciones críticas: KYC, habilitación de aulas y acceso a datos sensibles.</div></div></div></div></section><section class="cv-sa"><div class="cv-eyebrow">Roadmap de Desarrollo</div><h2>MVP funcional. Evolución controlada.</h2><p class="cv-intro">Cuatro fases que permiten lanzar rápido e incorporar complejidad de forma progresiva.</p><div class="rm-g"><div class="rm-p r1"><div class="rm-tag">Fase 1 — MVP</div><div class="rm-title">Institucional + Registro</div><ul><li>Alta de colegios y docentes</li><li>KYC básico con aprobación manual</li><li>Registro de alumnos con código</li><li>Login seguro y gestión de roles</li></ul></div><div class="rm-p r2"><div class="rm-tag">Fase 2 — Core</div><div class="rm-title">Sociograma + Contenido</div><ul><li>Encuesta sociométrica completa</li><li>Algoritmo de procesamiento</li><li>Mapa de red visual</li><li>Módulo de contenido inicial</li></ul></div><div class="rm-p r3"><div class="rm-tag">Fase 3 — Reportes</div><div class="rm-title">Alertas + PDF</div><ul><li>Dashboard del docente</li><li>Alertas automáticas por riesgo</li><li>Reporte PDF descargable</li><li>Encuesta para familias</li></ul></div><div class="rm-p r4"><div class="rm-tag">Fase 4 — Evolución</div><div class="rm-title">Features Avanzados</div><ul><li>Sociograma histórico evolutivo</li><li>Integración con orientación</li><li>App móvil nativa</li><li>Gamificación para alumnos</li></ul></div></div></section><section class="cv-cta"><h2>¿Tu colegio quiere sumarse?</h2><p>Ingresá con tu cuenta para acceder a la plataforma o contactanos para comenzar.</p></section><footer class="cv-ft"><div class="cv-ft-logo">'
LANDING_HTML_5 = '<span>© 2025 ConVivir — Plataforma de Convivencia Escolar</span></div><span>Confidencial · v1.0</span></footer></div>'

# ── Usuarios ──────────────────────────────────────────────────────────────────
USERS = {
    "admin@convivir.ar":  {"password":"admin123",   "role":"admin",   "name":"Administrador"},
    "docente@colegio.ar": {"password":"docente123", "role":"teacher", "name":"Prof. María García"},
    "alumno@colegio.ar":  {"password":"alumno123",  "role":"student", "name":"Lucas Martínez"},
}

# ── Estado de sesión ──────────────────────────────────────────────────────────
if "logged_in"  not in st.session_state: st.session_state.logged_in  = False
if "user"       not in st.session_state: st.session_state.user       = None

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN / LANDING
# ══════════════════════════════════════════════════════════════════════════════
def login_as(role, name, email):
    st.session_state.logged_in     = True
    st.session_state.show_login    = False
    st.session_state.show_colegio  = False
    st.session_state.user = {"email": email, "role": role, "name": name}
    st.rerun()

def show_login_page():
    if "show_login"   not in st.session_state: st.session_state.show_login   = False
    if "show_colegio" not in st.session_state: st.session_state.show_colegio = False

    full_html = (LANDING_CSS + LANDING_HTML_1 + LOGO_NAV + LANDING_HTML_2 +
                 LOGO_HERO + LANDING_HTML_3 + LOGO_MOD + LANDING_HTML_4 +
                 LOGO_NAV + LANDING_HTML_5)
    st.markdown(full_html, unsafe_allow_html=True)

    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div:first-child {
        position:fixed; top:13px; right:52px; z-index:200;
    }
    </style>""", unsafe_allow_html=True)

    _, col_btn = st.columns([12, 1])
    with col_btn:
        if st.button("Ingresar →", type="primary", key="open_login"):
            st.session_state.show_login   = True
            st.session_state.show_colegio = False
            st.rerun()

    if not st.session_state.show_login:
        return

    st.markdown("""
    <style>
    .ov { position:fixed; inset:0; z-index:998; background:rgba(3,9,26,0.9); backdrop-filter:blur(16px); }
    .pcard-wrap { border-radius:16px; padding:24px 14px 20px; border:1px solid rgba(74,158,255,0.13); background:rgba(255,255,255,0.035); text-align:center; margin-bottom:4px; }
    .pcard-ico { font-size:38px; margin-bottom:10px; }
    .pcard-nm  { font-family:'Sora',sans-serif; font-size:14px; font-weight:700; color:#0a1f5c; margin-bottom:4px; }
    .pcard-ds  { font-size:11px; color:#5c6e8a; line-height:1.5; }
    .panel-hd  { font-family:'Sora',sans-serif; font-size:19px; font-weight:800; color:#0a1f5c; letter-spacing:-0.4px; margin-bottom:4px; margin-top:12px; }
    .panel-sb  { font-size:12.5px; color:#5c6e8a; margin-bottom:20px; }
    </style>
    <div class="ov"></div>""", unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 1.6, 1])
    with col_mid:
        with st.container(border=True):
            st.markdown(
                "<div style='display:flex;align-items:center;gap:8px;'>" + LOGO_NAV +
                "<span style='font-family:Sora,sans-serif;font-size:17px;font-weight:800;"
                "color:#0a1f5c;'>Con<span style='color:#1a6fff;'>Vivir</span></span></div>",
                unsafe_allow_html=True)

            if not st.session_state.show_colegio:
                st.markdown("<div class='panel-hd'>¿Cómo querés ingresar?</div>"
                            "<div class='panel-sb'>Seleccioná tu perfil para entrar directo</div>",
                            unsafe_allow_html=True)
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("<div class='pcard-wrap'><div class='pcard-ico'>🏛️</div>"
                                "<div class='pcard-nm'>Administrador</div>"
                                "<div class='pcard-ds'>Gestión de colegios,<br>docentes y KYC</div></div>",
                                unsafe_allow_html=True)
                    if st.button("Entrar como Admin", key="go_admin", use_container_width=True, type="primary"):
                        login_as("admin", "Administrador", "admin@convivir.ar")
                with col_b:
                    st.markdown("<div class='pcard-wrap'><div class='pcard-ico'>🏫</div>"
                                "<div class='pcard-nm'>Colegio</div>"
                                "<div class='pcard-ds'>Docentes, familias<br>y alumnos</div></div>",
                                unsafe_allow_html=True)
                    if st.button("Entrar a Colegio →", key="go_colegio", use_container_width=True):
                        st.session_state.show_colegio = True
                        st.rerun()
                st.markdown("---")
                if st.button("← Cerrar", key="cancel_login", use_container_width=True):
                    st.session_state.show_login = False
                    st.rerun()
            else:
                st.markdown("<div class='panel-hd'>Colegio</div>"
                            "<div class='panel-sb'>¿Con qué perfil ingresás?</div>",
                            unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("<div class='pcard-wrap'><div class='pcard-ico'>👨‍🏫</div>"
                                "<div class='pcard-nm'>Docente</div>"
                                "<div class='pcard-ds'>Sociograma, alertas<br>y reportes</div></div>",
                                unsafe_allow_html=True)
                    if st.button("Soy Docente", key="go_teacher", use_container_width=True, type="primary"):
                        login_as("teacher", "Prof. María García", "docente@colegio.ar")
                with c2:
                    st.markdown("<div class='pcard-wrap'><div class='pcard-ico'>👨‍👩‍👧</div>"
                                "<div class='pcard-nm'>Familia</div>"
                                "<div class='pcard-ds'>Contenido y<br>seguimiento</div></div>",
                                unsafe_allow_html=True)
                    if st.button("Soy Familia", key="go_family", use_container_width=True, type="primary"):
                        login_as("student", "Carlos Martínez (Padre)", "familia@colegio.ar")
                with c3:
                    st.markdown("<div class='pcard-wrap'><div class='pcard-ico'>🎒</div>"
                                "<div class='pcard-nm'>Alumno</div>"
                                "<div class='pcard-ds'>Encuesta y<br>contenido</div></div>",
                                unsafe_allow_html=True)
                    if st.button("Soy Alumno", key="go_student", use_container_width=True, type="primary"):
                        login_as("student", "Lucas Martínez", "alumno@colegio.ar")
                st.markdown("---")
                if st.button("← Volver", key="back_colegio", use_container_width=True):
                    st.session_state.show_colegio = False
                    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def show_sidebar():
    user = st.session_state.user
    role = user["role"]
    with st.sidebar:
        st.markdown(
            "<div style='display:flex;align-items:center;gap:9px;padding:6px 0 14px;'>" +
            LOGO_NAV +
            "<span style='font-size:18px;font-weight:800;color:white;letter-spacing:-0.4px;'>ConVivir</span></div>",
            unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("👤 **" + user["name"] + "**")
        badge  = {"admin":"badge-admin","teacher":"badge-teacher","student":"badge-student"}[role]
        labels = {"admin":"Administrador","teacher":"Docente","student":"Alumno"}
        st.markdown("<span class='" + badge + "'>" + labels[role] + "</span>", unsafe_allow_html=True)
        st.markdown("---")

        if role == "admin":
            pages = {"🏛️ Dashboard Admin":"admin_dashboard","🏫 Colegios":"admin_colegios",
                     "👨‍🏫 Docentes":"admin_docentes","✅ KYC / Validaciones":"admin_kyc"}
        elif role == "teacher":
            pages = {"📊 Mi Dashboard":"teacher_dashboard","🚪 Gestión de Aulas":"teacher_aulas",
                     "🕸️ Sociograma":"teacher_sociograma","🚨 Alertas":"teacher_alertas","📋 Reportes":"teacher_reportes"}
        else:
            pages = {"🏠 Inicio":"student_home","📝 Encuesta Sociométrica":"student_encuesta",
                     "📚 Contenido Educativo":"student_contenido"}

        if "current_page" not in st.session_state:
            st.session_state.current_page = list(pages.values())[0]

        for label, key in pages.items():
            if st.button(label, key="nav_"+key, use_container_width=True):
                st.session_state.current_page = key
                st.rerun()
        st.markdown("---")
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.current_page = None
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINAS — ADMIN
# ══════════════════════════════════════════════════════════════════════════════
def page_admin_dashboard():
    st.title("🏛️ Dashboard Administrador")
    col1,col2,col3,col4 = st.columns(4)
    col1.metric("🏫 Colegios Activos",   sum(1 for c in COLEGIOS if c["estado"]=="Activo"))
    col2.metric("⏳ Pendientes KYC",     sum(1 for c in COLEGIOS if c["estado"]=="Pendiente KYC"))
    col3.metric("👨‍🏫 Docentes validados", sum(1 for d in DOCENTES_MOCK if d["kyc"]=="Aprobado"))
    col4.metric("🚨 Alertas altas",      sum(1 for a in ALERTAS_MOCK if a["prioridad"]=="Alta" and a["estado"]=="Pendiente"), delta_color="inverse")
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Estado de colegios")
        df_e = pd.Series([c["estado"] for c in COLEGIOS]).value_counts().reset_index()
        df_e.columns = ["Estado","Cantidad"]
        fig = px.pie(df_e, names="Estado", values="Cantidad", hole=0.45,
                     color="Estado", color_discrete_map={"Activo":"#1d7a55","Pendiente KYC":"#d4580a","Suspendido":"#c0392b"})
        fig.update_layout(margin=dict(t=20,b=20,l=0,r=0), legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.subheader("KYC de docentes")
        df_k = pd.Series([d["kyc"] for d in DOCENTES_MOCK]).value_counts().reset_index()
        df_k.columns = ["KYC","Cantidad"]
        fig2 = px.bar(df_k, x="KYC", y="Cantidad", text="Cantidad",
                      color="KYC", color_discrete_map={"Aprobado":"#1d7a55","Pendiente":"#d4580a","En revisión":"#1a56a0"})
        fig2.update_layout(showlegend=False, margin=dict(t=20,b=20,l=0,r=0))
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)
    st.subheader("Colegios registrados")
    st.dataframe(pd.DataFrame(COLEGIOS).drop("id",axis=1), use_container_width=True, hide_index=True)

def page_admin_colegios():
    st.title("🏫 Gestión de Colegios")
    busqueda = st.text_input("🔍 Buscar colegio", placeholder="Nombre o ciudad...")
    filtro   = st.selectbox("Estado", ["Todos","Activo","Pendiente KYC","Suspendido"])
    colegios = [c for c in COLEGIOS if (not busqueda or busqueda.lower() in c["nombre"].lower()) and (filtro=="Todos" or c["estado"]==filtro)]
    for c in colegios:
        icon = {"Activo":"🟢","Pendiente KYC":"🟡","Suspendido":"🔴"}.get(c["estado"],"⚪")
        with st.expander(f"{icon} **{c['nombre']}** — {c['ciudad']}"):
            col1,col2,col3,col4 = st.columns(4)
            col1.metric("Docentes",c["docentes"]); col2.metric("Aulas",c["aulas"])
            col3.metric("Estado",c["estado"]);     col4.metric("Ciudad",c["ciudad"])

def page_admin_docentes():
    st.title("👨‍🏫 Gestión de Docentes")
    filtro = st.selectbox("Filtrar por KYC",["Todos","Aprobado","Pendiente","En revisión"])
    docentes = [d for d in DOCENTES_MOCK if filtro=="Todos" or d["kyc"]==filtro]
    for d in docentes:
        icon = {"Aprobado":"✅","Pendiente":"⏳","En revisión":"🔍"}.get(d["kyc"],"❓")
        with st.expander(f"{icon} **{d['nombre']}** — {d['colegio']}"):
            c1,c2,c3 = st.columns(3)
            c1.markdown(f"📧 {d['email']}"); c2.metric("Aulas",d["aulas"]); c3.metric("KYC",d["kyc"])
            if d["kyc"] in ("Pendiente","En revisión"):
                ca,cb = st.columns(2)
                if ca.button("✅ Aprobar", key="ok_"+str(d["id"]), type="primary"): st.success("Aprobado (demo)")
                if cb.button("❌ Rechazar", key="rej_"+str(d["id"])): st.error("Rechazado (demo)")

def page_admin_kyc():
    st.title("✅ KYC — Validación de Docentes")
    pendientes = [d for d in DOCENTES_MOCK if d["kyc"] in ("Pendiente","En revisión")]
    if not pendientes:
        st.success("🎉 No hay solicitudes KYC pendientes.")
        return
    for d in pendientes:
        with st.container(border=True):
            c1,c2 = st.columns([3,1])
            with c1:
                st.markdown(f"### {d['nombre']}")
                st.markdown(f"📧 {d['email']} | 🏫 {d['colegio']}")
            with c2:
                if st.button("✅ Aprobar", key="kyc_ok_"+str(d["id"]), type="primary", use_container_width=True): st.success("Aprobado (demo)")
                if st.button("❌ Rechazar", key="kyc_rej_"+str(d["id"]), use_container_width=True): st.error("Rechazado (demo)")
            st.markdown("📄 DNI_frente.pdf ✅ &nbsp; 📄 Título_docente.pdf ✅ &nbsp; 📄 Constancia_laboral.pdf ⏳")

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINAS — DOCENTE
# ══════════════════════════════════════════════════════════════════════════════
def page_teacher_dashboard():
    user = st.session_state.user
    st.title(f"📊 Dashboard — {user['name']}")
    aulas     = get_aulas()
    total_aulas = len(aulas)
    total_alumnos = sum(len(a["alumnos"]) for a in aulas.values())
    alertas_pend  = sum(1 for a in ALERTAS_MOCK if a["estado"]=="Pendiente")
    col1,col2,col3,col4 = st.columns(4)
    col1.metric("🚪 Mis Aulas",           total_aulas)
    col2.metric("👩‍🎓 Total alumnos",       total_alumnos)
    col3.metric("🚨 Alertas pendientes",   alertas_pend, delta_color="inverse")
    col4.metric("📝 Encuestas activas",    len(aulas))
    st.markdown("---")
    st.subheader("Estado de aulas")
    for codigo, aula in aulas.items():
        resp  = get_respuestas_aula(codigo)
        total = len(aula["alumnos"])
        pct   = round(len(resp)/total*100) if total else 0
        col_a, col_b, col_c = st.columns([3,1,1])
        col_a.markdown(f"**{aula['nombre']}** · `{codigo}`")
        col_b.metric("Respuestas", f"{len(resp)}/{total}")
        col_c.metric("Participación", f"{pct}%")

def page_teacher_aulas():
    st.title("🚪 Gestión de Aulas")
    tab1, tab2 = st.tabs(["📋 Mis aulas", "➕ Crear nueva aula"])
    with tab1:
        aulas = get_aulas()
        for codigo, aula in aulas.items():
            resp  = get_respuestas_aula(codigo)
            n     = len(resp)
            total = len(aula["alumnos"])
            pct   = round(n/total*100) if total else 0
            icon  = "🟢" if pct>=60 else ("🟡" if pct>0 else "⚪")
            with st.expander(f"{icon} **{aula['nombre']}** · `{codigo}` · {n}/{total} respuestas ({pct}%)"):
                col1,col2,col3 = st.columns(3)
                col1.metric("Alumnos",total); col2.metric("Respondieron",n); col3.metric("Participación",f"{pct}%")
                st.markdown("#### 📢 Código para los alumnos")
                st.markdown(f"<div style='background:#e8f0fe;border-radius:10px;padding:16px;"
                            f"font-size:28px;font-weight:800;letter-spacing:4px;color:#0f2240;"
                            f"text-align:center;'>{codigo}</div>", unsafe_allow_html=True)
                st.caption("Los alumnos van a **Encuesta Sociométrica** y escriben este código + su número de lista.")
                respondieron = {r["alumno_id"] for r in resp}
                st.markdown("#### 👥 Alumnos")
                cols = st.columns(3)
                for i, a in enumerate(aula["alumnos"]):
                    cols[i%3].markdown(f"{'✅' if a['id'] in respondieron else '⏳'} {a['id']}. {a['nombre']}")
    with tab2:
        st.markdown("### Cargá el listado de alumnos")
        metodo = st.radio("Método", ["📄 Subir Excel","✏️ Cargar manualmente"], horizontal=True)
        col1,col2 = st.columns(2)
        nombre_aula = col1.text_input("Nombre del aula", placeholder="Ej: 4° B Primaria")
        codigo_aula = col2.text_input("Código de acceso", placeholder="Ej: CUARTOB2025",
                                      help="Sin espacios, mayúsculas").upper().replace(" ","")
        alumnos_lista = []
        if metodo == "📄 Subir Excel":
            plantilla = pd.DataFrame({"Nombre":["Juan García","María López"],"Genero":["M","F"]})
            buf = io.BytesIO(); plantilla.to_excel(buf, index=False)
            st.download_button("⬇️ Descargar plantilla", data=buf.getvalue(),
                               file_name="plantilla_alumnos.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            archivo = st.file_uploader("Subí el Excel", type=["xlsx","xls","csv"])
            if archivo:
                try:
                    df = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
                    df.columns = [c.strip().lower() for c in df.columns]
                    col_n = next((c for c in df.columns if "nombre" in c), None)
                    col_g = next((c for c in df.columns if "gen" in c or "sex" in c), None)
                    if col_n:
                        df = df.dropna(subset=[col_n])
                        for _, row in df.iterrows():
                            g = str(row[col_g]).upper()[0] if col_g else "?"
                            alumnos_lista.append({"nombre":row[col_n].strip(),"genero":g})
                        st.success(f"✅ {len(alumnos_lista)} alumnos cargados.")
                        st.dataframe(pd.DataFrame(alumnos_lista), use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            texto = st.text_area("Lista (Nombre, M/F por línea)", placeholder="Juan García, M\nMaría López, F", height=200)
            if texto:
                for linea in texto.strip().split("\n"):
                    partes = linea.strip().split(",")
                    if partes[0].strip():
                        alumnos_lista.append({"nombre":partes[0].strip(),
                                              "genero":partes[1].strip().upper()[0] if len(partes)>1 else "?"})
                if alumnos_lista: st.info(f"{len(alumnos_lista)} alumnos listos.")
        st.markdown("---")
        if st.button("🚀 Crear aula", type="primary", use_container_width=True):
            if not nombre_aula: st.error("Ingresá el nombre del aula.")
            elif len(codigo_aula) < 4: st.error("El código debe tener al menos 4 caracteres.")
            elif not alumnos_lista: st.error("Cargá al menos un alumno.")
            elif get_aula(codigo_aula): st.error(f"Ya existe el código {codigo_aula}.")
            else:
                crear_aula(codigo_aula, nombre_aula, user["name"] if (user:=st.session_state.user) else "Docente", alumnos_lista)
                st.success(f"✅ Aula **{nombre_aula}** creada con {len(alumnos_lista)} alumnos.")
                st.markdown(f"<div style='background:#e8f0fe;border-radius:10px;padding:16px;"
                            f"font-size:28px;font-weight:800;letter-spacing:4px;color:#0f2240;"
                            f"text-align:center;'>{codigo_aula}</div>", unsafe_allow_html=True)
                st.balloons()

def page_teacher_sociograma():
    st.title("🕸️ Sociograma")
    PERFIL_COLOR = {"Popular":"#1d7a55","Integrado":"#1a56a0","Controvertido":"#5b3fa0",
                    "Aislado":"#d4580a","Rechazado":"#c0392b","Sin datos":"#9a9690"}
    aulas = get_aulas()
    if not aulas: st.warning("No hay aulas."); return
    codigos = list(aulas.keys())
    idx = st.selectbox("Aula", range(len(codigos)),
                       format_func=lambda i: f"{aulas[codigos[i]]['nombre']} ({codigos[i]})")
    codigo = codigos[idx]
    aula   = aulas[codigo]
    resp   = get_respuestas_aula(codigo)
    total  = len(aula["alumnos"])
    n      = len(resp)
    pct    = round(n/total*100) if total else 0
    c1,c2,c3 = st.columns(3)
    c1.metric("Alumnos",total); c2.metric("Respondieron",n)
    c3.metric("Participación",f"{pct}%", delta="Suficiente" if pct>=60 else "Necesitás más")
    if n == 0:
        st.info(f"Todavía no hay respuestas. Código del aula: **`{codigo}`**"); return
    datos = calcular_sociograma(codigo)
    edges = datos.pop("_edges",[])
    datos.pop("_n_respuestas",None); datos.pop("_total_alumnos",None)
    col_a,col_b = st.columns([3,1])
    with col_a:
        mostrar = st.radio("Vínculos:", ["Todos","Solo positivos","Solo negativos"], horizontal=True)
    with col_b:
        solo_alertas = st.checkbox("Solo alertas 🚨")
    cols_ley = st.columns(len(PERFIL_COLOR))
    for col,(perfil,color) in zip(cols_ley, PERFIL_COLOR.items()):
        col.markdown(f"<span style='background:{color};color:white;padding:2px 10px;"
                     f"border-radius:20px;font-size:11px;font-weight:700'>{perfil}</span>",
                     unsafe_allow_html=True)
    st.markdown("---")
    G = nx.DiGraph()
    for aid in datos: G.add_node(aid)
    edge_f = []
    for (src,dst,tipo,dim) in edges:
        tv = "negativo" if tipo=="victima" else tipo
        if mostrar=="Solo positivos" and tv!="positivo": continue
        if mostrar=="Solo negativos" and tv!="negativo": continue
        edge_f.append((src,dst,tv)); G.add_edge(src,dst,tipo=tv)
    pos = nx.spring_layout(G, seed=42, k=2.8)
    traces = []
    for (src,dst,tv) in edge_f:
        if src not in pos or dst not in pos: continue
        x0,y0=pos[src]; x1,y1=pos[dst]
        color = "#1d7a55" if tv=="positivo" else "#c0392b"
        op = 0.75
        if solo_alertas and datos.get(dst,{}).get("alerta") is None: op=0.05
        traces.append(go.Scatter(x=[x0,x1,None],y=[y0,y1,None],mode="lines",
                                 line=dict(width=1.6,color=color),opacity=op,hoverinfo="none",showlegend=False))
    nx_l,ny_l,nt,nc,ns,nh = [],[],[],[],[],[]
    for aid,info in datos.items():
        if aid not in pos: continue
        if solo_alertas and info["alerta"] is None: continue
        x,y=pos[aid]; nx_l.append(x); ny_l.append(y)
        nt.append(info["nombre"].split()[0])
        nc.append(PERFIL_COLOR.get(info["perfil"],"#9a9690"))
        ns.append(32 if info["perfil"]=="Popular" else 22)
        alerta_txt = f"<br>🚨 {info['alerta']}" if info["alerta"] else ""
        nh.append(f"<b>{info['nombre']}</b><br>Perfil: {info['perfil']}<br>"
                  f"Votos ✅: {info['votos_positivos']} · ❌: {info['votos_negativos']}"
                  f"<br>{'✅ Respondió' if info['respondio'] else '❌ No respondió'}{alerta_txt}")
    fig = go.Figure(data=traces+[go.Scatter(x=nx_l,y=ny_l,mode="markers+text",text=nt,
                    textposition="top center",textfont=dict(size=11,color="#0f2240"),
                    marker=dict(size=ns,color=nc,line=dict(width=2,color="white")),
                    hovertext=nh,hoverinfo="text",showlegend=False)])
    fig.update_layout(height=560,margin=dict(l=20,r=20,t=20,b=20),
                      xaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
                      yaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
                      plot_bgcolor="rgba(249,246,240,0.4)",paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.subheader("Tabla de perfiles")
    rows = [{"Nombre":v["nombre"],"Perfil":v["perfil"],"Votos ✅":v["votos_positivos"],
             "Votos ❌":v["votos_negativos"],"Respondió":"✅" if v["respondio"] else "❌",
             "Alerta":v["alerta"] or "—"} for v in datos.values()]
    st.dataframe(pd.DataFrame(rows).sort_values("Votos ✅",ascending=False),
                 use_container_width=True, hide_index=True)
    mensajes = [(r["alumno_id"],r["mensaje_docente"]) for r in resp if r.get("mensaje_docente","").strip()]
    if mensajes:
        st.markdown("---"); st.subheader("💌 Mensajes privados")
        for aid,msg in mensajes:
            nombre = next((v["nombre"] for k,v in datos.items() if k==aid), f"Alumno #{aid}")
            with st.expander(f"Mensaje de {nombre}"): st.markdown(f"> {msg}")

def page_teacher_alertas():
    st.title("🚨 Alertas")
    filtro = st.selectbox("Filtrar", ["Todas","Alta","Media","Baja"])
    alertas = [a for a in ALERTAS_MOCK if filtro=="Todas" or a["prioridad"]==filtro]
    for alerta in alertas:
        css = {"Alta":"alert-high","Media":"alert-medium","Baja":"alert-low"}.get(alerta["prioridad"],"")
        icon = {"Alta":"🔴","Media":"🟡","Baja":"🟢"}.get(alerta["prioridad"],"")
        with st.expander(f"{icon} **{alerta['alumno']}** — {alerta['tipo']} ({alerta['estado']})"):
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Prioridad",alerta["prioridad"]); c2.metric("Estado",alerta["estado"])
            c3.metric("Fecha",alerta["fecha"]);         c4.metric("Aula",alerta["aula"])
            if alerta["tipo"]=="Rechazo elevado":
                st.info("💡 Revisá las dinámicas del grupo y considerá una actividad de integración.")
            elif alerta["tipo"]=="Aislamiento":
                st.info("💡 Facilitá espacios de participación. Considerá comunicarte con la familia.")
            else:
                st.info("💡 Monitoreá la situación. El alumno recibe elecciones positivas y negativas.")
            nota = st.text_area("Nota de seguimiento", value=alerta.get("nota",""), key="nota_"+str(alerta["id"]))
            ca,cb = st.columns(2)
            if ca.button("💾 Guardar nota", key="save_"+str(alerta["id"]), type="primary"): st.success("Nota guardada (demo)")
            if cb.button("✅ Marcar como resuelta", key="res_"+str(alerta["id"])): st.success("Resuelta (demo)")

def page_teacher_reportes():
    st.title("📋 Reportes")
    aulas = get_aulas()
    if not aulas: st.info("No hay aulas."); return
    codigos = list(aulas.keys())
    idx = st.selectbox("Aula", range(len(codigos)),
                       format_func=lambda i: f"{aulas[codigos[i]]['nombre']} ({codigos[i]})")
    codigo = codigos[idx]
    datos  = calcular_sociograma(codigo)
    datos.pop("_edges",None); datos.pop("_n_respuestas",None); datos.pop("_total_alumnos",None)
    resp   = get_respuestas_aula(codigo)
    total  = len(aulas[codigo]["alumnos"])
    n_resp = len(resp)
    en_riesgo = sum(1 for v in datos.values() if isinstance(v,dict) and v.get("alerta"))
    c1,c2,c3 = st.columns(3)
    c1.metric("Encuestados",f"{n_resp}/{total}")
    c2.metric("En riesgo",en_riesgo,delta_color="inverse")
    c3.metric("Participación",f"{round(n_resp/total*100) if total else 0}%")
    perfiles = [v["perfil"] for v in datos.values() if isinstance(v,dict) and v["perfil"]!="Sin datos"]
    if perfiles:
        df_p = pd.Series(perfiles).value_counts().reset_index()
        df_p.columns = ["Perfil","Cantidad"]
        color_map = {"Popular":"#1d7a55","Integrado":"#1a56a0","Aislado":"#d4580a","Rechazado":"#c0392b","Controvertido":"#5b3fa0"}
        fig = px.bar(df_p, x="Perfil", y="Cantidad", color="Perfil", color_discrete_map=color_map, text="Cantidad")
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, margin=dict(t=20,b=20,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    rows = [{"Nombre":v["nombre"],"Perfil":v["perfil"],"Votos ✅":v["votos_positivos"],
             "Votos ❌":v["votos_negativos"],"Respondió":"✅" if v["respondio"] else "❌",
             "Alerta":v["alerta"] or "—"} for v in datos.values() if isinstance(v,dict)]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINAS — ALUMNO
# ══════════════════════════════════════════════════════════════════════════════
def page_student_home():
    user = st.session_state.user
    st.title(f"👋 Hola, {user['name'].split()[0]}!")
    st.markdown("Bienvenido/a a ConVivir — tu espacio para mejorar la convivencia en el aula.")
    with st.container(border=True):
        c1,c2 = st.columns([2,1])
        with c1:
            st.markdown("### 📝 Tu encuesta está disponible")
            st.markdown("Respondé la encuesta de convivencia de tu aula. Es confidencial.")
        with c2:
            if st.button("Ir a la encuesta →", type="primary", use_container_width=True):
                st.session_state.current_page = "student_encuesta"; st.rerun()
    st.markdown("---")
    c1,c2,c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("### 📝 Encuesta"); st.markdown("Respondé sobre tu aula de forma anónima.")
            if st.button("Ir a la encuesta", use_container_width=True):
                st.session_state.current_page = "student_encuesta"; st.rerun()
    with c2:
        with st.container(border=True):
            st.markdown("### 📚 Contenido"); st.markdown("Artículos y guías sobre convivencia.")
            if st.button("Ver contenido", use_container_width=True):
                st.session_state.current_page = "student_contenido"; st.rerun()
    with c3:
        with st.container(border=True):
            st.markdown("### 💬 Mensaje al docente"); st.markdown("Enviá un mensaje confidencial.")
            if st.button("Enviar mensaje", use_container_width=True):
                st.session_state.show_mensaje = True; st.rerun()
    if st.session_state.get("show_mensaje"):
        st.markdown("---"); st.subheader("💬 Mensaje confidencial")
        st.info("Solo lo ve tu docente.")
        msg = st.text_area("Escribí tu mensaje:", placeholder="Podés contar lo que está pasando...")
        if st.button("Enviar", type="primary"):
            if msg: st.success("✅ Mensaje enviado."); st.session_state.show_mensaje = False
            else: st.error("Escribí algo antes de enviar.")

def page_student_encuesta():
    st.title("📝 Encuesta de Convivencia")
    if "enc_alumno_id"     not in st.session_state: st.session_state.enc_alumno_id     = None
    if "enc_codigo_aula"   not in st.session_state: st.session_state.enc_codigo_aula   = None
    if "enc_alumno_nombre" not in st.session_state: st.session_state.enc_alumno_nombre = ""
    if "enc_enviada"       not in st.session_state: st.session_state.enc_enviada       = False
    if "enc_paso"          not in st.session_state: st.session_state.enc_paso          = 1

    if st.session_state.enc_paso == 1:
        st.markdown("### 👋 Antes de empezar, identificate")
        st.info("Tus respuestas son **completamente confidenciales**.")
        with st.form("id_form"):
            codigo = st.text_input("Código de aula", placeholder="Ej: AULA2025").upper()
            numero = st.number_input("Tu número de lista", min_value=1, max_value=60, step=1)
            if st.form_submit_button("Continuar →", type="primary", use_container_width=True):
                aula = get_aula(codigo)
                if not aula: st.error("Código incorrecto."); return
                alumno = get_alumno_by_numero(codigo, int(numero))
                if not alumno: st.error(f"No encontré el número {int(numero)}."); return
                if ya_respondio(codigo, alumno["id"]): st.warning(f"¡Hola {alumno['nombre']}! Ya respondiste. ¡Gracias!"); return
                st.session_state.enc_alumno_id=alumno["id"]; st.session_state.enc_codigo_aula=codigo
                st.session_state.enc_alumno_nombre=alumno["nombre"]; st.session_state.enc_paso=2
                st.rerun()
        return

    if st.session_state.enc_enviada:
        st.balloons()
        st.markdown("<div style='text-align:center;padding:48px;'><div style='font-size:64px;'>✅</div>"
                    "<h2 style='color:#0f2240;'>¡Gracias por responder!</h2>"
                    "<p style='color:#5c5852;'>Tus respuestas fueron guardadas de forma confidencial.</p></div>",
                    unsafe_allow_html=True)
        if st.button("← Volver al inicio"):
            for k in ["enc_enviada","enc_paso","enc_alumno_id","enc_codigo_aula","enc_alumno_nombre"]:
                st.session_state[k] = (False if k=="enc_enviada" else (1 if k=="enc_paso" else None))
            st.rerun()
        return

    codigo=st.session_state.enc_codigo_aula; alumno_id=st.session_state.enc_alumno_id
    nombre=st.session_state.enc_alumno_nombre; aula=get_aula(codigo)
    companeros=[a for a in aula["alumnos"] if a["id"]!=alumno_id]
    id_por_nombre={a["nombre"]:a["id"] for a in companeros}
    lista=list(id_por_nombre.keys())
    st.markdown(f"### Hola, **{nombre}** 👋 · Aula: **{aula['nombre']}**")
    st.markdown("<div style='background:#e8f0fe;border-left:4px solid #1a56a0;border-radius:8px;"
                "padding:14px 18px;margin:12px 0 20px;'><strong>🔒 Tus respuestas son confidenciales</strong><br>"
                "<span style='font-size:14px;color:#1a3a7a;'>Ningún compañero/a puede ver lo que elegís. "
                "Tu docente solo ve resultados generales del aula.</span></div>", unsafe_allow_html=True)
    with st.form("enc_form"):
        st.markdown("## 🌟 Tus relaciones")
        st.markdown("**1. ¿Quiénes te caen mejor o con quiénes te gusta más estar?**")
        me_gusta    = st.multiselect("Elegí hasta 3", lista, max_selections=3, key="f_me_gusta")
        st.markdown("**2. ¿Con quiénes preferís no estar o trabajar?**")
        no_me_gusta = st.multiselect("Elegí hasta 3", lista, max_selections=3, key="f_no_me_gusta")
        st.markdown("**3. ¿Quiénes son tus mejores amigos/as del aula?**")
        mis_amigos  = st.multiselect("Elegí hasta 3", lista, max_selections=3, key="f_mis_amigos")
        st.markdown("---")
        st.markdown("## 🤝 ¿Quiénes se portan bien con los demás?")
        st.markdown("**4. ¿Quiénes ayudan a sus compañeros cuando los necesitan?**")
        ayuda = st.multiselect("Elegí hasta 3", lista, max_selections=3, key="f_ayuda")
        st.markdown("**5. ¿Quiénes animan o consuelan cuando alguien está triste?**")
        anima = st.multiselect("Elegí hasta 3", lista, max_selections=3, key="f_anima")
        st.markdown("---")
        st.markdown("## ⚠️ Situaciones que no están bien")
        st.caption("Esto ayuda al docente a mejorar la convivencia. Es confidencial.")
        st.markdown("**6. ¿Hay alguien que insulte, se burle o se ría de sus compañeros?**")
        insulta = st.multiselect("Elegí hasta 3", lista, max_selections=3, key="f_insulta")
        st.markdown("**7. ¿Hay alguien que no deje participar o excluya a otros?**")
        no_deja = st.multiselect("Elegí hasta 3", lista, max_selections=3, key="f_no_deja")
        st.markdown("---")
        st.markdown("## 💬 Sobre vos")
        acoso = st.radio(
            "**8. En los últimos meses, ¿algún compañero/a te hizo sentir mal de forma repetida?**",
            ["No, no me pasó nada de eso","Sí, me pasó una o dos veces",
             "Sí, me pasa seguido (más de dos veces al mes)","Sí, me pasa casi todas las semanas"], key="f_acoso")
        st.markdown("---")
        st.markdown("#### 💌 Mensaje privado para tu docente (opcional)")
        mensaje = st.text_area("Solo lo/la ve él/ella.", placeholder="Podés escribir lo que sea.", key="f_mensaje")
        if st.form_submit_button("✅ Enviar mi encuesta", type="primary", use_container_width=True):
            def a_ids(lst): return [id_por_nombre[n] for n in lst if n in id_por_nombre]
            guardar_respuesta(codigo, alumno_id, {
                "me_gusta":a_ids(me_gusta),"no_me_gusta":a_ids(no_me_gusta),"mis_amigos":a_ids(mis_amigos),
                "ayuda":a_ids(ayuda),"anima":a_ids(anima),"insulta":a_ids(insulta),
                "no_deja_participar":a_ids(no_deja),"acoso_sufrido":acoso,"mensaje_docente":mensaje,
            })
            st.session_state.enc_enviada=True; st.rerun()

def page_student_contenido():
    st.title("📚 Contenido Educativo")
    ARTICULOS = [
        {"titulo":"¿Qué es el bullying y cómo reconocerlo?","tipo":"Artículo","tiempo":"4 min",
         "contenido":"El **bullying** es cualquier comportamiento agresivo y repetido para lastimar a otra persona.\n\n**Señales:**\n- Evita ir al colegio\n- Está triste o asustado\n- Tiene pocos amigos\n\n**¿Qué hacer?** Hablá con tu docente o un adulto de confianza."},
        {"titulo":"Cómo pedir ayuda si estás pasando mal","tipo":"Guía","tiempo":"3 min",
         "contenido":"Pedir ayuda **no es de débiles** — es lo más valiente que podés hacer.\n\n1. Identificá a alguien de confianza\n2. Buscá un momento tranquilo para hablar\n3. Contá lo que está pasando\n4. Recordá: **merecés estar bien**."},
        {"titulo":"Ser buen compañero/a","tipo":"Artículo","tiempo":"5 min",
         "contenido":"Las **pequeñas acciones** hacen la diferencia:\n- Saludá a todos\n- Incluí a quien está solo\n- No te rías si alguien se equivoca\n- Defendé a quien está siendo maltratado"},
    ]
    for a in ARTICULOS:
        icon = {"Artículo":"📄","Guía":"📋"}.get(a["tipo"],"📄")
        with st.expander(f"{icon} **{a['titulo']}** · {a['tiempo']}"):
            st.markdown(a["contenido"])
    st.markdown("---")
    st.warning("**🆘 ¿Necesitás ayuda urgente?**\n\n- Hablá con un adulto de confianza\n- **Línea de ayuda:** 102 (Consejo Nacional de la Niñez)")

# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def route():
    page = st.session_state.get("current_page","")
    role = st.session_state.user["role"]
    if   page=="admin_dashboard"  or (role=="admin"   and not page): page_admin_dashboard()
    elif page=="admin_colegios":   page_admin_colegios()
    elif page=="admin_docentes":   page_admin_docentes()
    elif page=="admin_kyc":        page_admin_kyc()
    elif page=="teacher_dashboard" or (role=="teacher" and not page): page_teacher_dashboard()
    elif page=="teacher_aulas":    page_teacher_aulas()
    elif page=="teacher_sociograma": page_teacher_sociograma()
    elif page=="teacher_alertas":  page_teacher_alertas()
    elif page=="teacher_reportes": page_teacher_reportes()
    elif page=="student_home"      or (role=="student" and not page): page_student_home()
    elif page=="student_encuesta": page_student_encuesta()
    elif page=="student_contenido": page_student_contenido()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    show_login_page()
else:
    show_sidebar()
    route()
