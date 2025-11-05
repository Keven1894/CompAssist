# MCP Protocol Documentation

## Overview

MCP (Model Context Protocol) implementation using JSON-RPC 2.0 for standardized agent-to-agent communication.

## Endpoint

```
POST http://localhost:8000/mcp
```

## Protocol

JSON-RPC 2.0 specification.

## Methods

### mcp.get_dev_info

Get development information: system specs and development tools.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.get_dev_info",
  "params": {},
  "id": 1
}
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

### mcp.check_environment

Check and analyze computer environment.

**Request:**
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

### mcp.setup_system

Setup and configure system.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.setup_system",
  "params": {
    "config_path": "config/default.yaml"
  },
  "id": 1
}
```

### mcp.check_updates

Check for system and software updates.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.check_updates",
  "params": {
    "auto_apply": false
  },
  "id": 1
}
```

### mcp.diagnose_issues

Detect system issues.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.diagnose_issues",
  "params": {
    "categories": ["disk", "memory"]
  },
  "id": 1
}
```

### mcp.fix_issues

Fix detected issues.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.fix_issues",
  "params": {
    "auto_fix": true,
    "issue_ids": ["disk-1"]
  },
  "id": 1
}
```

### mcp.list_capabilities

List all available capabilities.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.list_capabilities",
  "params": {},
  "id": 1
}
```

### mcp.get_status

Get assistant status.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.get_status",
  "params": {},
  "id": 1
}
```

## Error Handling

Errors follow JSON-RPC 2.0 error format:

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32603,
    "message": "Internal error",
    "data": "Error details"
  },
  "id": 1
}
```

## Error Codes

- `-32600`: Invalid Request
- `-32601`: Method not found
- `-32603`: Internal error

## Server Info

**GET** `/mcp/info`

Get MCP server information.

## Batch Requests

MCP supports batch requests:

```json
[
  {
    "jsonrpc": "2.0",
    "method": "mcp.get_dev_info",
    "params": {},
    "id": 1
  },
  {
    "jsonrpc": "2.0",
    "method": "mcp.get_status",
    "params": {},
    "id": 2
  }
]
```

## Examples

See [API Overview](overview.md) for detailed examples.

