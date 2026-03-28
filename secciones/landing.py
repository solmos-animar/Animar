import streamlit as st

def show_landing():
    # Nota: No dejes espacios al inicio de cada línea de HTML dentro de f"""
    st.markdown(f"""
<div style="padding: 100px 56px;">
    <div style="max-width: 1200px;">
        <span style="background: rgba(26,111,255,0.1); color: #60a5fa; padding: 6px 14px; border-radius: 100px; font-size: 12px; font-weight: 700; text-transform: uppercase;">Documento de Análisis y Diseño</span>
        <h1 style="font-family: 'Sora', sans-serif; font-size: 64px; color: white; margin: 20px 0;">ConVivir<br>Plataforma de Convivencia</h1>
        <p style="font-size: 20px; color: rgba(221,232,248,0.6); max-width: 800px;">Solución digital para instituciones educativas orientada a prevenir bullying y detectar dinámicas de exclusión.</p>
        
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 60px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 40px;">
            <div><div style="font-size: 32px; font-weight: 800; color: white;">1 de 3.</div><div style="font-size: 13px; color: rgba(221,232,248,0.4);">alumnos vive o presencia situaciones de bullying</div></div>
            <div><div style="font-size: 32px; font-weight: 800; color: white;">24+</div><div style="font-size: 13px; color: rgba(221,232,248,0.4);">pantallas y flujos diseñados</div></div>
            <div><div style="font-size: 32px; font-weight: 800; color: white;">5.</div><div style="font-size: 13px; color: rgba(221,232,248,0.4);">módulos integrados</div></div>
            <div><div style="font-size: 32px; font-weight: 800; color: white;">4.</div><div style="font-size: 13px; color: rgba(221,232,248,0.4);">actores del sistema</div></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
