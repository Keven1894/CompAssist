# Getting Started

## Installation

### Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Docker Desktop** (optional, for Docker deployment)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install API Dependencies (for agent communication)

```bash
pip install -r requirements-api.txt
```

### Step 3: Verify Installation

```bash
# Set PYTHONPATH
$env:PYTHONPATH="<project-root-directory>"
# Example: $env:PYTHONPATH="C:\projects\local-computer-assistant"

# Test the assistant
py src/main.py check
```

## Quick Start

### Run Local Assistant

```bash
# Check environment
py src/main.py check

# Setup system
py src/main.py setup --config config/default.yaml

# Diagnose issues
py src/main.py diagnose

# Fix issues
py src/main.py fix
```

### Start API Server

```bash
# Start server
py src/api/server.py

# Server will be available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

## Next Steps

- See [Quick Start Guide](quickstart.md) for detailed usage
- See [Docker Setup](docker-setup.md) for containerized deployment
- See [API Overview](../api/overview.md) for agent communication

