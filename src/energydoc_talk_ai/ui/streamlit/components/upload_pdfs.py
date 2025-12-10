import streamlit as st
"""
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

"""

import streamlit as st

def render_upload_section():
    # Créer un expander pour contenir toute la section d'upload
    # J'utilise 'expanded=True' par défaut pour que l'utilisateur voie la zone au début.
    with st.expander("📂 Upload de PDF", expanded=True) as expander:
        
        # Le header n'est plus nécessaire à l'intérieur car l'expander sert de titre.
        # st.header("📂 Upload de PDF") 

        files = st.file_uploader("Upload PDF", 
                                 type="pdf", 
                                 accept_multiple_files=True, 
                                 key="uploader_widget")

        if files:
            st.session_state.uploaded_pdfs = files
            st.session_state.flag_uploaded_pdfs = True
            
            # Afficher le succès et Fermer l'expander automatiquement après l'upload
            st.success(f"{len(files)} fichier(s) PDF uploadé(s) avec succès")
            
            # 💡 Astuce intelligente : Fermer l'expander une fois les fichiers téléchargés
            # pour donner plus d'espace aux étapes suivantes.
            # Cependant, Streamlit ne permet pas de modifier l'état 'expanded' directement 
            # dans un callback ou après l'affichage du widget. 
            # On peut simplement laisser le message de succès visible, ce qui est déjà bien.
            
        else:
            st.info("Aucun fichier PDF uploadé pour le moment.")
            st.session_state.flag_uploaded_pdfs = False
            
    # Si les fichiers sont uploadés, on peut afficher un résumé à l'extérieur de l'expander
    # pour que l'utilisateur se souvienne du nombre de fichiers, même si l'expander est fermé.
    if 'flag_uploaded_pdfs' in st.session_state and st.session_state.flag_uploaded_pdfs:
        st.write(f"**{len(st.session_state.uploaded_pdfs)}** PDF(s) prêt(s) pour le traitement.")