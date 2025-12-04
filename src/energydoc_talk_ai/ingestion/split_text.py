# src/energydoc_talk_ai/ingestion/split_text.py
"""
Module de découpe du texte des pages PDF en chunks pour le pipeline RAG.

Ce module reçoit en entrée :
    pages : List[Tuple[int, str]]
        → typiquement retourné par extract_text_from_pdf_ram()
          sous la forme (page_number, texte)

Puis transforme chaque page en plusieurs `Document` LangChain
selon la configuration du text splitter.

Chaque `Document` possède :
    - page_content : str
        Le texte du chunk.
    - metadata : dict
        Métadonnées associées, typiquement :
            {
                "source": str,      # identifiant / nom du PDF
                "page": int,        # numéro de page d'origine
                "pdf_name": str,    # nom du fichier PDF (affichage / debug)
            }

Ce module est 100% compatible avec un flux où les PDFs sont chargés
en mémoire (RAM) et non depuis le disque.
"""

from __future__ import annotations
from typing import List, Tuple

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from energydoc_talk_ai.core.config import settings
from energydoc_talk_ai.core.logger import setup_logger

# Initialisation du logger pour ce module
logger = setup_logger(logger_name="split_text")


# ---------------------------------------------------------------------------
# Config du Text Splitter
# ---------------------------------------------------------------------------
def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Initialise et retourne un TextSplitter configuré pour la découpe
    du texte extrait des PDFs.

    Le splitter utilise une stratégie récursive avec plusieurs séparateurs
    (sauts de ligne, ponctuation, espaces) et des paramètres globaux
    définis dans la configuration de l'application :

        - settings.CHUNK_SIZE
        - settings.CHUNK_OVERLAP

    Returns
    -------
    RecursiveCharacterTextSplitter
        Instance prête à être utilisée pour créer des chunks.
    """
    logger.debug(
        "Initialisation du TextSplitter "
        f"(chunk_size={settings.CHUNK_SIZE}, "
        f"chunk_overlap={settings.CHUNK_OVERLAP})"
    )

    return RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "! ",
            "? ",
            " ",
            "",
        ],
    )


# ---------------------------------------------------------------------------
# Split pages → Documents LangChain
# ---------------------------------------------------------------------------
def split_pages_into_documents(
    pages: List[Tuple[int, str]],
    source: str,
) -> List[Document]:
    """
    Transforme une liste de pages (numéro, texte) en une liste de
    `Document` LangChain, prêts à être indexés dans un VectorStore.

    Cette fonction est neutre vis-à-vis de la provenance des données :
    les pages peuvent provenir d'un PDF lu sur disque ou d'un PDF
    chargé entièrement en mémoire (RAM), du moment que le format
    d'entrée est respecté.

    Parameters
    ----------
    pages : List[Tuple[int, str]]
        Liste de tuples (page_number, texte) retournée par
        `extract_text_from_pdf_ram()` ou équivalent.
        - page_number (int) : numéro de la page commençant à 1
        - texte (str) : contenu textuel brut de la page
    source : str
        Identifiant de la source du document. En contexte RAM-only,
        il s'agit typiquement du nom du fichier PDF (ex: "contrat.pdf").
        Cette valeur est propagée dans les métadonnées des Documents.

    Returns
    -------
    List[Document]
        Liste de chunks (`Document` LangChain) contenant :
            - page_content : texte du chunk
            - metadata :
                - "source"   : identifiant de la source (str)
                - "page"     : numéro de la page d'origine (int)
                - "pdf_name" : nom du PDF (str)

        Si aucune page n'est fournie ou qu'aucun texte exploitable
        n'est trouvé, une liste vide est retournée.
    """
    logger.info(f"Début du split en chunks du document : {source}")

    documents: List[Document] = []

    if not pages:
        logger.warning(f"Aucune page à split pour la source : {source}")
        return []

    logger.info(f"{len(pages)} pages chargées pour découpage.")

    splitter = get_text_splitter()

    for page_number, text in pages:

        if not text or not text.strip():
            logger.debug(f"Page {page_number} vide — ignorée.")
            continue

        base_metadata = {
            "source": source,
            "page": page_number,
            "pdf_name": source,  # en RAM, source = nom du PDF
        }

        try:
            docs = splitter.create_documents(
                texts=[text],
                metadatas=[base_metadata],
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"Erreur lors du split de la page {page_number}: {exc}")
            continue

        logger.debug(
            f"Page {page_number} découpée en {len(docs)} chunk(s)."
        )

        documents.extend(docs)

    logger.info(
        f"Split terminé : {len(documents)} chunks générés "
        f"depuis {len(pages)} pages."
    )

    return documents
# src/pdf_talk_ai/ingestion/split_text.py
"""
Module de découpe du texte des pages PDF en chunks pour le pipeline RAG.

Ce module reçoit en entrée :
    pages : List[Tuple[int, str]]
        → typiquement retourné par extract_text_from_pdf_ram()
          sous la forme (page_number, texte)

Puis transforme chaque page en plusieurs `Document` LangChain
selon la configuration du text splitter.

Chaque `Document` possède :
    - page_content : str
        Le texte du chunk.
    - metadata : dict
        Métadonnées associées, typiquement :
            {
                "source": str,      # identifiant / nom du PDF
                "page": int,        # numéro de page d'origine
                "pdf_name": str,    # nom du fichier PDF (affichage / debug)
            }

Ce module est 100% compatible avec un flux où les PDFs sont chargés
en mémoire (RAM) et non depuis le disque.
"""

#from __future__ import annotations
from typing import List, Tuple

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from energydoc_talk_ai.core.config import settings
from energydoc_talk_ai.core.logger import setup_logger

# Initialisation du logger pour ce module
logger = setup_logger(logger_name="split_text")


# ---------------------------------------------------------------------------
# Config du Text Splitter
# ---------------------------------------------------------------------------
def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Initialise et retourne un TextSplitter configuré pour la découpe
    du texte extrait des PDFs.

    Le splitter utilise une stratégie récursive avec plusieurs séparateurs
    (sauts de ligne, ponctuation, espaces) et des paramètres globaux
    définis dans la configuration de l'application :

        - settings.CHUNK_SIZE
        - settings.CHUNK_OVERLAP

    Returns
    -------
    RecursiveCharacterTextSplitter
        Instance prête à être utilisée pour créer des chunks.
    """
    logger.debug(
        "Initialisation du TextSplitter "
        f"(chunk_size={settings.CHUNK_SIZE}, "
        f"chunk_overlap={settings.CHUNK_OVERLAP})"
    )

    return RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "! ",
            "? ",
            " ",
            "",
        ],
    )


# ---------------------------------------------------------------------------
# Split pages → Documents LangChain
# ---------------------------------------------------------------------------
def split_pages_into_documents(
    pages: List[Tuple[int, str]],
    source: str,
) -> List[Document]:
    """
    Transforme une liste de pages (numéro, texte) en une liste de
    `Document` LangChain, prêts à être indexés dans un VectorStore.

    Cette fonction est neutre vis-à-vis de la provenance des données :
    les pages peuvent provenir d'un PDF lu sur disque ou d'un PDF
    chargé entièrement en mémoire (RAM), du moment que le format
    d'entrée est respecté.

    Parameters
    ----------
    pages : List[Tuple[int, str]]
        Liste de tuples (page_number, texte) retournée par
        `extract_text_from_pdf_ram()` ou équivalent.
        - page_number (int) : numéro de la page commençant à 1
        - texte (str) : contenu textuel brut de la page
    source : str
        Identifiant de la source du document. En contexte RAM-only,
        il s'agit typiquement du nom du fichier PDF (ex: "contrat.pdf").
        Cette valeur est propagée dans les métadonnées des Documents.

    Returns
    -------
    List[Document]
        Liste de chunks (`Document` LangChain) contenant :
            - page_content : texte du chunk
            - metadata :
                - "source"   : identifiant de la source (str)
                - "page"     : numéro de la page d'origine (int)
                - "pdf_name" : nom du PDF (str)

        Si aucune page n'est fournie ou qu'aucun texte exploitable
        n'est trouvé, une liste vide est retournée.
    """
    logger.info(f"Début du split en chunks du document : {source}")

    documents: List[Document] = []

    if not pages:
        logger.warning(f"Aucune page à split pour la source : {source}")
        return []

    logger.info(f"{len(pages)} pages chargées pour découpage.")

    splitter = get_text_splitter()

    for page_number, text in pages:

        if not text or not text.strip():
            logger.debug(f"Page {page_number} vide — ignorée.")
            continue

        base_metadata = {
            "source": source,
            "page": page_number,
            "pdf_name": source,  # en RAM, source = nom du PDF
        }

        try:
            docs = splitter.create_documents(
                texts=[text],
                metadatas=[base_metadata],
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"Erreur lors du split de la page {page_number}: {exc}")
            continue

        logger.debug(
            f"Page {page_number} découpée en {len(docs)} chunk(s)."
        )

        documents.extend(docs)

    logger.info(
        f"Split terminé : {len(documents)} chunks générés "
        f"depuis {len(pages)} pages."
    )

    return documents
