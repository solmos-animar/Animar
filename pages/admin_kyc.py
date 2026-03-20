import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.mock_data import DOCENTES


def render():
    st.title("✅ KYC — Validación de Docentes")
    st.info("Revisá y aprobá la documentación enviada por los docentes para habilitarlos en la plataforma.")

    pendientes = [d for d in DOCENTES if d["kyc"] in ("Pendiente", "En revisión")]

    if not pendientes:
        st.success("🎉 No hay solicitudes KYC pendientes.")
        return

    st.markdown(f"**{len(pendientes)} solicitud(es) pendiente(s)**")

    for d in pendientes:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {d['nombre']}")
                st.markdown(f"📧 {d['email']} &nbsp;|&nbsp; 🏫 {d['colegio']}")
                st.markdown(f"Estado KYC: **{d['kyc']}**")

            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✅ Aprobar", key=f"kyc_ok_{d['id']}", type="primary", use_container_width=True):
                    st.success(f"✅ {d['nombre']} aprobado (demo)")
                if st.button("❌ Rechazar", key=f"kyc_rej_{d['id']}", use_container_width=True):
                    st.error(f"❌ {d['nombre']} rechazado (demo)")

            # Simular documentos adjuntos
            st.markdown("**Documentos adjuntos:**")
            doc_col1, doc_col2, doc_col3 = st.columns(3)
            doc_col1.markdown("📄 DNI_frente.pdf ✅")
            doc_col2.markdown("📄 Título_docente.pdf ✅")
            doc_col3.markdown("📄 Constancia_laboral.pdf ⏳")
            st.markdown("---")
