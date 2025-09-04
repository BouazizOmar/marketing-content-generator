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
        
        ADDITIONAL CONTEXT:
        {context}
        
        INSTRUCTIONS:
        - Create compelling, actionable marketing content
        - Use professional but engaging language
        - Include specific examples and actionable tips
        - Keep the tone appropriate for the target audience
        - Structure the content with clear headings and bullet points
        
        Generate the content now:
        """)
        
        self.fallback_prompt = ChatPromptTemplate.from_template("""
        Create marketing content for: {prompt}
        
        Generate engaging marketing content:
        """)
    
    def generate_content_with_llm(self, prompt: str, context: str = "") -> str:
        """
        Generate content using OpenAI language model.
        
        Args:
            prompt: The main content generation prompt
            context: Additional context from uploaded files
            
        Returns:
            Generated marketing content
        """
        if not self.llm:
            logger.warning("LLM not available, using fallback content generation")
            return self._generate_fallback_content(prompt, context)
        
        try:
            # Create the chain
            chain = (
                {"prompt": RunnablePassthrough(), "context": lambda x: context}
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
            logger.error(f"LLM error type: {type(e)}")
            logger.error(f"LLM error details: {e}")
            return self._generate_fallback_content(prompt, context)
    
    def _generate_fallback_content(self, prompt: str, context: str = "") -> str:
        """
        Generate fallback content when LLM is not available.
        
        Args:
            prompt: The main content generation prompt
            context: Additional context from uploaded files
            
        Returns:
            Generated fallback content
        """
        # Simple template-based content generation
        fallback_content = f"""
# Marketing Content: {prompt}

## Overview
Based on your request for "{prompt}", here's a comprehensive marketing strategy.

## Strategic Recommendations
1. **Content Strategy**: Develop content that addresses your target audience
2. **Audience Engagement**: Focus on customer engagement and value delivery
3. **Channel Optimization**: Leverage digital channels effectively

## Action Items
- Create compelling content around your key message
- Implement best practices in your marketing
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
            context = state.get("context", "")
            
            if not prompt:
                logger.error("No prompt provided to content agent")
                state["content"] = "Error: No prompt provided for content generation."
                return state
            
            # Generate content
            content = self.generate_content_with_llm(prompt, context)
            
            # Update state with generated content
            state["content"] = content
            logger.info(f"Content agent generated content of length {len(content)}")
            
            return state
            
        except Exception as e:
            logger.error(f"Error in content agent: {str(e)}")
            logger.error(f"Content agent error type: {type(e)}")
            logger.error(f"Content agent error details: {e}")
            state["content"] = f"Error generating content: {str(e)}"
            return state
