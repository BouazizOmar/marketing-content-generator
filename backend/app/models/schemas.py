from pydantic import BaseModel, Field
from typing import Optional

class GenerateRequest(BaseModel):
    """Request model for content generation endpoint."""
    prompt: str = Field(..., description="The prompt for content generation", min_length=1, max_length=1000)
    file: Optional[str] = Field(None, description="Base64-encoded CSV or PDF file content")

class GenerateResponse(BaseModel):
    """Response model for content generation endpoint."""
    content: str = Field(..., description="Generated marketing content")
    image_url: Optional[str] = Field(None, description="URL to generated image (if applicable)")

class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
