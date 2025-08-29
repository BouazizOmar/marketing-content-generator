#!/usr/bin/env python3
"""
Startup script for the Marketing Content Generator API.
Run this file to start the FastAPI application.
"""

import uvicorn
from app.config.settings import settings

if __name__ == "__main__":
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Log level: {settings.LOG_LEVEL}")
    
    if not settings.OPENAI_API_KEY:
        print("⚠️  Warning: OpenAI API key not configured. Content generation will use fallback mode.")
    
    print(f"🚀 Server starting at http://localhost:8000")
    print(f"📚 API documentation available at http://localhost:8000/docs")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
