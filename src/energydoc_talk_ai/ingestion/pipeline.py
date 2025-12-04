"""
Pipeline complet d'ingestion pour PDFs en RAM (aucune lecture disque).

Étapes :
    1. Extraction du texte page par page depuis RAM
    2. Split en chunks (Documents LangChain)
    3. Insertion batchée dans le VectorStore (ex: Pinecone)
"""

#from __future__ import annotations

from typing import Iterable, List, Tuple
from langchain.schema import Document

from energydoc_talk_ai.core.logger import setup_logger
from energydoc_talk_ai.ingestion.vector_store import get_vector_store, add_documents_batch_safe
from energydoc_talk_ai.ingestion.extract_text import extract_text_from_pdf_ram
from energydoc_talk_ai.ingestion.split_text import split_pages_into_documents


# Logger
logger = setup_logger(logger_name="ingestion_pipeline_ram")


def ingestion_pipeline_ram(pdf_files: Iterable[Tuple[str, bytes]]) -> None:
    """
    Ingestion de PDFs chargés en mémoire (RAM).

    Parameters
    ----------
    pdf_files : Iterable[Tuple[str, bytes]]
        Liste de tuples :
            (file_name, file_bytes)
        Exemple avec Streamlit :
            uploaded_files = st.file_uploader(..., accept_multiple_files=True)
            files = [(f.name, f.read()) for f in uploaded_files]

    Pipeline :
        1. Extraction du texte en RAM
        2. Split en chunks
        3. Indexation dans Pinecone
    """

    pdf_files = list(pdf_files)
    logger.info(f"Pipeline RAM : {len(pdf_files)} PDFs chargés.")

    all_documents: List[Document] = []

    # ======================================================================
    # 🔁 Boucle sur les PDFs
    # ======================================================================
    for file_name, file_bytes in pdf_files:

        logger.info(f"Traitement du PDF (RAM) : {file_name}")

        # 1) Extraction RAM
        logger.debug("Extraction du texte en RAM…")
        try:
            pages = extract_text_from_pdf_ram(file_bytes)
        except Exception as exc:
            logger.error(f"Erreur extraction {file_name} : {exc}")
            continue

        if not pages:
            logger.warning(f"Aucun texte extrait → ignoré : {file_name}")
            continue

        logger.info(f"{len(pages)} pages extraites depuis {file_name}.")

        # 2) Split pages → chunks LangChain
        logger.debug("Découpage en chunks…")

        docs = split_pages_into_documents(
            pages=pages,
            source=file_name,  # metadata pour RAG
        )

        logger.info(f"{len(docs)} chunks générés pour {file_name}.")
        all_documents.extend(docs)

    # ======================================================================
    # 📌 Indexation Pinecone
    # ======================================================================
    if not all_documents:
        logger.info("Aucun chunk à indexer. Pipeline terminé.")
        return

    logger.info(
        f"Indexation dans Pinecone : {len(all_documents)} chunks à insérer..."
    )

    vector_store = get_vector_store()

    # Google GenAI / Pinecone = batch obligatoire
    add_documents_batch_safe(vector_store, all_documents, batch_size=32)

    logger.info(
        f"Ingestion RAM terminée. "
        f"{len(all_documents)} chunks indexés dans Pinecone."
    )
