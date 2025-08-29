import logging
from fastapi import APIRouter, HTTPException
from ..models.schemas import TrendsResponse
from ..utils.agents.trend_agent import TrendAgent

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize the trend agent
trend_agent = TrendAgent()

@router.get("/", response_model=TrendsResponse)
async def get_marketing_trends():
    """
    Get current marketing trends.
    
    Returns:
        TrendsResponse with list of current marketing trends
    """
    try:
        logger.info("Marketing trends request received")
        
        # Get trends from the trend agent
        trends = trend_agent.get_trends(use_real_api=False)  # Use mock for now
        
        if not trends:
            logger.warning("No trends retrieved, using fallback")
            trends = [
                "Digital transformation in marketing",
                "Customer experience optimization",
                "Data-driven marketing strategies"
            ]
        
        response = TrendsResponse(trends=trends)
        logger.info(f"Successfully retrieved {len(trends)} marketing trends")
        
        return response
        
    except Exception as e:
        logger.error(f"Error retrieving marketing trends: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve marketing trends"
        )

@router.get("/real")
async def get_real_trends():
    """
    Get real marketing trends using Google Trends API (if available).
    
    Returns:
        Dictionary with real trends or fallback to mock data
    """
    try:
        logger.info("Real marketing trends request received")
        
        # Attempt to get real trends
        trends = trend_agent.get_trends(use_real_api=True)
        
        if not trends:
            logger.warning("Real trends unavailable, using mock data")
            trends = trend_agent.get_mock_trends()
        
        return {
            "status": "success",
            "trends": trends,
            "source": "google_trends" if trend_agent.pytrends else "mock_data",
            "count": len(trends)
        }
        
    except Exception as e:
        logger.error(f"Error retrieving real trends: {str(e)}")
        # Fallback to mock trends
        fallback_trends = trend_agent.get_mock_trends()
        return {
            "status": "fallback",
            "trends": fallback_trends,
            "source": "mock_data",
            "count": len(fallback_trends),
            "error": str(e)
        }

@router.get("/status")
async def get_trends_status():
    """Get the status of the trends service."""
    try:
        pytrends_available = trend_agent.pytrends is not None
        
        return {
            "status": "operational",
            "pytrends_available": pytrends_available,
            "mock_trends_count": len(trend_agent.get_mock_trends()),
            "service": "marketing_trends_api"
        }
        
    except Exception as e:
        logger.error(f"Error getting trends status: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "service": "marketing_trends_api"
        }
