from src.processor import process_311_request
from src.config import setup_llm

# Configure LLM
setup_llm()

# Example request
request = {
    "service_request_id": "101005820254",
    "status": "closed",
    "status_notes": "Resolved.",
    "service_name": "Requests for Street Cleaning",
    "service_code": "Public Works Department:Street Cleaning:Requests for Street Cleaning",
    "description": "Garbage on sidewalk",
    "requested_datetime": "2024-12-14T01:00:00Z",
    "updated_datetime": "2024-12-14T01:25:16Z",
    "address": "19 Worcester St, Roxbury, Ma, 02118",
    "lat": 42.33801041,
    "long": -71.07624045,
    "media_url": "https://spot-boston-res.cloudinary.com/image/upload/v1734138056/boston/production/x1vhcizd7nvzb7xdzkfe.jpg#spot=e8762677-4564-41c3-b58b-3ddd206801cb",
    "token": "93a90056-cccf-4d22-88bf-116c157d041e",
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
print("\nFull Result:")
print(result.model_dump_json(indent=2))
