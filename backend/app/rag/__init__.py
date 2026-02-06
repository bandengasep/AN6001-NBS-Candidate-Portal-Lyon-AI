"""RAG (Retrieval-Augmented Generation) module."""

from .embeddings import get_embedding, get_embeddings_batch
from .retriever import retrieve_relevant_documents
from .ingestion import ingest_documents, chunk_text

__all__ = [
    "get_embedding",
    "get_embeddings_batch",
    "retrieve_relevant_documents",
    "ingest_documents",
    "chunk_text",
]
