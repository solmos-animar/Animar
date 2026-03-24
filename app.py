st.set_page_config(

    page_title="ConVivir — Plataforma de Convivencia Escolar",

    page_icon="🕸️",

    layout="wide",

    initial_sidebar_state="expanded",

)



# ── Estilos globales (pantallas internas post-login) ──────────────────────────

st.markdown("""

<style>

  [data-testid="stSidebar"] { background-color: #1a2e2a; }

  [data-testid="stSidebar"] * { color: white !important; }

  [data-testid="stSidebar"] hr { border-color: rgba(77,184,160,0.25); }

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



# ── Datos de usuarios de prueba ───────────────────────────────────────────────

USERS = {

    "admin@convivir.ar":   {"password": "admin123",   "role": "admin",   "name": "Administrador"},

    "docente@colegio.ar":  {"password": "docente123", "role": "teacher", "name": "Prof. María García"},

    "alumno@colegio.ar":   {"password": "alumno123",  "role": "student", "name": "Lucas Martínez"},

}



# ── Estado de sesión ──────────────────────────────────────────────────────────

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "user" not in st.session_state:

    st.session_state.user = None



# ── CSS de la landing ─────────────────────────────────────────────────────────

LANDING_CSS = """

<style>

@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

.block-container { padding:0!important; max-width:100%!important; }

header[data-testid="stHeader"] { display:none; }

[data-testid="stSidebar"] { display:none; }



.cv { font-family:'DM Sans',sans-serif; background:#03091a; color:#dde8f8; min-height:100vh; }



.cv-nav {

    position:fixed; top:0; left:0; right:0; z-index:100;

    display:flex; align-items:center; justify-content:space-between;

    padding:0 52px; height:66px;

    background:rgba(3,9,26,0.9); backdrop-filter:blur(20px);

    border-bottom:1px solid rgba(74,158,255,0.1);

}

.cv-logo { display:flex; align-items:center; gap:10px; }

.cv-logo-txt { font-family:'Sora',sans-serif; font-size:20px; font-weight:800; color:#fff; letter-spacing:-0.4px; }

.cv-logo-txt em { font-style:normal; color:#4a9eff; }

.cv-nav-links { display:flex; gap:34px; font-size:13px; font-weight:500; color:rgba(221,232,248,0.4); }



.cv-hero {

    min-height:100vh; display:flex; flex-direction:column; justify-content:center;

    padding:120px 52px 80px; position:relative; overflow:hidden;

    background:

        radial-gradient(ellipse 90% 65% at 50% -5%, rgba(26,111,255,0.2) 0%, transparent 65%),

        radial-gradient(ellipse 45% 45% at 87% 38%, rgba(59,130,246,0.08) 0%, transparent 55%),

        #03091a;

}

.cv-hero::before {

    content:''; position:absolute; inset:0;

    background-image:

        linear-gradient(rgba(74,158,255,0.035) 1px, transparent 1px),

        linear-gradient(90deg, rgba(74,158,255,0.035) 1px, transparent 1px);

    background-size:64px 64px;

    mask-image:radial-gradient(ellipse 80% 55% at 50% 0%, black, transparent 72%);

}

.cv-hero-inner {

    display:grid; grid-template-columns:1fr auto; gap:72px;

    align-items:center; max-width:1200px; position:relative; z-index:1;

}

.cv-tag {

    display:inline-flex; align-items:center; gap:7px;

    background:rgba(26,111,255,0.1); border:1px solid rgba(74,158,255,0.22);

    border-radius:100px; padding:5px 14px;

    font-size:10.5px; font-weight:700; letter-spacing:2px;

    text-transform:uppercase; color:#60a5fa; margin-bottom:22px;

}

.cv-hero h1 {

    font-family:'Sora',sans-serif;

    font-size:clamp(36px,5vw,66px); font-weight:800;

    line-height:1.07; letter-spacing:-2.5px; color:#fff; margin-bottom:20px;

}

.cv-hero h1 em { font-style:normal; color:#4a9eff; }

.cv-hero-sub {

    font-size:16.5px; font-weight:300; line-height:1.75;

    color:rgba(221,232,248,0.52); max-width:510px;

}

.cv-logo-hero {

    position:relative; width:210px; height:210px;

    display:flex; align-items:center; justify-content:center; flex-shrink:0;

}



.cv-stats {

    display:flex; gap:0; margin-top:56px; padding-top:40px;

    border-top:1px solid rgba(74,158,255,0.09); position:relative; z-index:1;

}

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



LANDING_HTML_1 = """

<div class="cv">

  <nav class="cv-nav">

    <div class="cv-logo">

"""

LANDING_HTML_2 = """

      <span class="cv-logo-txt">Con<em>Vivir</em></span>

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

"""

LANDING_HTML_3 = """

      </div>

    </div>

    <div class="cv-stats">

      <div class="cv-stat"><div class="cv-stat-n">1 de 3<b>.</b></div><div class="cv-stat-l">alumnos vive o presencia<br>situaciones de bullying</div></div>

      <div class="cv-stat"><div class="cv-stat-n">24<b>+</b></div><div class="cv-stat-l">pantallas y flujos<br>diseñados en el MVP</div></div>

      <div class="cv-stat"><div class="cv-stat-n">5<b>.</b></div><div class="cv-stat-l">módulos integrados:<br>Admin · Aulas · Sociograma · Contenido · Reportes</div></div>

      <div class="cv-stat"><div class="cv-stat-n">4<b>.</b></div><div class="cv-stat-l">actores del sistema
