import streamlit as st

from energydoc_talk_ai.ui.streamlit.components.setup_session_state import init_session_state
from energydoc_talk_ai.ui.streamlit.components.render_sidebar import render_sidebar
from energydoc_talk_ai.ui.streamlit.components.render_ingestion import render_ingestion_button
from energydoc_talk_ai.ui.streamlit.components.upload_pdfs import render_upload_section
from energydoc_talk_ai.ui.streamlit.components.chat_box import render_chat_box

# -------------------------------------------------------------------------------

def main():
    st.set_page_config(
        page_title="EnergyDocTalk AI – Assistant RAG",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()
    render_sidebar()

    st.title("📄 EnergyDocTalk AI — Assistant RAG Intelligen 🧠")
    st.write(
        "**Upload tes PDF, lance l’ingestion, et pose n’importe quelle question !**\n"
        "Ce chatbot utilise un pipeline RAG complet (LangChain + Pinecone + Google Embeddings + Groq LLaMA3)."
    )

    render_upload_section()
    if st.session_state.flag_uploaded_pdfs:
        render_ingestion_button()

    if st.session_state.ingestion_done:
        render_chat_box()


if __name__ == "__main__":
    main()
