import streamlit as st

def show_landing():
    # Usamos un solo st.markdown con unsafe_allow_html=True
    # para renderizar todo el HTML de la landing.
    
    st.markdown("""
<div class="landing-content">
  <section class="landing-hero">
    <div class="hero-inner">
      <div class="hero-text">
        <span class="pilla pilla-blue">Documento de Análisis y Diseño</span>
        <h1 class="landing-h1">Prevención del bullying<br>basada en datos</h1>
        <p class="landing-lead">ConVivir combina sociogramas de aula, contenido educativo y gestión institucional para que docentes detecten situaciones de acoso antes de que escalen.</p>
      </div>
    </div>
    
    <div class="landing-grid landing-grid-4 stats-bar">
      <div class="stat-card">
        <div class="stat-value">1 de 3.</div>
        <div class="stat-label">alumnos vive o presencia situations de bullying</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">24+</div>
        <div class="stat-label">pantallas y flujos diseñados</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">5.</div>
        <div class="stat-label">módulos integrados</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">4.</div>
        <div class="stat-label">actores con flujos</div>
      </div>
    </div>
  </section>

  <section class="landing-section">
    <div class="eyebrow">El Problema</div>
    <h2 class="landing-h2">El bullying existe.<br>El problema es que no lo vemos.</h2>
    <p class="landing-section-intro">Sin herramientas adecuadas, los docentes actúan cuando el daño ya ocurrió. La dinámica social del aula es invisible hasta que se vuelve urgente.</p>
    
    <div class="landing-grid landing-grid-3">
      <div class="card">
        <h4>👁️ Dinámica invisible</h4>
        <p>Los docentes no tienen forma objetiva de ver quién está aislado en el aula.</p>
        <div class="stat-value" style="font-size: 32px; color: #4a9eff; margin-top:20px;">70%</div>
      </div>
      <div class="card">
        <h4>⏱️ Intervención tardía</h4>
        <p>Cuando el problema se hace visible, el daño ya ocurrió.</p>
        <div class="stat-value" style="font-size: 32px; color: #4a9eff; margin-top:20px;">6 meses</div>
      </div>
      <div class="card">
        <h4>🧩 Fragmentación</h4>
        <p>No existe una plataforma que integre diagnóstico y seguimiento.</p>
        <div class="stat-value" style="font-size: 32px; color: #4a9eff; margin-top:20px;">0</div>
      </div>
    </div>
  </section>

  <footer class="landing-footer">
    <div class="footer-content">
      <span>© 2026 ConVivir — Plataforma de Convivencia Escolar</span>
      <span>Confidencial · v1.1 · Borrador Inicial</span>
    </div>
  </footer>
</div>
""", unsafe_allow_html=True)
