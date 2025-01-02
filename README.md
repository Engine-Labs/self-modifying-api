# Self Modifying API

⚠️ **SECURITY WARNING** ⚠️

**THIS IS A PROOF OF CONCEPT ONLY - DO NOT USE IN PRODUCTION**

This project allows arbitrary code execution through its API endpoints. Deploying this to the internet would create severe security vulnerabilities. This project is intended for educational and experimental purposes only.

## Project Overview

The Self Modifying API is an experimental FastAPI application that can modify its own codebase and API surface through HTTP requests. It demonstrates a unique approach to dynamic API modification where the API can accept POST requests that result in changes to its own functionality.

### Key Features

- Accepts Python code through POST requests
- Automatically creates new API endpoints from submitted code
- Self-modifying codebase through GitHub integration
- Automatic deployment updates (via Render)
- GPT/OpenAI Assistant API integration capabilities

### How It Works

The core functionality revolves around a single POST request handler that:

1. Accepts Python code as a string (following a specific format)
2. Commits the code to its own GitHub repository
3. Updates `app.py` to expose the new route in the API
4. Triggers a new deployment automatically

## Prerequisites

- Python 3.7+
- Git
- FastAPI understanding
- Access to GitHub repository
- Render.com account (for deployment)

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd self-modifying-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the development server:
   ```bash
   ./bin/dev
   ```

## Usage

The API accepts POST requests with Python code that defines new endpoints. The code must follow a specific format:

```python
from fastapi import APIRouter
router = APIRouter()

@router.get("/your-endpoint")
def your_function():
    return {"your": "response"}
```

### Example Request

```json
{
  "code": "from fastapi import APIRouter\nimport random\n\nrouter = APIRouter()\n\n@router.get(\"/random-number\")\ndef generate_random_number():\n    return {\"random_number\": random.randint(1, 100)}",
  "filepath": "random_number.py"
}
```

## GPT Integration

This API can be integrated with GPT/OpenAI's Assistant API. While the original intention was to allow GPTs to bootstrap their own actions, current limitations in GPT's dynamic API documentation import affect full functionality.

### GPT Configuration

- **Name**: `API Builder`
- **Description**: `Make API endpoints on the fly`
- **Instructions**:
```
You make API endpoints by writing Python code for a FastAPI backend. Always use:

from fastapi import APIRouter
router = APIRouter()

when creating new endpoints.
```

### Integration Setup

1. The API exposes endpoint documentation via `/openai.json`
2. Server URL must be manually added to GPT configuration
3. Actions need to be reloaded when new endpoints are created

### Example Integration
![](self-modifying-gpt.png)

## Known Limitations

- No automatic handling of new dependencies (e.g., if new endpoint requires numpy)
- GPTs don't dynamically import API documentation
- Manual reload required for new endpoints in GPT configuration
- Security considerations for arbitrary code execution

## Contributing

While this is a proof of concept, contributions that improve security, add features, or fix bugs are welcome. Please ensure you:

1. Create an issue first to discuss changes
2. Follow existing code style
3. Add appropriate tests
4. Update documentation

## License

This project is intended for educational purposes. See the LICENSE file for details.

## Security Considerations

This project intentionally allows arbitrary code execution, which is extremely dangerous in a production environment. Key risks include:

- Remote code execution
- Server compromise
- Data exposure
- Resource exhaustion
- Network security vulnerabilities

**DO NOT deploy this application to any public-facing environment.**