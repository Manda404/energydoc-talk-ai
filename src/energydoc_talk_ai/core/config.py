"""
Configuration hybride EnergyDocTalk AI :
----------------------------------------

✔ Compatible local (.env via Pydantic)
✔ Compatible Streamlit Cloud (st.secrets)
✔ Centralise toutes les clés API et chemins
✔ Valide automatiquement les dossiers
"""

from pathlib import Path
import streamlit as st
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict, field_validator


def _get_secret(key: str, default=None):
    """
    Fonction utilitaire pour récupérer une variable :
    - depuis st.secrets (Streamlit Cloud)
    - sinon depuis l'env local (.env)
    """
    if key in st.secrets:
        return st.secrets[key]
    return default


class Settings(BaseSettings):
    """
    Configuration principale du projet EnergyDocTalk AI.
    """

    # -------------------------------------------------------------------------
    # Pydantic Settings (uniquement pour usage local avec .env)
    # -------------------------------------------------------------------------
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # CHEMINS
    # -------------------------------------------------------------------------
    project_root: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parents[3],
        description="Racine du projet EnergyDocTalk AI.",
    )

    data_dir: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parents[3] / "data",
        description="Dossier principal contenant les données.",
    )

    logs_dir: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parents[3] / "logs",
        description="Dossier contenant les logs.",
    )

    # -------------------------------------------------------------------------
    # API KEYS (lecture Streamlit Secrets > .env)
    # -------------------------------------------------------------------------

    # Pinecone
    PINECONE_API_KEY: str = Field(
        default_factory=lambda: _get_secret("PINECONE_API_KEY"),
        description="Clé API Pinecone."
    )
    PINECONE_SERVERLESS_REGION: str | None = Field(
        default_factory=lambda: _get_secret("PINECONE_SERVERLESS_REGION", None),
        description="Région Pinecone (serverless)."
    )
    PINECONE_INDEX_NAME: str = Field(
        default_factory=lambda: _get_secret("PINECONE_INDEX_NAME", "energydoc-talk-ai"),
        description="Nom de l'index Pinecone."
    )

    PINECONE_DIMENSION: int = Field(
        default=3072,
        description="Dimension des embeddings Google utilisés par Pinecone."
    )
    PINECONE_METRIC: str = Field(
        default="dotproduct",
        description="Métrique de similarité dans Pinecone."
    )

    # Google
    GOOGLE_API_KEY: str = Field(
        default_factory=lambda: _get_secret("GOOGLE_API_KEY"),
        description="Clé API Google Generative AI."
    )
    EMBEDDING_MODEL: str = Field(
        default_factory=lambda: _get_secret("EMBEDDING_MODEL", "text-embedding-004"),
        description="Modèle d'embedding Google."
    )

    # Groq
    GROQ_API_KEY: str = Field(
        default_factory=lambda: _get_secret("GROQ_API_KEY"),
        description="Clé API Groq."
    )
    LLM_MODEL: str = Field(
        default_factory=lambda: _get_secret("LLM_MODEL", "llama3-8b-8192"),
        description="Modèle LLaMA 3 utilisé via Groq."
    )

    # Debug
    DEBUG: bool = Field(default=False)

    # -------------------------------------------------------------------------
    # PARAMÈTRES DE CHUNKING
    # -------------------------------------------------------------------------
    CHUNK_SIZE: int = Field(default=800)
    CHUNK_OVERLAP: int = Field(default=200)

    # -------------------------------------------------------------------------
    # Validation automatique des dossiers
    # -------------------------------------------------------------------------
    @field_validator("data_dir", "logs_dir")
    def ensure_dirs(cls, v: Path) -> Path:
        v.mkdir(parents=True, exist_ok=True)
        return v


# Instance globale
settings = Settings()
