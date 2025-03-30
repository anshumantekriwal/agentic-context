# Agentic Context API

This API allows you to interact with an agentic context system for document processing and querying.

## Authentication

All API requests require authentication using a secret API key. Include the API key in the request header:

```
X-API-Key: your_api_key_here
```

The API key is a 10-digit alphanumeric code that must be provided with every request. Without a valid API key, requests will be rejected with a 401 Unauthorized response.

## API Endpoints

### Upload Document

Upload a document to be processed by the agent.

**Endpoint:** `/upload`

**Method:** `POST`

**Headers:**

- `X-API-Key`: Your API key
- `Content-Type`: `multipart/form-data`

**Request Body:**

- `file`: The document file to upload

**Response:**

```json
{
  "agent_id": "string",
  "filename": "string",
  "chunk_count": "integer"
}
```

### Query Document

Query the processed document using natural language.

**Endpoint:** `/query`

**Method:** `POST`

**Headers:**

- `X-API-Key`: Your API key
- `Content-Type`: `application/json`

**Request Body:**

```json
{
  "query": "string",
  "agent_id": "string"
}
```

**Response:**

```json
{
  "answer": "string",
  "source_chunks": ["string"]
}
```

## Example Usage

### Command Line (curl)

```bash
# Upload a document
curl -X POST https://agentic-context.onrender.com/api/v1/upload \
  -H "X-API-Key: your_api_key_here" \
  -F "file=@uploads/CS.pdf" \
  -F "agent_id=test"

# Query the document
curl -X POST https://agentic-context.onrender.com/api/v1/query \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"query": "Who wrote Intro to Statistical Learning with Python?", "agent_id": "test"}'
```

### Python

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "https://agentic-context.onrender.com/api/v1"
headers = {"X-API-Key": API_KEY}

# Upload a document
files = {
    "file": ("CS.pdf", open("uploads/CS.pdf", "rb")),
    "agent_id": (None, "test")
}
response = requests.post(f"{BASE_URL}/upload", files=files, headers=headers)
upload_data = response.json()

# Query the document
query_data = {
    "query": "Who wrote Intro to Statistical Learning with Python?",
    "agent_id": "test"
}
response = requests.post(
    f"{BASE_URL}/query",
    json=query_data,
    headers=headers
)
query_result = response.json()
```

## Error Responses

- `401 Unauthorized`: Invalid or missing API key
- `400 Bad Request`: Invalid request format or missing required fields
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

## Rate Limiting

The API has rate limiting in place to ensure fair usage. Please contact the administrator for specific rate limit details.
