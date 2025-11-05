# Agent-to-Agent Communication Design

## Overview

This document outlines the design for enabling other AI agents to communicate with the Local Computer Assistant using modern A2A (Agent-to-Agent) protocols.

## Protocol Selection

Based on 2024-2025 best practices, we'll implement **dual protocol support**:

### 1. **MCP (Model Context Protocol)** - Primary
- **Why**: Industry standard for AI agent communication
- **Protocol**: JSON-RPC 2.0 over HTTP/HTTPS
- **Features**: 
  - Secure tool invocation
  - Typed data exchange
  - OAuth-based security
  - Capability discovery
  - Context sharing

### 2. **REST API** - Secondary
- **Why**: Simple, universal access
- **Protocol**: RESTful HTTP/HTTPS
- **Features**:
  - Standard REST endpoints
  - JSON request/response
  - OpenAPI documentation
  - Easy integration

## Architecture

```
┌─────────────────────────────────────────────┐
│         Other AI Agents                     │
│  - Cursor AI                                │
│  - Claude Desktop                           │
│  - Custom Agents                            │
└──────────────┬──────────────────────────────┘
               │
               │ HTTP/HTTPS
               │ JSON-RPC (MCP) or REST
               │
┌──────────────▼──────────────────────────────┐
│      API Gateway Layer                       │
│  ┌──────────────────────────────────────┐   │
│  │  MCP Server (JSON-RPC 2.0)          │   │
│  │  - Tool Invocation                   │   │
│  │  - Capability Discovery              │   │
│  │  - Context Sharing                   │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │  REST API Server (FastAPI)           │   │
│  │  - /api/v1/check                     │   │
│  │  - /api/v1/setup                     │   │
│  │  - /api/v1/diagnose                  │   │
│  │  - /api/v1/fix                       │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │  Authentication Layer                │   │
│  │  - OAuth 2.0                         │   │
│  │  - JWT Tokens                        │   │
│  │  - API Keys                          │   │
│  └──────────────────────────────────────┘   │
└──────────────┬──────────────────────────────┘
               │
               │ Internal API
               │
┌──────────────▼──────────────────────────────┐
│      Local Computer Assistant Core          │
│  - EnvironmentChecker                       │
│  - SetupManager                            │
│  - UpdateManager                           │
│  - ProblemSolver                           │
└─────────────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: REST API Server
1. FastAPI-based REST server
2. Core endpoints for all assistant functions
3. JSON request/response format
4. OpenAPI/Swagger documentation
5. Basic authentication (API keys)

### Phase 2: MCP Server
1. JSON-RPC 2.0 server implementation
2. Tool registration and discovery
3. Capability negotiation
4. Context sharing mechanisms
5. OAuth 2.0 integration

### Phase 3: Security & Discovery
1. OAuth 2.0 implementation
2. JWT token management
3. Agent registry/discovery service
4. Rate limiting
5. Request logging and monitoring

### Phase 4: Advanced Features
1. WebSocket support for streaming
2. Agent-to-agent messaging
3. Task delegation
4. Event notifications
5. Health checks and status reporting

## API Endpoints Design

### REST API Endpoints

```
POST   /api/v1/check           # Check environment
POST   /api/v1/setup           # Setup system
POST   /api/v1/update          # Check/apply updates
POST   /api/v1/diagnose        # Diagnose issues
POST   /api/v1/fix             # Fix issues
GET    /api/v1/status          # Get assistant status
GET    /api/v1/capabilities    # List capabilities
GET    /api/v1/health          # Health check
```

### MCP Methods

```
mcp.check_environment(params)      # Check environment
mcp.setup_system(params)           # Setup system
mcp.check_updates(params)          # Check updates
mcp.diagnose_issues(params)        # Diagnose issues
mcp.fix_issues(params)             # Fix issues
mcp.list_capabilities()            # List capabilities
mcp.get_status()                    # Get status
```

## Security Considerations

1. **Authentication**:
   - OAuth 2.0 for production
   - API keys for development
   - JWT tokens for sessions

2. **Authorization**:
   - Role-based access control (RBAC)
   - Capability-based permissions
   - Least-privilege principle

3. **Data Protection**:
   - TLS encryption (HTTPS)
   - Input validation and sanitization
   - Rate limiting
   - Request logging

4. **Network Security**:
   - Firewall rules
   - IP whitelisting (optional)
   - CORS configuration

## Message Format

### REST Request
```json
{
  "command": "check",
  "parameters": {
    "verbose": true,
    "include_software": true
  }
}
```

### REST Response
```json
{
  "status": "success",
  "data": {
    "system": {...},
    "resources": {...},
    "software": [...]
  },
  "timestamp": "2025-01-20T10:30:00Z"
}
```

### MCP Request (JSON-RPC 2.0)
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.check_environment",
  "params": {
    "verbose": true,
    "include_software": true
  },
  "id": 1
}
```

### MCP Response (JSON-RPC 2.0)
```json
{
  "jsonrpc": "2.0",
  "result": {
    "system": {...},
    "resources": {...},
    "software": [...]
  },
  "id": 1
}
```

## Discovery Mechanism

### Agent Registry
- Self-registration endpoint
- Capability advertisement
- Health status reporting
- Service discovery via DNS or registry

### Agent Card Format
```json
{
  "agent_id": "local-computer-assistant",
  "name": "Local Computer Assistant",
  "version": "1.0.0",
  "capabilities": [
    "environment_check",
    "system_setup",
    "update_management",
    "problem_diagnosis",
    "automated_fixes"
  ],
  "endpoints": {
    "rest": "http://localhost:8000/api/v1",
    "mcp": "http://localhost:8000/mcp"
  },
  "authentication": {
    "methods": ["oauth2", "api_key"],
    "oauth2_endpoint": "http://localhost:8000/oauth2"
  }
}
```

## Next Steps

1. **Implement REST API** (FastAPI)
2. **Implement MCP Server** (JSON-RPC 2.0)
3. **Add Authentication** (OAuth 2.0 + API Keys)
4. **Create Agent Registry** (Discovery service)
5. **Documentation** (OpenAPI/Swagger)
6. **Testing** (Unit tests + Integration tests)

