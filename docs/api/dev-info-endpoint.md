# Development Information API - Quick Reference

## Overview

The assistant can provide comprehensive development information including:
- ✅ System specifications (CPU, memory, disk)
- ✅ Development tools status (Python, Docker, Git, Node, Java)
- ✅ Development environment readiness assessment
- ✅ Recommendations for development setup

## REST API Endpoint

### GET `/api/v1/dev-info`

Get development information (system specs + dev tools)

**Request:**
```bash
curl http://localhost:8000/api/v1/dev-info
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "system": {
      "os": "windows",
      "os_version": "10.0.26100",
      "architecture": "64bit",
      "hostname": "GISBG",
      "processor": "Intel(R) Core(TM) i9-14900K"
    },
    "specs": {
      "cpu": {
        "cores": 32,
        "usage_percent": 4.7,
        "processor": "Intel(R) Core(TM) i9-14900K"
      },
      "memory": {
        "total_gb": 63.8,
        "available_gb": 48.5,
        "used_percent": 24.0,
        "status": "excellent"
      },
      "disk": {
        "total_gb": 1862.1,
        "free_gb": 1754.2,
        "used_percent": 5.8,
        "status": "excellent"
      }
    },
    "development_tools": {
      "python": {
        "installed": true,
        "version": "Python 3.11.6",
        "status": "installed"
      },
      "docker": {
        "installed": true,
        "version": "Docker version 28.5.1",
        "status": "installed",
        "daemon_running": true
      },
      "git": {
        "installed": false,
        "status": "not_installed"
      }
    },
    "development_environment": {
      "python_version": "Python 3.11.6",
      "docker_available": true,
      "docker_running": true,
      "git_available": false,
      "node_available": false,
      "java_available": false
    },
    "readiness": {
      "development_ready": true,
      "missing_tools": ["git"],
      "recommendations": [
        "Install Git for version control"
      ]
    }
  }
}
```

## MCP Endpoint

### Method: `mcp.get_dev_info`

Get development information via JSON-RPC 2.0

**Request:**
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "mcp.get_dev_info",
    "params": {},
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "system": {...},
    "specs": {...},
    "development_tools": {...},
    "development_environment": {...},
    "readiness": {...}
  },
  "id": 1
}
```

## Python Client Example

```python
import requests

# REST API
response = requests.get("http://localhost:8000/api/v1/dev-info")
dev_info = response.json()["data"]

print(f"OS: {dev_info['system']['os']}")
print(f"CPU Cores: {dev_info['specs']['cpu']['cores']}")
print(f"Memory: {dev_info['specs']['memory']['total_gb']} GB")
print(f"Python: {dev_info['development_environment']['python_version']}")
print(f"Docker: {'Available' if dev_info['development_environment']['docker_available'] else 'Not installed'}")

# MCP
mcp_request = {
    "jsonrpc": "2.0",
    "method": "mcp.get_dev_info",
    "params": {},
    "id": 1
}
response = requests.post("http://localhost:8000/mcp", json=mcp_request)
dev_info = response.json()["result"]
```

## Use Cases

1. **Development Environment Check**: Quickly assess if system is ready for development
2. **Agent Configuration**: Other AI agents can discover system capabilities
3. **Environment Setup**: Get recommendations for missing tools
4. **System Monitoring**: Track resource usage and system health

## Status Indicators

- **Memory Status**: `excellent` (<50%), `good` (50-75%), `warning` (75-90%), `critical` (>90%)
- **Disk Status**: Same as memory status
- **Development Ready**: `true` if Python is installed
- **Tool Status**: `installed` or `not_installed`

## Testing

```bash
# Start server
$env:PYTHONPATH="<project-root-directory>"
# Example: $env:PYTHONPATH="C:\projects\local-computer-assistant"
py src/api/server.py

# Test REST endpoint
curl http://localhost:8000/api/v1/dev-info

# Test MCP endpoint
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"mcp.get_dev_info","params":{},"id":1}'
```

