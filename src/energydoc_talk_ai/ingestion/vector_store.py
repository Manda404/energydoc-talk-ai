# src/energydoc_talk_ai/ingestion/vector_store.py

"""
Module de création et récupération du VectorStore Pinecone.

Ce module :
- Initialise un client Pinecone
- Crée l’index si nécessaire
- Attache un modèle d’embedding (Google / OpenAI / autre)
- Retourne un VectorStore compatible LangChain

Utilisé dans le pipeline RAG :
    documents → embeddings → PineconeVectorStore
"""

import time
from typing import List
from langchain.schema import Document
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from energydoc_talk_ai.core.config import settings
from energydoc_talk_ai.core.logger import setup_logger
from energydoc_talk_ai.ingestion.embeddings import get_embeddings



# ------------------------------------------------------------------------------
# Suppression de l’index Pinecone (utilitaire)
# ------------------------------------------------------------------------------
def delete_pinecone_index() -> None:
    """
    Supprime un index Pinecone uniquement s'il existe.
    Ne lève PAS d'erreur si l'index n'existe pas.
    """

    # Initialisation du logger
    logger = setup_logger(logger_name="delete_pinecone_index")


    logger.info(f"Vérification pour suppression de l’index : {settings.PINECONE_INDEX_NAME}")

    pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    # Liste des index existants
    existing_indexes = [idx["name"] for idx in pc.list_indexes()]

    # Si l'index n'existe pas → rien à faire
    if settings.PINECONE_INDEX_NAME not in existing_indexes:
        logger.warning(
            f"Index '{settings.PINECONE_INDEX_NAME}' introuvable → aucune suppression."
        )
        return

    # Suppression
    logger.info(f"Suppression de l’index '{settings.PINECONE_INDEX_NAME}'...")
    pc.delete_index(settings.PINECONE_INDEX_NAME)
    logger.info(f"Index '{settings.PINECONE_INDEX_NAME}' supprimé avec succès.")



# ------------------------------------------------------------------------------
# Initialisation du client Pinecone
# ------------------------------------------------------------------------------
def get_pinecone_client() -> Pinecone:
    """
    Initialise le client Pinecone et crée l'index si nécessaire.

    Returns
    -------
    Pinecone
        Client Pinecone configuré avec API Key + Region.
    """
    # Initialisation du logger
    logger = setup_logger(logger_name="get_pinecone_client")
    
    logger.info("Initialisation du client Pinecone...")

    # Création du client Pinecone
    try:
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        logger.debug("Client Pinecone initialisé.")
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Impossible d'initialiser le client Pinecone : {exc}")
        raise

    # Configuration serverless (AWS)
    spec = ServerlessSpec(
        cloud="aws",
        region=settings.PINECONE_SERVERLESS_REGION,
    )

    # Liste des index existants
    try:
        existing_indexes = [i["name"] for i in pc.list_indexes()]
        logger.info(f"Index existants : {existing_indexes}")
    except Exception as exc:
        logger.error(f"Impossible de lister les index Pinecone : {exc}")
        raise

    # Création de l'index si inexistant
    if settings.PINECONE_INDEX_NAME not in existing_indexes:
        logger.warning(
            f"Index '{settings.PINECONE_INDEX_NAME}' introuvable → création..."
        )

        try:
            pc.create_index(
                name=settings.PINECONE_INDEX_NAME,
                dimension=settings.PINECONE_DIMENSION,  # Google embeddings en fonction du modèle d'embedding utilisé
                metric=settings.PINECONE_METRIC,
                spec=spec,
            )
        except Exception as exc:
            logger.error(f"Erreur création index Pinecone : {exc}")
            raise

        # Attendre que l’index soit prêt
        logger.info("Création de l’index en cours...")

        while True:
            try:
                status = pc.describe_index(settings.PINECONE_INDEX_NAME).status
                logger.debug(f"Statut index : {status}")
            except Exception as exc:
                logger.error(f"Impossible de récupérer le statut : {exc}")
                raise

            if status.get("ready", False):
                logger.info("Index prêt ! 🚀")
                break

            time.sleep(1)
            logger.debug("Attente disponibilité index...")

    else:
        logger.info(
            f"Index '{settings.PINECONE_INDEX_NAME}' déjà existant → utilisation."
        )

    return pc


# ----------------------------------------------------------------------
# Ajout : Insertion batchée pour éviter la limite Google
# ----------------------------------------------------------------------
def add_documents_batch_safe(
    vector_store: PineconeVectorStore,
    documents: List[Document],
    batch_size: int = 32,
) -> None:
    """
    Ajout sécurisé de documents dans Pinecone en batchs,
    pour éviter les limites d'embeddings Google GenAI.

    Parameters
    ----------
    vector_store : PineconeVectorStore
        Le VectorStore LangChain cible.
    documents : List[Document]
        Les chunks à indexer.
    batch_size : int
        Taille du batch à embeder (+ recomm: 16 ou 32 avec Google).
    """
    # Initialisation du logger
    logger = setup_logger(logger_name="add_documents_batch_safe")

    logger.info(
        f"Indexation batchée avec batch_size={batch_size} "
        f"({len(documents)} documents au total)."
    )

    for i in range(0, len(documents), batch_size):
        batch = documents[i : i + batch_size]
        logger.info(f" → Batch {i//batch_size + 1}: {len(batch)} documents")

        # Embeddings + insertion
        vector_store.add_documents(batch)

        logger.debug("Batch indexé avec succès.")

    logger.info("Indexation batchée terminée.")


# ------------------------------------------------------------------------------
# Récupération du VectorStore LangChain
# ------------------------------------------------------------------------------
def get_vector_store() -> PineconeVectorStore:
    """
    Retourne un VectorStore LangChain basé sur l'index Pinecone existant.

    Returns
    -------
    PineconeVectorStore
        Le VectorStore configuré avec l'embedding choisi.
    """
    # Initialisation du logger
    logger = setup_logger(logger_name="get_vector_store")
    
    logger.info("Initialisation du VectorStore Pinecone...")

    pc = get_pinecone_client()

    # Récupérer l’index Pinecone
    try:
        index = pc.Index(settings.PINECONE_INDEX_NAME)
        logger.debug(f"Index récupéré : {settings.PINECONE_INDEX_NAME}")
    except Exception as exc:
        logger.error(f"Impossible de récupérer l’index : {exc}")
        raise

    # Embeddings (Google / OpenAI / HuggingFace)
    try:
        embeddings = get_embeddings()
        logger.debug("Embedding model chargé.")
    except Exception as exc:
        logger.error(f"Impossible de charger les embeddings : {exc}")
        raise

    # Création du VectorStore LangChain
    try:
        vector_store = PineconeVectorStore(
            index=index,
            embedding=embeddings,
            text_key="text",  # clé utilisée dans les documents stockés
        )
        logger.info("VectorStore Pinecone initialisé avec succès.")
    except Exception as exc:
        logger.error(f"Impossible d'initialiser le VectorStore : {exc}")
        raise

    return vector_store
