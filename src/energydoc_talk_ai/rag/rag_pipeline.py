# src/energydoc_talk_ai/rag/rag_pipeline.py

from langchain.chains import RetrievalQA
from energydoc_talk_ai.rag.llm import get_llm
from energydoc_talk_ai.rag.retriever import get_retriever
from energydoc_talk_ai.rag.prompt import get_rag_prompt


def get_rag_chain() -> RetrievalQA:
    """
    Construit et retourne la chaîne RAG complète :
      - Retriever (Pinecone)
      - Prompt personnalisé
      - LLM Groq (LLaMA3)
    """

    llm = get_llm()
    retriever = get_retriever()
    prompt = get_rag_prompt()

    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",  # concatène les chunks en un seul contexte
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )

    return rag_chain
