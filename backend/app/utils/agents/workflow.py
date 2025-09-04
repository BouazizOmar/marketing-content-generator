import logging
from typing import TypedDict, List, Dict, Any, Annotated
from langgraph.graph import StateGraph, END
from .content_agent import ContentAgent

logger = logging.getLogger(__name__)

class ContentState(TypedDict):
    """State definition for the content generation workflow."""
    prompt: str
    content: str
    context: str
    image_url: str | None

class ContentWorkflow:
    """LangGraph workflow for marketing content generation."""
    
    def __init__(self):
        self.content_agent = ContentAgent()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        # Create the state graph
        workflow = StateGraph(ContentState)
        
        # Add nodes
        workflow.add_node("content_agent", self._content_agent_node)
        
        # Define the flow: content_agent -> END
        workflow.set_entry_point("content_agent")
        workflow.add_edge("content_agent", END)
        
        # Compile the graph
        compiled_graph = workflow.compile()
        
        logger.info("Content generation workflow built successfully")
        return compiled_graph
    
    def _content_agent_node(self, state: ContentState) -> ContentState:
        """
        Execute the content agent node.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with generated content
        """
        try:
            logger.info("Executing content agent node")
            
            # Run content agent
            updated_state = self.content_agent.run(state)
            
            # Ensure content is in the state
            if "content" not in updated_state or not updated_state["content"]:
                logger.warning("No content generated, using fallback")
                updated_state["content"] = "Error: Content generation failed. Please try again."
            
            # Set default image_url if not present
            if "image_url" not in updated_state:
                updated_state["image_url"] = None
            
            logger.info(f"Content agent completed with content length {len(updated_state['content'])}")
            return updated_state
            
        except Exception as e:
            logger.error(f"Error in content agent node: {str(e)}")
            # Return state with error content
            state["content"] = f"Error generating content: {str(e)}"
            state["image_url"] = None
            return state
    
    def run(self, prompt: str, context: str = "", config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run the complete content generation workflow.
        
        Args:
            prompt: The content generation prompt
            context: Additional context from uploaded files
            config: Optional configuration for the workflow
            
        Returns:
            Dictionary with generated content and metadata
        """
        try:
            # Initialize state
            initial_state = ContentState(
                prompt=prompt,
                content="",
                context=context,
                image_url=None
            )
            
            logger.info(f"Starting content generation workflow for prompt: {prompt[:50]}...")
            
            # Run the workflow
            result = self.graph.invoke(initial_state, config=config or {})
            logger.info(f"Workflow result type: {type(result)}")
            logger.info(f"Workflow result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
            
            # Extract results - handle different LangGraph result formats
            if isinstance(result, dict):
                # Try different possible keys for final state
                final_state = (
                    result.get("end", {}) or 
                    result.get("__end__", {}) or 
                    result.get("final", {}) or
                    result
                )
            else:
                # If result is not a dict, use it directly
                final_state = result if hasattr(result, 'get') else {}
            
            logger.info(f"Final state extracted: {final_state}")
            
            # Prepare response
            response = {
                "content": final_state.get("content", ""),
                "image_url": final_state.get("image_url"),
                "prompt": final_state.get("prompt", ""),
                "context_processed": bool(final_state.get("context", ""))
            }
            
            logger.info("Content generation workflow completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error running content generation workflow: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e}")
            return {
                "content": f"Error: Content generation failed - {str(e)}",
                "image_url": None,
                "prompt": prompt,
                "context_processed": False
            }
    
    def get_workflow_info(self) -> Dict[str, Any]:
        """Get information about the workflow structure."""
        return {
            "nodes": ["content_agent"],
            "flow": "content_agent -> END",
            "state_schema": {
                "prompt": "str",
                "content": "str",
                "context": "str",
                "image_url": "str | None"
            }
        }
