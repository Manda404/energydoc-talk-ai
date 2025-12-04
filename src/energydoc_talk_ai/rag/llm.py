# src/energydoc_talk_ai/rag/llm_groq.py

from langchain_groq import ChatGroq
from energydoc_talk_ai.core.config import settings


def get_llm() -> ChatGroq:
    """
    Configure et retourne un LLM Groq (LLaMA3, Mixtral, etc.).

    Modèle défini dans .env :
    LLM_MODEL=llama3-8b-8192
    """
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.LLM_MODEL,
        temperature=0.1,
        max_tokens=1024,
    )
