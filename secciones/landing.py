import streamlit as st

# ══════════════════════════════════════════════════════════════════════════════
# LOGOS SVG — Identidad visual Animar
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

# ── CSS de la landing ──────────────────────────────────────────────────────────
LANDING_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
.block-container { padding:0!important; max-width:100%!important; }

.cv { font-family:'DM Sans',sans-serif; background:#03091a; color:#dde8f8; min-height:100vh; width: 100%; margin-top: -80px; }

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

# ── Bloques HTML ─────────────────────────────────────────────────────────────
LANDING_HTML_1 = """
<div class="cv">
  <section class="cv-hero">
    <div class="cv-hero-inner">
      <div>
        <div class="cv-tag">Plataforma de Convivencia Escolar</div>
        <h1>Prevención del bullying<br><em>basada en datos</em><br>para colegios</h1>
        <p class="cv-hero-sub">ConVivir combina sociogramas de aula, contenido educativo y gestión institucional para que docentes detecten situaciones de acoso antes de que escalen.</p>
      </div>
      <div class="cv-logo-hero">
"""

LANDING_HTML_2 = """
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

LANDING_HTML_3 = """
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
    <p>Contactanos para comenzar la implementación en tu institución.</p>
  </section>

  <footer class="cv-ft">
    <div class="cv-ft-logo">
      <span>© 2026 ConVivir — Plataforma de Convivencia Escolar</span>
    </div>
    <span>Confidencial · v1.1 · Marzo 2026</span>
  </footer>
</div>
"""

def show_landing():
    """
    Renderiza la landing page completa con toda la información original.
    """
    full_html = (
        LANDING_CSS
        + LANDING_HTML_1 + LOGO_HERO
        + LANDING_HTML_2 + LOGO_MOD
        + LANDING_HTML_3
    )
    st.markdown(full_html, unsafe_allow_html=True)
