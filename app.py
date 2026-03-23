import streamlit as st

st.set_page_config(
    page_title="ConVivir — Animar Infancias & Educación",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# PALETA ANIMAR
# teal:   #4db8a0  (color principal)
# teal2:  #2a9a82  (hover)
# orange: #e8621a  (acento)
# dark:   #1a2e2a  (textos oscuros / sidebar)
# cream:  #f5f0eb  (fondo interior)
# cream2: #ede8e0  (fondo alterno)
# ══════════════════════════════════════════════════════════════════════════════

# ── Estilos globales (pantallas internas post-login) ──────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* Sidebar */
[data-testid="stSidebar"] { background-color: #1a2e2a !important; }
[data-testid="stSidebar"] * { color: white !important; font-family:'DM Sans',sans-serif !important; }
[data-testid="stSidebar"] hr { border-color: rgba(77,184,160,0.3) !important; }
[data-testid="stSidebar"] .stButton > button {
    background: rgba(77,184,160,0.15) !important;
    border: 1px solid rgba(77,184,160,0.25) !important;
    color: white !important;
    border-radius: 8px !important;
    font-family:'DM Sans',sans-serif !important;
    font-weight: 500 !important;
    transition: all .15s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(77,184,160,0.35) !important;
    border-color: #4db8a0 !important;
}

/* Fondo interior */
.main, .block-container { background: #f5f0eb !important; }
.main .block-container { padding-top: 2rem; }

/* Tipografía */
h1 { font-family:'Sora',sans-serif !important; color:#1a2e2a !important; font-weight:800 !important; letter-spacing:-0.5px !important; }
h2 { font-family:'Sora',sans-serif !important; color:#1a2e2a !important; font-weight:700 !important; letter-spacing:-0.3px !important; }
h3 { font-family:'Sora',sans-serif !important; color:#2a9a82 !important; font-weight:700 !important; }
p, li, label { font-family:'DM Sans',sans-serif !important; }

/* Botones primarios */
.stButton > button[kind="primary"] {
    background: #4db8a0 !important;
    border: none !important;
    font-family:'Sora',sans-serif !important;
    font-weight:700 !important;
    border-radius: 8px !important;
    letter-spacing: 0.2px !important;
}
.stButton > button[kind="primary"]:hover { background: #2a9a82 !important; }

/* Badges */
.badge-admin   { background:#d4ede8; color:#1a6b5a; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; }
.badge-teacher { background:#d4ede8; color:#1a6b5a; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; }
.badge-student { background:#fde8d0; color:#c0511a; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; }

/* Alertas */
.alert-high   { background:#fdeaea; border-left:4px solid #c0392b; border-radius:8px; padding:12px 16px; margin:8px 0; }
.alert-medium { background:#fef0e6; border-left:4px solid #e8621a; border-radius:8px; padding:12px 16px; margin:8px 0; }
.alert-low    { background:#d4ede8; border-left:4px solid #4db8a0; border-radius:8px; padding:12px 16px; margin:8px 0; }

/* Métricas */
[data-testid="stMetric"] { background:white; border-radius:12px; padding:14px 18px; border:1px solid #e0d8d0; }
[data-testid="stMetricLabel"] { color:#6b5e52 !important; font-family:'DM Sans',sans-serif !important; }
[data-testid="stMetricValue"] { color:#1a2e2a !important; font-family:'Sora',sans-serif !important; font-weight:800 !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LOGOS EN SVG — Paleta Animar (teal + orange)
# ══════════════════════════════════════════════════════════════════════════════

# Logo navbar (fondo teal, figura blanca)
LOGO_NAV = (
    '<svg width="36" height="36" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="100" height="100" rx="14" fill="#4db8a0"/>'
    '<path d="M10,94 L36,18 L50,18 L50,94 Z" fill="#1a2e2a" opacity="0.9"/>'
    '<path d="M90,94 L64,18 L50,18 L50,94 Z" fill="#1a2e2a" opacity="0.9"/>'
    '<circle cx="50" cy="42" r="10" fill="white"/>'
    '<path d="M50,52 Q34,44 26,30" stroke="white" stroke-width="8" stroke-linecap="round" fill="none"/>'
    '<path d="M50,52 Q66,44 74,30" stroke="white" stroke-width="8" stroke-linecap="round" fill="none"/>'
    '<line x1="50" y1="52" x2="50" y2="72" stroke="white" stroke-width="8" stroke-linecap="round"/>'
    '<line x1="50" y1="72" x2="41" y2="88" stroke="white" stroke-width="7" stroke-linecap="round"/>'
    '<line x1="50" y1="72" x2="59" y2="88" stroke="white" stroke-width="7" stroke-linecap="round"/>'
    '<rect x="44" y="14" width="12" height="8" rx="2" fill="#e8621a"/>'
    '</svg>'
)

# Logo hero grande con gradiente teal
LOGO_HERO = (
    '<svg width="140" height="140" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">'
    '<defs>'
    '<linearGradient id="hg2" x1="0%" y1="0%" x2="100%" y2="100%">'
    '<stop offset="0%" stop-color="#4db8a0"/>'
    '<stop offset="100%" stop-color="#1a6b5a"/>'
    '</linearGradient>'
    '<filter id="gl2"><feGaussianBlur stdDeviation="4" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    '</defs>'
    '<rect width="200" height="200" rx="32" fill="url(#hg2)"/>'
    '<path d="M14,190 L58,24 L100,24 L100,190 Z" fill="#1a2e2a" opacity="0.75"/>'
    '<path d="M186,190 L142,24 L100,24 L100,190 Z" fill="#1a2e2a" opacity="0.75"/>'
    '<circle cx="100" cy="82" r="20" fill="white" filter="url(#gl2)"/>'
    '<path d="M100,102 Q75,90 56,64" stroke="white" stroke-width="15" stroke-linecap="round" fill="none" filter="url(#gl2)"/>'
    '<path d="M100,102 Q125,90 144,64" stroke="white" stroke-width="15" stroke-linecap="round" fill="none" filter="url(#gl2)"/>'
    '<line x1="100" y1="102" x2="100" y2="146" stroke="white" stroke-width="15" stroke-linecap="round" filter="url(#gl2)"/>'
    '<line x1="100" y1="146" x2="82" y2="178" stroke="white" stroke-width="13" stroke-linecap="round" filter="url(#gl2)"/>'
    '<line x1="100" y1="146" x2="118" y2="178" stroke="white" stroke-width="13" stroke-linecap="round" filter="url(#gl2)"/>'
    '<rect x="88" y="18" width="24" height="14" rx="4" fill="#e8621a"/>'
    '</svg>'
)

# Logo módulo M3 (sociograma)
LOGO_MOD = (
    '<svg width="42" height="42" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="100" height="100" rx="18" fill="rgba(77,184,160,0.15)"/>'
    '<path d="M12,92 L36,20 L50,20 L50,92 Z" fill="#4db8a0" opacity="0.8"/>'
    '<path d="M88,92 L64,20 L50,20 L50,92 Z" fill="#4db8a0" opacity="0.8"/>'
    '<circle cx="50" cy="44" r="9" fill="#1a2e2a"/>'
    '<path d="M50,53 Q39,47 32,36" stroke="#1a2e2a" stroke-width="6" stroke-linecap="round" fill="none"/>'
    '<path d="M50,53 Q61,47 68,36" stroke="#1a2e2a" stroke-width="6" stroke-linecap="round" fill="none"/>'
    '<line x1="50" y1="53" x2="50" y2="70" stroke="#1a2e2a" stroke-width="6" stroke-linecap="round"/>'
    '<line x1="50" y1="70" x2="43" y2="83" stroke="#1a2e2a" stroke-width="5" stroke-linecap="round"/>'
    '<line x1="50" y1="70" x2="57" y2="83" stroke="#1a2e2a" stroke-width="5" stroke-linecap="round"/>'
    '<rect x="44" y="14" width="12" height="8" rx="2" fill="#e8621a"/>'
    '</svg>'
)

# Logo sidebar (sobre fondo oscuro — figura en teal)
LOGO_SIDEBAR = (
    '<svg width="32" height="32" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="100" height="100" rx="14" fill="#4db8a0"/>'
    '<path d="M10,94 L36,18 L50,18 L50,94 Z" fill="#1a2e2a" opacity="0.85"/>'
    '<path d="M90,94 L64,18 L50,18 L50,94 Z" fill="#1a2e2a" opacity="0.85"/>'
    '<circle cx="50" cy="42" r="10" fill="white"/>'
    '<path d="M50,52 Q34,44 26,30" stroke="white" stroke-width="8" stroke-linecap="round" fill="none"/>'
    '<path d="M50,52 Q66,44 74,30" stroke="white" stroke-width="8" stroke-linecap="round" fill="none"/>'
    '<line x1="50" y1="52" x2="50" y2="72" stroke="white" stroke-width="8" stroke-linecap="round"/>'
    '<line x1="50" y1="72" x2="41" y2="88" stroke="white" stroke-width="7" stroke-linecap="round"/>'
    '<line x1="50" y1="72" x2="59" y2="88" stroke="white" stroke-width="7" stroke-linecap="round"/>'
    '<rect x="44" y="14" width="12" height="8" rx="2" fill="#e8621a"/>'
    '</svg>'
)

# ── Datos de usuarios ─────────────────────────────────────────────────────────
USERS = {
    "admin@convivir.ar":  {"password": "admin123",   "role": "admin",   "name": "Administrador"},
    "docente@colegio.ar": {"password": "docente123", "role": "teacher", "name": "Prof. María García"},
    "alumno@colegio.ar":  {"password": "alumno123",  "role": "student", "name": "Lucas Martínez"},
}

# ── Estado de sesión ──────────────────────────────────────────────────────────
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user"      not in st.session_state: st.session_state.user      = None

# ══════════════════════════════════════════════════════════════════════════════
# CSS LANDING — Identidad Animar
# Fondo oscuro con acento teal y naranja, tipografía Sora bold
# ══════════════════════════════════════════════════════════════════════════════
LANDING_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500&display=swap');

.block-container { padding:0!important; max-width:100%!important; }
header[data-testid="stHeader"] { display:none; }
[data-testid="stSidebar"]      { display:none; }

/* ── BASE ── */
.cv {
    font-family:'DM Sans',sans-serif;
    background:#0e1c19;
    color:#dde8e4;
    min-height:100vh;
}

/* ── NAV ── */
.cv-nav {
    position:fixed; top:0; left:0; right:0; z-index:100;
    display:flex; align-items:center; justify-content:space-between;
    padding:0 52px; height:66px;
    background:rgba(14,28,25,0.92);
    backdrop-filter:blur(20px);
    border-bottom:1px solid rgba(77,184,160,0.15);
}
.cv-logo { display:flex; align-items:center; gap:11px; }
.cv-logo-txt {
    font-family:'Sora',sans-serif; font-size:20px; font-weight:800;
    color:#fff; letter-spacing:-0.4px;
}
.cv-logo-txt em { font-style:normal; color:#4db8a0; }
.cv-logo-sub {
    font-size:9px; font-weight:600; letter-spacing:2.5px;
    text-transform:uppercase; color:rgba(221,232,228,0.35);
    display:block; margin-top:1px;
}
.cv-nav-links {
    display:flex; gap:34px; font-size:13px; font-weight:500;
    color:rgba(221,232,228,0.4);
}

/* ── HERO ── */
.cv-hero {
    min-height:100vh; display:flex; flex-direction:column; justify-content:center;
    padding:120px 52px 80px; position:relative; overflow:hidden;
    background:
        radial-gradient(ellipse 90% 65% at 50% -5%, rgba(77,184,160,0.18) 0%, transparent 65%),
        radial-gradient(ellipse 45% 45% at 87% 38%, rgba(232,98,26,0.07) 0%, transparent 55%),
        #0e1c19;
}
.cv-hero::before {
    content:''; position:absolute; inset:0;
    background-image:
        linear-gradient(rgba(77,184,160,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(77,184,160,0.04) 1px, transparent 1px);
    background-size:60px 60px;
    mask-image:radial-gradient(ellipse 80% 55% at 50% 0%, black, transparent 72%);
}
.cv-hero-inner {
    display:grid; grid-template-columns:1fr auto; gap:72px;
    align-items:center; max-width:1200px; position:relative; z-index:1;
}
.cv-tag {
    display:inline-flex; align-items:center; gap:7px;
    background:rgba(77,184,160,0.12); border:1px solid rgba(77,184,160,0.3);
    border-radius:100px; padding:5px 16px;
    font-size:10px; font-weight:700; letter-spacing:2.5px;
    text-transform:uppercase; color:#4db8a0; margin-bottom:22px;
}
.cv-hero h1 {
    font-family:'Sora',sans-serif;
    font-size:clamp(38px,5vw,68px); font-weight:800;
    line-height:1.06; letter-spacing:-2.5px; color:#fff; margin-bottom:20px;
}
.cv-hero h1 em { font-style:normal; color:#4db8a0; }
.cv-hero h1 strong { color:#e8621a; font-style:normal; }
.cv-hero-sub {
    font-size:16.5px; font-weight:300; line-height:1.75;
    color:rgba(221,232,228,0.55); max-width:510px;
}

/* Logo hero — anillos animados */
.cv-logo-hero {
    position:relative; width:220px; height:220px;
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
}
.cv-logo-ring1 {
    position:absolute; inset:0; border-radius:50%;
    border:1px solid rgba(77,184,160,0.18);
    animation:spin1 22s linear infinite;
}
.cv-logo-ring1::after {
    content:''; position:absolute; top:-6px; left:50%; transform:translateX(-50%);
    width:12px; height:12px; border-radius:50%; background:#4db8a0;
    box-shadow:0 0 16px 4px rgba(77,184,160,0.6);
}
.cv-logo-ring2 {
    position:absolute; inset:24px; border-radius:50%;
    border:1px dashed rgba(232,98,26,0.12);
    animation:spin1 35s linear infinite reverse;
}
.cv-logo-ring2::after {
    content:''; position:absolute; bottom:-5px; left:50%; transform:translateX(-50%);
    width:8px; height:8px; border-radius:50%; background:#e8621a;
    box-shadow:0 0 10px 3px rgba(232,98,26,0.5);
}
@keyframes spin1 { to { transform:rotate(360deg); } }
.cv-logo-glow {
    position:absolute; inset:-30px; border-radius:50%;
    background:radial-gradient(circle, rgba(77,184,160,0.14) 0%, transparent 68%);
    animation:pulse1 4s ease-in-out infinite;
}
@keyframes pulse1 { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(1.1)} }

/* Stats */
.cv-stats {
    display:flex; gap:0; margin-top:56px; padding-top:40px;
    border-top:1px solid rgba(77,184,160,0.12); position:relative; z-index:1;
}
.cv-stat { flex:1; padding-right:36px; margin-right:36px; border-right:1px solid rgba(77,184,160,0.08); }
.cv-stat:last-child { border-right:none; padding-right:0; margin-right:0; }
.cv-stat-n { font-family:'Sora',sans-serif; font-size:36px; font-weight:800; letter-spacing:-2px; line-height:1; color:#fff; margin-bottom:5px; }
.cv-stat-n b { color:#4db8a0; }
.cv-stat-l { font-size:12px; color:rgba(221,232,228,0.36); line-height:1.55; }

/* ── SECCIONES ── */
.cv-s  { padding:84px 52px; }
.cv-sa { padding:84px 52px; background:rgba(77,184,160,0.04); border-top:1px solid rgba(77,184,160,0.08); border-bottom:1px solid rgba(77,184,160,0.08); }
.cv-eyebrow { font-size:10px; font-weight:700; letter-spacing:3px; text-transform:uppercase; color:#4db8a0; margin-bottom:14px; }
.cv-s h2, .cv-sa h2 { font-family:'Sora',sans-serif; font-size:clamp(24px,2.7vw,40px); font-weight:800; letter-spacing:-1px; color:#fff; line-height:1.1; margin-bottom:12px; }
.cv-intro { font-size:16px; color:rgba(221,232,228,0.48); max-width:560px; line-height:1.72; margin-bottom:48px; }

/* Problema cards */
.pg { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.pc { background:rgba(255,255,255,0.03); border:1px solid rgba(77,184,160,0.1); border-radius:18px; padding:28px; transition:all .2s; }
.pc:hover { border-color:rgba(77,184,160,0.35); background:rgba(77,184,160,0.06); transform:translateY(-3px); }
.pc-icon { font-size:26px; margin-bottom:14px; }
.pc h3 { font-family:'Sora',sans-serif; font-size:15px; font-weight:700; color:#fff; margin-bottom:10px; }
.pc p  { font-size:13px; color:rgba(221,232,228,0.46); line-height:1.65; }
.pc-stat { font-family:'Sora',sans-serif; font-size:30px; font-weight:800; color:#e8621a; margin-top:18px; letter-spacing:-1px; }
.pc-sub  { font-size:10.5px; color:rgba(221,232,228,0.28); margin-top:3px; }

/* Módulos */
.mg { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; }
.mc { background:rgba(255,255,255,0.025); border:1px solid rgba(77,184,160,0.09); border-radius:16px; padding:22px 14px 18px; text-align:center; transition:all .2s; }
.mc:hover { background:rgba(77,184,160,0.08); border-color:rgba(77,184,160,0.35); transform:translateY(-5px); box-shadow:0 12px 30px rgba(77,184,160,0.12); }
.mc-icon { font-size:26px; margin-bottom:8px; }
.mc-logo { width:42px; height:42px; margin:0 auto 8px; display:flex; align-items:center; justify-content:center; }
.mc-id   { font-family:'Sora',monospace; font-size:9px; color:#4db8a0; font-weight:700; letter-spacing:1.5px; margin-bottom:5px; }
.mc-name { font-family:'Sora',sans-serif; font-size:12px; font-weight:700; color:#fff; line-height:1.3; margin-bottom:6px; }
.mc-desc { font-size:10.5px; color:rgba(221,232,228,0.36); line-height:1.55; }

/* Actores */
.ag { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }
.ac { border-radius:18px; padding:26px 20px; border:1px solid transparent; transition:transform .2s; }
.ac:hover { transform:translateY(-4px); }
.ac-adm { background:linear-gradient(145deg,rgba(77,184,160,.18),rgba(77,184,160,.04)); border-color:rgba(77,184,160,.3); }
.ac-tch { background:linear-gradient(145deg,rgba(77,184,160,.18),rgba(77,184,160,.04)); border-color:rgba(77,184,160,.3); }
.ac-stu { background:linear-gradient(145deg,rgba(232,98,26,.18),rgba(232,98,26,.04)); border-color:rgba(232,98,26,.3); }
.ac-fam { background:linear-gradient(145deg,rgba(232,98,26,.12),rgba(232,98,26,.03)); border-color:rgba(232,98,26,.25); }
.ac-emoji { font-size:30px; margin-bottom:12px; display:block; }
.ac-badge { display:inline-block; padding:3px 12px; border-radius:100px; font-size:9px; font-weight:700; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:9px; }
.ab-a { background:rgba(77,184,160,.25); color:#7ad4c0; }
.ab-t { background:rgba(77,184,160,.25); color:#7ad4c0; }
.ab-s { background:rgba(232,98,26,.25); color:#f4a070; }
.ab-f { background:rgba(232,98,26,.18); color:#f4a070; }
.ac-name { font-family:'Sora',sans-serif; font-size:14px; font-weight:700; color:#fff; margin-bottom:8px; }
.ac-desc { font-size:12.5px; color:rgba(221,232,228,0.46); line-height:1.65; }

/* Flujo */
.fg { display:flex; gap:0; position:relative; margin-top:44px; }
.fg::before { content:''; position:absolute; top:26px; left:26px; right:26px; height:2px; background:linear-gradient(90deg,#4db8a0,rgba(77,184,160,.1)); }
.fs { flex:1; text-align:center; padding:0 10px; }
.fs-n { width:52px; height:52px; border-radius:50%; margin:0 auto 12px; background:#0e1c19; border:2px solid #4db8a0; display:flex; align-items:center; justify-content:center; font-family:'Sora',sans-serif; font-size:16px; font-weight:800; color:#4db8a0; position:relative; z-index:1; }
.fs-t { font-family:'Sora',sans-serif; font-size:12px; font-weight:700; color:#fff; margin-bottom:5px; }
.fs-d { font-size:11px; color:rgba(221,232,228,0.36); line-height:1.6; }

/* Privacidad */
.priv-g { display:grid; grid-template-columns:1fr 1fr; gap:13px; }
.priv-i { display:flex; gap:14px; align-items:flex-start; background:rgba(255,255,255,0.025); border:1px solid rgba(77,184,160,0.09); border-radius:14px; padding:20px; }
.priv-ico { font-size:20px; flex-shrink:0; margin-top:1px; }
.priv-t { font-family:'Sora',sans-serif; font-size:13.5px; font-weight:700; color:#fff; margin-bottom:4px; }
.priv-d { font-size:12px; color:rgba(221,232,228,0.42); line-height:1.6; }

/* Roadmap */
.rm-g { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }
.rm-p { border-radius:16px; padding:26px 22px; background:rgba(255,255,255,0.025); border:1px solid rgba(77,184,160,0.09); position:relative; overflow:hidden; }
.rm-p::before { content:''; position:absolute; top:0; left:0; right:0; height:4px; }
.r1::before { background:#4db8a0; }
.r2::before { background:#3aaa90; }
.r3::before { background:#e8621a; }
.r4::before { background:#c04e10; }
.rm-tag { font-size:9px; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:9px; }
.r1 .rm-tag, .r2 .rm-tag { color:#4db8a0; }
.r3 .rm-tag, .r4 .rm-tag { color:#e8621a; }
.rm-title { font-family:'Sora',sans-serif; font-size:15px; font-weight:700; color:#fff; margin-bottom:13px; }
.rm-p ul { list-style:none; }
.rm-p ul li { font-size:12px; color:rgba(221,232,228,0.48); padding:5px 0; border-bottom:1px solid rgba(77,184,160,0.07); line-height:1.5; }
.rm-p ul li::before { content:'→ '; color:rgba(77,184,160,0.5); }

/* CTA */
.cv-cta {
    padding:88px 52px; text-align:center;
    background:radial-gradient(ellipse 55% 70% at 50% 50%, rgba(77,184,160,0.1) 0%, transparent 65%);
}
.cv-cta h2 { font-family:'Sora',sans-serif; font-size:44px; font-weight:800; letter-spacing:-2px; color:#fff; margin-bottom:14px; }
.cv-cta p { font-size:17px; color:rgba(221,232,228,0.42); }

/* Footer */
.cv-ft {
    padding:24px 52px;
    border-top:1px solid rgba(77,184,160,0.1);
    display:flex; justify-content:space-between; align-items:center;
    font-size:11.5px; color:rgba(221,232,228,0.22);
}
.cv-ft-logo { display:flex; align-items:center; gap:8px; }

/* Login panel cards */
.pcard-wrap {
    border-radius:16px; padding:24px 14px 20px;
    border:1px solid rgba(77,184,160,0.2);
    background:rgba(77,184,160,0.05);
    text-align:center; margin-bottom:4px;
    transition: all .2s;
}
.pcard-ico  { font-size:38px; margin-bottom:10px; }
.pcard-nm   { font-family:'Sora',sans-serif; font-size:14px; font-weight:700; color:#1a2e2a; margin-bottom:4px; }
.pcard-ds   { font-size:11px; color:#5c7a72; line-height:1.5; }
.panel-hd   { font-family:'Sora',sans-serif; font-size:19px; font-weight:800; color:#1a2e2a; letter-spacing:-0.4px; margin-bottom:4px; margin-top:12px; }
.panel-sb   { font-size:12.5px; color:#6b8a82; margin-bottom:20px; }
</style>
"""

# ── HTML Landing ──────────────────────────────────────────────────────────────
LANDING_HTML_1 = """
<div class="cv">
  <nav class="cv-nav">
    <div class="cv-logo">
"""
LANDING_HTML_2 = """
      <div>
        <span class="cv-logo-txt">Con<em>Vivir</em></span>
        <span class="cv-logo-sub">Animar · Infancias &amp; Educación</span>
      </div>
    </div>
    <div class="cv-nav-links">
      <span>El problema</span><span>Solución</span><span>Actores</span><span>Roadmap</span>
    </div>
  </nav>

  <section class="cv-hero">
    <div class="cv-hero-inner">
      <div>
        <div class="cv-tag">Plataforma de Convivencia Escolar</div>
        <h1>Prevención del bullying<br><em>basada en datos</em><br>para colegios</h1>
        <p class="cv-hero-sub">ConVivir combina sociogramas de aula, contenido educativo y gestión institucional para que docentes detecten situaciones de acoso antes de que escalen.</p>
      </div>
      <div class="cv-logo-hero">
        <div class="cv-logo-glow"></div>
        <div class="cv-logo-ring1"></div>
        <div class="cv-logo-ring2"></div>
"""
LANDING_HTML_3 = """
      </div>
    </div>
    <div class="cv-stats">
      <div class="cv-stat"><div class="cv-stat-n">1 de 3<b>.</b></div><div class="cv-stat-l">alumnos vive o presencia<br>situaciones de bullying</div></div>
      <div class="cv-stat"><div class="cv-stat-n">24<b>+</b></div><div class="cv-stat-l">pantallas y flujos<br>diseñados en el MVP</div></div>
      <div class="cv-stat"><div class="cv-stat-n">5<b>.</b></div><div class="cv-stat-l">módulos integrados:<br>Admin · Aulas · Sociograma · Contenido · Reportes</div></div>
      <div class="cv-stat"><div class="cv-stat-n">4<b>.</b></div><div class="cv-stat-l">actores del sistema con<br>flujos completamente diferenciados</div></div>
    </div>
  </section>

  <section class="cv-s">
    <div class="cv-eyebrow">El Problema</div>
    <h2>El bullying existe.<br>El problema es que no lo vemos.</h2>
    <p class="cv-intro">Sin herramientas adecuadas, los docentes actúan cuando el daño ya ocurrió. La dinámica social del aula es invisible hasta que se vuelve urgente.</p>
    <div class="pg">
      <div class="pc"><div class="pc-icon">👁️</div><h3>Sin visibilidad de la dinámica grupal</h3><p>Los docentes no tienen forma objetiva de ver quién está aislado, quién domina y quién está en riesgo dentro del aula.</p><div class="pc-stat">70%</div><div class="pc-sub">de casos no son reportados al docente</div></div>
      <div class="pc"><div class="pc-icon">⏱️</div><h3>Intervención tardía</h3><p>Cuando el problema se hace visible, ya generó daño psicológico, social y académico en el alumno afectado.</p><div class="pc-stat">6 meses</div><div class="pc-sub">tiempo promedio antes de una intervención</div></div>
      <div class="pc"><div class="pc-icon">🧩</div><h3>Herramientas fragmentadas</h3><p>No existe una plataforma que integre diagnóstico, contenido y seguimiento en un solo lugar seguro.</p><div class="pc-stat">0</div><div class="pc-sub">plataformas integrales disponibles en Argentina</div></div>
    </div>
  </section>

  <section class="cv-sa">
    <div class="cv-eyebrow">La Solución</div>
    <h2>5 módulos. Un ecosistema completo.</h2>
    <p class="cv-intro">Cada módulo cubre una parte del ciclo: gestión institucional → diagnóstico → acción → seguimiento.</p>
    <div class="mg">
      <div class="mc"><div class="mc-icon">🏛️</div><div class="mc-id">M1</div><div class="mc-name">Backoffice Admin</div><div class="mc-desc">Alta de colegios, KYC y auditoría</div></div>
      <div class="mc"><div class="mc-icon">🚪</div><div class="mc-id">M2</div><div class="mc-name">Gestión de Aulas</div><div class="mc-desc">Creación y habilitación con código de acceso</div></div>
      <div class="mc"><div class="mc-logo">
"""
LANDING_HTML_4 = """
      </div><div class="mc-id">M3</div><div class="mc-name">Sociograma</div><div class="mc-desc">Encuesta confidencial y mapa de relaciones</div></div>
      <div class="mc"><div class="mc-icon">📚</div><div class="mc-id">M4</div><div class="mc-name">Contenido</div><div class="mc-desc">Guías adaptadas al rol del usuario</div></div>
      <div class="mc"><div class="mc-icon">📊</div><div class="mc-id">M5</div><div class="mc-name">Reportes</div><div class="mc-desc">Alertas automáticas y PDF descargables</div></div>
    </div>
  </section>

  <section class="cv-s">
    <div class="cv-eyebrow">Actores del Sistema</div>
    <h2>Cuatro roles. Flujos completamente diferenciados.</h2>
    <p class="cv-intro">Cada usuario accede únicamente a lo que necesita y está autorizado a ver.</p>
    <div class="ag">
      <div class="ac ac-adm"><span class="ac-emoji">🏛️</span><div><span class="ac-badge ab-a">Administrador</span></div><div class="ac-name">Backoffice Admin</div><p class="ac-desc">Gestiona colegios, valida docentes mediante KYC y controla el acceso al ecosistema.</p></div>
      <div class="ac ac-tch"><span class="ac-emoji">👨‍🏫</span><div><span class="ac-badge ab-t">Docente</span></div><div class="ac-name">Docente Validado</div><p class="ac-desc">Habilita aulas, visualiza el sociograma, gestiona alertas y descarga reportes completos.</p></div>
      <div class="ac ac-stu"><span class="ac-emoji">🎒</span><div><span class="ac-badge ab-s">Alumno</span></div><div class="ac-name">Alumno Registrado</div><p class="ac-desc">Completa la encuesta de forma confidencial y accede a contenido adaptado a su edad.</p></div>
      <div class="ac ac-fam"><span class="ac-emoji">👨‍👩‍👧</span><div><span class="ac-badge ab-f">Familia</span></div><div class="ac-name">Familia / Tutor</div><p class="ac-desc">Se vincula al alumno y accede a recursos orientados a prevención en el hogar.</p></div>
    </div>
  </section>

  <section class="cv-sa">
    <div class="cv-eyebrow">Cómo Funciona</div>
    <h2>Del registro al diagnóstico en 6 pasos.</h2>
    <p class="cv-intro">El flujo principal del docente, desde el alta institucional hasta la intervención sobre una alerta.</p>
    <div class="fg">
      <div class="fs"><div class="fs-n">1</div><div class="fs-t">Alta institucional</div><div class="fs-d">El colegio se registra y pasa el proceso KYC</div></div>
      <div class="fs"><div class="fs-n">2</div><div class="fs-t">Habilitación del aula</div><div class="fs-d">El docente crea el aula y comparte el código</div></div>
      <div class="fs"><div class="fs-n">3</div><div class="fs-t">Encuesta sociométrica</div><div class="fs-d">Los alumnos responden de forma confidencial</div></div>
      <div class="fs"><div class="fs-n">4</div><div class="fs-t">Sociograma generado</div><div class="fs-d">El sistema genera el mapa de relaciones</div></div>
      <div class="fs"><div class="fs-n">5</div><div class="fs-t">Alerta automática</div><div class="fs-d">El docente es notificado si hay alumno en riesgo</div></div>
      <div class="fs"><div class="fs-n">6</div><div class="fs-t">Intervención y reporte</div><div class="fs-d">El docente actúa y descarga el reporte PDF</div></div>
    </div>
  </section>

  <section class="cv-s">
    <div class="cv-eyebrow">Privacidad y Seguridad</div>
    <h2>Los datos de los menores son intocables.</h2>
    <p class="cv-intro">El diseño garantiza por arquitectura que ningún alumno pueda ver las respuestas de otro.</p>
    <div class="priv-g">
      <div class="priv-i"><div class="priv-ico">🔒</div><div><div class="priv-t">Respuestas 100% confidenciales</div><div class="priv-d">Ningún compañero puede ver las elecciones de otro. Solo el docente accede a resultados agregados.</div></div></div>
      <div class="priv-i"><div class="priv-ico">🛡️</div><div><div class="priv-t">Cumplimiento Ley 25.326</div><div class="priv-d">Protección de Datos Personales de Argentina. Consentimiento digital de tutores para datos de menores.</div></div></div>
      <div class="priv-i"><div class="priv-ico">🔑</div><div><div class="priv-t">Autenticación robusta</div><div class="priv-d">JWT con refresh tokens. 2FA obligatorio para el Admin. Roles validados en cada endpoint.</div></div></div>
      <div class="priv-i"><div class="priv-ico">📋</div><div><div class="priv-t">Auditoría inmutable</div><div class="priv-d">Log de acciones críticas: KYC, habilitación de aulas y acceso a datos sensibles.</div></div></div>
    </div>
  </section>

  <section class="cv-sa">
    <div class="cv-eyebrow">Roadmap de Desarrollo</div>
    <h2>MVP funcional. Evolución controlada.</h2>
    <p class="cv-intro">Cuatro fases que permiten lanzar rápido e incorporar complejidad de forma progresiva.</p>
    <div class="rm-g">
      <div class="rm-p r1"><div class="rm-tag">Fase 1 — MVP</div><div class="rm-title">Institucional + Registro</div><ul><li>Alta de colegios y docentes</li><li>KYC básico con aprobación manual</li><li>Registro de alumnos con código</li><li>Login seguro y gestión de roles</li></ul></div>
      <div class="rm-p r2"><div class="rm-tag">Fase 2 — Core</div><div class="rm-title">Sociograma + Contenido</div><ul><li>Encuesta sociométrica completa</li><li>Algoritmo de procesamiento</li><li>Mapa de red visual</li><li>Módulo de contenido inicial</li></ul></div>
      <div class="rm-p r3"><div class="rm-tag">Fase 3 — Reportes</div><div class="rm-title">Alertas + PDF</div><ul><li>Dashboard del docente</li><li>Alertas automáticas por riesgo</li><li>Reporte PDF descargable</li><li>Encuesta para familias</li></ul></div>
      <div class="rm-p r4"><div class="rm-tag">Fase 4 — Evolución</div><div class="rm-title">Features Avanzados</div><ul><li>Sociograma histórico evolutivo</li><li>Integración con orientación</li><li>App móvil nativa</li><li>Gamificación para alumnos</li></ul></div>
    </div>
  </section>

  <section class="cv-cta">
    <h2>¿Tu colegio quiere sumarse?</h2>
    <p>Ingresá con tu cuenta para acceder a la plataforma o contactanos para comenzar.</p>
  </section>

  <footer class="cv-ft">
    <div class="cv-ft-logo">
"""
LANDING_HTML_5 = """
      <span>© 2025 ConVivir — <strong>Animar</strong> Infancias &amp; Educación</span>
    </div>
    <span>animar.escolar@gmail.com · @animar.escolar</span>
  </footer>
</div>
"""

# ── Login ─────────────────────────────────────────────────────────────────────
def login_as(role, name, email):
    st.session_state.logged_in    = True
    st.session_state.show_login   = False
    st.session_state.show_colegio = False
    st.session_state.user = {"email": email, "role": role, "name": name}
    st.rerun()

def show_login():
    if "show_login"   not in st.session_state: st.session_state.show_login   = False
    if "show_colegio" not in st.session_state: st.session_state.show_colegio = False

    full_html = (
        LANDING_CSS
        + LANDING_HTML_1 + LOGO_NAV
        + LANDING_HTML_2 + LOGO_HERO
        + LANDING_HTML_3 + LOGO_MOD
        + LANDING_HTML_4 + LOGO_NAV
        + LANDING_HTML_5
    )
    st.markdown(full_html, unsafe_allow_html=True)

    # Botón "Ingresar →" fijo arriba a la derecha
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div:first-child {
        position:fixed; top:13px; right:52px; z-index:200;
    }
    /* Botón Ingresar con color Animar */
    div[data-testid="stVerticalBlock"] > div:first-child .stButton > button {
        background: #4db8a0 !important;
        border: none !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 8px 22px !important;
        font-size: 14px !important;
    }
    div[data-testid="stVerticalBlock"] > div:first-child .stButton > button:hover {
        background: #2a9a82 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col_btn = st.columns([12, 1])
    with col_btn:
        if st.button("Ingresar →", type="primary", key="open_login"):
            st.session_state.show_login   = True
            st.session_state.show_colegio = False
            st.rerun()

    if not st.session_state.show_login:
        return

    # Panel de login centrado (sin overlay oscuro)
    _, col_mid, _ = st.columns([1, 1.6, 1])
    with col_mid:
        with st.container(border=True):
            # Logo + nombre
            st.markdown(
                "<div style='display:flex;align-items:center;gap:10px;margin-bottom:4px;'>"
                + LOGO_NAV
                + "<div><span style='font-family:Sora,sans-serif;font-size:17px;font-weight:800;"
                  "color:#1a2e2a;'>Con<span style='color:#4db8a0;'>Vivir</span></span>"
                  "<span style='display:block;font-size:9px;font-weight:600;letter-spacing:2px;"
                  "text-transform:uppercase;color:#8aaa9a;'>Animar · Infancias &amp; Educación</span></div>"
                  "</div>",
                unsafe_allow_html=True
            )

            if not st.session_state.show_colegio:
                st.markdown(
                    "<div class='panel-hd'>¿Cómo querés ingresar?</div>"
                    "<div class='panel-sb'>Seleccioná tu perfil para entrar directo</div>",
                    unsafe_allow_html=True
                )
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(
                        "<div class='pcard-wrap'><div class='pcard-ico'>🏛️</div>"
                        "<div class='pcard-nm'>Administrador</div>"
                        "<div class='pcard-ds'>Gestión de colegios,<br>docentes y KYC</div></div>",
                        unsafe_allow_html=True
                    )
                    if st.button("Entrar como Admin", key="go_admin", use_container_width=True, type="primary"):
                        login_as("admin", "Administrador", "admin@convivir.ar")
                with col_b:
                    st.markdown(
                        "<div class='pcard-wrap'><div class='pcard-ico'>🏫</div>"
                        "<div class='pcard-nm'>Colegio</div>"
                        "<div class='pcard-ds'>Docentes, familias<br>y alumnos</div></div>",
                        unsafe_allow_html=True
                    )
                    if st.button("Entrar a Colegio →", key="go_colegio", use_container_width=True):
                        st.session_state.show_colegio = True
                        st.rerun()
                st.markdown("---")
                if st.button("← Cerrar", key="cancel_login", use_container_width=True):
                    st.session_state.show_login = False
                    st.rerun()

            else:
                st.markdown(
                    "<div class='panel-hd'>Colegio</div>"
                    "<div class='panel-sb'>¿Con qué perfil ingresás?</div>",
                    unsafe_allow_html=True
                )
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(
                        "<div class='pcard-wrap'><div class='pcard-ico'>👨‍🏫</div>"
                        "<div class='pcard-nm'>Docente</div>"
                        "<div class='pcard-ds'>Sociograma, alertas<br>y reportes</div></div>",
                        unsafe_allow_html=True
                    )
                    if st.button("Soy Docente", key="go_teacher", use_container_width=True, type="primary"):
                        login_as("teacher", "Prof. María García", "docente@colegio.ar")
                with c2:
                    st.markdown(
                        "<div class='pcard-wrap'><div class='pcard-ico'>👨‍👩‍👧</div>"
                        "<div class='pcard-nm'>Familia</div>"
                        "<div class='pcard-ds'>Contenido y<br>seguimiento</div></div>",
                        unsafe_allow_html=True
                    )
                    if st.button("Soy Familia", key="go_family", use_container_width=True, type="primary"):
                        login_as("student", "Carlos Martínez (Padre)", "familia@colegio.ar")
                with c3:
                    st.markdown(
                        "<div class='pcard-wrap'><div class='pcard-ico'>🎒</div>"
                        "<div class='pcard-nm'>Alumno</div>"
                        "<div class='pcard-ds'>Encuesta y<br>contenido</div></div>",
                        unsafe_allow_html=True
                    )
                    if st.button("Soy Alumno", key="go_student", use_container_width=True, type="primary"):
                        login_as("student", "Lucas Martínez", "alumno@colegio.ar")
                st.markdown("---")
                if st.button("← Volver", key="back_colegio", use_container_width=True):
                    st.session_state.show_colegio = False
                    st.rerun()

# ── Sidebar ───────────────────────────────────────────────────────────────────
def show_sidebar():
    user = st.session_state.user
    role = user["role"]

    with st.sidebar:
        st.markdown(
            "<div style='display:flex;align-items:center;gap:10px;padding:8px 0 6px;'>"
            + LOGO_SIDEBAR
            + "<div><span style='font-size:17px;font-weight:800;color:white;letter-spacing:-0.4px;"
              "font-family:Sora,sans-serif;'>ConVivir</span>"
              "<span style='display:block;font-size:8px;font-weight:600;letter-spacing:2px;"
              "text-transform:uppercase;color:rgba(77,184,160,0.6);margin-top:1px;'>Animar · Infancias &amp; Educación</span>"
              "</div></div>",
            unsafe_allow_html=True
        )
        st.markdown("---")
        st.markdown("👤 **" + user["name"] + "**")
        badge  = {"admin":"badge-admin","teacher":"badge-teacher","student":"badge-student"}[role]
        labels = {"admin":"Administrador","teacher":"Docente","student":"Alumno"}
        st.markdown("<span class='" + badge + "'>" + labels[role] + "</span>", unsafe_allow_html=True)
        st.markdown("---")

        if role == "admin":
            pages = {
                "🏛️ Dashboard Admin": "admin_dashboard",
                "🏫 Colegios":         "admin_colegios",
                "👨‍🏫 Docentes":        "admin_docentes",
                "✅ KYC / Validaciones":"admin_kyc",
            }
        elif role == "teacher":
            pages = {
                "📊 Mi Dashboard":       "teacher_dashboard",
                "🚪 Gestión de Aulas":   "teacher_aulas",
                "🕸️ Sociograma":         "teacher_sociograma",
                "🚨 Alertas":            "teacher_alertas",
                "📋 Reportes":           "teacher_reportes",
            }
        else:
            pages = {
                "🏠 Inicio":              "student_home",
                "📝 Encuesta Sociométrica":"student_encuesta",
                "📚 Contenido Educativo": "student_contenido",
            }

        if "current_page" not in st.session_state:
            st.session_state.current_page = list(pages.values())[0]

        for label, key in pages.items():
            if st.button(label, key="nav_" + key, use_container_width=True):
                st.session_state.current_page = key
                st.rerun()

        st.markdown("---")
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state.logged_in    = False
            st.session_state.user         = None
            st.session_state.current_page = None
            st.rerun()

# ── Router ────────────────────────────────────────────────────────────────────
def route():
    page = st.session_state.get("current_page", "")
    role = st.session_state.user["role"]

    if page == "admin_dashboard" or (role == "admin" and not page):
        from views import admin_dashboard; admin_dashboard.render()
    elif page == "admin_colegios":
        from views import admin_colegios; admin_colegios.render()
    elif page == "admin_docentes":
        from views import admin_docentes; admin_docentes.render()
    elif page == "admin_kyc":
        from views import admin_kyc; admin_kyc.render()
    elif page == "teacher_dashboard" or (role == "teacher" and not page):
        from views import teacher_dashboard; teacher_dashboard.render()
    elif page == "teacher_aulas":
        from views import teacher_aulas; teacher_aulas.render()
    elif page == "teacher_sociograma":
        from views import teacher_sociograma; teacher_sociograma.render()
    elif page == "teacher_alertas":
        from views import teacher_alertas; teacher_alertas.render()
    elif page == "teacher_reportes":
        from views import teacher_reportes; teacher_reportes.render()
    elif page == "student_home" or (role == "student" and not page):
        from views import student_home; student_home.render()
    elif page == "student_encuesta":
        from views import student_encuesta; student_encuesta.render()
    elif page == "student_contenido":
        from views import student_contenido; student_contenido.render()

# ── Main ──────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    show_login()
else:
    show_sidebar()
    route()
