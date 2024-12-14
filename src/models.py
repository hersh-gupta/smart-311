from pydantic import BaseModel
from datetime import datetime
import dspy
from .config import ServiceNameLiteral

class ProcessedRequest(BaseModel):
    """A 311 request with AI-enhanced categorization and description"""
    original_service: ServiceNameLiteral
    recommended_service: ServiceNameLiteral
    updated_description: str
    emergency: bool = False
    image_verified: bool = False
    confidence: float
    rationale: str
    service_request_id: str
    status: str
    address: str
    lat: float
    long: float
    requested_datetime: datetime
    updated_datetime: datetime

class RequestInput(dspy.Signature):
    """Input format for 311 request processing"""
    service_request_id: str = dspy.InputField()
    status: str = dspy.InputField()
    service_name: ServiceNameLiteral = dspy.InputField()
    description: str = dspy.InputField()
    address: str = dspy.InputField()
    lat: float = dspy.InputField()
    long: float = dspy.InputField()
    requested_datetime: datetime = dspy.InputField()
    updated_datetime: datetime = dspy.InputField()
    image: dspy.Image = dspy.InputField()

    def __call__(self) -> ProcessedRequest:
        """Process the request and return enhanced version"""