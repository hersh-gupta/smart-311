from datetime import datetime
from .models import ProcessedRequest, RequestInput
from .config import FORMATTED_SYSTEM_PROMPT, ServiceNameLiteral
import dspy

class VerifierSignature(dspy.Signature):
    """Signature for verifying service classification"""
    description: str = dspy.InputField()
    location: str = dspy.InputField()
    current_service: ServiceNameLiteral = dspy.InputField()
    image: dspy.Image = dspy.InputField()
    
    keep_service: bool = dspy.OutputField(desc="Whether to keep the current service classification")
    recommended_service: ServiceNameLiteral = dspy.OutputField(desc="The recommended service if different")
    confidence: float = dspy.OutputField(desc="Confidence in the classification (0-1)")
    rationale: str = dspy.OutputField(desc="Reasoning for the recommendation")

    def forward(self):
        # Apply system prompt for consistent processing
        self.prompt = FORMATTED_SYSTEM_PROMPT

class EnhancerSignature(dspy.Signature):
    """Signature for enhancing request description"""
    description: str = dspy.InputField()
    location: str = dspy.InputField()
    image: dspy.Image = dspy.InputField()
    service_name: ServiceNameLiteral = dspy.InputField()  # Added to provide context
    
    enhanced_description: str = dspy.OutputField(desc="Enhanced actionable description to be more detailed and actionable for city workers")
    emergency: bool = dspy.OutputField(desc="Whether this poses immediate threat to public safety and shows active danger to a person")
    image_verified: bool = dspy.OutputField(desc="Whether the image supports the issue")

    def forward(self):
        # Apply system prompt for consistent processing
        self.prompt = FORMATTED_SYSTEM_PROMPT

class ServiceVerifier(dspy.Module):
    """Verifies if the current service classification is correct"""
    def forward(self, description: str, image: dspy.Image, 
                current_service: ServiceNameLiteral,
                address: str):
        
        predict = dspy.Predict(VerifierSignature)
        result = predict(
            description=description,
            location=address,
            current_service=current_service,
            image=image
        )
        
        # Default to original service with 0.5 confidence if conditions are met
        if (len(description.strip()) < 10 or  # Very short/vague description
            "multiple issues" in result.rationale.lower() or
            "conflicting information" in result.rationale.lower() or
            "insufficient context" in result.rationale.lower()):
            result.keep_service = True
            result.confidence = 0.5
            result.recommended_service = current_service
        
        return result

class DescriptionEnhancer(dspy.Module):
    """Enhances the request description with relevant details"""
    def forward(self, description: str, image: dspy.Image, address: str, service_name: ServiceNameLiteral):
        predict = dspy.Predict(EnhancerSignature)
        result = predict(
            description=description,
            location=address,
            image=image,
            service_name=service_name
        )
        
        return result

class RequestProcessor(dspy.Module):
    """Main module for processing 311 requests"""
    def __init__(self):
        super().__init__()
        self.verifier = ServiceVerifier()
        self.enhancer = DescriptionEnhancer()
    
    def forward(self, request: RequestInput) -> ProcessedRequest:
        # Verify service classification
        verification = self.verifier(
            request.description,
            request.image,
            request.service_name,
            request.address
        )
        
        # Enhance description
        enhancement = self.enhancer(
            request.description,
            request.image,
            request.address,
            verification.recommended_service if not verification.keep_service else request.service_name
        )
        
        # Construct final response
        return ProcessedRequest(
            service_request_id=request.service_request_id,
            status=request.status,
            address=request.address,
            lat=request.lat,
            long=request.long,
            requested_datetime=request.requested_datetime,
            updated_datetime=request.updated_datetime,
            original_service=request.service_name,
            recommended_service=(verification.recommended_service 
                               if not verification.keep_service 
                               else request.service_name),
            updated_description=enhancement.enhanced_description,
            emergency=enhancement.emergency,
            image_verified=enhancement.image_verified,
            confidence=verification.confidence,
            rationale=verification.rationale
        )

def process_311_request(request_json: dict):
    """Process a 311 request from JSON format"""
    # Load image from URL
    image = dspy.Image.from_url(request_json['media_url'])
    
    # Convert datetime strings to datetime objects
    requested_dt = datetime.fromisoformat(request_json['requested_datetime'].replace('Z', '+00:00'))
    updated_dt = datetime.fromisoformat(request_json['updated_datetime'].replace('Z', '+00:00'))
    
    # Initialize the processor
    processor = RequestProcessor()
    
    # Create input
    request_input = RequestInput(
        service_request_id=request_json['service_request_id'],
        status=request_json['status'],
        service_name=request_json['service_name'],
        description=request_json['description'],
        address=request_json['address'],
        lat=request_json['lat'],
        long=request_json['long'],
        requested_datetime=requested_dt,
        updated_datetime=updated_dt,
        image=image
    )
    
    # Process request
    result = processor(request_input)
    return result