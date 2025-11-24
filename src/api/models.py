from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class ResearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="The research question")
    num_results: Optional[int] = Field(default=5, ge=1, le=10, description="Number of search results")
    stream: Optional[bool] = Field(default=True, description="Whether to stream the response")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the latest developments in quantum computing?",
                "num_results": 5,
                "stream": True
            }
        }

class Source(BaseModel):
    title: str
    url: str
    highlights: Optional[List[str]] = []
    published_date: Optional[str] = None
    author: Optional[str] = None

class ResearchResponse(BaseModel):
    query: str
    answer: str
    sources: List[Source]
    research_time_seconds: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the latest developments in quantum computing?",
                "answer": "Recent developments in quantum computing include...",
                "sources": [
                    {
                        "title": "Quantum Computing Breakthrough 2025",
                        "url": "https://example.com/article",
                        "highlights": ["Key development...", "Important findings..."]
                    },
                ],
                "research_time_seconds": 8.856,
                "timestamp": "2025-11-22T12:30:00"
            }
        }

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    services: Dict[str, str] = {}

class StreamChunk(BaseModel):
    type: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))