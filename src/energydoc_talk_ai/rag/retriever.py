# src/energydoc_talk_ai/rag/retriever.py

from langchain.schema import BaseRetriever
from energydoc_talk_ai.ingestion.vector_store import get_vector_store


def get_retriever(top_k: int = 4) -> BaseRetriever:
    """
    Retourne un retriever configuré via PineconeVectorStore.as_retriever().

    Paramètres
    ----------
    top_k : int
        Nombre de chunks les plus pertinents à récupérer pour le RAG.
    """
    vector_store = get_vector_store()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )

    return retriever