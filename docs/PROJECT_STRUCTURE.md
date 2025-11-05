# Project Structure

```
local-computer-assistant/
├── src/                          # Source code
│   ├── api/                      # API server (REST + MCP)
│   │   ├── server.py            # FastAPI REST server
│   │   ├── mcp_server.py        # MCP JSON-RPC 2.0 server
│   │   └── dev_info.py          # Development info provider
│   ├── checker/                  # Environment checking
│   │   └── environment_checker.py
│   ├── core/                     # Core utilities
│   │   ├── logger.py            # Logging setup
│   │   └── platform.py           # Platform detection
│   ├── setup/                    # Setup automation
│   │   └── setup_manager.py
│   ├── update/                   # Update management
│   │   └── update_manager.py
│   ├── troubleshooting/          # Problem detection & fixes
│   │   └── problem_solver.py
│   └── main.py                   # CLI entry point
│
├── config/                       # Configuration files
│   ├── default.yaml             # Default configuration
│   └── user_example.yaml      # User-specific config template
│
├── docs/                         # Documentation
│   ├── getting-started/          # Quick start guides
│   ├── api/                      # API documentation
│   ├── architecture/             # Architecture docs
│   └── guides/                   # User guides
│
├── scripts/                      # Platform-specific scripts
│   ├── install-lightshot.ps1
│   └── README.md
│
├── data/                         # Data storage (git-ignored)
├── logs/                         # Log files (git-ignored)
│
├── requirements.txt              # Python dependencies
├── requirements-api.txt          # API dependencies
├── Dockerfile                    # Docker container definition
├── docker-compose.yml            # Docker Compose config
└── README.md                     # Main readme
```

## Module Descriptions

### `src/api/`
API server implementation for agent-to-agent communication:
- **server.py**: FastAPI REST server with endpoints
- **mcp_server.py**: MCP (JSON-RPC 2.0) server implementation
- **dev_info.py**: Development information provider

### `src/checker/`
Environment checking and analysis:
- **environment_checker.py**: System info, resources, software, network, security checks

### `src/core/`
Core utilities and platform abstraction:
- **logger.py**: Centralized logging with color output
- **platform.py**: Platform detection and system information

### `src/setup/`
System setup and configuration:
- **setup_manager.py**: Software installation and system configuration

### `src/update/`
Update management:
- **update_manager.py**: Check for system and software updates

### `src/troubleshooting/`
Problem detection and resolution:
- **problem_solver.py**: Detect issues and apply fixes

## Configuration Files

### `config/default.yaml`
Default configuration template with:
- Platform settings
- Software packages
- System settings
- Environment variables
- Thresholds

### `config/user_example.yaml`
User-specific configuration (example)

## Documentation Structure

- **getting-started/**: Installation and quick start guides
- **api/**: API documentation and usage
- **architecture/**: System design and architecture
- **guides/**: Step-by-step guides for specific tasks
