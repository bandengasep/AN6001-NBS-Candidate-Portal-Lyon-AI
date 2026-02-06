"""Embedding generation using OpenAI."""

from openai import OpenAI
from app.config import get_settings


def get_openai_client() -> OpenAI:
    """Get OpenAI client instance."""
    settings = get_settings()
    return OpenAI(api_key=settings.openai_api_key)


def get_embedding(text: str) -> list[float]:
    """Generate embedding for a single text.

    Args:
        text: Text to embed

    Returns:
        List of floats representing the embedding vector
    """
    settings = get_settings()
    client = get_openai_client()

    # Clean and truncate text if needed
    text = text.replace("\n", " ").strip()
    if not text:
        return [0.0] * settings.embedding_dimensions

    response = client.embeddings.create(
        model=settings.embedding_model,
        input=text,
        dimensions=settings.embedding_dimensions
    )

    return response.data[0].embedding


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for multiple texts in batch.

    Args:
        texts: List of texts to embed

    Returns:
        List of embedding vectors
    """
    settings = get_settings()
    client = get_openai_client()

    # Clean texts
    cleaned_texts = [t.replace("\n", " ").strip() for t in texts]
    cleaned_texts = [t if t else " " for t in cleaned_texts]  # Handle empty strings

    response = client.embeddings.create(
        model=settings.embedding_model,
        input=cleaned_texts,
        dimensions=settings.embedding_dimensions
    )

    # Sort by index to maintain order
    sorted_data = sorted(response.data, key=lambda x: x.index)
    return [item.embedding for item in sorted_data]
