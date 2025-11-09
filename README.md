# Local Computer Assistant

A comprehensive local computer assistant for standardizing computer environment checking, setup, updates, and problem solving. Starting with Windows support, with plans to expand to Linux for various use cases (art design, study, financial, etc.).

## Features

- **Environment Checking**: Analyze system configuration, installed software, resources
- **Setup Automation**: Standardize and automate software installation and configuration
- **Update Management**: Check for and apply system and software updates
- **Problem Solving**: Detect issues and provide automated fixes
- **Agent-to-Agent Communication**: REST API and MCP (JSON-RPC 2.0) endpoints for AI agent integration

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Docker Desktop (optional, for containerized deployment)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install API dependencies (for agent communication)
pip install -r requirements-api.txt
```

### Usage

```bash
# Set PYTHONPATH (adjust path to your project location)
$env:PYTHONPATH="<project-root-directory>"
# Example: $env:PYTHONPATH="C:\projects\local-computer-assistant"

# Run commands
py src/main.py check          # Check environment
py src/main.py setup          # Setup system
py src/main.py diagnose       # Diagnose issues
py src/main.py fix            # Fix issues

# Start API server (for agent communication)
py src/api/server.py
```

## Docker Deployment

```bash
# Build image
docker build -t local-computer-assistant .

# Run container
docker run -it --rm --privileged local-computer-assistant check

# Or use docker-compose
docker-compose up
```

## API Endpoints

Once the server is running (`py src/api/server.py`):

- **Swagger UI**: http://localhost:8000/docs
- **Development Info**: http://localhost:8000/api/v1/dev-info
- **MCP Endpoint**: http://localhost:8000/mcp

### Example: Get Development Information

**REST API:**
```bash
curl http://localhost:8000/api/v1/dev-info
```

**MCP (JSON-RPC 2.0):**
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

## Project Structure

```
local-computer-assistant/
├── src/                    # Source code
│   ├── api/               # API server (REST + MCP)
│   ├── checker/           # Environment checking
│   ├── core/              # Core utilities
│   ├── setup/             # Setup automation
│   ├── update/            # Update management
│   ├── troubleshooting/   # Problem detection & fixes
│   └── main.py            # CLI entry point
├── config/                # Configuration files
├── docs/                  # Documentation (organized by topic)
│   ├── getting-started/  # Installation & quick start
│   ├── api/               # API documentation
│   ├── architecture/      # Architecture & design
│   └── guides/            # User guides
├── scripts/               # Platform-specific scripts
├── data/                  # Data storage (git-ignored)
├── logs/                  # Log files (git-ignored)
├── requirements.txt       # Python dependencies
├── requirements-api.txt   # API dependencies
├── Dockerfile             # Docker container definition
└── docker-compose.yml     # Docker Compose config
```

## Documentation

📖 **New to CompAssist?** Start with:
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Comprehensive project overview
- **[INDEX.md](INDEX.md)** - Complete project index and navigation guide
- **[docs/getting-started/installation.md](docs/getting-started/installation.md)** - Installation guide

See `docs/` directory for detailed documentation organized by topic:

### Getting Started
- `docs/getting-started/installation.md` - Installation guide
- `docs/getting-started/quickstart.md` - Quick start guide
- `docs/getting-started/docker-setup.md` - Docker setup

### API Documentation
- `docs/api/overview.md` - API overview and setup
- `docs/api/rest-api.md` - REST API endpoints
- `docs/api/mcp-protocol.md` - MCP (JSON-RPC 2.0) protocol
- `docs/api/dev-info-endpoint.md` - Development info endpoint

### Architecture
- `docs/architecture/design.md` - System architecture
- `docs/architecture/agent-communication.md` - Agent communication design
- `docs/architecture/docker-feasibility.md` - Docker deployment analysis

### Guides
- `docs/guides/docker-installation.md` - Docker installation
- `docs/guides/lightshot-installation.md` - Lightshot installation

See `docs/README.md` for complete documentation index.

## Platform Support

- ✅ **Windows**: Full support
- 🔄 **Linux**: Basic support (expanding)
- 🔄 **macOS**: Planned

## License

MIT
