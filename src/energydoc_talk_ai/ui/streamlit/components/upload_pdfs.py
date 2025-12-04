import streamlit as st

def render_upload_section():
    st.header("📂 Upload de PDF")

    files = st.file_uploader("Upload PDF", type="pdf", accept_multiple_files=True, key="uploader_widget")

    if files:
        st.session_state.uploaded_pdfs = files
        st.session_state.flag_uploaded_pdfs = True
        st.success(f"{len(files)} fichier(s) PDF uploadé(s) avec succès")
    else:
        st.info("Aucun fichier PDF uploadé pour le moment.")
        st.session_state.flag_uploaded_pdfs = False
