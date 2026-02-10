"""Pydantic models for the application."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single chat message."""

    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    message: str = Field(..., min_length=1, description="User message")
    conversation_id: str | None = Field(None, description="Optional conversation ID for history")


class ChatResponse(BaseModel):
    """Response from chat endpoint."""

    response: str = Field(..., description="Assistant response")
    conversation_id: str = Field(..., description="Conversation ID for follow-up")
    sources: list[dict[str, Any]] = Field(default_factory=list, description="Retrieved sources")
    show_handoff_form: bool = Field(default=False, description="Whether to show advisor hand-off form")


class Document(BaseModel):
    """A document stored in the vector database."""

    id: str | None = None
    content: str = Field(..., description="Document text content")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    embedding: list[float] | None = Field(None, description="Vector embedding")


class Program(BaseModel):
    """An NBS degree program."""

    id: str | None = None
    name: str = Field(..., description="Program name")
    degree_type: str = Field(..., description="Type: MBA, MSc, PhD, etc.")
    description: str = Field(..., description="Program description")
    duration: str | None = Field(None, description="Program duration")
    url: str | None = Field(None, description="Program URL")
    requirements: dict[str, Any] = Field(default_factory=dict, description="Admission requirements")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ProgramComparison(BaseModel):
    """Comparison between two or more programs."""

    programs: list[str] = Field(..., min_length=2, description="Program names to compare")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    version: str = "1.0.0"
