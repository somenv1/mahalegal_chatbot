from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

from ...models.schemas import (
    ChatRequest, 
    ChatResponse, 
    FineVerificationRequest,
    FineVerificationResponse
)
from ...core.rag_system import rag_system

router = APIRouter(prefix="/api/v1", tags=["chat"])
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return AI-generated response based on Maharashtra traffic laws.
    
    This endpoint uses RAG (Retrieval-Augmented Generation) to provide accurate legal information.
    """
    try:
        # Convert conversation history to dict format
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ] if request.conversation_history else []
        
        # Query the RAG system
        result = rag_system.query(
            question=request.message,
            conversation_history=history
        )
        
        return ChatResponse(
            answer=result["answer"],
            sources=result.get("sources", [])
        )
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing your request: {str(e)}"
        )


@router.post("/verify-fine", response_model=FineVerificationResponse)
async def verify_fine(request: FineVerificationRequest):
    """
    Verify fine amount for a traffic violation.
    
    Can search by violation type or code to get accurate fine information.
    """
    try:
        # If violation type is provided, search for matching violations
        if request.violation_type:
            violations = rag_system.search_violation_by_type(request.violation_type)
            
            if not violations:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No violation found matching '{request.violation_type}'"
                )
            
            # Return the first match
            violation = violations[0]
            
            return FineVerificationResponse(
                vehicle_number=request.vehicle_number,
                violation_type=violation.get('violation_name', 'Unknown'),
                fine_amount=violation.get('fine_amount', 0),
                applicable_section=violation.get('section', 'N/A'),
                description=violation.get('description', ''),
                payment_link="https://mahatrafficechallan.gov.in"
            )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide violation_type to verify fine"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying fine: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying fine: {str(e)}"
        )


@router.get("/violations")
async def list_violations(search: str = None):
    """
    List all traffic violations or search for specific violations.
    
    Query params:
        search: Optional search term to filter violations
    """
    try:
        if search:
            violations = rag_system.search_violation_by_type(search)
        else:
            violations = list(rag_system.fines_data.values())
        
        return {
            "total": len(violations),
            "violations": violations[:20]  # Limit to 20 results
        }
    
    except Exception as e:
        logger.error(f"Error listing violations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving violations: {str(e)}"
        )
