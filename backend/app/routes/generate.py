import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from ..models.schemas import GenerateRequest, GenerateResponse
from ..utils.file_parser import parse_file_content
from ..utils.agents.workflow import ContentWorkflow

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize the content generation workflow
content_workflow = ContentWorkflow()

@router.post("/generate", response_model=GenerateResponse)
async def generate_content(request: GenerateRequest):
    """
    Generate marketing content using LangGraph workflow.
    
    Args:
        request: GenerateRequest containing prompt and optional file
        
    Returns:
        GenerateResponse with generated content and optional image URL
    """
    try:
        logger.info(f"Content generation request received for prompt: {request.prompt[:50]}...")
        
        # Parse file content if provided
        context = ""
        if request.file:
            logger.info("Processing uploaded file")
            context = parse_file_content(request.file)
            if not context:
                logger.warning("File parsing failed, proceeding without context")
                context = ""
            else:
                logger.info(f"File parsed successfully, context length: {len(context)}")
        
        # Run the content generation workflow
        logger.info("Starting content generation workflow")
        result = content_workflow.run(
            prompt=request.prompt,
            context=context
        )
        
        # Check if content generation was successful
        if not result.get("content") or result["content"].startswith("Error:"):
            logger.error(f"Content generation failed: {result.get('content', 'Unknown error')}")
            raise HTTPException(
                status_code=500,
                detail="Content generation failed. Please try again."
            )
        
        # Prepare response
        response = GenerateResponse(
            content=result["content"],
            image_url=result.get("image_url")
        )
        
        logger.info(f"Content generation completed successfully. Content length: {len(result['content'])}")
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in content generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/workflow-info")
async def get_workflow_info():
    """Get information about the content generation workflow."""
    try:
        info = content_workflow.get_workflow_info()
        return {
            "status": "success",
            "workflow": info
        }
    except Exception as e:
        logger.error(f"Error getting workflow info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve workflow information"
        )
