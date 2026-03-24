import streamlit as st

st.set_page_config(
    page_title="ConVivir — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos globales post-login ───────────────────────────────────────────────
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

CREDS = {
    "colegio": {
        "email": "docente@colegio.ar",
        "password": "docente123",
        "role": "teacher",
        "name": "Prof. María García",
    },
    "admin": {
        "email": "admin@convivir.ar",
        "password": "admin123",
        "role": "admin",
        "name": "Administrador",
    },
    "alumno": {
        "email": "alumno@colegio.ar",
        "password": "alumno123",
        "role": "student",
        "name": "Lucas Martínez",
    },
}

# ── Estado de sesión ──────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "login_panel" not in st.session_state:
    st.session_state.login_panel = None
if "current_page" not in st.session_state:
    st.session_state.current_page = None

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
.ag { display:grid; grid-template-columns:repeat(3,1fr); gap:13px; }
.ac { border-radius:18px; padding:24px 20px; border:1px solid transparent; transition:transform .2s; }
.ac:hover { transform:translateY(-4px); }
.ac-adm { background:linear-gradient(145deg,rgba(26,86,160,.2),rgba(26,86,160,.05)); border-color:rgba(26,86,160,.3); }
.ac-tch { background:linear-gradient(145deg,rgba(29,122,85,.2),rgba(29,122,85,.05)); border-color:rgba(29,122,85,.3); }
.ac-stu { background:linear-gradient(145deg,rgba(212,88,10,.2),rgba(212,88,10,.05)); border-color:rgba(212,88,10,.3); }
.ac-emoji { font-size:28px; margin-bottom:11px; display:block; }
.ac-badge { display:inline-block; padding:2px 10px; border-radius:100px; font-size:9px; font-weight:700; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:8px; }
.ab-a { background:rgba(26,86,160,.28); color:#93b4e8; }
.ab-t { background:rgba(29,122,85,.28); color:#6dd9a8; }
.ab-s { background:rgba(212,88,10,.28); color:#f4a461; }
.ac-name { font-family:'Sora',sans-serif; font-size:14px; font-weight:700; color:#fff; margin-bottom:7px; }
.ac-desc { font-size:12.5px; color:rgba(221,232,248,0.46); line-height:1.65; }
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
      <div class="cv-stat"><div class="cv-stat-n">3<b>.</b></div><div class="cv-stat-l">actores del sistema con<br>flujos diferenciados</div></div>
    </div>
  </section>

  <section class="cv-s">
    <div class="cv-eyebrow">El Problema</div>
    <h2>El bullying existe.<br>El problema es que no lo vemos.</h2>
    <p class="cv-intro">Sin herramientas adecuadas, los docentes actúan cuando el daño ya ocurrió. La dinámica social del aula es invisible hasta que se vuelve urgente.</p>
    <div class="pg">
      <div class="pc"><div class="pc-icon">👁️</div><h3>Sin visibilidad de la dinámica grupal</h3><p>Los docentes no tienen forma objetiva de ver quién está aislado, quién domina y quién está en riesgo dentro del aula.</p><div class="pc-stat">70%</div><div class="pc-sub">de casos no son reportados al docente</div></div>
      <div class="pc"><div class="pc-icon">⏱️</div><h3>Intervención tardía</h3><p>Cuando el problema se hace visible, ya generó daño psicológico, social y académico en el alumno afectado.</p><div class="pc-stat">6 meses</div><div class="pc-sub">tiempo promedio antes de una intervención</div></div>
      <div class="pc"><div class="pc-icon">🧩</div><h3>Herramientas fragmentadas</h3><p>No existe una plataforma que integre diagnóstico, contenido y seguimiento en un solo lugar seguro.</p><div class="pc-stat">1</div><div class="pc-sub">plataforma integral en desarrollo</div></div>
    </div>
  </section>

  <section class="cv-sa">
    <div class="cv-eyebrow">La Solución</div>
    <h2>5 módulos. Un ecosistema completo.</h2>
    <p class="cv-intro">Cada módulo cubre una parte del ciclo: gestión institucional → diagnóstico → acción → seguimiento.</p>
    <div class="mg">
      <div class="mc"><div class="mc-icon">🏛️</div><div class="mc-id">M1</div><div class="mc-name">Backoffice Admin</div><div class="mc-desc">Alta de colegios y validación</div></div>
      <div class="mc"><div class="mc-icon">🚪</div><div class="mc-id">M2</div><div class="mc-name">Gestión de Aulas</div><div class="mc-desc">Creación y habilitación con código</div></div>
      <div class="mc"><div class="mc-logo">
"""
LANDING_HTML_4 = """
      </div><div class="mc-id">M3</div><div class="mc-name">Sociograma</div><div class="mc-desc">Encuesta confidencial y mapa de relaciones</div></div>
      <div class="mc"><div class="mc-icon">📚</div><div class="mc-id">M4</div><div class="mc-name">Contenido</div><div class="mc-desc">Guías adaptadas al rol del usuario</div></div>
      <div class="mc"><div class="mc-icon">📊</div><div class="mc-id">M5</div><div class="mc-name">Reportes</div><div class="mc-desc">Alertas y síntesis descargable</div></div>
    </div>
  </section>

  <section class="cv-s">
    <div class="cv-eyebrow">Actores del Sistema</div>
    <h2>Tres roles. Flujos diferenciados.</h2>
    <p class="cv-intro">Cada usuario accede únicamente a lo que necesita y está autorizado a ver.</p>
    <div class="ag">
      <div class="ac ac-adm"><span class="ac-emoji">🏛️</span><div><span class="ac-badge ab-a">Administrador</span></div><div class="ac-name">Backoffice Admin</div><p class="ac-desc">Gestiona colegios y valida el acceso al ecosistema.</p></div>
      <div class="ac ac-tch"><span class="ac-emoji">👨‍🏫</span><div><span class="ac-badge ab-t">Docente</span></div><div class="ac-name">Docente Validado</div><p class="ac-desc">Habilita aulas, visualiza el sociograma y gestiona alertas.</p></div>
      <div class="ac ac-stu"><span class="ac-emoji">🎒</span><div><span class="ac-badge ab-s">Alumno</span></div><div class="ac-name">Alumno Registrado</div><p class="ac-desc">Completa la encuesta de forma confidencial y accede a contenido adaptado.</p></div>
    </div>
  </section>

  <section class="cv-cta">
    <h2>¿Tu colegio quiere sumarse?</h2>
    <p>Ingresá con tu cuenta para acceder a la plataforma.</p>
  </section>

  <footer class="cv-ft">
    <div class="cv-ft-logo">
"""
LANDING_HTML_5 = """
      <span>© 2026 ConVivir — Plataforma de Convivencia Escolar</span>
    </div>
    <span>Confidencial · v1.0</span>
  </footer>
</div>
"""

def do_login(profile, email_input, pass_input):
    cred = CREDS[profile]
    if email_input == cred["email"] and pass_input == cred["password"]:
        st.session_state.logged_in = True
        st.session_state.login_panel = None
        st.session_state.user = {
            "email": cred["email"],
            "role": cred["role"],
            "name": cred["name"],
        }
        role = cred["role"]
        if role == "admin":
            st.session_state.current_page = "admin_dashboard"
        elif role == "teacher":
            st.session_state.current_page = "teacher_dashboard"
        else:
            st.session_state.current_page = "student_home"
        st.rerun()
    else:
        st.error("Email o contraseña incorrectos.")

def show_login():
    full_html = (
        LANDING_CSS
        + LANDING_HTML_1 + LOGO_NAV
        + LANDING_HTML_2 + LOGO_HERO
        + LANDING_HTML_3 + LOGO_MOD
        + LANDING_HTML_4 + LOGO_NAV
        + LANDING_HTML_5
    )
    st.markdown(full_html, unsafe_allow_html=True)

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;700;800&display=swap');
    .main > div { background:#f5f0eb !important; }
    .block-container { padding-top:0 !important; }
    </style>
    """, unsafe_allow_html=True)

    _, col_btn = st.columns([12, 1])
    with col_btn:
        if st.button("Ingresar →", type="primary", key="open_login"):
            st.session_state.login_panel = "select"
            st.rerun()

    if st.session_state.login_panel is None:
        return

    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_c, _ = st.columns([1, 3, 1])
    with col_c:
        st.markdown(
            "<div style='text-align:center;margin-bottom:8px;'>" + LOGO_NAV + "</div>"
            "<p style='text-align:center;font-family:Sora,sans-serif;font-size:22px;"
            "font-weight:800;color:#1a2e2a;margin:12px 0 4px;'>¿Con qué perfil ingresás?</p>"
            "<p style='text-align:center;font-size:14px;color:#8a9a92;margin-bottom:32px;'>"
            "Hacé click en tu perfil y cargá tus datos</p>",
            unsafe_allow_html=True
        )

    perfiles = [
        ("colegio", "🏫", "Colegio", "Docentes que gestionan aulas y sociogramas"),
        ("admin", "🏛️", "Administrador", "Gestión institucional y validación"),
        ("alumno", "🎒", "Alumno", "Completa la encuesta y accede a contenido"),
    ]

    _, col_grid, _ = st.columns([1, 3, 1])
    with col_grid:
        cols = st.columns(3)
        for i, (key, ico, nombre, desc) in enumerate(perfiles):
            with cols[i]:
                st.markdown(
                    f"""
                    <div style="background:white;border-radius:18px;border:2px solid #e0d8d0;
                    padding:24px 16px;text-align:center;min-height:170px;">
                        <div style="font-size:42px;margin-bottom:10px;">{ico}</div>
                        <div style="font-weight:800;font-size:17px;color:#1a2e2a;">{nombre}</div>
                        <div style="font-size:12px;color:#7a8a82;margin-top:8px;line-height:1.5;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button(f"Ingresar como {nombre}", key=f"sel_{key}", use_container_width=True):
                    st.session_state.login_panel = key
                    st.rerun()

    panel = st.session_state.login_panel
    if panel in CREDS:
        cred = CREDS[panel]
        nombres = {"colegio": "Colegio", "admin": "Administrador", "alumno": "Alumno"}
        st.markdown("<br>", unsafe_allow_html=True)
        _, col_form, _ = st.columns([1, 1.2, 1])
        with col_form:
            with st.container(border=True):
                st.markdown(
                    f"### Acceso — {nombres[panel]}\n"
                    f"Demo: `{cred['email']}` / `{cred['password']}`"
                )
                with st.form(f"form_{panel}"):
                    email = st.text_input("Email", value=cred["email"])
                    pwd = st.text_input("Contraseña", type="password", value=cred["password"])
                    c1, c2 = st.columns(2)
                    with c1:
                        submitted = st.form_submit_button("Ingresar →", type="primary", use_container_width=True)
                    with c2:
                        cancelled = st.form_submit_button("Cancelar", use_container_width=True)

                if submitted:
                    do_login(panel, email, pwd)
                if cancelled:
                    st.session_state.login_panel = None
                    st.rerun()

def show_sidebar():
    user = st.session_state.user
    role = user["role"]

    with st.sidebar:
        st.markdown(
            "<div style='display:flex;align-items:center;gap:9px;padding:6px 0 14px;'>"
            + LOGO_SIDEBAR
            + "</div>",
            unsafe_allow_html=True
        )
        st.markdown("---")
        st.markdown(f"👤 **{user['name']}**")

        badge_map = {
            "admin": ("badge-admin", "Administrador"),
            "teacher": ("badge-teacher", "Docente"),
            "student": ("badge-student", "Alumno"),
        }
        badge_class, label = badge_map[role]
        st.markdown(f"<span class='{badge_class}'>{label}</span>", unsafe_allow_html=True)
        st.markdown("---")

        if role == "admin":
            pages = {
                "🏛️ Dashboard Admin": "admin_dashboard",
                "🏫 Colegios": "admin_colegios",
                "👨‍🏫 Docentes": "admin_docentes",
                "✅ Validaciones": "admin_kyc",
            }
        elif role == "teacher":
            pages = {
                "📊 Mi Dashboard": "teacher_dashboard",
                "🚪 Gestión de Aulas": "teacher_aulas",
                "🕸️ Sociograma": "teacher_sociograma",
                "🚨 Alertas": "teacher_alertas",
                "📋 Reportes": "teacher_reportes",
            }
        else:
            pages = {
                "🏠 Inicio": "student_home",
                "📝 Encuesta Sociométrica": "student_encuesta",
                "📚 Contenido Educativo": "student_contenido",
            }

        for label, key in pages.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()

        st.markdown("---")
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.current_page = None
            st.session_state.login_panel = None
            st.rerun()

def route():
    page = st.session_state.get("current_page", "")
    role = st.session_state.user["role"]

    if page == "admin_dashboard" or (role == "admin" and not page):
        from views import admin_dashboard
        admin_dashboard.render()
    elif page == "admin_colegios":
        from views import admin_colegios
        admin_colegios.render()
    elif page == "admin_docentes":
        from views import admin_docentes
        admin_docentes.render()
    elif page == "admin_kyc":
        from views import admin_kyc
        admin_kyc.render()
    elif page == "teacher_dashboard" or (role == "teacher" and not page):
        from views import teacher_dashboard
        teacher_dashboard.render()
    elif page == "teacher_aulas":
        from views import teacher_aulas
        teacher_aulas.render()
    elif page == "teacher_sociograma":
        from views import teacher_sociograma
        teacher_sociograma.render()
    elif page == "teacher_alertas":
        from views import teacher_alertas
        teacher_alertas.render()
    elif page == "teacher_reportes":
        from views import teacher_reportes
        teacher_reportes.render()
    elif page == "student_home" or (role == "student" and not page):
        from views import student_home
        student_home.render()
    elif page == "student_encuesta":
        from views import student_encuesta
        student_encuesta.render()
    elif page == "student_contenido":
        from views import student_contenido
        student_contenido.render()
    else:
        st.warning("Página no encontrada.")

if not st.session_state.logged_in:
    show_login()
else:
    show_sidebar()
    route()
