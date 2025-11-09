# API Documentation

Documentation for CompAssist API interfaces.

## Overview

CompAssist provides two API interfaces for programmatic access and agent-to-agent communication:
1. **REST API** - HTTP/JSON endpoints
2. **MCP Protocol** - Model Context Protocol (JSON-RPC 2.0)

## Documents in This Directory

### [`overview.md`](overview.md)
**API Overview and Setup**
- Introduction to both APIs
- Installation and setup
- Environment configuration
- Quick start examples

### [`rest-api.md`](rest-api.md)
**REST API Reference**
- Endpoint documentation
- Request/response formats
- Authentication
- Error handling
- Usage examples

### [`mcp-protocol.md`](mcp-protocol.md)
**Model Context Protocol (MCP)**
- MCP overview and specification
- JSON-RPC 2.0 implementation
- Available methods
- Protocol examples
- Client integration

### [`dev-info-endpoint.md`](dev-info-endpoint.md)
**Development Information API**
- Development info endpoint details
- System specifications
- Installed tools detection
- Response format
- Use cases

## Quick Reference

### Starting the Servers

**REST API:**
```bash
# Set API key (optional)
export API_KEY="your-secret-key"

# Start server
python src/api/server.py

# Access Swagger UI
# http://localhost:8000/docs
```

**MCP Server:**
```bash
# Start server
python src/api/mcp_server.py

# Server runs on http://localhost:8001
```

### Authentication

**REST API:**
```bash
curl -H "X-API-Key: your-secret-key" http://localhost:8000/api/v1/dev-info
```

**MCP:**
No authentication by default (designed for local agent communication).

## API Endpoints Summary

### REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/dev-info` | GET | Development information |
| `/docs` | GET | Swagger UI documentation |
| `/openapi.json` | GET | OpenAPI specification |

### MCP Methods

| Method | Description |
|--------|-------------|
| `mcp.get_dev_info` | Get development information |
| `mcp.list_capabilities` | List available methods |

## Use Cases

### For Developers
- **System inspection**: Query installed tools and versions
- **Environment verification**: Check development environment
- **CI/CD integration**: Automated environment checks

### For AI Agents
- **Capability discovery**: What tools are available?
- **System awareness**: What's the system configuration?
- **Tool invocation**: Request system operations
- **Agent coordination**: Share system state with other agents

## Examples

### REST API Example
```bash
# Get development information
curl http://localhost:8000/api/v1/dev-info

# Response
{
  "system": {
    "os": "Windows",
    "version": "10.0.19045",
    "architecture": "AMD64"
  },
  "tools": {
    "python": {"installed": true, "version": "3.11.0"},
    "git": {"installed": true, "version": "2.42.0"},
    "docker": {"installed": true, "version": "24.0.6"}
  }
}
```

### MCP Example
```bash
# Call MCP method
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "mcp.get_dev_info",
    "params": {},
    "id": 1
  }'

# Response
{
  "jsonrpc": "2.0",
  "result": {
    "system": {...},
    "tools": {...}
  },
  "id": 1
}
```

## Development

### Adding New Endpoints

**REST API (`src/api/server.py`):**
```python
@app.get("/api/v1/new-endpoint")
async def new_endpoint():
    return {"status": "ok"}
```

**MCP Server (`src/api/mcp_server.py`):**
```python
@mcp.method()
async def get_new_info(params: dict) -> dict:
    return {"info": "data"}
```

### Testing APIs

**REST API:**
```bash
# Health check
curl http://localhost:8000/health

# With authentication
curl -H "X-API-Key: test-key" http://localhost:8000/api/v1/dev-info
```

**MCP:**
```bash
# Test JSON-RPC call
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"mcp.list_capabilities","id":1}'
```

## Security

### REST API
- **API Key authentication**: Optional but recommended
- **HTTPS**: Use reverse proxy for production
- **CORS**: Configure for web clients
- **Rate limiting**: Add middleware if needed

### MCP
- **Local use**: Designed for localhost communication
- **Network security**: Use firewall rules
- **Agent trust**: Only for trusted agents

## Dependencies

Install API dependencies:
```bash
pip install -r requirements-api.txt
```

**Required packages:**
- `fastapi` - REST API framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `python-multipart` - Form data support

## Troubleshooting

### Server won't start
```bash
# Check port availability
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux

# Use different port
uvicorn src.api.server:app --port 8080
```

### Authentication errors
```bash
# Set API key
export API_KEY="your-key"  # Linux
$env:API_KEY="your-key"  # Windows

# Or pass in request
curl -H "X-API-Key: your-key" ...
```

### Import errors
```bash
# Set PYTHONPATH
export PYTHONPATH=/path/to/project  # Linux
$env:PYTHONPATH="C:\path\to\project"  # Windows
```

## Related Documentation

- **Main README**: `/README.md`
- **Installation**: `/docs/getting-started/installation.md`
- **Architecture**: `/docs/architecture/agent-communication.md`
- **Source Code**: `/src/api/`

## External Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [OpenAPI Specification](https://swagger.io/specification/)


