import streamlit as st

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


def show_landing():
    full_html = (
        # CSS ya está en desktop.css — solo el HTML aquí
        LANDING_HTML_1 + LOGO_NAV
        + LANDING_HTML_2 + LOGO_HERO
        + LANDING_HTML_3 + LOGO_MOD
        + LANDING_HTML_4 + LOGO_NAV
        + LANDING_HTML_5
    )
    st.markdown(full_html, unsafe_allow_html=True)


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
      <span>© 2025 ConVivir — Plataforma de Convivencia Escolar</span>
    </div>
    <span>Confidencial · v1.0 · Borrador Inicial</span>
  </footer>
</div>
"""
