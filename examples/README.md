# Examples

This directory contains example implementations of the Smart 311 System, demonstrating different ways to use the system:

## Files

### `simple-example.py`
A standalone example that shows the core functionality using just DSPy and LLaVA. This is useful for:
- Understanding the basic concepts
- Quick prototyping
- Testing the system without installing the full package

### `abstracted-example.py`
A more complete example using the modular approach from the `src/` directory. This demonstrates:
- Proper project structure
- Configuration management
- Full feature set including confidence scoring and emergency detection

## Usage

To run the examples:

1. Make sure you have the prerequisites installed:
   ```bash
   pip install dspy-ai pydantic
   ```

2. Install and start Ollama with LLaVA:
   ```bash
   ollama pull llava:7b
   ollama run llava:7b
   ```

3. Run either example:
   ```bash
   python examples/simple-example.py
   # or
   python examples/abstracted-example.py
   ```

## Note
These examples use a local instance of LLaVA through Ollama. For production use, consider using a hosted API service.