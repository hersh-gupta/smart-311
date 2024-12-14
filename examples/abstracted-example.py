from src.processor import process_311_request
from src.config import setup_llm

# Configure LLM
setup_llm()

# Example request
request = {
    "service_request_id": "101005820652",
    "status": "open",
    "service_name": "Requests for Street Cleaning",
    "description": "Lots of trash behind Washington St SL stop by Blackstone school",
    "requested_datetime": "2024-12-14T18:00:00Z",
    "updated_datetime": "2024-12-14T18:01:35Z",
    "address": "Intersection Of Mystic St And Washington St, Roxbury, Ma",
    "lat": 42.34047663,
    "long": -71.07111052,
    "media_url": "https://spot-boston-res.cloudinary.com/image/upload/v1734199257/boston/production/uc0xuhevrghsuq8gmdyu.jpg"
}

# Process request
result = process_311_request(request)

# Print results
print(f"Original Service: {result.original_service}")
print(f"Recommended Service: {result.recommended_service}")
print(f"Enhanced Description: {result.updated_description}")
print(f"Confidence: {result.confidence}")
print(f"Emergency: {result.emergency}")
print(f"Image Verified: {result.image_verified}")