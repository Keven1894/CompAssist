# REST API Documentation

## Overview

The Local Computer Assistant exposes a REST API for agent-to-agent communication and programmatic access.

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### Development Information

**GET** `/dev-info`

Get system specifications and development tools information.

**Response:**
```json
{
  "status": "success",
  "data": {
    "system": {...},
    "specs": {...},
    "development_tools": {...},
    "development_environment": {...},
    "readiness": {...}
  }
}
```

### Environment Check

**POST** `/check`

Check computer environment.

**Request Body:**
```json
{
  "verbose": false,
  "include_software": true,
  "include_network": true,
  "include_security": true
}
```

### Setup System

**POST** `/setup`

Setup system from configuration.

**Request Body:**
```json
{
  "config_path": "config/default.yaml",
  "packages": ["git", "python"]
}
```

### Check Updates

**POST** `/update`

Check for system and software updates.

**Request Body:**
```json
{
  "auto_apply": false
}
```

### Diagnose Issues

**POST** `/diagnose`

Detect system issues.

**Request Body:**
```json
{
  "categories": ["disk", "memory"]
}
```

### Fix Issues

**POST** `/fix`

Fix detected issues.

**Request Body:**
```json
{
  "auto_fix": true,
  "issue_ids": ["disk-1", "memory-1"]
}
```

### Status

**GET** `/status`

Get assistant status.

### Capabilities

**GET** `/capabilities`

List all available capabilities.

### Agent Info

**GET** `/agent-info`

Get agent information for discovery.

### Health Check

**GET** `/health`

Health check endpoint.

## Authentication

Currently uses basic API key authentication (development mode).
For production, implement OAuth 2.0.

## Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Examples

See [Dev Info Endpoint](dev-info-endpoint.md) for detailed examples.

