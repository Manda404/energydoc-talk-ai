import streamlit as st
from energydoc_talk_ai.ingestion.vector_store import check_pinecone_index_exists

def init_session_state():
    """
    Initialise toutes les variables essentielles du session_state
    pour éviter les erreurs d'attribut manquant.
    """
    defaults = {
            # Indique si le processus d'ingestion (lecture, embedding, stockage Pinecone) est terminé.
            "ingestion_done": False, 
            # Liste des messages (utilisateur/assistant) pour le chat.
            "messages": [],
            # Liste des objets fichiers PDF uploadés par l'utilisateur.
            "uploaded_pdfs": [],
            # Flag pour indiquer si des fichiers PDF ont été uploadés dans la session.
            "flag_uploaded_pdfs": False,
            # Flag pour indiquer si l'index vectoriel Pinecone existe déjà.
            "flag_index_exists": check_pinecone_index_exists(),
            
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
