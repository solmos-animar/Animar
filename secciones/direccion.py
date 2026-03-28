import streamlit as st

def render():
    # Header con Pill (Etiqueta)
    st.markdown('<span class="cv-pill pill-green">Institución</span>', unsafe_allow_html=True)
    st.markdown('<h1>Panel de Dirección</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6b7280; font-size: 18px;">Vista global del clima escolar y estado de implementación de ConVivir.</p>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    # ── Métricas Rápidas ──────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        {"label": "Instituciones", "val": "1", "color": "#1a56a0"},
        {"label": "Aulas Activas", "val": "12", "color": "#1d7a55"},
        {"label": "Alumnos", "val": "342", "color": "#0f2240"},
        {"label": "Alertas", "val": "3", "color": "#d4580a"}
    ]

    for i, m in enumerate([col1, col2, col3, col4]):
        with m:
            st.markdown(f"""
                <div class="cv-card" style="padding: 20px; text-align: center;">
                    <span style="font-size: 12px; text-transform: uppercase; color: #6b7280; letter-spacing: 0.1em;">{metrics[i]['label']}</span>
                    <div style="font-size: 32px; font-weight: 800; color: {metrics[i]['color']}; margin-top: 5px;">{metrics[i]['val']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    # ── Cuerpo Principal ──────────────────────────────────────────────────
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.markdown("""
            <div class="cv-card">
                <h3>🏫 Estado de las Aulas</h3>
                <p style="font-size: 14px; color: #6b7280;">Seguimiento del progreso de encuestas sociométricas por curso.</p>
                <hr style="margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <div><strong>3° Año "A" - Primaria</strong><br><span style="font-size: 12px; color: #6b7280;">Docente: Marta Gómez</span></div>
                    <span class="cv-pill pill-green">85% completado</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <div><strong>4° Año "B" - Primaria</strong><br><span style="font-size: 12px; color: #6b7280;">Docente: Roberto Peña</span></div>
                    <span class="cv-pill pill-orange">40% en progreso</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div><strong>5° Año "A" - Primaria</strong><br><span style="font-size: 12px; color: #6b7280;">Docente: Lucía Fernández</span></div>
                    <span class="cv-pill pill-blue">Pendiente</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown("""
            <div class="cv-card" style="border-left: 5px solid #d4580a;">
                <h3 style="color: #d4580a;">⚠️ Alertas Recientes</h3>
                <p style="font-size: 14px; color: #6b7280;">Casos detectados que requieren revisión del equipo directivo.</p>
                <div style="background: #fff1e8; padding: 12px; border-radius: 12px; margin-top: 15px;">
                    <strong style="color: #d4580a; font-size: 13px;">Aislamiento detectado</strong>
                    <p style="font-size: 12px; margin: 5px 0;">Un alumno en 3°A no ha sido seleccionado en ninguna dinámica positiva.</p>
                </div>
                <div style="background: #f3f4f6; padding: 12px; border-radius: 12px; margin-top: 10px;">
                    <strong style="color: #0f2240; font-size: 13px;">Mensaje Confidencial</strong>
                    <p style="font-size: 12px; margin: 5px 0;">Nuevo mensaje de ayuda recibido en 4°B dirigido al docente.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Botón de acción institucional
    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("Generar Reporte Mensual PDF", use_container_width=True, type="primary"):
        st.success("Reporte generado con éxito (Simulación)")
