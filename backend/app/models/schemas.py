from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatMessage(BaseModel):
    """Schema for a single chat message"""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """Schema for incoming chat request"""
    message: str = Field(..., min_length=1, max_length=2000, description="User's question")
    conversation_history: Optional[List[ChatMessage]] = Field(default=[], description="Previous messages")


class ChatResponse(BaseModel):
    """Schema for chat response"""
    answer: str = Field(..., description="Chatbot's response")
    sources: Optional[List[str]] = Field(default=[], description="Source documents used")
    timestamp: datetime = Field(default_factory=datetime.now)


class FineVerificationRequest(BaseModel):
    """Schema for fine verification request"""
    challan_number: Optional[str] = Field(None, description="E-challan number")
    vehicle_number: str = Field(..., description="Vehicle registration number")
    violation_type: Optional[str] = Field(None, description="Type of traffic violation")


class FineVerificationResponse(BaseModel):
    """Schema for fine verification response"""
    vehicle_number: str
    violation_type: str
    fine_amount: int
    applicable_section: str
    description: str
    payment_link: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    app_name: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)
