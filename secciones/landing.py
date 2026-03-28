import streamlit as st

def show_landing():
    st.markdown("""
<div style="max-width: 1000px;">
    <span style="background: rgba(26,111,255,0.1); color: #60a5fa; padding: 6px 14px; border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase;">Documento de Análisis y Diseño</span>
    <h1 style="font-family: 'Sora', sans-serif; font-size: 56px; color: white; margin: 24px 0;">Prevención del bullying<br>basada en datos</h1>
    <p style="font-size: 18px; color: rgba(221,232,248,0.6); line-height: 1.6;">Solución digital para instituciones educativas orientada a prevenir bullying, detectar dinámicas de exclusión y ofrecer herramientas concretas.</p>
    
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 50px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 40px;">
        <div><div style="font-size: 28px; font-weight: 800; color: white;">1 de 3.</div><div style="font-size: 12px; color: rgba(221,232,248,0.4);">alumnos vive o presencia bullying</div></div>
        <div><div style="font-size: 28px; font-weight: 800; color: white;">24+</div><div style="font-size: 12px; color: rgba(221,232,248,0.4);">pantallas diseñadas</div></div>
        <div><div style="font-size: 28px; font-weight: 800; color: white;">5.</div><div style="font-size: 12px; color: rgba(221,232,248,0.4);">módulos integrados</div></div>
        <div><div style="font-size: 28px; font-weight: 800; color: white;">4.</div><div style="font-size: 12px; color: rgba(221,232,248,0.4);">actores del sistema</div></div>
    </div>
</div>
""", unsafe_allow_html=True)
