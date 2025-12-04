"""
embeddings.py

Module responsable de l'initialisation du modèle d'embeddings utilisé par
EnergyDocTalk AI.

Ce module permet d'obtenir un embedding Google Generative AI prêt à l'emploi,
utilisé pour :

- l’ingestion (indexation des documents PDF dans Pinecone)
- le retrieval (dans le pipeline RAG)

Il centralise :
- la configuration du modèle (via settings)
- la gestion de la clé API Google
"""

from energydoc_talk_ai.core.config import settings
from energydoc_talk_ai.core.logger import setup_logger
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Initialisation du logger
logger = setup_logger("embeddings")


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    """
    Initialise et retourne un modèle d'embeddings Google Generative AI.

    Returns
    -------
    GoogleGenerativeAIEmbeddings
        Le modèle d'embedding configuré avec :
        - settings.EMBEDDING_MODEL
        - settings.GOOGLE_API_KEY

    Raises
    ------
    Exception
        Si le modèle ne peut pas être initialisé (ex : clé API invalide).
    """

    logger.info(
        f"Initialisation du modèle Google Embeddings : {settings.EMBEDDING_MODEL}"
    )

    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
        )

        logger.debug("Embeddings Google GenAI initialisés avec succès.")
        return embeddings

    except Exception as exc:
        logger.error(f"Erreur lors de l'initialisation des embeddings : {exc}")
        raise
