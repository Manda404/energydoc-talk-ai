import streamlit as st
from energydoc_talk_ai.ingestion.pipeline import ingestion_pipeline_ram

def render_ingestion_button():
    #st.header("⚙️ 2. Ingestion RAG")

    if st.button("🚀 Lancer l'ingestion", type="primary"):
        if not st.session_state.get("uploaded_pdfs"):
            st.warning("Tu dois d'abord uploader au moins un PDF.")
            st.session_state.flag_upload_pdfs = False
            return

        with st.spinner("Ingestion en cours (extraction, chunking, Pinecone)…"):
            try:
                if st.session_state.uploaded_pdfs:
                    pdfs_ram = [(f.name, f.read()) for f in st.session_state.uploaded_pdfs]
                    ingestion_pipeline_ram(pdfs_ram)
                    st.session_state.ingestion_done = True
                    st.success("Ingestion terminée ✅")
            except Exception as e:
                st.error(f"Erreur durant l'ingestion : {e}")