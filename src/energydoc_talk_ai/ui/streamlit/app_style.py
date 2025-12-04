import streamlit as st
from typing import Dict, Any, List

# --- NOUVELLES COULEURS & STYLING PLUS MODERNE (CORRIGÉ) ---
# Inspiré d'un thème "AI moderne"
PRIMARY_COLOR = "#007BFF"     # Bleu vif pour l'accent
BACKGROUND_COLOR = "#F8F9FA"  # Gris très clair pour le fond de l'app
CHAT_BG = "#FFFFFF"           # Blanc pour la zone de chat principale
USER_MSG_COLOR = "#DCEAFE"    # Bleu pastel pour l'utilisateur
ASSISTANT_MSG_COLOR = "#F1F3F5" # Gris clair doux pour l'assistant
TEXT_COLOR = "#212529"        # Couleur de texte sombre pour un bon contraste


# --- CLASSES MOCK (SIMULATION) ---

class MockDoc:
    """Simule un document source (chunk) retourné par le RAG."""
    def __init__(self, source: str, page: int, content: str):
        self.metadata = {"source": source, "page": page}
        self.page_content = content + " [Contenu tronqué pour l'exemple...]"

class MockRAG:
    """Simule la chaîne RAG pour la démonstration de l'interface."""
    def __call__(self, input_dict: Dict[str, str]) -> Dict[str, Any]:
        query = input_dict["query"]
        
        # Logique de réponse simulée
        if "ingestion" in query.lower():
            return {
                "result": "L'ingestion des documents est la première étape du processus RAG, où les PDF sont analysés, découpés et stockés sous forme d'embeddings vectoriels pour une recherche sémantique efficace.",
                "source_documents": [
                    MockDoc("Processus RAG V1.pdf", 12, "L'ingestion est l'étape initiale..."),
                    MockDoc("Guide d'utilisation 2024.pdf", 5, "Les documents sont 'chunkés'...")
                ]
            }
        return {
            "result": f"C'est une excellente question sur '{query}'. L'analyse montre que le sujet est traité dans plusieurs de vos documents sources. L'IA a trouvé la meilleure réponse.",
            "source_documents": [
                MockDoc("Source A.pdf", 3, "Le contenu de la page 3 est très pertinent..."),
                MockDoc("Source B.pdf", 7, "Une mention de ce sujet est trouvée ici...")
            ]
        }
            
def get_rag_chain() -> MockRAG:
    """Retourne la chaîne RAG (ici, la classe de mock)."""
    # En production, cela retournerait la véritable chaîne RAG
    return MockRAG()


# --- FONCTION PRINCIPALE DU CHAT STYLÉ ---

def render_chat_box_styled():
    """Affiche et gère l'interface de chat stylée."""
    
    # 1. Injection du CSS stylé
    st.markdown(
        f"""
        <style>
        /* Surcharge du fond principal de la page */
        .stApp {{
            background-color: {BACKGROUND_COLOR};
        }}

        /* Style global pour la zone de chat */
        .chat-container {{
            background-color: {CHAT_BG};
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); /* Ombre douce */
            padding: 15px;
            height: 60vh; 
            max-height: 550px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
            scrollbar-width: thin; /* Firefox */
            scrollbar-color: {PRIMARY_COLOR} {CHAT_BG};
        }}
        
        /* Style des messages */
        .chat-message {{
            padding: 10px 15px;
            border-radius: 20px;
            max-width: 85%;
            font-size: 15px;
            line-height: 1.5;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08); /* Ombre légère pour les bulles */
        }}

        /* Message Utilisateur (aligné à droite) */
        .user-msg {{
            background-color: {USER_MSG_COLOR};
            color: {TEXT_COLOR};
            margin-left: auto;
            border-bottom-right-radius: 4px; /* Coin cassé */
        }}
        
        /* Message Assistant (aligné à gauche) */
        .assistant-msg {{
            background-color: {ASSISTANT_MSG_COLOR};
            color: {TEXT_COLOR};
            margin-right: auto;
            border-bottom-left-radius: 4px; /* Coin cassé */
        }}
        
        /* Bar de saisie (text_input) */
        div.stTextInput > div > div > input {{
            border-radius: 25px;
            border: 1px solid #CED4DA;
            padding: 10px 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) inset;
        }}

        /* Bouton "Envoyer" stylisé */
        .stButton>button {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border-radius: 25px;
            padding: 10px 20px;
            font-weight: bold;
            border: none;
            transition: background-color 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #0056b3; 
        }}

        /* Titre */
        .main-header {{
            font-size: 2em;
            color: #343A40;
            margin-bottom: 20px;
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown('<div class="main-header">⚡️ EnergyDoc Chat AI</div>', unsafe_allow_html=True)
    st.header("💬 3. Discussion avec les PDF")

    # Vérification de l'ingestion
    if "ingestion_done" not in st.session_state or not st.session_state.ingestion_done:
         st.warning("⚠️ Tu dois d'abord ingérer des PDFs avant de poser des questions.")
         return

    # Initialisation des messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Bienvenue ! Je suis prêt à répondre à vos questions sur les documents ingérés."}
        ]

    # 2. AFFICHAGE DES MESSAGES
    chat_display_container = st.container()
    
    with chat_display_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        for msg in st.session_state.messages:
            role_icon = "🧑" if msg["role"] == "user" else "🤖"
            css_class = "user-msg" if msg["role"] == "user" else "assistant-msg"
            
            content_html = f'<div class="chat-message {css_class}">{role_icon} {msg["content"]}</div>'
            st.markdown(content_html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # 3. BARRE DE SAISIE ET FORMULAIRE
    with st.form(key="chat_form", clear_on_submit=True):
        input_container = st.container()
        
        with input_container:
            # Utilisation de colonnes pour aligner l'entrée et le bouton
            input_col, button_col = st.columns([5, 1])
            
            with input_col:
                user_input = st.text_input("Pose ta question :", "", label_visibility="collapsed")
            
            with button_col:
                submitted = st.form_submit_button("Envoyer", type="primary")

    # 4. TRAITEMENT DE LA QUESTION
    if submitted and user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        
        rag = get_rag_chain()

        with st.spinner("Analyse des documents en cours..."):
            result = rag({"query": user_input})
        
        answer = result["result"]
        sources = result["source_documents"]

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        st.session_state.last_sources = sources
        st.rerun()

    # 5. AFFICHAGE DES SOURCES AMÉLIORÉ
    if "last_sources" in st.session_state and st.session_state.last_sources:
        st.markdown("---")
        with st.expander("📚 Sources utilisées"):
            for i, doc in enumerate(st.session_state.last_sources):
                st.markdown(f"### Source {i + 1}: {doc.metadata.get('source')} (Page {doc.metadata.get('page', 'N/A')})")
                st.markdown(f"> **Extrait :** *{doc.page_content.strip()}*")


# --- EXÉCUTION DU SCRIPT (pour le test) ---

if __name__ == '__main__':
    # Simuler l'état initial : "ingestion terminée" pour afficher le chat
    if "ingestion_done" not in st.session_state:
        st.session_state.ingestion_done = True
        
    render_chat_box_styled()