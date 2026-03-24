import streamlit as st
import random

st.set_page_config(
    page_title="ConVivir — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# LOGOS SVG
# ══════════════════════════════════════════════════════════════════════════════
LOGO_NAV = (
    '<svg width="148" height="40" viewBox="0 0 296 80" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4,76 L24,8 L32,8 L32,76 Z" fill="#4db8a0"/>'
    '<path d="M60,76 L40,8 L32,8 L32,76 Z" fill="#4db8a0"/>'
    '<circle cx="32" cy="23" r="7.5" fill="#0e1c19"/>'
    '<path d="M32,30.5 Q21,25 17,14" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round" fill="none"/>'
    '<path d="M32,30.5 Q43,25 47,14" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round" fill="none"/>'
    '<line x1="32" y1="30.5" x2="32" y2="48" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round"/>'
    '<line x1="32" y1="48" x2="26" y2="61" stroke="#0e1c19" stroke-width="4.5" stroke-linecap="round"/>'
    '<line x1="32" y1="48" x2="38" y2="61" stroke="#0e1c19" stroke-width="4.5" stroke-linecap="round"/>'
    '<rect x="27" y="3" width="10" height="7" rx="1.5" fill="#e8621a"/>'
    '<text x="74" y="50" font-family="Arial Black,Impact,sans-serif" font-size="36" font-weight="900" fill="#1a2e2a" letter-spacing="1">ANIMAR</text>'
    '<text x="74" y="66" font-family="Arial,sans-serif" font-size="9.5" font-weight="400" fill="#4db8a0" letter-spacing="2.5">INFANCIAS &amp; EDUCACI&#xD3;N</text>'
    '</svg>'
)
LOGO_HERO = (
    '<svg width="200" height="228" viewBox="0 0 200 228" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M8,182 L70,10 L100,10 L100,182 Z" fill="#4db8a0"/>'
    '<path d="M192,182 L130,10 L100,10 L100,182 Z" fill="#4db8a0"/>'
    '<circle cx="100" cy="48" r="17" fill="#0e1c19"/>'
    '<path d="M100,65 Q74,53 58,32" stroke="#0e1c19" stroke-width="13" stroke-linecap="round" fill="none"/>'
    '<path d="M100,65 Q126,53 142,32" stroke="#0e1c19" stroke-width="13" stroke-linecap="round" fill="none"/>'
    '<line x1="100" y1="65" x2="100" y2="108" stroke="#0e1c19" stroke-width="13" stroke-linecap="round"/>'
    '<line x1="100" y1="108" x2="83" y2="140" stroke="#0e1c19" stroke-width="11" stroke-linecap="round"/>'
    '<line x1="100" y1="108" x2="117" y2="140" stroke="#0e1c19" stroke-width="11" stroke-linecap="round"/>'
    '<rect x="88" y="2" width="24" height="15" rx="3" fill="#e8621a"/>'
    '<text x="100" y="207" text-anchor="middle" font-family="Arial Black,Impact,sans-serif" font-size="38" font-weight="900" fill="white" letter-spacing="2">ANIMAR</text>'
    '<text x="100" y="224" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="400" fill="rgba(221,232,228,0.55)" letter-spacing="2.5">INFANCIAS &amp; EDUCACI&#xD3;N</text>'
    '</svg>'
)
LOGO_MOD = (
    '<svg width="42" height="42" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="100" height="100" rx="14" fill="rgba(77,184,160,0.15)"/>'
    '<path d="M8,94 L33,12 L50,12 L50,94 Z" fill="#4db8a0"/>'
    '<path d="M92,94 L67,12 L50,12 L50,94 Z" fill="#4db8a0"/>'
    '<circle cx="50" cy="30" r="9" fill="#0e1c19"/>'
    '<path d="M50,39 Q38,33 31,21" stroke="#0e1c19" stroke-width="6.5" stroke-linecap="round" fill="none"/>'
    '<path d="M50,39 Q62,33 69,21" stroke="#0e1c19" stroke-width="6.5" stroke-linecap="round" fill="none"/>'
    '<line x1="50" y1="39" x2="50" y2="58" stroke="#0e1c19" stroke-width="6.5" stroke-linecap="round"/>'
    '<line x1="50" y1="58" x2="43" y2="72" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round"/>'
    '<line x1="50" y1="58" x2="57" y2="72" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round"/>'
    '<rect x="44" y="6" width="12" height="8" rx="2" fill="#e8621a"/>'
    '</svg>'
)
LOGO_SIDEBAR = (
    '<svg width="148" height="40" viewBox="0 0 296 80" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4,76 L24,8 L32,8 L32,76 Z" fill="#4db8a0"/>'
    '<path d="M60,76 L40,8 L32,8 L32,76 Z" fill="#4db8a0"/>'
    '<circle cx="32" cy="23" r="7.5" fill="#0e1c19"/>'
    '<path d="M32,30.5 Q21,25 17,14" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round" fill="none"/>'
    '<path d="M32,30.5 Q43,25 47,14" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round" fill="none"/>'
    '<line x1="32" y1="30.5" x2="32" y2="48" stroke="#0e1c19" stroke-width="5.5" stroke-linecap="round"/>'
    '<line x1="32" y1="48" x2="26" y2="61" stroke="#0e1c19" stroke-width="4.5" stroke-linecap="round"/>'
    '<line x1="32" y1="48" x2="38" y2="61" stroke="#0e1c19" stroke-width="4.5" stroke-linecap="round"/>'
    '<rect x="27" y="3" width="10" height="7" rx="1.5" fill="#e8621a"/>'
    '<text x="74" y="50" font-family="Arial Black,Impact,sans-serif" font-size="36" font-weight="900" fill="white" letter-spacing="1">ANIMAR</text>'
    '<text x="74" y="66" font-family="Arial,sans-serif" font-size="9.5" font-weight="400" fill="rgba(77,184,160,0.65)" letter-spacing="2.5">INFANCIAS &amp; EDUCACI&#xD3;N</text>'
    '</svg>'
)

# ══════════════════════════════════════════════════════════════════════════════
# MOCK DATA
# ══════════════════════════════════════════════════════════════════════════════
MOCK_COLEGIOS = [
    {"id": "C001", "nombre": "Instituto Modelo Nacional", "ciudad": "Buenos Aires", "alumnos": 520, "docentes": 34, "estado": "Activo", "kyc": "Aprobado", "fecha_alta": "12/03/2024"},
    {"id": "C002", "nombre": "Colegio San Martín de Porres", "ciudad": "Córdoba", "alumnos": 310, "docentes": 21, "estado": "Activo", "kyc": "Aprobado", "fecha_alta": "28/03/2024"},
    {"id": "C003", "nombre": "Escuela Técnica Nº 7", "ciudad": "Rosario", "alumnos": 480, "docentes": 29, "estado": "Pendiente", "kyc": "En revisión", "fecha_alta": "05/05/2024"},
    {"id": "C004", "nombre": "Colegio Privado Los Álamos", "ciudad": "Mendoza", "alumnos": 220, "docentes": 16, "estado": "Activo", "kyc": "Aprobado", "fecha_alta": "18/01/2024"},
    {"id": "C005", "nombre": "Bachillerato Popular del Sur", "ciudad": "La Plata", "alumnos": 190, "docentes": 14, "estado": "Suspendido", "kyc": "Rechazado", "fecha_alta": "02/02/2024"},
    {"id": "C006", "nombre": "Escuela Normal Sup. Nº 1", "ciudad": "Tucumán", "alumnos": 610, "docentes": 41, "estado": "Pendiente", "kyc": "En revisión", "fecha_alta": "20/05/2024"},
]

MOCK_ALUMNOS_4A = [
    {"id": "A01", "nombre": "Lucas Martínez",     "riesgo": "alto",   "tipo": "Aislado extremo",     "nominaciones_rec": 0, "nominaciones_env": 2, "rechazos": 4},
    {"id": "A02", "nombre": "Valentina Torres",   "riesgo": "alto",   "tipo": "Objetivo de acoso",   "nominaciones_rec": 1, "nominaciones_env": 3, "rechazos": 5},
    {"id": "A03", "nombre": "Mateo González",      "riesgo": "medio",  "tipo": "En periferia",        "nominaciones_rec": 2, "nominaciones_env": 2, "rechazos": 2},
    {"id": "A04", "nombre": "Sofía Ramírez",       "riesgo": "bajo",   "tipo": "Integrado",           "nominaciones_rec": 5, "nominaciones_env": 4, "rechazos": 0},
    {"id": "A05", "nombre": "Benjamín López",      "riesgo": "bajo",   "tipo": "Líder positivo",      "nominaciones_rec": 8, "nominaciones_env": 5, "rechazos": 0},
    {"id": "A06", "nombre": "Camila Fernández",    "riesgo": "bajo",   "tipo": "Integrado",           "nominaciones_rec": 4, "nominaciones_env": 4, "rechazos": 1},
    {"id": "A07", "nombre": "Joaquín Herrera",     "riesgo": "medio",  "tipo": "En periferia",        "nominaciones_rec": 2, "nominaciones_env": 1, "rechazos": 3},
    {"id": "A08", "nombre": "Isabella Díaz",       "riesgo": "bajo",   "tipo": "Integrado",           "nominaciones_rec": 5, "nominaciones_env": 4, "rechazos": 0},
    {"id": "A09", "nombre": "Thiago Morales",      "riesgo": "medio",  "tipo": "En periferia",        "nominaciones_rec": 1, "nominaciones_env": 2, "rechazos": 2},
    {"id": "A10", "nombre": "Mia Castillo",        "riesgo": "bajo",   "tipo": "Integrado",           "nominaciones_rec": 6, "nominaciones_env": 5, "rechazos": 0},
]

MOCK_AULAS = [
    {"id": "AU4A", "nombre": "4º Año "A"",  "turno": "Mañana", "alumnos": 32, "respondieron": 28, "alertas_altas": 2, "alertas_medias": 1, "estado": "Activo",   "codigo": "CV-4A-2024", "fecha": "10/03/2024"},
    {"id": "AU5B", "nombre": "5º Año "B"",  "turno": "Tarde",  "alumnos": 28, "respondieron": 28, "alertas_altas": 0, "alertas_medias": 0, "estado": "Completo", "codigo": "CV-5B-2024", "fecha": "10/03/2024"},
    {"id": "AU3C", "nombre": "3º Año "C"",  "turno": "Mañana", "alumnos": 30, "respondieron": 0,  "alertas_altas": 0, "alertas_medias": 0, "estado": "Pendiente","codigo": "CV-3C-2024", "fecha": "15/04/2024"},
]

MOCK_CONTENIDO_DOCENTE = [
    {"titulo": "Cómo identificar señales tempranas de bullying",     "tipo": "Guía práctica", "tiempo": "8 min",  "nivel": "Esencial"},
    {"titulo": "Protocolo de intervención ante alerta roja",         "tipo": "Protocolo",     "tiempo": "12 min", "nivel": "Esencial"},
    {"titulo": "Dinámica: Círculo de confianza (actividad grupal)",  "tipo": "Actividad",     "tiempo": "45 min", "nivel": "Avanzado"},
    {"titulo": "Guía de conversación individual con el alumno",      "tipo": "Guía práctica", "tiempo": "10 min", "nivel": "Esencial"},
    {"titulo": "Cómo comunicar la situación a la familia",           "tipo": "Protocolo",     "tiempo": "7 min",  "nivel": "Avanzado"},
    {"titulo": "Legislación Argentina sobre violencia escolar",      "tipo": "Marco legal",   "tiempo": "15 min", "nivel": "Referencia"},
]

MOCK_CONTENIDO_FAMILIA = [
    {"titulo": "¿Cómo saber si mi hijo es víctima de bullying?",     "tipo": "Guía",     "tiempo": "6 min",  "publico": "Familias"},
    {"titulo": "Qué decir (y qué NO decir) cuando tu hijo te cuenta", "tipo": "Guía",   "tiempo": "8 min",  "publico": "Familias"},
    {"titulo": "Cómo trabajar la autoestima en casa",                "tipo": "Actividad","tiempo": "30 min", "publico": "Familias"},
    {"titulo": "Hablar de emociones: guía por edades",               "tipo": "Guía",     "tiempo": "10 min", "publico": "Familias"},
    {"titulo": "Cuándo y cómo comunicarte con la escuela",           "tipo": "Protocolo","tiempo": "5 min",  "publico": "Familias"},
    {"titulo": "Redes sociales y acoso digital: señales de alerta",  "tipo": "Guía",     "tiempo": "9 min",  "publico": "Familias"},
]

MOCK_ALUMNO_COMPAS = [
    "Valentina Torres", "Camila Fernández", "Sofía Ramírez", "Isabella Díaz",
    "Mia Castillo", "Mateo González", "Benjamín López", "Joaquín Herrera",
    "Thiago Morales",
]

# ══════════════════════════════════════════════════════════════════════════════
# ESTILOS GLOBALES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #1a2e2a; }
  [data-testid="stSidebar"] * { color: white !important; }
  [data-testid="stSidebar"] hr { border-color: rgba(77,184,160,0.25); }
  .main .block-container { padding-top: 1.5rem; }
  h1,h2 { color: #0a1f5c; }
  h3 { color: #1a56a0; }
  .badge-admin   { background:#e8effe; color:#1a56a0; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-teacher { background:#e6f4ee; color:#1d7a55; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-student { background:#fde8d0; color:#d4580a; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-family  { background:#ede8fe; color:#5b3fa0; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .alert-high   { background:#fdeaea; border-left:4px solid #c0392b; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-medium { background:#fef3e2; border-left:4px solid #d4580a; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-low    { background:#e6f4ee; border-left:4px solid #1d7a55; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .card { background:white; border:1px solid #eaeaea; border-radius:14px; padding:20px; margin-bottom:12px; }
  .card:hover { border-color:#4db8a0; box-shadow:0 4px 16px rgba(77,184,160,0.12); }
  .tag-esencial  { background:#e6f4ee; color:#1d7a55; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:700; }
  .tag-avanzado  { background:#e8effe; color:#1a56a0; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:700; }
  .tag-ref       { background:#f5f5f5; color:#555; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:700; }
  .tag-guia      { background:#fde8d0; color:#d4580a; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:700; }
  .riesgo-alto   { color:#c0392b; font-weight:700; }
  .riesgo-medio  { color:#d4580a; font-weight:700; }
  .riesgo-bajo   { color:#1d7a55; font-weight:700; }
  .kyc-aprobado  { background:#e6f4ee; color:#1d7a55; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
  .kyc-revision  { background:#fef3e2; color:#d4580a; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
  .kyc-rechazado { background:#fdeaea; color:#c0392b; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
  .nav-item-active { background:rgba(77,184,160,0.15); border-radius:8px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LANDING CSS + HTML
# ══════════════════════════════════════════════════════════════════════════════
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
.cv-stats { display:flex; gap:0; margin-top:56px; padding-top:40px; border-top:1px solid rgba(74,158,255,0.09); position:relative; z-index:1; }
.cv-stat { flex:1; padding-right:36px; margin-right:36px; border-right:1px solid rgba(74,158,255,0.07); }
.cv-stat:last-child { border-right:none; }
.cv-stat-n { font-family:'Sora',sans-serif; font-size:36px; font-weight:800; letter-spacing:-2px; line-height:1; color:#fff; margin-bottom:5px; }
.cv-stat-n b { color:#4a9eff; }
.cv-stat-l { font-size:12px; color:rgba(221,232,248,0.36); line-height:1.55; }
.cv-s  { padding:84px 52px; }
.cv-sa { padding:84px 52px; background:rgba(26,111,255,0.022); border-top:1px solid rgba(74,158,255,0.065); border-bottom:1px solid rgba(74,158,255,0.065); }
.cv-eyebrow { font-size:10px; font-weight:700; letter-spacing:2.8px; text-transform:uppercase; color:#4a9eff; margin-bottom:13px; }
.cv-s h2, .cv-sa h2 { font-family:'Sora',sans-serif; font-size:clamp(24px,2.7vw,38px); font-weight:800; letter-spacing:-1px; color:#fff; line-height:1.12; margin-bottom:12px; }
.cv-intro { font-size:16px; color:rgba(221,232,248,0.48); max-width:560px; line-height:1.72; margin-bottom:48px; }
.pg { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.pc { background:rgba(255,255,255,0.023); border:1px solid rgba(74,158,255,0.09); border-radius:18px; padding:26px; }
.pc-icon { font-size:24px; margin-bottom:12px; }
.pc h3 { font-family:'Sora',sans-serif; font-size:15px; font-weight:700; color:#fff; margin-bottom:9px; }
.pc p  { font-size:13px; color:rgba(221,232,248,0.46); line-height:1.65; }
.pc-stat { font-family:'Sora',sans-serif; font-size:28px; font-weight:800; color:#4a9eff; margin-top:16px; letter-spacing:-1px; }
.pc-sub  { font-size:10.5px; color:rgba(221,232,248,0.28); margin-top:2px; }
.mg { display:grid; grid-template-columns:repeat(5,1fr); gap:11px; }
.mc { background:rgba(255,255,255,0.02); border:1px solid rgba(74,158,255,0.08); border-radius:16px; padding:22px 14px 18px; text-align:center; }
.mc-icon { font-size:26px; margin-bottom:8px; }
.mc-logo { width:40px; height:40px; margin:0 auto 8px; }
.mc-id   { font-family:'Sora',monospace; font-size:9px; color:#4a9eff; font-weight:700; letter-spacing:1.5px; margin-bottom:5px; }
.mc-name { font-family:'Sora',sans-serif; font-size:12px; font-weight:700; color:#fff; line-height:1.3; margin-bottom:6px; }
.mc-desc { font-size:10.5px; color:rgba(221,232,248,0.36); line-height:1.55; }
.ag { display:grid; grid-template-columns:repeat(4,1fr); gap:13px; }
.ac { border-radius:18px; padding:24px 20px; border:1px solid transparent; }
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
.r1::before { background:#1a6fff; } .r2::before { background:#0ea5e9; } .r3::before { background:#06b6d4; } .r4::before { background:#6366f1; }
.rm-tag { font-size:9px; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }
.r1 .rm-tag { color:#4a9eff; } .r2 .rm-tag { color:#38bdf8; } .r3 .rm-tag { color:#22d3ee; } .r4 .rm-tag { color:#818cf8; }
.rm-title { font-family:'Sora',sans-serif; font-size:14.5px; font-weight:700; color:#fff; margin-bottom:12px; }
.rm-p ul { list-style:none; }
.rm-p ul li { font-size:11.5px; color:rgba(221,232,248,0.46); padding:4px 0; border-bottom:1px solid rgba(74,158,255,0.055); line-height:1.5; }
.rm-p ul li::before { content:'→ '; color:rgba(74,158,255,0.35); }
.cv-cta { padding:84px 52px; text-align:center; }
.cv-cta h2 { font-family:'Sora',sans-serif; font-size:42px; font-weight:800; letter-spacing:-2px; color:#fff; margin-bottom:14px; }
.cv-cta p { font-size:16px; color:rgba(221,232,248,0.42); }
.cv-ft { padding:22px 52px; border-top:1px solid rgba(74,158,255,0.07); display:flex; justify-content:space-between; align-items:center; font-size:11px; color:rgba(221,232,248,0.2); }
</style>
"""

LANDING_BODY = """
<div class="cv">
  <nav class="cv-nav">
    <div class="cv-logo">
      <span style="font-family:'Sora',sans-serif;font-size:20px;font-weight:800;color:#fff;">Con<em style="font-style:normal;color:#4a9eff;">Vivir</em></span>
    </div>
    <div class="cv-nav-links"><span>El problema</span><span>Solución</span><span>Actores</span><span>Roadmap</span></div>
  </nav>
  <section class="cv-hero">
    <div class="cv-hero-inner">
      <div>
        <div class="cv-tag">Plataforma de Convivencia Escolar</div>
        <h1>Prevención del bullying<br><em>basada en datos</em><br>para colegios</h1>
        <p class="cv-hero-sub">ConVivir combina sociogramas de aula, contenido educativo y gestión institucional para que docentes detecten situaciones de acoso antes de que escalen.</p>
      </div>
    </div>
    <div class="cv-stats">
      <div class="cv-stat"><div class="cv-stat-n">1 de 3<b>.</b></div><div class="cv-stat-l">alumnos vive o presencia<br>situaciones de bullying</div></div>
      <div class="cv-stat"><div class="cv-stat-n">24<b>+</b></div><div class="cv-stat-l">pantallas y flujos<br>diseñados en el MVP</div></div>
      <div class="cv-stat"><div class="cv-stat-n">5<b>.</b></div><div class="cv-stat-l">módulos integrados</div></div>
      <div class="cv-stat"><div class="cv-stat-n">4<b>.</b></div><div class="cv-stat-l">actores del sistema</div></div>
    </div>
  </section>
  <section class="cv-s">
    <div class="cv-eyebrow">El Problema</div>
    <h2>El bullying existe.<br>El problema es que no lo vemos.</h2>
    <p class="cv-intro">Sin herramientas adecuadas, los docentes actúan cuando el daño ya ocurrió.</p>
    <div class="pg">
      <div class="pc"><div class="pc-icon">👁️</div><h3>Sin visibilidad de la dinámica grupal</h3><p>Los docentes no tienen forma objetiva de ver quién está aislado o en riesgo.</p><div class="pc-stat">70%</div><div class="pc-sub">de casos no son reportados al docente</div></div>
      <div class="pc"><div class="pc-icon">⏱️</div><h3>Intervención tardía</h3><p>Cuando el problema se hace visible, ya generó daño psicológico y social.</p><div class="pc-stat">6 meses</div><div class="pc-sub">tiempo promedio antes de una intervención</div></div>
      <div class="pc"><div class="pc-icon">🧩</div><h3>Herramientas fragmentadas</h3><p>No existe una plataforma que integre diagnóstico, contenido y seguimiento.</p><div class="pc-stat">0</div><div class="pc-sub">plataformas integrales en Argentina</div></div>
    </div>
  </section>
  <section class="cv-sa">
    <div class="cv-eyebrow">La Solución</div>
    <h2>5 módulos. Un ecosistema completo.</h2>
    <p class="cv-intro">Cada módulo cubre una parte del ciclo: gestión → diagnóstico → acción → seguimiento.</p>
    <div class="mg">
      <div class="mc"><div class="mc-icon">🏛️</div><div class="mc-id">M1</div><div class="mc-name">Backoffice Admin</div><div class="mc-desc">Alta de colegios, KYC y auditoría</div></div>
      <div class="mc"><div class="mc-icon">🚪</div><div class="mc-id">M2</div><div class="mc-name">Gestión de Aulas</div><div class="mc-desc">Creación y habilitación con código</div></div>
      <div class="mc"><div class="mc-icon">🕸️</div><div class="mc-id">M3</div><div class="mc-name">Sociograma</div><div class="mc-desc">Encuesta confidencial y mapa de relaciones</div></div>
      <div class="mc"><div class="mc-icon">📚</div><div class="mc-id">M4</div><div class="mc-name">Contenido</div><div class="mc-desc">Guías adaptadas al rol del usuario</div></div>
      <div class="mc"><div class="mc-icon">📊</div><div class="mc-id">M5</div><div class="mc-name">Reportes</div><div class="mc-desc">Alertas automáticas y PDF descargables</div></div>
    </div>
  </section>
  <section class="cv-s">
    <div class="cv-eyebrow">Actores del Sistema</div>
    <h2>Cuatro roles. Flujos completamente diferenciados.</h2>
    <div class="ag">
      <div class="ac ac-adm"><span class="ac-emoji">🏛️</span><div><span class="ac-badge ab-a">Administrador</span></div><div class="ac-name">Backoffice Admin</div><p class="ac-desc">Gestiona colegios, valida docentes mediante KYC y controla el acceso.</p></div>
      <div class="ac ac-tch"><span class="ac-emoji">👨‍🏫</span><div><span class="ac-badge ab-t">Docente</span></div><div class="ac-name">Docente Validado</div><p class="ac-desc">Habilita aulas, visualiza el sociograma y descarga reportes.</p></div>
      <div class="ac ac-stu"><span class="ac-emoji">🎒</span><div><span class="ac-badge ab-s">Alumno</span></div><div class="ac-name">Alumno Registrado</div><p class="ac-desc">Completa la encuesta de forma confidencial y accede a contenido.</p></div>
      <div class="ac ac-fam"><span class="ac-emoji">👨‍👩‍👧</span><div><span class="ac-badge ab-f">Familia</span></div><div class="ac-name">Familia / Tutor</div><p class="ac-desc">Se vincula al alumno y accede a recursos de prevención.</p></div>
    </div>
  </section>
  <section class="cv-cta">
    <h2>¿Tu colegio quiere sumarse?</h2>
    <p>Ingresá con tu cuenta para acceder a la plataforma.</p>
  </section>
  <footer class="cv-ft">
    <span>© 2025 ConVivir — Plataforma de Convivencia Escolar</span>
    <span>Confidencial · v1.0 · MVP</span>
  </footer>
</div>
"""

# ══════════════════════════════════════════════════════════════════════════════
# AUTH DATA
# ══════════════════════════════════════════════════════════════════════════════
CREDS = {
    "colegio": {"email": "docente@colegio.ar",  "password": "docente123", "role": "teacher", "name": "Prof. María García"},
    "admin":   {"email": "admin@convivir.ar",    "password": "admin123",   "role": "admin",   "name": "Administrador"},
    "familia": {"email": "familia@colegio.ar",   "password": "familia123", "role": "family",  "name": "Carlos Martínez"},
    "alumno":  {"email": "alumno@colegio.ar",    "password": "alumno123",  "role": "student", "name": "Lucas Martínez"},
}

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
defaults = {
    "logged_in": False, "user": None, "login_panel": None,
    "current_view": "dashboard", "encuesta_paso": 0,
    "encuesta_respuestas": {}, "encuesta_enviada": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN SCREEN
# ══════════════════════════════════════════════════════════════════════════════
def do_login(profile, email_input, pass_input):
    cred = CREDS[profile]
    if email_input == cred["email"] and pass_input == cred["password"]:
        st.session_state.logged_in = True
        st.session_state.login_panel = None
        st.session_state.current_view = "dashboard"
        st.session_state.user = {"email": cred["email"], "role": cred["role"], "name": cred["name"]}
        st.rerun()
    else:
        st.error("Email o contraseña incorrectos.")

def show_login():
    st.markdown(LANDING_CSS + LANDING_BODY, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .login-header { text-align:center; margin-bottom:32px; }
    .login-title { font-family:'Sora',sans-serif; font-size:24px; font-weight:800; color:#1a2e2a; margin:12px 0 6px; }
    .login-sub { font-size:14px; color:#7a8a82; margin:0; }
    .pwidget { background:white; border-radius:18px; border:2px solid #e0d8d0; padding:28px 14px 22px; text-align:center; box-shadow:0 4px 20px rgba(26,46,42,0.06); }
    .pwidget-ico  { font-size:44px; margin-bottom:12px; display:block; }
    .pwidget-name { font-family:'Sora',sans-serif; font-size:15px; font-weight:800; color:#1a2e2a; margin-bottom:5px; }
    .pwidget-desc { font-size:12px; color:#8a9a92; line-height:1.5; }
    .pwidget-active { border-color:#4db8a0 !important; background:linear-gradient(160deg,#f0faf7,white) !important; }
    div[data-testid="stVerticalBlock"] > div:first-child { position:fixed; top:14px; right:52px; z-index:200; }
    div[data-testid="stVerticalBlock"] > div:first-child .stButton > button { background:#4db8a0 !important; border:none !important; font-weight:700 !important; border-radius:8px !important; padding:9px 22px !important; font-size:14px !important; color:white !important; }
    </style>
    """, unsafe_allow_html=True)

    _, col_btn = st.columns([12, 1])
    with col_btn:
        if st.button("Ingresar →", type="primary", key="open_login"):
            st.session_state.login_panel = "select"
            st.rerun()

    if st.session_state.login_panel is None:
        return

    panel = st.session_state.login_panel
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="login-header">
      <h2 class="login-title">Seleccioná tu perfil</h2>
      <p class="login-sub">Para acceder a la plataforma de convivencia escolar</p>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3, p4 = st.columns(4)
    profiles = [
        ("colegio", p1, "🏫", "Colegio", "Docentes y equipo directivo"),
        ("admin",   p2, "🏛️", "Administrador", "Backoffice central Animar"),
        ("familia", p3, "👨‍👩‍👧", "Familia", "Tutores legales y familias"),
        ("alumno",  p4, "🎒", "Alumno", "Estudiantes registrados"),
    ]
    for key, col, ico, name, desc in profiles:
        with col:
            active = " pwidget-active" if panel == key else ""
            st.markdown(f"""
            <div class="pwidget{active}">
                <span class="pwidget-ico">{ico}</span>
                <div class="pwidget-name">{name}</div>
                <div class="pwidget-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Acceder", key=f"p_{key}", use_container_width=True):
                st.session_state.login_panel = key
                st.rerun()

    if panel != "select":
        st.markdown("---")
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c2:
            names = {"colegio": "Docente / Directivo", "admin": "Administrador", "familia": "Familia / Tutor", "alumno": "Alumno"}
            st.markdown(f"#### Ingresar como {names[panel]}")
            email_input = st.text_input("Email", value=CREDS[panel]["email"], key="login_email")
            pass_input  = st.text_input("Contraseña", type="password", value=CREDS[panel]["password"], key="login_pass")
            if st.button("Iniciar Sesión", key="btn_do_login", use_container_width=True, type="primary"):
                do_login(panel, email_input, pass_input)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def build_sidebar():
    user = st.session_state.user
    role = user["role"]

    st.sidebar.markdown(f'<div style="padding:10px 0 16px;">{LOGO_SIDEBAR}</div>', unsafe_allow_html=True)
    badge_map = {"admin": "admin", "teacher": "teacher", "student": "student", "family": "family"}
    role_label = {"admin": "ADMIN", "teacher": "DOCENTE", "student": "ALUMNO", "family": "FAMILIA"}
    st.sidebar.markdown(f"""
    <div style="padding:8px 0 16px;">
      <span class="badge-{badge_map[role]}">{role_label[role]}</span>
      <h3 style="color:white;margin:8px 0 2px;font-size:15px;">{user['name']}</h3>
      <p style="color:rgba(255,255,255,0.45);font-size:11px;margin:0;">{user['email']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")

    menus = {
        "admin":   [("dashboard","🏠","Inicio"), ("colegios","🏛️","Gestión Colegios"), ("kyc","📋","Validación KYC"), ("auditoria","🔐","Auditoría")],
        "teacher": [("dashboard","🏠","Inicio"), ("aulas","🚪","Mis Aulas"), ("sociograma","🕸️","Sociograma"), ("contenido","📚","Contenido Guía"), ("alertas","📊","Alertas y Reportes")],
        "student": [("dashboard","🏠","Inicio"), ("encuesta","📝","Encuesta Sociométrica"), ("contenido_alu","🎒","Contenido para Vos")],
        "family":  [("dashboard","🏠","Inicio"), ("mi_alumno","👨‍👩‍👧","Mi Alumno"), ("recursos","🏠","Recursos para el Hogar")],
    }

    for view_id, icon, label in menus[role]:
        active = st.session_state.current_view == view_id
        bg = "background:rgba(77,184,160,0.18);border-radius:8px;" if active else ""
        st.sidebar.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:9px 10px;cursor:pointer;{bg}color:{'white' if active else 'rgba(255,255,255,0.65)'};font-size:14px;">
          <span>{icon}</span><span>{label}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.sidebar.button(label, key=f"nav_{view_id}", use_container_width=True):
            st.session_state.current_view = view_id
            st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión", key="logout", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# VIEWS — ADMIN
# ══════════════════════════════════════════════════════════════════════════════
def view_admin_dashboard():
    st.markdown("## 🏠 Panel de Administración")
    st.markdown("**ConVivir Backoffice** — Vista global de la plataforma")
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Colegios Activos", "4", "+1 este mes")
    c2.metric("Pendientes KYC", "2", "⚠️ Requieren revisión")
    c3.metric("Total Alumnos", "1.730", "+310 nuevos")
    c4.metric("Alertas Activas", "7", "3 de riesgo alto")
    st.markdown("---")
    st.markdown("### Actividad Reciente")
    actividad = [
        ("hace 10 min", "🟢", "Instituto Modelo Nacional completó el sociograma de 4ºA"),
        ("hace 1 hora", "🟡", "Escuela Normal Sup. Nº 1 envió documentación KYC incompleta"),
        ("hace 3 horas","🔴", "Alerta alta generada: Lucas Martínez (Instituto Modelo — 4ºA)"),
        ("hace 5 horas","🟢", "Colegio Los Álamos: 5ºB completó encuesta (28/28 alumnos)"),
        ("ayer",        "🔵", "Nueva inscripción: Escuela Normal Sup. Nº 1 (Tucumán)"),
    ]
    for tiempo, dot, texto in actividad:
        st.markdown(f"""
        <div class="card" style="display:flex;gap:14px;align-items:center;">
          <span style="font-size:20px;">{dot}</span>
          <div>
            <div style="font-size:13px;color:#222;">{texto}</div>
            <div style="font-size:11px;color:#aaa;">{tiempo}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

def view_admin_colegios():
    st.markdown("## 🏛️ Gestión de Colegios")
    st.markdown("Listado de instituciones registradas en la plataforma.")
    st.markdown("---")

    col_search, col_filter, col_btn = st.columns([3, 2, 1])
    with col_search:
        busqueda = st.text_input("🔍 Buscar institución...", placeholder="Nombre o ciudad")
    with col_filter:
        filtro = st.selectbox("Estado", ["Todos", "Activo", "Pendiente", "Suspendido"])
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("+ Nuevo Colegio", type="primary", use_container_width=True)

    st.markdown("---")

    colegios = MOCK_COLEGIOS
    if busqueda:
        colegios = [c for c in colegios if busqueda.lower() in c["nombre"].lower() or busqueda.lower() in c["ciudad"].lower()]
    if filtro != "Todos":
        colegios = [c for c in colegios if c["estado"] == filtro]

    # Header tabla
    h1, h2, h3, h4, h5, h6, h7 = st.columns([0.6, 3, 1.5, 1, 1, 1.2, 1])
    for col, label in zip([h1,h2,h3,h4,h5,h6,h7], ["ID","Institución","Ciudad","Alumnos","Docentes","Estado KYC","Acciones"]):
        col.markdown(f"<small style='color:#888;font-weight:700;text-transform:uppercase;font-size:10px;'>{label}</small>", unsafe_allow_html=True)

    st.markdown("<hr style='margin:4px 0 8px;'>", unsafe_allow_html=True)

    for c in colegios:
        kyc_badge = {
            "Aprobado": '<span class="kyc-aprobado">✓ Aprobado</span>',
            "En revisión": '<span class="kyc-revision">⏳ En revisión</span>',
            "Rechazado": '<span class="kyc-rechazado">✗ Rechazado</span>',
        }[c["kyc"]]
        col1, col2, col3, col4, col5, col6, col7 = st.columns([0.6, 3, 1.5, 1, 1, 1.2, 1])
        col1.markdown(f"<span style='font-size:11px;color:#888;'>{c['id']}</span>", unsafe_allow_html=True)
        col2.markdown(f"<span style='font-weight:600;font-size:14px;'>{c['nombre']}</span><br><span style='font-size:11px;color:#888;'>Alta: {c['fecha_alta']}</span>", unsafe_allow_html=True)
        col3.write(c["ciudad"])
        col4.write(str(c["alumnos"]))
        col5.write(str(c["docentes"]))
        col6.markdown(kyc_badge, unsafe_allow_html=True)
        with col7:
            if st.button("Ver", key=f"ver_col_{c['id']}"):
                st.toast(f"Abriendo {c['nombre']}...")
        st.markdown("<hr style='margin:4px 0;border-color:#f0f0f0;'>", unsafe_allow_html=True)

def view_admin_kyc():
    st.markdown("## 📋 Validación KYC")
    st.markdown("Revisión de documentación institucional para habilitar el acceso a la plataforma.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["⏳ Pendientes de revisión", "✅ Historial de validaciones"])

    with tab1:
        pendientes = [c for c in MOCK_COLEGIOS if c["kyc"] == "En revisión"]
        if not pendientes:
            st.info("No hay solicitudes pendientes en este momento.")
        for c in pendientes:
            with st.expander(f"📁 {c['nombre']} — {c['ciudad']} (ID: {c['id']})"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Datos de la institución**")
                    st.write(f"🏫 **Nombre:** {c['nombre']}")
                    st.write(f"📍 **Ciudad:** {c['ciudad']}")
                    st.write(f"👥 **Alumnos estimados:** {c['alumnos']}")
                    st.write(f"📅 **Fecha de solicitud:** {c['fecha_alta']}")
                with col_b:
                    st.markdown("**Documentación adjunta**")
                    st.markdown("""
                    - 📄 Estatuto institucional .pdf ✅
                    - 📄 CUIT/Personería jurídica .pdf ✅
                    - 📄 Nota de autorización directivo .pdf ✅
                    - 📄 Padrón de docentes .xlsx ⚠️ *Incompleto*
                    """)
                st.markdown("**Observaciones del revisor**")
                obs = st.text_area("Agregar observación...", key=f"obs_{c['id']}", height=80)
                ca, cb, cc = st.columns([1,1,2])
                with ca:
                    if st.button("✅ Aprobar", key=f"apro_{c['id']}", type="primary"):
                        st.success(f"✓ {c['nombre']} aprobado correctamente.")
                with cb:
                    if st.button("❌ Rechazar", key=f"rech_{c['id']}"):
                        st.error(f"✗ {c['nombre']} rechazado.")

    with tab2:
        aprobados = [c for c in MOCK_COLEGIOS if c["kyc"] in ["Aprobado", "Rechazado"]]
        for c in aprobados:
            icon = "✅" if c["kyc"] == "Aprobado" else "❌"
            col1, col2, col3, col4 = st.columns([3, 2, 1.5, 1])
            col1.write(f"{icon} **{c['nombre']}**")
            col2.write(c["ciudad"])
            col3.write(c["fecha_alta"])
            col4.write(c["kyc"])

def view_admin_auditoria():
    st.markdown("## 🔐 Log de Auditoría")
    st.markdown("Registro inmutable de acciones críticas en la plataforma.")
    st.markdown("---")
    logs = [
        {"ts":"2024-05-20 14:32:11","usuario":"admin@convivir.ar","accion":"KYC_APROBADO","entidad":"Instituto Modelo Nacional","ip":"200.45.12.88","nivel":"INFO"},
        {"ts":"2024-05-20 11:15:43","usuario":"docente@colegio.ar","accion":"SOCIOGRAMA_GENERADO","entidad":"Aula 4ºA","ip":"181.23.45.6","nivel":"INFO"},
        {"ts":"2024-05-20 09:02:55","usuario":"sistema","accion":"ALERTA_ALTA_GENERADA","entidad":"Lucas Martínez (4ºA)","ip":"—","nivel":"WARN"},
        {"ts":"2024-05-19 18:44:00","usuario":"admin@convivir.ar","accion":"KYC_RECHAZADO","entidad":"Bachillerato Popular del Sur","ip":"200.45.12.88","nivel":"WARN"},
        {"ts":"2024-05-19 10:30:22","usuario":"docente@colegio.ar","accion":"AULA_HABILITADA","entidad":"Aula 3ºC — código CV-3C-2024","ip":"181.23.45.6","nivel":"INFO"},
        {"ts":"2024-05-18 16:10:09","usuario":"alumno@colegio.ar","accion":"ENCUESTA_ENVIADA","entidad":"4ºA — Lucas Martínez","ip":"190.10.22.4","nivel":"INFO"},
        {"ts":"2024-05-18 08:05:33","usuario":"admin@convivir.ar","accion":"LOGIN_ADMIN","entidad":"Backoffice","ip":"200.45.12.88","nivel":"INFO"},
    ]
    nivel_col = {"INFO": "#1d7a55", "WARN": "#d4580a", "ERROR": "#c0392b"}

    h1,h2,h3,h4,h5,h6 = st.columns([2,2,2,2,1.5,0.8])
    for col, lbl in zip([h1,h2,h3,h4,h5,h6], ["Timestamp","Usuario","Acción","Entidad","IP","Nivel"]):
        col.markdown(f"<small style='color:#888;font-weight:700;text-transform:uppercase;font-size:10px;'>{lbl}</small>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:4px 0 6px;'>", unsafe_allow_html=True)

    for l in logs:
        c1,c2,c3,c4,c5,c6 = st.columns([2,2,2,2,1.5,0.8])
        c1.markdown(f"<code style='font-size:11px;'>{l['ts']}</code>", unsafe_allow_html=True)
        c2.markdown(f"<span style='font-size:12px;'>{l['usuario']}</span>", unsafe_allow_html=True)
        c3.markdown(f"<span style='font-size:12px;font-weight:600;'>{l['accion']}</span>", unsafe_allow_html=True)
        c4.markdown(f"<span style='font-size:12px;'>{l['entidad']}</span>", unsafe_allow_html=True)
        c5.markdown(f"<code style='font-size:11px;'>{l['ip']}</code>", unsafe_allow_html=True)
        c6.markdown(f"<span style='color:{nivel_col[l['nivel']]};font-weight:700;font-size:11px;'>{l['nivel']}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:3px 0;border-color:#f5f5f5;'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# VIEWS — TEACHER
# ══════════════════════════════════════════════════════════════════════════════
def view_teacher_dashboard():
    st.markdown("## 🏠 Bienvenida, Prof. García")
    st.markdown("**Instituto Modelo Nacional** — Panel del Docente")
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Aulas Activas", "3")
    c2.metric("Alumnos Totales", "90")
    c3.metric("Alertas Altas", "2", "🔴 Requieren atención")
    c4.metric("Encuestas Completas", "56/60")

    st.markdown("---")
    st.markdown("### 🔴 Alertas que requieren acción")
    st.markdown('<div class="alert-high"><b>RIESGO ALTO — 4ºA:</b> Lucas Martínez identificado como "Aislado extremo" (0 nominaciones recibidas, 4 rechazos). <b>Se recomienda intervención inmediata.</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-high"><b>RIESGO ALTO — 4ºA:</b> Valentina Torres identificada como posible "Objetivo de acoso" (5 rechazos recibidos). Revisar sociograma.</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-medium"><b>RIESGO MEDIO — 4ºA:</b> Mateo González en periferia del grupo. Monitorear evolución en el próximo período.</div>', unsafe_allow_html=True)
    st.markdown("### ✅ Estado de Aulas")
    for a in MOCK_AULAS:
        pct = int(a["respondieron"]/a["alumnos"]*100) if a["alumnos"] else 0
        col1, col2, col3 = st.columns([3,2,1])
        with col1:
            st.markdown(f"**{a['nombre']}** — Turno {a['turno']}")
            st.progress(pct/100, text=f"{a['respondieron']}/{a['alumnos']} alumnos respondieron ({pct}%)")
        with col2:
            if a["alertas_altas"] > 0:
                st.markdown(f"🔴 {a['alertas_altas']} alertas altas &nbsp; 🟠 {a['alertas_medias']} medias", unsafe_allow_html=True)
            else:
                st.markdown("🟢 Sin alertas críticas")
        with col3:
            st.markdown(f"<span class='kyc-{'aprobado' if a['estado']=='Completo' else 'revision' if a['estado']=='Activo' else 'rechazado'}'>{a['estado']}</span>", unsafe_allow_html=True)

def view_teacher_aulas():
    st.markdown("## 🚪 Mis Aulas")
    st.markdown("Gestión de aulas habilitadas para el sociograma.")
    st.markdown("---")

    col_a, col_b = st.columns([4,1])
    with col_b:
        if st.button("➕ Nueva Aula", type="primary", use_container_width=True):
            st.session_state["show_nueva_aula"] = True

    if st.session_state.get("show_nueva_aula"):
        with st.form("form_nueva_aula"):
            st.markdown("#### Crear nueva aula")
            na1, na2 = st.columns(2)
            with na1:
                n_anio = st.selectbox("Año", ["1º","2º","3º","4º","5º","6º"])
                n_div = st.selectbox("División", ["A","B","C","D"])
            with na2:
                n_turno = st.selectbox("Turno", ["Mañana","Tarde","Noche"])
                n_alumnos = st.number_input("Nº de alumnos", 10, 45, 30)
            submitted = st.form_submit_button("Crear Aula y Generar Código", type="primary")
            if submitted:
                import random, string
                codigo = f"CV-{n_anio[0]}{n_div}-{''.join(random.choices(string.digits,k=4))}"
                st.success(f"✅ Aula {n_anio} '{n_div}' creada. Código de acceso: **{codigo}**")
                st.session_state["show_nueva_aula"] = False

    for a in MOCK_AULAS:
        pct = int(a["respondieron"]/a["alumnos"]*100) if a["alumnos"] else 0
        estado_color = {"Activo":"#d4580a","Completo":"#1d7a55","Pendiente":"#888"}[a["estado"]]
        with st.expander(f"{a['nombre']} — {a['alumnos']} alumnos — Turno {a['turno']}", expanded=(a["id"]=="AU4A")):
            c1, c2, c3 = st.columns([2,2,1])
            with c1:
                st.markdown(f"**Código de acceso:** `{a['codigo']}`")
                st.markdown(f"**Habilitada:** {a['fecha']}")
                st.markdown(f"**Estado:** <span style='color:{estado_color};font-weight:700;'>{a['estado']}</span>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"**Participación:** {a['respondieron']}/{a['alumnos']} alumnos")
                st.progress(pct/100)
                if a["alertas_altas"] > 0:
                    st.markdown(f"🔴 **{a['alertas_altas']} alertas de riesgo alto**")
                if a["alertas_medias"] > 0:
                    st.markdown(f"🟠 {a['alertas_medias']} alertas de riesgo medio")
            with c3:
                st.button("Ver Sociograma", key=f"btn_socio_{a['id']}", use_container_width=True)
                st.button("📥 Descargar PDF", key=f"btn_pdf_{a['id']}", use_container_width=True)
                if a["estado"] == "Pendiente":
                    st.button("📤 Enviar Código", key=f"btn_env_{a['id']}", use_container_width=True)

def view_teacher_sociograma():
    st.markdown("## 🕸️ Sociograma — 4º Año 'A'")
    st.markdown("Mapa de relaciones interpersonales generado a partir de la encuesta sociométrica. 28/32 alumnos respondieron.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["📊 Tabla de resultados", "🗺️ Mapa de relaciones"])

    with tab1:
        st.markdown("### Índices sociométricos por alumno")
        st.markdown("""
        <style>
        .tbl-header { display:grid; grid-template-columns:2fr 1.2fr 1fr 1fr 1fr 1.2fr; gap:8px; padding:8px 12px; background:#f5f7fa; border-radius:8px; margin-bottom:6px; }
        .tbl-row    { display:grid; grid-template-columns:2fr 1.2fr 1fr 1fr 1fr 1.2fr; gap:8px; padding:10px 12px; border:1px solid #eaeaea; border-radius:8px; margin-bottom:4px; align-items:center; }
        .tbl-lbl    { font-size:10px; font-weight:700; text-transform:uppercase; color:#888; }
        </style>
        <div class="tbl-header">
          <div class="tbl-lbl">Alumno</div>
          <div class="tbl-lbl">Nivel de riesgo</div>
          <div class="tbl-lbl">Nom. recibidas</div>
          <div class="tbl-lbl">Nom. enviadas</div>
          <div class="tbl-lbl">Rechazos</div>
          <div class="tbl-lbl">Clasificación</div>
        </div>
        """, unsafe_allow_html=True)

        for a in MOCK_ALUMNOS_4A:
            riesgo_html = {
                "alto":  '<span class="riesgo-alto">🔴 Alto</span>',
                "medio": '<span class="riesgo-medio">🟠 Medio</span>',
                "bajo":  '<span class="riesgo-bajo">🟢 Bajo</span>',
            }[a["riesgo"]]
            st.markdown(f"""
            <div class="tbl-row">
              <div style="font-weight:600;">{a['nombre']}</div>
              <div>{riesgo_html}</div>
              <div style="text-align:center;">{a['nominaciones_rec']}</div>
              <div style="text-align:center;">{a['nominaciones_env']}</div>
              <div style="text-align:center;color:#c0392b;font-weight:{'700' if a['rechazos']>2 else '400'};">{a['rechazos']}</div>
              <div style="font-size:12px;color:#555;">{a['tipo']}</div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Visualización del grafo de relaciones")
        st.info("💡 Los nodos de color rojo indican alumnos en riesgo alto. El tamaño del nodo representa el número de nominaciones recibidas.")

        # SVG Sociograma estático representativo
        svg_socio = """
        <svg viewBox="0 0 700 460" xmlns="http://www.w3.org/2000/svg" style="width:100%;background:#fafbfc;border-radius:16px;border:1px solid #eaeaea;">
          <!-- Conexiones positivas -->
          <line x1="350" y1="230" x2="200" y2="130" stroke="#4db8a0" stroke-width="2" opacity="0.5"/>
          <line x1="350" y1="230" x2="480" y2="140" stroke="#4db8a0" stroke-width="2" opacity="0.5"/>
          <line x1="350" y1="230" x2="500" y2="300" stroke="#4db8a0" stroke-width="2" opacity="0.5"/>
          <line x1="350" y1="230" x2="260" y2="340" stroke="#4db8a0" stroke-width="2" opacity="0.5"/>
          <line x1="200" y1="130" x2="480" y2="140" stroke="#4db8a0" stroke-width="1.5" opacity="0.35"/>
          <line x1="480" y1="140" x2="500" y2="300" stroke="#4db8a0" stroke-width="1.5" opacity="0.35"/>
          <line x1="200" y1="130" x2="260" y2="340" stroke="#4db8a0" stroke-width="1.5" opacity="0.35"/>
          <line x1="500" y1="300" x2="400" y2="390" stroke="#4db8a0" stroke-width="1.5" opacity="0.35"/>
          <line x1="260" y1="340" x2="400" y2="390" stroke="#4db8a0" stroke-width="1.5" opacity="0.35"/>
          <!-- Conexiones de riesgo hacia aislados -->
          <line x1="100" y1="260" x2="200" y2="130" stroke="#e8621a" stroke-width="1" stroke-dasharray="5,4" opacity="0.4"/>
          <line x1="100" y1="260" x2="350" y2="230" stroke="#e8621a" stroke-width="1" stroke-dasharray="5,4" opacity="0.3"/>
          <line x1="590" y1="360" x2="500" y2="300" stroke="#e8621a" stroke-width="1" stroke-dasharray="5,4" opacity="0.4"/>
          <!-- Rechazo -->
          <line x1="100" y1="380" x2="200" y2="130" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.3"/>
          <line x1="100" y1="380" x2="350" y2="230" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.3"/>
          <line x1="100" y1="380" x2="480" y2="140" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.2"/>
          <!-- Nodo líder: Benjamín López -->
          <circle cx="350" cy="230" r="28" fill="#1d7a55" opacity="0.9"/>
          <text x="350" y="234" text-anchor="middle" fill="white" font-size="10" font-weight="700">Benjamín</text>
          <text x="350" y="246" text-anchor="middle" fill="rgba(255,255,255,0.7)" font-size="8">8 nom.</text>
          <!-- Nodo integrado: Sofía -->
          <circle cx="200" cy="130" r="22" fill="#4db8a0" opacity="0.85"/>
          <text x="200" y="134" text-anchor="middle" fill="white" font-size="9" font-weight="700">Sofía</text>
          <text x="200" y="146" text-anchor="middle" fill="rgba(255,255,255,0.7)" font-size="8">5 nom.</text>
          <!-- Nodo integrado: Camila -->
          <circle cx="480" cy="140" r="20" fill="#4db8a0" opacity="0.8"/>
          <text x="480" y="144" text-anchor="middle" fill="white" font-size="9">Camila</text>
          <!-- Nodo integrado: Mia -->
          <circle cx="500" cy="300" r="21" fill="#4db8a0" opacity="0.8"/>
          <text x="500" y="304" text-anchor="middle" fill="white" font-size="9">Mia</text>
          <!-- Nodo integrado: Isabella -->
          <circle cx="260" cy="340" r="20" fill="#4db8a0" opacity="0.8"/>
          <text x="260" y="344" text-anchor="middle" fill="white" font-size="9">Isabella</text>
          <!-- Nodo integrado periférico -->
          <circle cx="400" cy="390" r="17" fill="#7ecdb8" opacity="0.7"/>
          <text x="400" y="394" text-anchor="middle" fill="white" font-size="8">Mateo</text>
          <!-- Nodo aislado: Lucas (RIESGO ALTO) -->
          <circle cx="100" cy="380" r="18" fill="#c0392b" opacity="0.9"/>
          <circle cx="100" cy="380" r="25" fill="none" stroke="#c0392b" stroke-width="2" stroke-dasharray="4,3" opacity="0.5"/>
          <text x="100" y="376" text-anchor="middle" fill="white" font-size="9" font-weight="700">Lucas</text>
          <text x="100" y="388" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="7">⚠ Aislado</text>
          <!-- Nodo objetivo acoso: Valentina (RIESGO ALTO) -->
          <circle cx="100" cy="260" r="18" fill="#c0392b" opacity="0.85"/>
          <circle cx="100" cy="260" r="25" fill="none" stroke="#c0392b" stroke-width="2" stroke-dasharray="4,3" opacity="0.45"/>
          <text x="100" y="256" text-anchor="middle" fill="white" font-size="9" font-weight="700">Vale</text>
          <text x="100" y="268" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="7">⚠ Acoso</text>
          <!-- Nodo periferia: Joaquín (RIESGO MEDIO) -->
          <circle cx="590" cy="360" r="16" fill="#e8621a" opacity="0.8"/>
          <text x="590" y="358" text-anchor="middle" fill="white" font-size="8">Joaquín</text>
          <text x="590" y="369" text-anchor="middle" fill="rgba(255,255,255,0.7)" font-size="7">Periferia</text>
          <!-- Nodo periferia: Thiago -->
          <circle cx="600" cy="200" r="15" fill="#e8621a" opacity="0.7"/>
          <text x="600" y="204" text-anchor="middle" fill="white" font-size="8">Thiago</text>
          <!-- Leyenda -->
          <rect x="14" y="14" width="180" height="108" rx="10" fill="white" opacity="0.9" stroke="#eaeaea"/>
          <text x="26" y="34" font-size="10" font-weight="700" fill="#333">Leyenda</text>
          <circle cx="34" cy="50" r="7" fill="#1d7a55"/><text x="48" y="54" font-size="9" fill="#555">Líder positivo</text>
          <circle cx="34" cy="68" r="7" fill="#4db8a0"/><text x="48" y="72" font-size="9" fill="#555">Integrado</text>
          <circle cx="34" cy="86" r="7" fill="#e8621a"/><text x="48" y="90" font-size="9" fill="#555">En periferia (riesgo medio)</text>
          <circle cx="34" cy="104" r="7" fill="#c0392b"/><text x="48" y="108" font-size="9" fill="#555">Aislado / Acoso (riesgo alto)</text>
        </svg>
        """
        st.markdown(svg_socio, unsafe_allow_html=True)

def view_teacher_contenido():
    st.markdown("## 📚 Contenido para Docentes")
    st.markdown("Recursos y guías para la intervención en situaciones de convivencia.")
    st.markdown("---")

    tipo_filter = st.selectbox("Filtrar por tipo", ["Todos","Guía práctica","Protocolo","Actividad","Marco legal"])
    st.markdown("---")

    for item in MOCK_CONTENIDO_DOCENTE:
        if tipo_filter != "Todos" and item["tipo"] != tipo_filter:
            continue
        nivel_badge = {"Esencial":"<span class='tag-esencial'>★ Esencial</span>","Avanzado":"<span class='tag-avanzado'>⬆ Avanzado</span>","Referencia":"<span class='tag-ref'>📖 Referencia</span>"}[item["nivel"]]
        col1, col2, col3 = st.columns([4,1,1])
        with col1:
            st.markdown(f"""
            <div class="card">
              <div style="display:flex;gap:10px;align-items:center;margin-bottom:8px;">
                {nivel_badge}
                <span class="tag-guia">{item['tipo']}</span>
                <span style="font-size:11px;color:#aaa;">⏱ {item['tiempo']}</span>
              </div>
              <div style="font-weight:600;font-size:15px;color:#1a2e2a;">{item['titulo']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("Ver recurso", key=f"ver_doc_{item['titulo'][:15]}", use_container_width=True)
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("📥 Descargar", key=f"dl_doc_{item['titulo'][:15]}", use_container_width=True)

def view_teacher_alertas():
    st.markdown("## 📊 Alertas y Reportes")
    st.markdown("Panel de seguimiento y generación de documentación.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["🔔 Alertas activas", "📄 Reportes generados"])

    with tab1:
        alertas = [
            {"nivel":"alto","aula":"4ºA","alumno":"Lucas Martínez","motivo":"Aislado extremo: 0 nom. recibidas, 4 rechazos","fecha":"20/05/2024","accion":"Llamar a la familia, reunión individual"},
            {"nivel":"alto","aula":"4ºA","alumno":"Valentina Torres","motivo":"Posible objetivo de acoso: 5 rechazos en grupo","fecha":"20/05/2024","accion":"Observar dinámica, intervenir en actividad grupal"},
            {"nivel":"medio","aula":"4ºA","alumno":"Mateo González","motivo":"En periferia del grupo, 2 rechazos","fecha":"20/05/2024","accion":"Monitorear en próximo período"},
            {"nivel":"medio","aula":"4ºA","alumno":"Joaquín Herrera","motivo":"Pocas nominaciones recibidas, en periferia","fecha":"20/05/2024","accion":"Integrar en actividades grupales"},
        ]
        for al in alertas:
            css_class = f"alert-{al['nivel']}"
            icon = "🔴" if al["nivel"] == "alto" else "🟠"
            st.markdown(f"""
            <div class="{css_class}" style="margin-bottom:12px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-weight:700;">{icon} {al['alumno']} — {al['aula']}</span>
                <span style="font-size:11px;color:#888;">{al['fecha']}</span>
              </div>
              <div style="font-size:13px;margin:6px 0 4px;"><b>Motivo:</b> {al['motivo']}</div>
              <div style="font-size:12px;"><b>Acción sugerida:</b> {al['accion']}</div>
            </div>
            """, unsafe_allow_html=True)
            if al["nivel"] == "alto":
                c1, c2, c3 = st.columns([2,2,4])
                c1.button("✅ Marcar gestionada", key=f"al_gest_{al['alumno'][:8]}")
                c2.button("📝 Agregar nota", key=f"al_nota_{al['alumno'][:8]}")

    with tab2:
        reportes = [
            {"nombre":"Sociograma 4ºA — Mayo 2024","tipo":"Sociograma completo","fecha":"20/05/2024","estado":"Generado"},
            {"nombre":"Reporte de Alerta — Lucas Martínez","tipo":"Reporte individual","fecha":"20/05/2024","estado":"Generado"},
            {"nombre":"Sociograma 5ºB — Mayo 2024","tipo":"Sociograma completo","fecha":"19/05/2024","estado":"Generado"},
            {"nombre":"Resumen mensual — Abril 2024","tipo":"Reporte mensual","fecha":"30/04/2024","estado":"Archivado"},
        ]
        for r in reportes:
            col1, col2, col3 = st.columns([3,2,1])
            col1.markdown(f"**{r['nombre']}**<br><span style='font-size:11px;color:#888;'>{r['tipo']} · {r['fecha']}</span>", unsafe_allow_html=True)
            col2.write(r["estado"])
            col3.button("📥 PDF", key=f"rep_dl_{r['nombre'][:12]}", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# VIEWS — STUDENT
# ══════════════════════════════════════════════════════════════════════════════
def view_student_dashboard():
    st.markdown("## 🏠 Hola, Lucas 👋")
    st.markdown("Bienvenido a tu espacio en ConVivir. Aquí podés completar tu encuesta y acceder a contenido útil.")
    st.markdown("---")

    if not st.session_state.get("encuesta_enviada"):
        st.markdown("""
        <div class="alert-medium" style="font-size:15px;">
          📝 <b>Tenés una encuesta pendiente</b> — Tu docente habilitó la encuesta sociométrica del aula.<br>
          <span style="font-size:13px;">Tus respuestas son <b>100% confidenciales</b>. Ningún compañero puede verlas.</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Completar encuesta ahora →", type="primary"):
            st.session_state.current_view = "encuesta"
            st.rerun()
    else:
        st.markdown('<div class="alert-low">✅ <b>Encuesta completada.</b> ¡Gracias por participar!</div>', unsafe_allow_html=True)

    st.markdown("### 📚 Contenido recomendado para vos")
    contenido = [
        {"titulo":"¿Qué es el bullying y cómo reconocerlo?","emoji":"🎓","tiempo":"5 min"},
        {"titulo":"¿A quién puedo pedir ayuda si algo me pasa?","emoji":"🤝","tiempo":"4 min"},
        {"titulo":"Mis derechos en la escuela","emoji":"⚖️","tiempo":"6 min"},
    ]
    cols = st.columns(3)
    for i, item in enumerate(contenido):
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:24px 16px;">
              <div style="font-size:36px;margin-bottom:10px;">{item['emoji']}</div>
              <div style="font-weight:600;font-size:14px;color:#1a2e2a;margin-bottom:8px;">{item['titulo']}</div>
              <div style="font-size:11px;color:#aaa;">⏱ {item['tiempo']}</div>
            </div>
            """, unsafe_allow_html=True)

def view_student_encuesta():
    st.markdown("## 📝 Encuesta Sociométrica")
    st.markdown("""
    <div style="background:#f0faf7;border:1px solid #4db8a0;border-radius:12px;padding:14px 18px;margin-bottom:20px;">
      🔒 <b>Tus respuestas son completamente confidenciales.</b> Ningún compañero ni compañera puede ver lo que elegiste. Solo tu docente accede a resultados agrupados del aula.
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("encuesta_enviada"):
        st.markdown('<div class="alert-low" style="font-size:15px;padding:20px;">✅ <b>¡Encuesta enviada correctamente!</b><br>Gracias por participar. Tus respuestas ya fueron registradas.</div>', unsafe_allow_html=True)
        st.balloons()
        return

    paso = st.session_state.get("encuesta_paso", 0)
    resp = st.session_state.get("encuesta_respuestas", {})

    preguntas = [
        {"id":"q1","titulo":"¿Con quién preferirías hacer un trabajo en equipo?","sub":"Elegí hasta 3 compañeros","tipo":"multi","max":3},
        {"id":"q2","titulo":"¿Con quién preferirías NO hacer un trabajo en equipo?","sub":"Esta pregunta es opcional. Elegí hasta 2 compañeros.","tipo":"multi","max":2,"opcional":True},
        {"id":"q3","titulo":"¿Con quién pasás más tiempo en el recreo?","sub":"Elegí hasta 3 compañeros","tipo":"multi","max":3},
        {"id":"q4","titulo":"Si necesitás ayuda con algo difícil, ¿a quién le pedís?","sub":"Elegí hasta 2 compañeros","tipo":"multi","max":2},
        {"id":"q5","titulo":"¿Alguna vez sentiste que algún compañero te trató mal?","sub":"Tu respuesta es confidencial.","tipo":"single","opciones":["No, nunca","A veces sí","Sí, con frecuencia","Prefiero no responder"]},
        {"id":"q6","titulo":"¿Cómo te sentís en el grupo en general?","sub":"Elegí la opción que mejor te represente","tipo":"single","opciones":["Muy bien, me llevo bien con todos","Bien, tengo mis amigos","Regular, a veces me siento solo/a","Mal, me cuesta integrarme","Prefiero no responder"]},
    ]

    total = len(preguntas)
    st.progress((paso)/total, text=f"Pregunta {min(paso+1,total)} de {total}")
    st.markdown("---")

    if paso < total:
        preg = preguntas[paso]
        st.markdown(f"### {preg['titulo']}")
        st.markdown(f"<span style='color:#888;font-size:13px;'>{preg['sub']}</span>", unsafe_allow_html=True)
        st.markdown("")

        if preg["tipo"] == "multi":
            sel = st.multiselect(
                "Seleccioná tus opciones:",
                MOCK_ALUMNO_COMPAS,
                default=resp.get(preg["id"], []),
                max_selections=preg["max"],
                key=f"enc_{preg['id']}"
            )
        else:
            sel = st.radio(
                "Elegí una opción:",
                preg["opciones"],
                index=preg["opciones"].index(resp[preg["id"]]) if preg["id"] in resp else 0,
                key=f"enc_{preg['id']}"
            )

        st.markdown("---")
        c1, c2, _ = st.columns([1, 1, 3])
        with c1:
            if paso > 0:
                if st.button("← Anterior"):
                    resp[preg["id"]] = sel
                    st.session_state.encuesta_respuestas = resp
                    st.session_state.encuesta_paso = paso - 1
                    st.rerun()
        with c2:
            opcional = preg.get("opcional", False)
            btn_label = "Siguiente →" if paso < total - 1 else "Enviar encuesta ✓"
            if st.button(btn_label, type="primary"):
                if not opcional and (not sel or sel == []):
                    st.warning("Por favor respondé esta pregunta antes de continuar.")
                else:
                    resp[preg["id"]] = sel
                    st.session_state.encuesta_respuestas = resp
                    if paso < total - 1:
                        st.session_state.encuesta_paso = paso + 1
                    else:
                        st.session_state.encuesta_enviada = True
                    st.rerun()
    else:
        st.session_state.encuesta_enviada = True
        st.rerun()

def view_student_contenido():
    st.markdown("## 🎒 Contenido para Vos")
    st.markdown("Recursos pensados especialmente para estudiantes.")
    st.markdown("---")

    contenido_alu = [
        {"titulo":"¿Qué es el bullying y cómo reconocerlo?","emoji":"🎓","tiempo":"5 min","desc":"Entendé qué es el acoso escolar, cuáles son sus formas y cómo identificarlo."},
        {"titulo":"¿A quién puedo pedir ayuda si algo me pasa?","emoji":"🤝","tiempo":"4 min","desc":"Conocé los adultos de confianza en tu escuela y cómo acercarte a ellos."},
        {"titulo":"Mis derechos en la escuela","emoji":"⚖️","tiempo":"6 min","desc":"Todos los estudiantes tienen derechos. Conocelos y aprendé a defenderlos."},
        {"titulo":"¿Cómo ayudar a un compañero que está siendo acosado?","emoji":"💪","tiempo":"7 min","desc":"Ser testigo y actuar bien puede hacer una gran diferencia."},
        {"titulo":"Emociones difíciles: cómo manejar la bronca y la tristeza","emoji":"😌","tiempo":"8 min","desc":"Herramientas simples para entender y manejar lo que sentís."},
        {"titulo":"El ciberbullying: qué hacer si te pasa online","emoji":"💻","tiempo":"6 min","desc":"Guía clara sobre el acoso en redes sociales y cómo protegerte."},
    ]

    col1, col2 = st.columns(2)
    for i, item in enumerate(contenido_alu):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="card">
              <div style="display:flex;gap:14px;align-items:flex-start;">
                <span style="font-size:32px;">{item['emoji']}</span>
                <div>
                  <div style="font-weight:700;font-size:14px;color:#1a2e2a;margin-bottom:4px;">{item['titulo']}</div>
                  <div style="font-size:12px;color:#888;margin-bottom:8px;">{item['desc']}</div>
                  <span style="font-size:11px;color:#aaa;">⏱ {item['tiempo']}</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# VIEWS — FAMILY
# ══════════════════════════════════════════════════════════════════════════════
def view_family_dashboard():
    st.markdown("## 🏠 Bienvenido, Carlos 👋")
    st.markdown("Panel familiar — Lucas Martínez · 4º Año 'A' · Instituto Modelo Nacional")
    st.markdown("---")

    st.markdown("""
    <div class="alert-high" style="font-size:14px;margin-bottom:20px;">
      ⚠️ <b>Su hijo/a fue identificado en una situación de riesgo.</b><br>
      El equipo docente ya fue notificado y tomará contacto pronto. Te recomendamos leer los recursos de la sección "Recursos para el Hogar".
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Aula vinculada", "4º 'A'")
    c2.metric("Estado encuesta", "Completada ✅")
    c3.metric("Notificaciones", "1 nueva")

    st.markdown("---")
    st.markdown("### 📋 Perfil de Lucas")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        - **Nombre:** Lucas Martínez
        - **Año/División:** 4º Año 'A'
        - **Institución:** Instituto Modelo Nacional
        - **Turno:** Mañana
        """)
    with col_b:
        st.markdown("""
        - **Código de aula:** CV-4A-2024
        - **Encuesta sociométrica:** ✅ Completada
        - **Alertas activas:** 🔴 1 alerta de riesgo alto
        - **Docente a cargo:** Prof. María García
        """)

    st.markdown("---")
    st.markdown("### 📚 Recursos recomendados para tu situación")
    recursos_destacados = [
        {"titulo":"¿Cómo hablar con tu hijo/a sobre lo que le pasa en la escuela?","emoji":"💬","tiempo":"8 min"},
        {"titulo":"Señales de alerta que no debés ignorar","emoji":"🔍","tiempo":"6 min"},
        {"titulo":"Cuándo y cómo comunicarte con la escuela","emoji":"🏫","tiempo":"5 min"},
    ]
    cols = st.columns(3)
    for i, r in enumerate(recursos_destacados):
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:20px 14px;">
              <div style="font-size:32px;margin-bottom:10px;">{r['emoji']}</div>
              <div style="font-weight:600;font-size:13px;color:#1a2e2a;margin-bottom:8px;">{r['titulo']}</div>
              <div style="font-size:11px;color:#aaa;">⏱ {r['tiempo']}</div>
            </div>
            """, unsafe_allow_html=True)

def view_family_mi_alumno():
    st.markdown("## 👨‍👩‍👧 Mi Alumno — Lucas Martínez")
    st.markdown("Información de seguimiento y vínculo familiar.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["📋 Datos del alumno", "🔔 Notificaciones"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### Datos personales")
            st.text_input("Nombre completo", value="Lucas Martínez", disabled=True)
            st.text_input("Institución", value="Instituto Modelo Nacional", disabled=True)
            st.text_input("Año / División", value="4º Año 'A' — Turno Mañana", disabled=True)
            st.text_input("Docente", value="Prof. María García", disabled=True)
        with col_b:
            st.markdown("#### Vínculo familiar")
            st.text_input("Tu nombre", value="Carlos Martínez")
            st.selectbox("Relación con el alumno", ["Padre/Madre","Tutor Legal","Abuelo/a","Otro familiar"])
            st.text_input("Email de contacto", value="carlos@email.com")
            st.text_input("Teléfono", value="011-4444-5555")
        st.markdown("---")
        st.markdown("#### Estado en la plataforma")
        col1, col2 = st.columns(2)
        col1.metric("Encuesta sociométrica", "✅ Completada")
        col2.metric("Alertas activas", "1 — Riesgo alto 🔴")

    with tab2:
        notificaciones = [
            {"fecha":"20/05/2024","tipo":"Alerta","mensaje":"Tu hijo/a fue identificado como alumno en riesgo en el aula 4ºA. El docente fue notificado y tomará contacto.", "nivel":"alto"},
            {"fecha":"15/05/2024","tipo":"Encuesta","mensaje":"Lucas completó la encuesta sociométrica del aula 4ºA.", "nivel":"info"},
            {"fecha":"10/03/2024","tipo":"Registro","mensaje":"Lucas fue registrado exitosamente en el aula 4ºA con el código CV-4A-2024.", "nivel":"info"},
        ]
        for n in notificaciones:
            css = "alert-high" if n["nivel"]=="alto" else "alert-low"
            st.markdown(f"""
            <div class="{css}">
              <div style="display:flex;justify-content:space-between;">
                <span style="font-weight:700;">{n['tipo']}</span>
                <span style="font-size:11px;color:#888;">{n['fecha']}</span>
              </div>
              <div style="font-size:13px;margin-top:4px;">{n['mensaje']}</div>
            </div>
            """, unsafe_allow_html=True)

def view_family_recursos():
    st.markdown("## 🏠 Recursos para el Hogar")
    st.markdown("Guías y materiales para acompañar a tu hijo/a desde casa.")
    st.markdown("---")

    tipo_filter = st.selectbox("Filtrar por tipo", ["Todos","Guía","Actividad","Protocolo"])
    st.markdown("---")

    for item in MOCK_CONTENIDO_FAMILIA:
        if tipo_filter != "Todos" and item["tipo"] != tipo_filter:
            continue
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div class="card">
              <div style="display:flex;gap:10px;align-items:center;margin-bottom:8px;">
                <span class="tag-guia">{item['tipo']}</span>
                <span style="font-size:11px;color:#aaa;">⏱ {item['tiempo']}</span>
              </div>
              <div style="font-weight:600;font-size:15px;color:#1a2e2a;">{item['titulo']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("Ver recurso", key=f"fam_{item['titulo'][:15]}", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def route_view():
    role = st.session_state.user["role"]
    view = st.session_state.current_view

    routes = {
        "admin": {
            "dashboard": view_admin_dashboard,
            "colegios":  view_admin_colegios,
            "kyc":       view_admin_kyc,
            "auditoria": view_admin_auditoria,
        },
        "teacher": {
            "dashboard": view_teacher_dashboard,
            "aulas":     view_teacher_aulas,
            "sociograma":view_teacher_sociograma,
            "contenido": view_teacher_contenido,
            "alertas":   view_teacher_alertas,
        },
        "student": {
            "dashboard":    view_student_dashboard,
            "encuesta":     view_student_encuesta,
            "contenido_alu":view_student_contenido,
        },
        "family": {
            "dashboard": view_family_dashboard,
            "mi_alumno": view_family_mi_alumno,
            "recursos":  view_family_recursos,
        },
    }

    view_fn = routes.get(role, {}).get(view)
    if view_fn:
        view_fn()
    else:
        st.warning(f"Vista '{view}' no encontrada para el rol '{role}'.")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.logged_in:
    build_sidebar()
    route_view()
else:
    show_login()
