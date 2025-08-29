import logging
from typing import List, Dict, Any
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import HumanMessage, AIMessage
import pytrends
from pytrends.request import TrendReq

logger = logging.getLogger(__name__)

class TrendAgent:
    """Agent responsible for fetching current marketing trends."""
    
    def __init__(self):
        self.pytrends = None
        self._initialize_pytrends()
    
    def _initialize_pytrends(self):
        """Initialize pytrends client if available."""
        try:
            self.pytrends = TrendReq(hl='en-US', tz=360)
            logger.info("PyTrends initialized successfully")
        except Exception as e:
            logger.warning(f"PyTrends initialization failed: {str(e)}")
            self.pytrends = None
    
    def get_mock_trends(self) -> List[str]:
        """Get mock marketing trends for development/testing."""
        mock_trends = [
            "Sustainability and eco-friendly marketing",
            "AI-driven personalization",
            "Video content marketing",
            "Voice search optimization",
            "Social commerce integration",
            "Micro-influencer partnerships",
            "Interactive content experiences",
            "Data privacy compliance",
            "Omnichannel marketing strategies",
            "Local SEO and hyperlocal targeting"
        ]
        logger.info("Returning mock marketing trends")
        return mock_trends
    
    def get_google_trends(self, keywords: List[str] = None) -> List[str]:
        """Get real marketing trends using Google Trends API."""
        if not self.pytrends:
            logger.warning("PyTrends not available, falling back to mock trends")
            return self.get_mock_trends()
        
        try:
            # Default marketing-related keywords if none provided
            if not keywords:
                keywords = ["marketing trends", "digital marketing", "content marketing", "social media marketing"]
            
            # Build payload and get trends
            self.pytrends.build_payload(keywords, timeframe='today 3-m')
            trends_data = self.pytrends.interest_over_time()
            
            # Extract trending keywords
            trending_keywords = []
            for keyword in keywords:
                if keyword in trends_data.columns:
                    # Get the latest interest value
                    latest_interest = trends_data[keyword].iloc[-1]
                    if latest_interest > 50:  # High interest threshold
                        trending_keywords.append(f"{keyword} (trending)")
            
            if trending_keywords:
                logger.info(f"Retrieved {len(trending_keywords)} trending keywords from Google Trends")
                return trending_keywords
            else:
                logger.info("No high-interest trends found, returning mock trends")
                return self.get_mock_trends()
                
        except Exception as e:
            logger.error(f"Error fetching Google Trends: {str(e)}")
            return self.get_mock_trends()
    
    def get_trends(self, use_real_api: bool = False) -> List[str]:
        """
        Get marketing trends, either from real API or mock data.
        
        Args:
            use_real_api: Whether to attempt using real Google Trends API
            
        Returns:
            List of marketing trends
        """
        if use_real_api and self.pytrends:
            return self.get_google_trends()
        else:
            return self.get_mock_trends()
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the trend agent as part of LangGraph workflow.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with trends
        """
        try:
            # Extract prompt from state
            prompt = state.get("prompt", "")
            
            # Get trends based on prompt context
            if "trending" in prompt.lower() or "current" in prompt.lower():
                trends = self.get_trends(use_real_api=True)
            else:
                trends = self.get_trends(use_real_api=False)
            
            # Update state with trends
            state["trends"] = trends
            logger.info(f"Trend agent added {len(trends)} trends to state")
            
            return state
            
        except Exception as e:
            logger.error(f"Error in trend agent: {str(e)}")
            # Fallback to mock trends
            state["trends"] = self.get_mock_trends()
            return state
