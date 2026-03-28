import streamlit as st

def show_landing():
    # Usamos st.write con unsafe_allow_html=False para los SVGs y True para el contenedor
    # para evitar que Streamlit "escupa" el código como texto.
    
    # IMPORTANTE: Reemplazo el multiline string complejo por una estructura que Streamlit no confunda
    content = """
    <div style="background-color: #03091a; color: #dde8f8; padding: 60px; min-height: 100vh; font-family: 'DM Sans', sans-serif;">
        <span style="background: rgba(26,111,255,0.1); color: #60a5fa; padding: 6px 14px; border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase;">Documento de Análisis y Diseño</span>
        <h1 style="font-family: 'Sora', sans-serif; font-size: 56px; color: white; margin: 24px 0;">Prevención del bullying<br><span style="color:#4a9eff">basada en datos</span></h1>
        <p style="font-size: 18px; color: rgba(221,232,248,0.6); max-width: 800px; line-height:1.6;">ConVivir combina sociogramas de aula, contenido educativo y gestión institucional para que docentes detecten situaciones de acoso antes de que escalen.</p>
        
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 50px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 40px;">
            <div><div style="font-size: 28px; font-weight: 800; color: white;">1 de 3.</div><div style="font-size: 12px; color: rgba(221,232,248,0.4);">alumnos vive o presencia situaciones de bullying</div></div>
            <div><div style="font-size: 28px; font-weight: 800; color: white;">24+</div><div style="font-size: 12px; color: rgba(221,232,248,0.4);">pantallas y flujos diseñados en el MVP</div></div>
            <div><div style="font-size: 28px; font-weight: 800; color: white;">5.</div><div style="font-size: 12px; color: rgba(221,232,248,0.4);">módulos integrados: Admin · Aulas · Sociograma · Contenido · Reportes</div></div>
            <div><div style="font-size: 28px; font-weight: 800; color: white;">4.</div><div style="font-size: 12px; color: rgba(221,232,248,0.4);">actores del sistema con flujos diferenciados</div></div>
        </div>

        <h2 style="margin-top:80px; font-family: 'Sora', sans-serif; color: white;">El Problema</h2>
        <p style="color: rgba(221,232,248,0.6);">Sin herramientas adecuadas, los docentes actúan cuando el daño ya ocurrió.</p>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px;">
            <div style="background: rgba(255,255,255,0.03); padding: 24px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
                <h3 style="color:white;">👁️ Dinámica invisible</h3>
                <p style="font-size:14px; color: rgba(221,232,248,0.5);">Los docentes no tienen forma objetiva de ver quién está aislado.</p>
            </div>
            <div style="background: rgba(255,255,255,0.03); padding: 24px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
                <h3 style="color:white;">⏱️ Intervención tardía</h3>
                <p style="font-size:14px; color: rgba(221,232,248,0.5);">Cuando el problema se hace visible, el daño ya ocurrió.</p>
            </div>
            <div style="background: rgba(255,255,255,0.03); padding: 24px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
                <h3 style="color:white;">🧩 Fragmentación</h3>
                <p style="font-size:14px; color: rgba(221,232,248,0.5);">No existe una plataforma que integre diagnóstico y seguimiento.</p>
            </div>
        </div>
    </div>
    """
    st.markdown(content, unsafe_allow_html=True)
