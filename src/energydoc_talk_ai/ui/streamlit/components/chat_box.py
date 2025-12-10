import streamlit as st
from energydoc_talk_ai.rag.rag_pipeline import get_rag_chain


USER_COLOR = "#DCF8C6"       # vert clair style WhatsApp
ASSISTANT_COLOR = "#F1AE1D"  # blanc
BOX_BG = "#4FB713"


def render_chat_box():
    # Utilisation de st.expander pour contenir tout le chat
    # On le définit comme ouvert (True) pour que l'utilisateur puisse interagir immédiatement.
    with st.expander("💬 Discussion avec les PDF", expanded=True):
        
        # Le st.header a été retiré, le titre de l'expander suffit
        
        #if not st.session_state.ingestion_done or not st.session_state.flag_index_exists:
        if not st.session_state.flag_index_exists:
            st.warning("⚠️ Tu dois d'abord ingérer des PDFs avant de poser des questions.")
            return

        # Initialisation du chat
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # --- Styles CSS (inchangés) ---
        st.markdown(
            """
            <style>
            .chat-message {
                padding: 12px;
                margin: 8px;
                border-radius: 12px;
                max-width: 75%;
            }
            .user-msg {
                background-color: #DCF8C6;
                margin-left: auto;
                text-align: right;
            }
            .assistant-msg {
                background-color: #F1AE1D;
                margin-right: auto;
                text-align: left;
            }
            .chat-box {
                background-color: #F7F7F7;
                padding: 15px;
                border-radius: 12px;
                max-height: 550px;
                overflow-y: auto;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Zone chat-box visuelle
        # Le conteneur et l'affichage des messages sont maintenus dans l'expander
        with st.container():
            st.markdown('<div class="main-header">⚡️ EnergyDoc Chat AI</div>', unsafe_allow_html=True)
            
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="chat-message user-msg">🧑 {msg["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="chat-message assistant-msg"> 🤖 {msg["content"]}</div>',
                        unsafe_allow_html=True,
                    )
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Le formulaire est placé directement sous les messages, toujours dans l'expander
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Pose ta question :", "")
            submitted = st.form_submit_button("Envoyer")

        # --- Traitement de la question (inchangé) ---
        if submitted and user_input:
            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )

            rag = get_rag_chain()

            with st.spinner("Analyse des documents…"):
                result = rag({"query": user_input})

            answer = result["result"]
            sources = result["source_documents"]

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

            st.session_state.last_sources = sources
            st.rerun()

    # --- Sources (Restent à l'extérieur, sous le Chat) ---
    # Le expander pour les sources est généralement mieux en dehors du expander principal
    # du chat pour ne pas le surcharger visuellement.
    if "last_sources" in st.session_state:
        with st.expander("📚 Sources utilisées"):
            for doc in st.session_state.last_sources:
                # Ajout d'une ligne pour séparer les sources pour plus de clarté
                st.markdown("---") 
                st.markdown(f"- **Source** : {doc.metadata.get('source')}")
                st.code(doc.page_content[:400])