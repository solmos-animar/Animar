import streamlit as st

st.set_page_config(
    page_title="ConVivir — Plataforma de Convivencia Escolar",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos globales ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #0f2240; }
  [data-testid="stSidebar"] * { color: white !important; }
  [data-testid="stSidebar"] .stRadio label { color: rgba(255,255,255,0.8) !important; }
  [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }
  .main .block-container { padding-top: 2rem; }
  h1 { color: #0f2240; }
  h2 { color: #0f2240; }
  h3 { color: #1a56a0; }
  .metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    border: 1px solid #ebe9e4;
    box-shadow: 0 2px 8px rgba(15,34,64,0.08);
    margin-bottom: 1rem;
  }
  .badge-admin   { background:#e8effe; color:#1a56a0; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-teacher { background:#e6f4ee; color:#1d7a55; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .badge-student { background:#fde8d0; color:#d4580a; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700; }
  .alert-high   { background:#fdeaea; border-left:4px solid #c0392b; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-medium { background:#fef3e2; border-left:4px solid #d4580a; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .alert-low    { background:#e6f4ee; border-left:4px solid #1d7a55; border-radius:8px; padding:12px 16px; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ── Datos de usuarios de prueba ───────────────────────────────────────────────
USERS = {
    "admin@convivir.ar":    {"password": "admin123",   "role": "admin",   "name": "Administrador"},
    "docente@colegio.ar":   {"password": "docente123", "role": "teacher", "name": "Prof. María García"},
    "alumno@colegio.ar":    {"password": "alumno123",  "role": "student", "name": "Lucas Martínez"},
}

# ── Estado de sesión ──────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# ── Login ─────────────────────────────────────────────────────────────────────
def show_login():
    # Toggle login panel via query params workaround using session state
    if "show_login_panel" not in st.session_state:
        st.session_state.show_login_panel = False

    # ── Full landing page ─────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    .block-container { padding: 0 !important; max-width: 100% !important; }
    header[data-testid="stHeader"] { display: none; }
    [data-testid="stSidebar"] { display: none; }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    .cv-page {
        font-family: 'DM Sans', sans-serif;
        background: #040e1f;
        color: #e8eef8;
        min-height: 100vh;
    }

    /* ── NAV ── */
    .cv-nav {
        position: fixed; top: 0; left: 0; right: 0; z-index: 100;
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 56px;
        height: 68px;
        background: rgba(4,14,31,0.85);
        backdrop-filter: blur(16px);
        border-bottom: 1px solid rgba(99,140,210,0.12);
    }
    .cv-logo {
        font-family: 'Sora', sans-serif;
        font-size: 22px; font-weight: 800;
        color: #fff; letter-spacing: -0.5px;
    }
    .cv-logo span { color: #4a9eff; }
    .cv-nav-links {
        display: flex; gap: 36px;
        font-size: 13.5px; font-weight: 500; color: rgba(232,238,248,0.55);
    }
    .cv-btn-login {
        background: #1a6fff;
        color: white !important;
        border: none; border-radius: 8px;
        padding: 10px 24px;
        font-family: 'Sora', sans-serif;
        font-size: 13.5px; font-weight: 600;
        cursor: pointer; letter-spacing: 0.2px;
        transition: background 0.2s, transform 0.15s;
        text-decoration: none;
    }
    .cv-btn-login:hover { background: #0d5fe8; transform: translateY(-1px); }

    /* ── HERO ── */
    .cv-hero {
        padding: 168px 56px 96px;
        position: relative; overflow: hidden;
        background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(26,111,255,0.18) 0%, transparent 70%),
                    radial-gradient(ellipse 40% 40% at 80% 30%, rgba(74,158,255,0.08) 0%, transparent 60%),
                    #040e1f;
    }
    .cv-hero-tag {
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(26,111,255,0.12);
        border: 1px solid rgba(26,111,255,0.3);
        border-radius: 100px;
        padding: 6px 16px;
        font-size: 12px; font-weight: 600; letter-spacing: 1.2px;
        text-transform: uppercase; color: #4a9eff;
        margin-bottom: 28px;
    }
    .cv-hero h1 {
        font-family: 'Sora', sans-serif;
        font-size: clamp(42px, 5.5vw, 72px);
        font-weight: 800; line-height: 1.06;
        letter-spacing: -2px; color: #fff;
        max-width: 780px; margin-bottom: 24px;
    }
    .cv-hero h1 em { font-style: normal; color: #4a9eff; }
    .cv-hero-sub {
        font-size: 18px; font-weight: 300; line-height: 1.7;
        color: rgba(232,238,248,0.6);
        max-width: 560px; margin-bottom: 48px;
    }
    .cv-hero-actions { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }
    .cv-btn-primary {
        background: #1a6fff; color: white;
        border: none; border-radius: 10px;
        padding: 15px 32px;
        font-family: 'Sora', sans-serif;
        font-size: 15px; font-weight: 700;
        cursor: pointer; transition: all 0.2s;
        letter-spacing: -0.2px;
    }
    .cv-btn-primary:hover { background: #0d5fe8; transform: translateY(-2px); box-shadow: 0 8px 32px rgba(26,111,255,0.4); }
    .cv-btn-ghost {
        background: transparent; color: rgba(232,238,248,0.7);
        border: 1px solid rgba(232,238,248,0.15); border-radius: 10px;
        padding: 15px 28px;
        font-family: 'Sora', sans-serif;
        font-size: 15px; font-weight: 500;
        cursor: pointer; transition: all 0.2s;
    }
    .cv-btn-ghost:hover { border-color: rgba(74,158,255,0.4); color: #4a9eff; }

    /* Stats row */
    .cv-stats {
        display: flex; gap: 0;
        margin-top: 72px;
        border-top: 1px solid rgba(99,140,210,0.12);
        padding-top: 48px;
    }
    .cv-stat {
        flex: 1; padding: 0 40px 0 0;
        border-right: 1px solid rgba(99,140,210,0.1);
        margin-right: 40px;
    }
    .cv-stat:last-child { border-right: none; margin-right: 0; }
    .cv-stat-num {
        font-family: 'Sora', sans-serif;
        font-size: 40px; font-weight: 800;
        color: #fff; letter-spacing: -2px; line-height: 1;
        margin-bottom: 6px;
    }
    .cv-stat-num span { color: #4a9eff; }
    .cv-stat-label { font-size: 13px; color: rgba(232,238,248,0.45); font-weight: 400; line-height: 1.5; }

    /* ── PROBLEMA ── */
    .cv-section { padding: 96px 56px; }
    .cv-section-label {
        font-size: 11px; font-weight: 700; letter-spacing: 2px;
        text-transform: uppercase; color: #4a9eff; margin-bottom: 16px;
    }
    .cv-section h2 {
        font-family: 'Sora', sans-serif;
        font-size: clamp(28px, 3vw, 42px); font-weight: 800;
        letter-spacing: -1px; color: #fff; margin-bottom: 16px; line-height: 1.15;
    }
    .cv-section-intro {
        font-size: 17px; color: rgba(232,238,248,0.55);
        max-width: 600px; line-height: 1.7; margin-bottom: 56px;
    }

    /* Problem cards */
    .cv-problem-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; }
    .cv-problem-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(99,140,210,0.12);
        border-radius: 16px; padding: 28px 28px 24px;
        transition: border-color 0.2s, background 0.2s;
    }
    .cv-problem-card:hover { border-color: rgba(74,158,255,0.25); background: rgba(26,111,255,0.05); }
    .cv-problem-icon { font-size: 28px; margin-bottom: 16px; display: block; }
    .cv-problem-card h3 { font-family: 'Sora', sans-serif; font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 10px; }
    .cv-problem-card p { font-size: 13.5px; color: rgba(232,238,248,0.5); line-height: 1.65; }
    .cv-problem-stat { font-family: 'Sora', sans-serif; font-size: 28px; font-weight: 800; color: #4a9eff; margin-top: 16px; }
    .cv-problem-stat-label { font-size: 11px; color: rgba(232,238,248,0.35); margin-top: 2px; }

    /* ── SOLUCIÓN / MÓDULOS ── */
    .cv-modules { padding: 96px 56px; background: rgba(26,111,255,0.03); border-top: 1px solid rgba(99,140,210,0.08); border-bottom: 1px solid rgba(99,140,210,0.08); }
    .cv-mod-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 12px; margin-top: 48px; }
    .cv-mod-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(99,140,210,0.1);
        border-radius: 14px; padding: 24px 18px 20px;
        text-align: center;
        transition: all 0.2s;
    }
    .cv-mod-card:hover { background: rgba(26,111,255,0.08); border-color: rgba(74,158,255,0.3); transform: translateY(-4px); }
    .cv-mod-icon { font-size: 30px; margin-bottom: 12px; }
    .cv-mod-id { font-family: 'Sora', monospace; font-size: 10px; color: #4a9eff; font-weight: 700; letter-spacing: 1px; margin-bottom: 6px; }
    .cv-mod-name { font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 700; color: #fff; line-height: 1.3; margin-bottom: 8px; }
    .cv-mod-desc { font-size: 11.5px; color: rgba(232,238,248,0.4); line-height: 1.5; }

    /* ── ACTORES ── */
    .cv-actors { padding: 96px 56px; }
    .cv-actor-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-top: 48px; }
    .cv-actor-card {
        border-radius: 16px; padding: 28px 24px;
        border: 1px solid transparent;
        transition: transform 0.2s;
    }
    .cv-actor-card:hover { transform: translateY(-4px); }
    .cv-actor-admin   { background: linear-gradient(135deg, rgba(26,86,160,0.2), rgba(26,86,160,0.05)); border-color: rgba(26,86,160,0.3); }
    .cv-actor-teacher { background: linear-gradient(135deg, rgba(29,122,85,0.2), rgba(29,122,85,0.05)); border-color: rgba(29,122,85,0.3); }
    .cv-actor-student { background: linear-gradient(135deg, rgba(212,88,10,0.2), rgba(212,88,10,0.05)); border-color: rgba(212,88,10,0.3); }
    .cv-actor-family  { background: linear-gradient(135deg, rgba(91,63,160,0.2), rgba(91,63,160,0.05)); border-color: rgba(91,63,160,0.3); }
    .cv-actor-emoji { font-size: 32px; margin-bottom: 14px; display: block; }
    .cv-actor-badge {
        display: inline-block; padding: 3px 12px; border-radius: 100px;
        font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
        margin-bottom: 10px;
    }
    .badge-admin   { background: rgba(26,86,160,0.3); color: #7ab3f0; }
    .badge-teacher { background: rgba(29,122,85,0.3); color: #6dd9a8; }
    .badge-student { background: rgba(212,88,10,0.3); color: #f4a461; }
    .badge-family  { background: rgba(91,63,160,0.3); color: #b39ddb; }
    .cv-actor-name { font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 8px; }
    .cv-actor-desc { font-size: 13px; color: rgba(232,238,248,0.5); line-height: 1.65; }

    /* ── FLUJO ── */
    .cv-flow { padding: 96px 56px; background: rgba(26,111,255,0.03); border-top: 1px solid rgba(99,140,210,0.08); }
    .cv-flow-steps { display: flex; gap: 0; margin-top: 48px; position: relative; }
    .cv-flow-steps::before {
        content: ''; position: absolute;
        top: 28px; left: 28px; right: 28px; height: 2px;
        background: linear-gradient(90deg, #1a6fff, rgba(26,111,255,0.2));
    }
    .cv-flow-step { flex: 1; text-align: center; padding: 0 16px; position: relative; }
    .cv-flow-num {
        width: 56px; height: 56px; border-radius: 50%;
        background: #040e1f; border: 2px solid #1a6fff;
        display: inline-flex; align-items: center; justify-content: center;
        font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 800; color: #4a9eff;
        margin-bottom: 16px; position: relative; z-index: 1;
    }
    .cv-flow-title { font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 700; color: #fff; margin-bottom: 6px; }
    .cv-flow-desc { font-size: 12px; color: rgba(232,238,248,0.4); line-height: 1.6; }

    /* ── PRIVACIDAD ── */
    .cv-privacy { padding: 96px 56px; }
    .cv-privacy-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 48px; }
    .cv-privacy-item {
        display: flex; gap: 16px; align-items: flex-start;
        background: rgba(255,255,255,0.02); border: 1px solid rgba(99,140,210,0.1);
        border-radius: 12px; padding: 20px;
    }
    .cv-privacy-icon { font-size: 22px; flex-shrink: 0; margin-top: 2px; }
    .cv-privacy-title { font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 4px; }
    .cv-privacy-desc { font-size: 13px; color: rgba(232,238,248,0.45); line-height: 1.6; }

    /* ── ROADMAP ── */
    .cv-roadmap { padding: 96px 56px; background: rgba(26,111,255,0.03); border-top: 1px solid rgba(99,140,210,0.08); }
    .cv-phases { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-top: 48px; }
    .cv-phase {
        border-radius: 16px; padding: 28px 24px;
        background: rgba(255,255,255,0.02); border: 1px solid rgba(99,140,210,0.1);
        position: relative; overflow: hidden;
    }
    .cv-phase::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    }
    .phase1::before { background: #1a6fff; }
    .phase2::before { background: #0ea5e9; }
    .phase3::before { background: #06b6d4; }
    .phase4::before { background: #6366f1; }
    .cv-phase-tag { font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 10px; }
    .phase1 .cv-phase-tag { color: #1a6fff; }
    .phase2 .cv-phase-tag { color: #0ea5e9; }
    .phase3 .cv-phase-tag { color: #06b6d4; }
    .phase4 .cv-phase-tag { color: #6366f1; }
    .cv-phase-title { font-family: 'Sora', sans-serif; font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 14px; }
    .cv-phase ul { list-style: none; }
    .cv-phase ul li { font-size: 12.5px; color: rgba(232,238,248,0.5); padding: 5px 0; border-bottom: 1px solid rgba(99,140,210,0.06); line-height: 1.5; }
    .cv-phase ul li::before { content: '→ '; color: rgba(74,158,255,0.5); }

    /* ── CTA FINAL ── */
    .cv-cta {
        padding: 96px 56px;
        text-align: center;
        background: radial-gradient(ellipse 60% 80% at 50% 50%, rgba(26,111,255,0.12) 0%, transparent 70%);
    }
    .cv-cta h2 { font-family: 'Sora', sans-serif; font-size: 48px; font-weight: 800; letter-spacing: -2px; color: #fff; margin-bottom: 20px; }
    .cv-cta p { font-size: 18px; color: rgba(232,238,248,0.5); margin-bottom: 40px; }

    /* ── FOOTER ── */
    .cv-footer {
        padding: 28px 56px;
        border-top: 1px solid rgba(99,140,210,0.1);
        display: flex; justify-content: space-between; align-items: center;
        font-size: 12px; color: rgba(232,238,248,0.25);
    }
    </style>

    <div class="cv-page">

      <!-- NAV -->
      <nav class="cv-nav">
        <div class="cv-logo">Con<span>Vivir</span></div>
        <div class="cv-nav-links">
          <span>Problema</span>
          <span>Solución</span>
          <span>Actores</span>
          <span>Roadmap</span>
        </div>
      </nav>

      <!-- HERO -->
      <section class="cv-hero">
        <div class="cv-hero-tag">🕸️ Plataforma de Convivencia Escolar</div>
        <h1>Prevención del bullying<br><em>basada en datos</em><br>para colegios</h1>
        <p class="cv-hero-sub">
          ConVivir combina sociogramas de aula, contenido educativo y gestión institucional
          para que docentes detecten y actúen ante situaciones de acoso antes de que escalen.
        </p>

        <div class="cv-stats">
          <div class="cv-stat">
            <div class="cv-stat-num">1 de 3<span>.</span></div>
            <div class="cv-stat-label">alumnos vive o presencia<br>situaciones de bullying</div>
          </div>
          <div class="cv-stat">
            <div class="cv-stat-num">24<span>+</span></div>
            <div class="cv-stat-label">pantallas y flujos<br>diseñados en el MVP</div>
          </div>
          <div class="cv-stat">
            <div class="cv-stat-num">5<span>.</span></div>
            <div class="cv-stat-label">módulos integrados:<br>Admin · Aulas · Sociograma · Contenido · Reportes</div>
          </div>
          <div class="cv-stat">
            <div class="cv-stat-num">4<span>.</span></div>
            <div class="cv-stat-label">actores del sistema con<br>flujos completamente diferenciados</div>
          </div>
        </div>
      </section>

      <!-- PROBLEMA -->
      <section class="cv-section">
        <div class="cv-section-label">El Problema</div>
        <h2>El bullying existe.<br>El problema es que no lo vemos.</h2>
        <p class="cv-section-intro">
          Sin herramientas adecuadas, los docentes actúan cuando el daño ya ocurrió.
          La dinámica social del aula es invisible hasta que se vuelve urgente.
        </p>
        <div class="cv-problem-grid">
          <div class="cv-problem-card">
            <span class="cv-problem-icon">👁️‍🗨️</span>
            <h3>Sin visibilidad de la dinámica grupal</h3>
            <p>Los docentes no tienen forma objetiva de ver quién está aislado, quién domina y quién está en riesgo dentro del aula.</p>
            <div class="cv-problem-stat">70%</div>
            <div class="cv-problem-stat-label">de casos de bullying no son reportados al docente</div>
          </div>
          <div class="cv-problem-card">
            <span class="cv-problem-icon">⏱️</span>
            <h3>Intervención tardía</h3>
            <p>Cuando el problema se hace visible, ya generó daño psicológico, social y académico en el alumno afectado.</p>
            <div class="cv-problem-stat">6 meses</div>
            <div class="cv-problem-stat-label">es el tiempo promedio antes de una intervención</div>
          </div>
          <div class="cv-problem-card">
            <span class="cv-problem-icon">🧩</span>
            <h3>Herramientas fragmentadas</h3>
            <p>No existe una plataforma que integre diagnóstico, contenido educativo y seguimiento en un solo lugar seguro y auditable.</p>
            <div class="cv-problem-stat">0</div>
            <div class="cv-problem-stat-label">plataformas integrales disponibles en Argentina</div>
          </div>
        </div>
      </section>

      <!-- MÓDULOS -->
      <section class="cv-modules">
        <div class="cv-section-label">La Solución</div>
        <h2>5 módulos. Un ecosistema completo.</h2>
        <p class="cv-section-intro">Cada módulo cubre una parte del ciclo: gestión institucional → diagnóstico → acción → seguimiento.</p>
        <div class="cv-mod-grid">
          <div class="cv-mod-card">
            <div class="cv-mod-icon">🏛️</div>
            <div class="cv-mod-id">M1</div>
            <div class="cv-mod-name">Backoffice Admin</div>
            <div class="cv-mod-desc">Alta de colegios, validación KYC de docentes, gestión de permisos y auditoría</div>
          </div>
          <div class="cv-mod-card">
            <div class="cv-mod-icon">🚪</div>
            <div class="cv-mod-id">M2</div>
            <div class="cv-mod-name">Gestión de Aulas</div>
            <div class="cv-mod-desc">Creación y habilitación de aulas, registro de alumnos con código de acceso</div>
          </div>
          <div class="cv-mod-card">
            <div class="cv-mod-icon">🕸️</div>
            <div class="cv-mod-id">M3</div>
            <div class="cv-mod-name">Sociograma</div>
            <div class="cv-mod-desc">Encuesta sociométrica confidencial y mapa visual de relaciones del aula</div>
          </div>
          <div class="cv-mod-card">
            <div class="cv-mod-icon">📚</div>
            <div class="cv-mod-id">M4</div>
            <div class="cv-mod-name">Contenido</div>
            <div class="cv-mod-desc">Artículos y guías adaptados al rol: docente, alumno o familia</div>
          </div>
          <div class="cv-mod-card">
            <div class="cv-mod-icon">📊</div>
            <div class="cv-mod-id">M5</div>
            <div class="cv-mod-name">Reportes</div>
            <div class="cv-mod-desc">Alertas automáticas, perfiles individuales y reportes PDF descargables</div>
          </div>
        </div>
      </section>

      <!-- ACTORES -->
      <section class="cv-actors">
        <div class="cv-section-label">Actores del Sistema</div>
        <h2>Cuatro roles. Flujos completamente diferenciados.</h2>
        <p class="cv-section-intro">Cada usuario accede solo a lo que necesita y está autorizado a ver.</p>
        <div class="cv-actor-grid">
          <div class="cv-actor-card cv-actor-admin">
            <span class="cv-actor-emoji">🏛️</span>
            <div><span class="cv-actor-badge badge-admin">Administrador</span></div>
            <div class="cv-actor-name">Backoffice Admin</div>
            <p class="cv-actor-desc">Gestiona colegios, valida docentes mediante KYC y controla el acceso al ecosistema.</p>
          </div>
          <div class="cv-actor-card cv-actor-teacher">
            <span class="cv-actor-emoji">👨‍🏫</span>
            <div><span class="cv-actor-badge badge-teacher">Docente</span></div>
            <div class="cv-actor-name">Docente Validado</div>
            <p class="cv-actor-desc">Habilita aulas, visualiza el sociograma, gestiona alertas y accede a reportes completos.</p>
          </div>
          <div class="cv-actor-card cv-actor-student">
            <span class="cv-actor-emoji">🎒</span>
            <div><span class="cv-actor-badge badge-student">Alumno</span></div>
            <div class="cv-actor-name">Alumno Registrado</div>
            <p class="cv-actor-desc">Completa la encuesta sociométrica de forma confidencial y accede a contenido adaptado.</p>
          </div>
          <div class="cv-actor-card cv-actor-family">
            <span class="cv-actor-emoji">👨‍👩‍👧</span>
            <div><span class="cv-actor-badge badge-family">Familia</span></div>
            <div class="cv-actor-name">Familia / Tutor</div>
            <p class="cv-actor-desc">Se vincula al alumno y accede a contenido orientado a prevención en el hogar.</p>
          </div>
        </div>
      </section>

      <!-- FLUJO -->
      <section class="cv-flow">
        <div class="cv-section-label">Cómo Funciona</div>
        <h2>Del registro al diagnóstico en 4 pasos.</h2>
        <p class="cv-section-intro">El flujo principal del docente, desde que habilita el aula hasta que actúa sobre una alerta.</p>
        <div class="cv-flow-steps">
          <div class="cv-flow-step">
            <div class="cv-flow-num">1</div>
            <div class="cv-flow-title">Alta institucional</div>
            <div class="cv-flow-desc">El colegio se registra y pasa el proceso de KYC con el Admin</div>
          </div>
          <div class="cv-flow-step">
            <div class="cv-flow-num">2</div>
            <div class="cv-flow-title">Habilitación del aula</div>
            <div class="cv-flow-desc">El docente crea el aula y comparte el código con sus alumnos</div>
          </div>
          <div class="cv-flow-step">
            <div class="cv-flow-num">3</div>
            <div class="cv-flow-title">Encuesta sociométrica</div>
            <div class="cv-flow-desc">Los alumnos responden de forma individual y confidencial</div>
          </div>
          <div class="cv-flow-step">
            <div class="cv-flow-num">4</div>
            <div class="cv-flow-title">Sociograma generado</div>
            <div class="cv-flow-desc">El sistema procesa y genera el mapa de relaciones automáticamente</div>
          </div>
          <div class="cv-flow-step">
            <div class="cv-flow-num">5</div>
            <div class="cv-flow-title">Alerta automática</div>
            <div class="cv-flow-desc">Si detecta un alumno en riesgo, el docente recibe una notificación inmediata</div>
          </div>
          <div class="cv-flow-step">
            <div class="cv-flow-num">6</div>
            <div class="cv-flow-title">Intervención y reporte</div>
            <div class="cv-flow-desc">El docente accede al perfil, sigue las recomendaciones y descarga el reporte PDF</div>
          </div>
        </div>
      </section>

      <!-- PRIVACIDAD -->
      <section class="cv-privacy">
        <div class="cv-section-label">Privacidad y Seguridad</div>
        <h2>Los datos de los menores son intocables.</h2>
        <p class="cv-section-intro">El diseño garantiza por arquitectura que ningún alumno pueda ver las respuestas de otro.</p>
        <div class="cv-privacy-grid">
          <div class="cv-privacy-item">
            <div class="cv-privacy-icon">🔒</div>
            <div>
              <div class="cv-privacy-title">Respuestas 100% confidenciales</div>
              <div class="cv-privacy-desc">Ningún compañero puede ver las elecciones individuales de otro. Solo el docente accede a resultados agregados.</div>
            </div>
          </div>
          <div class="cv-privacy-item">
            <div class="cv-privacy-icon">🛡️</div>
            <div>
              <div class="cv-privacy-title">Cumplimiento Ley 25.326</div>
              <div class="cv-privacy-desc">Protección de Datos Personales de Argentina. Consentimiento digital de tutores para datos de menores.</div>
            </div>
          </div>
          <div class="cv-privacy-item">
            <div class="cv-privacy-icon">🔑</div>
            <div>
              <div class="cv-privacy-title">Autenticación robusta</div>
              <div class="cv-privacy-desc">JWT con refresh tokens. 2FA obligatorio para el Admin. Roles y permisos validados en cada endpoint.</div>
            </div>
          </div>
          <div class="cv-privacy-item">
            <div class="cv-privacy-icon">📋</div>
            <div>
              <div class="cv-privacy-title">Auditoría inmutable</div>
              <div class="cv-privacy-desc">Log de acciones críticas: aprobación KYC, habilitación de aulas, acceso a datos sensibles de alumnos.</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ROADMAP -->
      <section class="cv-roadmap">
        <div class="cv-section-label">Roadmap de Desarrollo</div>
        <h2>MVP funcional. Evolución controlada.</h2>
        <p class="cv-section-intro">Cuatro fases que permiten lanzar rápido e incorporar complejidad de forma progresiva.</p>
        <div class="cv-phases">
          <div class="cv-phase phase1">
            <div class="cv-phase-tag">Fase 1 — MVP</div>
            <div class="cv-phase-title">Institucional + Registro</div>
            <ul>
              <li>Alta de colegios y docentes</li>
              <li>KYC básico con aprobación manual</li>
              <li>Registro de alumnos con código</li>
              <li>Login seguro y gestión de roles</li>
            </ul>
          </div>
          <div class="cv-phase phase2">
            <div class="cv-phase-tag">Fase 2 — Core</div>
            <div class="cv-phase-title">Sociograma + Contenido</div>
            <ul>
              <li>Encuesta sociométrica completa</li>
              <li>Algoritmo de procesamiento</li>
              <li>Mapa de red visual</li>
              <li>Módulo de contenido inicial</li>
            </ul>
          </div>
          <div class="cv-phase phase3">
            <div class="cv-phase-tag">Fase 3 — Reportes</div>
            <div class="cv-phase-title">Alertas + PDF</div>
            <ul>
              <li>Dashboard del docente</li>
              <li>Alertas automáticas por riesgo</li>
              <li>Reporte PDF descargable</li>
              <li>Encuesta para familias</li>
            </ul>
          </div>
          <div class="cv-phase phase4">
            <div class="cv-phase-tag">Fase 4 — Evolución</div>
            <div class="cv-phase-title">Features Avanzados</div>
            <ul>
              <li>Sociograma histórico evolutivo</li>
              <li>Integración con orientación</li>
              <li>App móvil nativa</li>
              <li>Gamificación para alumnos</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- CTA FINAL -->
      <section class="cv-cta">
        <h2>¿Tu colegio quiere sumarse?</h2>
        <p>Ingresá con tu cuenta para acceder a la plataforma o contactanos para comenzar el proceso de incorporación.</p>
      </section>

      <!-- FOOTER -->
      <footer class="cv-footer">
        <span>© 2025 ConVivir — Plataforma de Convivencia Escolar</span>
        <span>Confidencial · v1.0 · Borrador Inicial</span>
      </footer>

    </div>
    """, unsafe_allow_html=True)

    # ── Botón de login flotante (arriba a la derecha) ─────────────────────────
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div:first-child {
        position: fixed; top: 14px; right: 56px; z-index: 200;
    }
    </style>
    """, unsafe_allow_html=True)

    col_spacer, col_btn = st.columns([12, 1])
    with col_btn:
        if st.button("Ingresar →", type="primary", key="open_login"):
            st.session_state.show_login_panel = True
            st.rerun()

    # ── Panel de login superpuesto ────────────────────────────────────────────
    if st.session_state.show_login_panel:
        st.markdown("""
        <style>
        .login-overlay {
            position: fixed; inset: 0; z-index: 999;
            background: rgba(4,14,31,0.75); backdrop-filter: blur(8px);
            display: flex; align-items: center; justify-content: center;
        }
        </style>
        <div class="login-overlay"></div>
        """, unsafe_allow_html=True)

        with st.container():
            col1, col2, col3 = st.columns([1, 1.2, 1])
            with col2:
                with st.container(border=True):
                    st.markdown("### 🕸️ Iniciar sesión en ConVivir")
                    email    = st.text_input("Email", placeholder="usuario@ejemplo.ar", key="login_email")
                    password = st.text_input("Contraseña", type="password", key="login_pass")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("Ingresar", type="primary", use_container_width=True, key="do_login"):
                            user = USERS.get(email)
                            if user and user["password"] == password:
                                st.session_state.logged_in = True
                                st.session_state.show_login_panel = False
                                st.session_state.user = {
                                    "email": email,
                                    "role": user["role"],
                                    "name": user["name"],
                                }
                                st.rerun()
                            else:
                                st.error("Email o contraseña incorrectos.")
                    with col_b:
                        if st.button("Cancelar", use_container_width=True, key="cancel_login"):
                            st.session_state.show_login_panel = False
                            st.rerun()

                    st.markdown("---")
                    st.markdown("**Usuarios de prueba:**")
                    st.code("admin@convivir.ar   / admin123\ndocente@colegio.ar  / docente123\nalumno@colegio.ar   / alumno123")

# ── Sidebar con navegación ────────────────────────────────────────────────────
def show_sidebar():
    user = st.session_state.user
    role = user["role"]

    with st.sidebar:
        st.markdown(f"## 🕸️ ConVivir")
        st.markdown("---")
        st.markdown(f"👤 **{user['name']}**")
        badge = {"admin": "badge-admin", "teacher": "badge-teacher", "student": "badge-student"}[role]
        labels = {"admin": "Administrador", "teacher": "Docente", "student": "Alumno"}
        st.markdown(f"<span class='{badge}'>{labels[role]}</span>", unsafe_allow_html=True)
        st.markdown("---")

        if role == "admin":
            pages = {
                "🏛️ Dashboard Admin": "admin_dashboard",
                "🏫 Colegios": "admin_colegios",
                "👨‍🏫 Docentes": "admin_docentes",
                "✅ KYC / Validaciones": "admin_kyc",
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

        if "current_page" not in st.session_state:
            st.session_state.current_page = list(pages.values())[0]

        for label, key in pages.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()

        st.markdown("---")
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.current_page = None
            st.rerun()

# ── Router de páginas ─────────────────────────────────────────────────────────
def route():
    page = st.session_state.get("current_page", "")
    role = st.session_state.user["role"]

    # Admin
    if page == "admin_dashboard" or (role == "admin" and not page):
        from pages import admin_dashboard; admin_dashboard.render()
    elif page == "admin_colegios":
        from pages import admin_colegios; admin_colegios.render()
    elif page == "admin_docentes":
        from pages import admin_docentes; admin_docentes.render()
    elif page == "admin_kyc":
        from pages import admin_kyc; admin_kyc.render()

    # Docente
    elif page == "teacher_dashboard" or (role == "teacher" and not page):
        from pages import teacher_dashboard; teacher_dashboard.render()
    elif page == "teacher_aulas":
        from pages import teacher_aulas; teacher_aulas.render()
    elif page == "teacher_sociograma":
        from pages import teacher_sociograma; teacher_sociograma.render()
    elif page == "teacher_alertas":
        from pages import teacher_alertas; teacher_alertas.render()
    elif page == "teacher_reportes":
        from pages import teacher_reportes; teacher_reportes.render()

    # Alumno
    elif page == "student_home" or (role == "student" and not page):
        from pages import student_home; student_home.render()
    elif page == "student_encuesta":
        from pages import student_encuesta; student_encuesta.render()
    elif page == "student_contenido":
        from pages import student_contenido; student_contenido.render()

# ── Main ──────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    show_login()
else:
    show_sidebar()
    route()
