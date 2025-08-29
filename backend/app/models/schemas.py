from pydantic import BaseModel, Field
from typing import List, Optional, Union

class GenerateRequest(BaseModel):
    """Request model for content generation endpoint."""
    prompt: str = Field(..., description="The prompt for content generation", min_length=1, max_length=1000)
    file: Optional[str] = Field(None, description="Base64-encoded CSV or PDF file content")

class GenerateResponse(BaseModel):
    """Response model for content generation endpoint."""
    content: str = Field(..., description="Generated marketing content")
    image_url: Optional[str] = Field(None, description="URL to generated image (if applicable)")

class TrendsResponse(BaseModel):
    """Response model for trends endpoint."""
    trends: List[str] = Field(..., description="List of current marketing trends")

class AnalyzeRequest(BaseModel):
    """Request model for content analysis endpoint."""
    content: str = Field(..., description="Content to analyze for sentiment", min_length=1)

class AnalyzeResponse(BaseModel):
    """Response model for content analysis endpoint."""
    sentiment: float = Field(..., description="Sentiment score between -1 (negative) and 1 (positive)")
    sentiment_label: str = Field(..., description="Human-readable sentiment label")

class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
