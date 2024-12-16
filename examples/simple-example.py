import dspy
from typing import Literal
import json

# Configure the local LLaVA model
lm = dspy.LM("ollama/llama3.2-vision", api_base="http://127.0.0.1:11434/", api_key="")
dspy.configure(lm=lm)

ServiceNameLiteral = Literal[
    "Outdoor Dining", "Streetlights", "Litter", "Broken Park Equipment",
    "Damaged Sign", "New Tree Requests", "Abandoned Bicycle", "Other",
    "Needle Cleanup", "Park Lights", "Residential Trash out Illegally",
    "Abandoned Vehicle", "Pothole", "Dead Animal Pickup", "Short Term Rental",
    "Broken Sidewalk", "Illegal Parking", "Traffic Signal", "Dead Tree Removal",
    "Tree Pruning", "Overflowing Trash Can", "Rodent Sighting", "Illegal Graffiti"
]

SYSTEM_PROMPT = """You are a municipal services assistant. Analyze the request description and image 
to create a detailed description for city workers. Also select the most appropriate service category from the available options.

GUIDELINES:
- Use professional, factual language
- Include details from both text and images
- Remove subjective or emotional language
- Focus on observable facts and specific details
- Include measurements or quantities when visible
- Note any accessibility or safety impacts
- If the image shows details not in the text, include them
- If image and text conflict, trust the image
"""

class EnhancerSignature(dspy.Signature):
    """Improve the description based on the original description and image."""
    image: dspy.Image = dspy.InputField(desc="The image showing the issue")
    original_description: str = dspy.InputField(desc="The original description text")
    enhanced_description: str = dspy.OutputField(desc="Enhanced actionable description")
    recommended_service_category: ServiceNameLiteral = dspy.OutputField(desc="Recommended service category")

    def forward(self):
        self.prompt = SYSTEM_PROMPT

# Initialize the predictor
predictor = dspy.Predict(EnhancerSignature)

# Example usage
image = dspy.Image.from_url(
    "https://spot-boston-res.cloudinary.com/image/upload/v1734138056/boston/production/x1vhcizd7nvzb7xdzkfe.jpg"
)
description = "Garbage on sidewalk"

result = predictor(image=image, original_description=description)
print(f"Enhanced Description: {result.enhanced_description}")
print(f"Recommended Service: {result.recommended_service_category}")
print("\nFull Result:")
print(json.dumps(result.toDict(), indent=2, default=str))