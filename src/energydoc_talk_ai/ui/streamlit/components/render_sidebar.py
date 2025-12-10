import streamlit as st
from datetime import datetime
from energydoc_talk_ai.ui.streamlit.components.setup_session_state import init_session_state
from energydoc_talk_ai.ingestion.vector_store import delete_pinecone_index

def render_sidebar():
    with st.sidebar:

        # ------------------------------------------------------------------
        # LOGO DU PROJET
        # ------------------------------------------------------------------
        st.image(
            "EnergyDocTalk-AI.png",  # Ton logo
            width="stretch",
            caption="EnergyDocTalk AI — Document Intelligence"
        )

        # ------------------------------------------------------------------
        # INFORMATIONS PRINCIPALES
        # ------------------------------------------------------------------
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 18px; margin-top: 15px;">
                <b>📄 EnergyDocTalk AI</b><br/>
                Version : <b>1.0.0</b><br/>
                📅 Créé le : <b>2025-11-22</b><br/>
                🔄 Dernière mise à jour : <b>{datetime.now().strftime("%Y-%m-%d")}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.write("### ⚙️ Paramètres de l'application")
        enable_chat = st.toggle("Activer le Chatbot 🤖")
        if enable_chat:
            st.success("✔ Chatbot activé ! Vous pouvez poser vos questions.")
  
        st.markdown("---")
        # ------------------------------------------------------------------
        # DESCRIPTION DU PROJET
        # ------------------------------------------------------------------
        st.markdown(
            """
            ### 🧠 À propos du projet

            **EnergyDocTalk AI** est un assistant intelligent basé sur une architecture  
            **RAG (Retrieval-Augmented Generation)** utilisant :

            - 📘 Extraction & chunking PDF  
            - 🔤 *Google Generative AI Embeddings*  
            - 📦 *Pinecone Vector Database*  
            - ⚡ *LLaMA 3 sur Groq*  
            - 🧩 *LangChain* pour orchestrer le RAG  

            Il permet de :
            - 🔎 Rechercher efficacement dans des documents PDF  
            - 💬 Poser des questions et obtenir des réponses fiables  
            - 📚 Afficher les sources et pages utilisées  
            """
        )

        st.markdown("---")
        # ------------------------------------------------------------------
        # AUTEUR & CONTACT
        # ------------------------------------------------------------------
        st.markdown(
            """
            ### 👤 Auteur
            **Rostand Surel Manda**

            ### 📬 Contact
            - 📞 Téléphone : 07 53 35 61 06  
            - 📧 Email : **rostandsurel@yahoo.com**  
            - 🐙 GitHub : [Manda404](https://github.com/Manda404)  
            - 💼 LinkedIn : [Rostand Surel](https://www.linkedin.com/in/rostand-surel/)  

            ---
            🚀 *PDFTalk AI — Votre assistant intelligent pour les documents PDF*
            """
        )

        st.markdown("---")
        # ------------------------------------------------------------------
        # BOUTON POUR RÉINITIALISER L'APPLICATION
        if st.button("Réinitialiser l'application"):
            # Réinitialiser l'état de session
            for key in st.session_state.keys(): 
                del st.session_state[key]

            # Supprimer l'index Pinecone
            try:
                delete_pinecone_index()
                st.success("L'index Pinecone a été supprimé avec succès.")
            except Exception as e:
                st.error(f"Erreur lors de la suppression de l'index Pinecone : {e}")
            st.rerun()