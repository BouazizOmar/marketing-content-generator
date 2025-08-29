import logging
from fastapi import APIRouter, HTTPException
from ..models.schemas import AnalyzeRequest, AnalyzeResponse
from ..utils.sentiment import analyze_sentiment

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=AnalyzeResponse)
async def analyze_content_sentiment(request: AnalyzeRequest):
    """
    Analyze the sentiment of provided content.
    
    Args:
        request: AnalyzeRequest containing content to analyze
        
    Returns:
        AnalyzeResponse with sentiment score and label
    """
    try:
        logger.info(f"Sentiment analysis request received for content length: {len(request.content)}")
        
        # Validate content length
        if len(request.content) > 10000:  # 10KB limit
            logger.warning("Content too long for analysis")
            raise HTTPException(
                status_code=400,
                detail="Content too long. Maximum length is 10,000 characters."
            )
        
        if len(request.content) < 10:
            logger.warning("Content too short for meaningful analysis")
            raise HTTPException(
                status_code=400,
                detail="Content too short. Minimum length is 10 characters."
            )
        
        # Perform sentiment analysis
        sentiment_score, sentiment_label = analyze_sentiment(request.content)
        
        # Create response
        response = AnalyzeResponse(
            sentiment=sentiment_score,
            sentiment_label=sentiment_label
        )
        
        logger.info(f"Sentiment analysis completed. Score: {sentiment_score:.3f}, Label: {sentiment_label}")
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Sentiment analysis failed: {str(e)}"
        )

@router.post("/detailed")
async def analyze_content_detailed(request: AnalyzeRequest):
    """
    Get detailed sentiment analysis including subjectivity.
    
    Args:
        request: AnalyzeRequest containing content to analyze
        
    Returns:
        Dictionary with detailed sentiment analysis
    """
    try:
        logger.info(f"Detailed sentiment analysis request received for content length: {len(request.content)}")
        
        # Validate content length
        if len(request.content) > 10000:
            raise HTTPException(
                status_code=400,
                detail="Content too long. Maximum length is 10,000 characters."
            )
        
        if len(request.content) < 10:
            raise HTTPException(
                status_code=400,
                detail="Content too short. Minimum length is 10 characters."
            )
        
        # Import the detailed analysis function
        from ..utils.sentiment import get_sentiment_details
        
        # Get detailed sentiment analysis
        sentiment_details = get_sentiment_details(request.content)
        
        # Add metadata
        response = {
            "status": "success",
            "content_length": len(request.content),
            "analysis": sentiment_details,
            "timestamp": "2024-01-01T00:00:00Z"  # You could use actual timestamp
        }
        
        logger.info("Detailed sentiment analysis completed successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in detailed sentiment analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Detailed sentiment analysis failed: {str(e)}"
        )

@router.get("/health")
async def get_analysis_health():
    """Get the health status of the sentiment analysis service."""
    try:
        # Test sentiment analysis with a simple text
        test_text = "This is a positive test message."
        sentiment_score, sentiment_label = analyze_sentiment(test_text)
        
        return {
            "status": "healthy",
            "service": "sentiment_analysis",
            "test_result": {
                "test_text": test_text,
                "sentiment_score": sentiment_score,
                "sentiment_label": sentiment_label
            },
            "dependencies": ["textblob"]
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "sentiment_analysis",
            "error": str(e),
            "dependencies": ["textblob"]
        }
