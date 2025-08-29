import logging
import os
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

logger = logging.getLogger(__name__)

class ContentAgent:
    """Agent responsible for generating marketing content using OpenAI."""
    
    def __init__(self):
        self.llm = None
        self._initialize_llm()
        self._setup_prompts()
    
    def _initialize_llm(self):
        """Initialize OpenAI language model."""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.warning("OpenAI API key not found, content generation will be limited")
                self.llm = None
                return
            
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                max_tokens=1000,
                api_key=api_key
            )
            logger.info("OpenAI language model initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing OpenAI model: {str(e)}")
            self.llm = None
    
    def _setup_prompts(self):
        """Setup prompt templates for content generation."""
        self.content_prompt = ChatPromptTemplate.from_template("""
        You are an expert marketing content creator. Generate engaging, professional marketing content based on the following:

        PROMPT: {prompt}
        
        CURRENT MARKETING TRENDS:
        {trends}
        
        ADDITIONAL CONTEXT:
        {context}
        
        INSTRUCTIONS:
        - Create compelling, actionable marketing content
        - Incorporate relevant trends naturally
        - Use professional but engaging language
        - Include specific examples and actionable tips
        - Keep the tone appropriate for the target audience
        - Structure the content with clear headings and bullet points
        
        Generate the content now:
        """)
        
        self.fallback_prompt = ChatPromptTemplate.from_template("""
        Create marketing content for: {prompt}
        
        Focus on: {trends}
        
        Generate engaging marketing content:
        """)
    
    def generate_content_with_llm(self, prompt: str, trends: List[str], context: str = "") -> str:
        """
        Generate content using OpenAI language model.
        
        Args:
            prompt: The main content generation prompt
            trends: List of current marketing trends
            context: Additional context from uploaded files
            
        Returns:
            Generated marketing content
        """
        if not self.llm:
            logger.warning("LLM not available, using fallback content generation")
            return self._generate_fallback_content(prompt, trends, context)
        
        try:
            # Format trends for prompt
            trends_text = "\n".join([f"- {trend}" for trend in trends])
            
            # Create the chain
            chain = (
                {"prompt": RunnablePassthrough(), "trends": lambda x: trends_text, "context": lambda x: context}
                | self.content_prompt
                | self.llm
                | StrOutputParser()
            )
            
            # Generate content
            content = chain.invoke(prompt)
            logger.info("Content generated successfully using OpenAI")
            return content
            
        except Exception as e:
            logger.error(f"Error generating content with LLM: {str(e)}")
            return self._generate_fallback_content(prompt, trends, context)
    
    def _generate_fallback_content(self, prompt: str, trends: List[str], context: str = "") -> str:
        """
        Generate fallback content when LLM is not available.
        
        Args:
            prompt: The main content generation prompt
            trends: List of current marketing trends
            context: Additional context from uploaded files
            
        Returns:
            Generated fallback content
        """
        # Simple template-based content generation
        trends_text = ", ".join(trends[:3])  # Use first 3 trends
        
        fallback_content = f"""
# Marketing Content: {prompt}

## Overview
Based on your request for "{prompt}", here's a comprehensive marketing strategy incorporating current industry trends.

## Key Trends to Leverage
{chr(10).join([f"- {trend}" for trend in trends[:5]])}

## Strategic Recommendations
1. **Content Strategy**: Develop content that addresses {trends[0] if trends else "current market needs"}
2. **Audience Engagement**: Focus on {trends[1] if len(trends) > 1 else "customer engagement"}
3. **Channel Optimization**: Leverage {trends[2] if len(trends) > 2 else "digital channels"}

## Action Items
- Create compelling content around {trends[0] if trends else "your key message"}
- Implement {trends[1] if len(trends) > 1 else "best practices"} in your marketing
- Monitor performance and adjust strategy based on results

## Additional Context
{context if context else "No additional context provided. Consider uploading relevant files for more targeted content."}

---
*This content was generated using our marketing content generator. For more personalized content, ensure your OpenAI API key is configured.*
        """
        
        logger.info("Fallback content generated successfully")
        return fallback_content.strip()
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the content agent as part of LangGraph workflow.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with generated content
        """
        try:
            # Extract required fields from state
            prompt = state.get("prompt", "")
            trends = state.get("trends", [])
            context = state.get("context", "")
            
            if not prompt:
                logger.error("No prompt provided to content agent")
                state["content"] = "Error: No prompt provided for content generation."
                return state
            
            # Generate content
            content = self.generate_content_with_llm(prompt, trends, context)
            
            # Update state with generated content
            state["content"] = content
            logger.info(f"Content agent generated content of length {len(content)}")
            
            return state
            
        except Exception as e:
            logger.error(f"Error in content agent: {str(e)}")
            state["content"] = f"Error generating content: {str(e)}"
            return state
