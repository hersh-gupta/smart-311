# Smart 311 System

Enhance municipal 311 service request processing using Large Multimodal Models (LMMs) to improve request categorization, description quality, and emergency response times. This example uses DSPy and LLaVA to analyze both text descriptions and images from 311 requests, providing more accurate service categorization and detailed descriptions for city workers.

## Features

- Automatic service category verification and recommendation
- Enhanced request descriptions based on both text and images
- Emergency situation detection
- Image verification against reported issues
- Professional language processing to remove subjective content
- Confidence scoring for service categorization

## Prerequisites

- Python 3.8+
- [DSPy](https://dspy.ai/)
- [Ollama](https://ollama.com/) with [LLaVA](https://llava-vl.github.io/) model (if using local model)

## Installation

```bash
git clone https://github.com/hersh-gupta/smart-311.git
cd smart-311
pip install dspy-ai pydantic

# Install Ollama and LLaVA model
# See https://ollama.ai for Ollama installation
ollama pull llava:7b
```

## Usage

### Examples
For code examples and different implementation approaches, check out [examples directory](examples/). It includes both a simple standalone implementation and a more complete example using the full project structure.

### Configuration
Customize the system in [`src/config.py`](src/config.py):

```python
# Change service categories
SERVICE_DEFINITIONS = {
    "Your Service": "Description of your service"
}

# Modify system prompt
SYSTEM_PROMPT = """Your custom prompt here"""

# Use different model
setup_llm(
    model_name="your-model",
    api_base="your-endpoint",
    api_key="your-key"
)
```

### Basic Example

```python
from smart_311 import process_311_request

# Example 311 request
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

# Process the request
result = process_311_request(request)

# Print the enhanced description and recommended service
print(f"Enhanced Description: {result.updated_description}")
print(f"Recommended Service: {result.recommended_service}")
print(f"Confidence: {result.confidence}")
```

```python
Recommended Service: Requests for Street Cleaning
Enhanced Description: The area is littered with trash and debris. A blue box is present on the sidewalk, which needs to be removed or emptied. The surrounding area also requires attention to maintain cleanliness in the neighborhood.
Confidence: 0.85
```

### Project Structure

```
smart-311/
├── src/
│   ├── processor.py           # Main request processing logic
│   ├── models.py              # Data models and type definitions
│   └── config.py              # Configuration and constants
├── examples/
│   ├── abstracted-example.py  # Uses the modules from /src
│   └── simple_example.py      # Stand-alone example
├── tests/
│   └── test_processor.py
└── README.md
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using [DSPy](https://github.com/stanfordnlp/dspy)
- Uses [LLaVA](https://github.com/haotian-liu/LLaVA) for multimodal analysis
- Inspired by real-world municipal 311 systems

## Technical Details

For more detailed technical information about how the system works, see the accompanying [blog post](https://hershgupta.com/posts/smarter-311-with-vision-models/).