"""
Module d'extraction de texte pour les fichiers PDF chargés EN MÉMOIRE (RAM).

Ce module utilise PyMuPDF (fitz) pour extraire du texte sans jamais écrire
ou lire un fichier sur disque. Idéal pour Streamlit Cloud et ingestion RAG RAM.
"""

import fitz  # PyMuPDF
from io import BytesIO
from typing import Union, List, Tuple
from energydoc_talk_ai.core.logger import setup_logger

# Initialisation du logger
logger = setup_logger(logger_name="extract_text_from_pdf_ram")


def extract_text_from_pdf_ram(file_data: Union[bytes, BytesIO]) -> List[Tuple[int, str]]:
    """
    Extrait le texte d'un PDF chargé uniquement en RAM.

    Parameters
    ----------
    file_data : bytes | BytesIO
        - bytes du PDF (ex: uploaded_file.read())
        - ou un buffer BytesIO (ex: BytesIO(uploaded_file.read()))

    Returns
    -------
    List[Tuple[int, str]]
        Liste de tuples (page_number, texte) :
        - page_number commence à 1
        - texte contient le texte brut extrait
        - seules les pages non vides sont renvoyées

    Raises
    ------
    RuntimeError
        Si l'ouverture du PDF échoue (fichier corrompu, vide, etc.)
    """

    logger.info("Début extraction texte PDF (RAM only).")

    # Normalisation : convertir en BytesIO si nécessaire
    if isinstance(file_data, bytes):
        file_data = BytesIO(file_data)

    # Ouverture du PDF depuis la RAM
    try:
        doc = fitz.open(stream=file_data, filetype="pdf")
        total_pages = len(doc)
        logger.info(f"PDF chargé en RAM : {total_pages} pages détectées.")
    except Exception as exc:
        logger.error(f"Impossible d'ouvrir le PDF en RAM : {exc}")
        raise RuntimeError(f"Impossible d'ouvrir le PDF en RAM : {exc}")

    extracted_pages: List[Tuple[int, str]] = []

    # Extraction page par page
    for page_index, page in enumerate(doc):
        page_number = page_index + 1

        try:
            text: str = page.get_text("text") or ""
            text = text.strip()
        except Exception as exc:
            logger.warning(f"Erreur extraction page {page_number} : {exc}")
            continue

        if text:
            extracted_pages.append((page_number, text))
        else:
            logger.debug(f"Page {page_number} vide ou non-textuelle.")

    doc.close()

    logger.info(
        f"Extraction RAM terminée : {len(extracted_pages)} pages extraites "
        f"sur {total_pages} pages détectées."
    )

    return extracted_pages