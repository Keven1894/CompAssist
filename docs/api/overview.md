# Agent-to-Agent Communication Setup Guide

## Overview

The Local Computer Assistant now supports communication with other AI agents via:
1. **REST API** - Standard HTTP endpoints
2. **MCP Server** - JSON-RPC 2.0 protocol (Model Context Protocol)

## Quick Start

### 1. Install API Dependencies

```bash
pip install -r requirements-api.txt
```

### 2. Start the API Server

```bash
# Set PYTHONPATH
$env:PYTHONPATH="<project-root-directory>"
# Example: $env:PYTHONPATH="C:\projects\local-computer-assistant"

# Run API server
py src/api/server.py
```

The server will start on `http://localhost:8000`

### 3. Access Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **MCP Info**: http://localhost:8000/mcp/info

## API Endpoints

### REST API

#### Check Environment
```bash
curl -X POST http://localhost:8000/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"verbose": true, "include_software": true}'
```

#### Setup System
```bash
curl -X POST http://localhost:8000/api/v1/setup \
  -H "Content-Type: application/json" \
  -d '{"config_path": "config/default.yaml"}'
```

#### Diagnose Issues
```bash
curl -X POST http://localhost:8000/api/v1/diagnose \
  -H "Content-Type: application/json" \
  -d '{"categories": ["disk", "memory"]}'
```

#### Fix Issues
```bash
curl -X POST http://localhost:8000/api/v1/fix \
  -H "Content-Type: application/json" \
  -d '{"auto_fix": true}'
```

### MCP (JSON-RPC 2.0)

#### Check Environment
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "mcp.check_environment",
    "params": {"verbose": true},
    "id": 1
  }'
```

#### List Capabilities
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "mcp.list_capabilities",
    "params": {},
    "id": 1
  }'
```

## Integration Examples

### Python Client Example

```python
import requests

# REST API
response = requests.post(
    "http://localhost:8000/api/v1/check",
    json={"verbose": True}
)
print(response.json())

# MCP (JSON-RPC 2.0)
mcp_request = {
    "jsonrpc": "2.0",
    "method": "mcp.check_environment",
    "params": {"verbose": True},
    "id": 1
}
response = requests.post("http://localhost:8000/mcp", json=mcp_request)
print(response.json())
```

### JavaScript/TypeScript Client Example

```typescript
// REST API
const response = await fetch('http://localhost:8000/api/v1/check', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ verbose: true })
});
const data = await response.json();

// MCP (JSON-RPC 2.0)
const mcpRequest = {
  jsonrpc: "2.0",
  method: "mcp.check_environment",
  params: { verbose: true },
  id: 1
};
const mcpResponse = await fetch('http://localhost:8000/mcp', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(mcpRequest)
});
const mcpData = await mcpResponse.json();
```

## Security

### Current Implementation
- Basic API key authentication (development)
- CORS enabled for all origins (configure for production)

### Production Recommendations
1. **OAuth 2.0**: Implement proper OAuth 2.0 flow
2. **JWT Tokens**: Use JWT for session management
3. **HTTPS**: Always use HTTPS in production
4. **Rate Limiting**: Implement rate limiting
5. **CORS**: Configure CORS properly for production
6. **API Keys**: Use environment variables for API keys

## Docker Deployment

The API server can run in Docker:

```dockerfile
# Add to Dockerfile
EXPOSE 8000
CMD ["python", "src/api/server.py"]
```

```bash
docker run -it --rm \
  -p 8000:8000 \
  --privileged \
  local-computer-assistant
```

## Agent Discovery

### Get Agent Information
```bash
curl http://localhost:8000/api/v1/agent-info
```

Returns agent card with capabilities and endpoints.

## Best Practices

1. **Use MCP for AI Agents**: MCP is designed specifically for AI agent communication
2. **Use REST for General Clients**: REST is simpler for web apps and scripts
3. **Handle Errors**: Always check response status and handle errors
4. **Rate Limiting**: Implement client-side rate limiting
5. **Logging**: Log all API calls for debugging
6. **Versioning**: Use API versioning (`/api/v1/`) for future compatibility

## Next Steps

1. ✅ REST API implemented
2. ✅ MCP Server implemented
3. ⏳ OAuth 2.0 authentication
4. ⏳ Rate limiting
5. ⏳ WebSocket support for streaming
6. ⏳ Agent registry/discovery service

