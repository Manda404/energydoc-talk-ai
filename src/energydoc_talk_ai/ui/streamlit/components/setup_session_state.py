import streamlit as st


def init_session_state():
    """
    Initialise toutes les variables essentielles du session_state
    pour éviter les erreurs d'attribut manquant.
    """
    defaults = {
        "ingestion_done": False,
        "messages": [],
        "uploaded_pdfs": [],
        "flag_uploaded_pdfs": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
