import logging
from textblob import TextBlob
from typing import Tuple

logger = logging.getLogger(__name__)

def analyze_sentiment(content: str) -> Tuple[float, str]:
    """
    Analyze the sentiment of given content using TextBlob.
    
    Args:
        content: Text content to analyze
        
    Returns:
        Tuple of (sentiment_score, sentiment_label)
        sentiment_score: Float between -1 (negative) and 1 (positive)
        sentiment_label: Human-readable sentiment description
    """
    try:
        # Create TextBlob object and get sentiment polarity
        blob = TextBlob(content)
        sentiment_score = blob.sentiment.polarity
        
        # Convert score to human-readable label
        if sentiment_score > 0.1:
            sentiment_label = "Positive"
        elif sentiment_score < -0.1:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"
        
        logger.info(f"Sentiment analysis completed. Score: {sentiment_score:.3f}, Label: {sentiment_label}")
        return sentiment_score, sentiment_label
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        # Return neutral sentiment as fallback
        return 0.0, "Neutral"

def get_sentiment_details(content: str) -> dict:
    """
    Get detailed sentiment analysis including subjectivity.
    
    Args:
        content: Text content to analyze
        
    Returns:
        Dictionary with sentiment details
    """
    try:
        blob = TextBlob(content)
        
        sentiment_details = {
            "polarity": blob.sentiment.polarity,
            "subjectivity": blob.sentiment.subjectivity,
            "label": "Positive" if blob.sentiment.polarity > 0.1 else "Negative" if blob.sentiment.polarity < -0.1 else "Neutral",
            "confidence": abs(blob.sentiment.polarity)
        }
        
        logger.info(f"Detailed sentiment analysis completed for content of length {len(content)}")
        return sentiment_details
        
    except Exception as e:
        logger.error(f"Error in detailed sentiment analysis: {str(e)}")
        return {
            "polarity": 0.0,
            "subjectivity": 0.0,
            "label": "Neutral",
            "confidence": 0.0
        }
