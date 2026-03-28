import streamlit as st

def show_landing():
    # Estructura compacta y limpia
    st.markdown(f"""
    <div class="cv">
      <section class="cv-hero">
        <div class="cv-hero-inner">
          <div>
            <div class="cv-tag">Plataforma de Convivencia Escolar</div>
            <h1>Prevención del bullying<br><em>basada en datos</em><br>para colegios</h1>
            <p class="cv-hero-sub">ConVivir combina sociogramas de aula, contenido educativo y gestión institucional para que docentes detecten situaciones de acoso antes de que escalen.</p>
          </div>
          <div class="cv-logo-hero">
            </div>
        </div>
        
        <div class="cv-stats">
          <div class="cv-stat">
            <div class="cv-stat-n">1 de 3<b>.</b></div>
            <div class="cv-stat-l">alumnos vive o presencia situaciones de bullying</div>
          </div>
          <div class="cv-stat">
            <div class="cv-stat-n">24<b>+</b></div>
            <div class="cv-stat-l">pantallas y flujos diseñados en el MVP</div>
          </div>
          <div class="cv-stat">
            <div class="cv-stat-n">5<b>.</b></div>
            <div class="cv-stat-l">módulos integrados: Admin, Aulas, Sociograma...</div>
          </div>
          <div class="cv-stat">
            <div class="cv-stat-n">4<b>.</b></div>
            <div class="cv-stat-l">actores del sistema con flujos diferenciados</div>
          </div>
        </div>
      </section>

      <section class="cv-s">
        <div class="cv-eyebrow">El Problema</div>
        <h2>El bullying existe.<br>El problema es que no lo vemos.</h2>
        <div class="pg">
          <div class="pc"><h3>👁️ Dinámica invisible</h3><p>Los docentes no tienen forma objetiva de ver quién está aislado en el aula.</p><div class="pc-stat">70%</div></div>
          <div class="pc"><h3>⏱️ Intervención tardía</h3><p>Cuando el problema se hace visible, el daño ya ocurrió.</p><div class="pc-stat">6 meses</div></div>
          <div class="pc"><h3>🧩 Fragmentación</h3><p>Faltan plataformas que integren diagnóstico y seguimiento.</p><div class="pc-stat">0</div></div>
        </div>
      </section>

      <footer class="cv-ft">
        <span>© 2026 ConVivir — Confidencial</span>
        <span>v1.1 · Marzo 2026</span>
      </footer>
    </div>
    """, unsafe_allow_html=True)
