# Source Code Directory

Core source code for the Local Computer Assistant (CompAssist).

## Overview

This directory contains all Python source code organized into modular packages for different functionalities.

## Directory Structure

```
src/
├── main.py                     # CLI entry point
├── core/                       # Core utilities
│   ├── logger.py              # Logging configuration
│   └── platform.py            # Platform detection
├── checker/                    # Environment checking
│   └── environment_checker.py # System analysis & reporting
├── setup/                      # Setup automation
│   ├── setup_manager.py       # Software installation manager
│   └── environment_setup.py   # Environment configuration
├── update/                     # Update management
│   └── update_manager.py      # Update detection & application
├── troubleshooting/            # Problem solving
│   └── problem_solver.py      # Issue detection & fixes
└── api/                        # Agent communication
    ├── server.py              # REST API server (FastAPI)
    ├── mcp_server.py          # MCP protocol server
    └── dev_info.py            # Development information provider
```

## Main Entry Point

### `main.py`
**CLI application** - Command-line interface for all operations.

**Commands:**
- `check` - Check system environment
- `setup` - Setup and install software
- `update` - Update system and packages
- `diagnose` - Diagnose system problems
- `fix` - Fix detected problems

**Usage:**
```bash
python src/main.py <command> [options]
```

**Examples:**
```bash
# Check environment
python src/main.py check

# Setup with specific config
python src/main.py setup --config config/user_example.yaml

# Diagnose problems
python src/main.py diagnose

# Fix problems
python src/main.py fix
```

## Core Modules (`core/`)

### `logger.py`
Centralized logging configuration.

**Features:**
- Configurable log levels
- File and console output
- Structured logging format
- Platform-aware formatting

**Usage:**
```python
from core.logger import get_logger

logger = get_logger(__name__)
logger.info("Operation started")
```

### `platform.py`
Platform detection and information.

**Features:**
- OS detection (Windows/Linux/macOS)
- Architecture detection (x86/x64/ARM)
- Version information
- Windows-specific info (WMI)

**Usage:**
```python
from core.platform import PlatformDetector

detector = PlatformDetector()
info = detector.detect()
print(f"OS: {info['os']}, Arch: {info['architecture']}")
```

## Checker Module (`checker/`)

### `environment_checker.py`
Comprehensive system environment checking.

**Features:**
- System information (OS, CPU, memory, disk)
- Installed software detection
- Development tools verification
- Network connectivity
- Security status
- Formatted report generation

**Classes:**
- `EnvironmentChecker` - Main checker class
- `SystemInfo` - System information collector
- `SoftwareDetector` - Software detection

**Usage:**
```python
from checker.environment_checker import EnvironmentChecker

checker = EnvironmentChecker()
report = checker.check_all()
checker.print_report(report)
```

## Setup Module (`setup/`)

### `setup_manager.py`
Software installation and setup management.

**Features:**
- Multi package manager support (winget, Chocolatey, apt, yum, dnf)
- Direct download installation
- Configuration-driven setup
- Installation verification

**Classes:**
- `SetupManager` - Main setup coordinator
- `PackageInstaller` - Package installation handler

**Usage:**
```python
from setup.setup_manager import SetupManager

manager = SetupManager()
manager.setup_from_config("config/default.yaml")
```

### `environment_setup.py`
Environment variable and PATH management.

**Features:**
- PATH configuration
- Environment variable setting
- Git PATH detection and setup
- Platform-specific handling

**Classes:**
- `EnvironmentSetup` - Environment configuration

**Usage:**
```python
from setup.environment_setup import EnvironmentSetup

env_setup = EnvironmentSetup()
env_setup.setup_git_path()
```

## Update Module (`update/`)

### `update_manager.py`
System and package update management.

**Features:**
- Update detection
- Package updates
- System updates
- Update reporting

**Classes:**
- `UpdateManager` - Update coordinator
- `PackageUpdater` - Package update handler

**Usage:**
```python
from update.update_manager import UpdateManager

manager = UpdateManager()
manager.check_updates()
manager.apply_updates()
```

## Troubleshooting Module (`troubleshooting/`)

### `problem_solver.py`
Problem detection and automated fixing.

**Features:**
- Disk space monitoring
- Memory usage detection
- Network connectivity issues
- Automated fixes
- Problem reporting

**Classes:**
- `ProblemSolver` - Main problem solver
- `SystemDiagnostics` - System diagnostics

**Usage:**
```python
from troubleshooting.problem_solver import ProblemSolver

solver = ProblemSolver()
problems = solver.diagnose()
solver.fix_all(problems)
```

## API Module (`api/`)

### `server.py`
REST API server for agent communication.

**Features:**
- FastAPI-based REST API
- Development information endpoint
- Health check endpoint
- API key authentication
- Swagger UI documentation

**Endpoints:**
- `GET /health` - Health check
- `GET /api/v1/dev-info` - Development information
- `GET /docs` - Swagger UI

**Usage:**
```bash
# Start server
python src/api/server.py

# Server runs on http://localhost:8000
# Docs at http://localhost:8000/docs
```

**Environment Variables:**
- `API_KEY` - API authentication key
- `PORT` - Server port (default: 8000)

### `mcp_server.py`
Model Context Protocol (MCP) server.

**Features:**
- JSON-RPC 2.0 implementation
- MCP protocol compliance
- Development information
- Capability listing

**Methods:**
- `mcp.get_dev_info` - Get development information
- `mcp.list_capabilities` - List available methods

**Usage:**
```bash
# Start MCP server
python src/api/mcp_server.py

# Server runs on http://localhost:8001
```

### `dev_info.py`
Development information provider.

**Features:**
- System specifications
- Installed development tools
- Version detection
- Structured information

**Classes:**
- `DevelopmentInfoProvider` - Dev info collector

**Usage:**
```python
from api.dev_info import DevelopmentInfoProvider

provider = DevelopmentInfoProvider()
info = provider.get_dev_info()
```

## Code Style

### Python Standards
- **PEP 8** compliance
- **Type hints** for function parameters and returns
- **Docstrings** for all classes and functions
- **Exception handling** with meaningful messages

### Example:
```python
def example_function(param: str, count: int = 0) -> dict:
    """
    Example function demonstrating code style.
    
    Args:
        param: Description of param
        count: Description of count
        
    Returns:
        Dictionary with results
        
    Raises:
        ValueError: If param is invalid
    """
    if not param:
        raise ValueError("param cannot be empty")
    
    return {"param": param, "count": count}
```

## Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Test Structure
```
tests/
├── test_checker.py
├── test_setup.py
├── test_update.py
├── test_troubleshooting.py
└── test_api.py
```

## Development

### Adding New Features

1. **Create module** in appropriate directory
2. **Follow naming conventions**: `feature_handler.py`
3. **Add docstrings** and type hints
4. **Update this README**
5. **Add tests**
6. **Update main.py** if adding CLI command

### Module Guidelines

- **Single responsibility**: Each module has one clear purpose
- **Dependency injection**: Pass dependencies, don't create them
- **Error handling**: Catch and handle exceptions appropriately
- **Logging**: Use logger for important events
- **Platform-aware**: Check platform before OS-specific operations

## Dependencies

Core dependencies (see `requirements.txt`):
- `pyyaml` - Configuration parsing
- `psutil` - System information
- `requests` - HTTP client
- `pywin32` (Windows) - Windows API
- `wmi` (Windows) - WMI access

API dependencies (see `requirements-api.txt`):
- `fastapi` - REST API framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation

## Common Patterns

### Logger Usage
```python
from core.logger import get_logger
logger = get_logger(__name__)
```

### Platform Detection
```python
from core.platform import PlatformDetector
detector = PlatformDetector()
if detector.is_windows():
    # Windows-specific code
```

### Configuration Loading
```python
import yaml
with open("config/default.yaml") as f:
    config = yaml.safe_load(f)
```

## Troubleshooting

### Import Errors
```bash
# Set PYTHONPATH
export PYTHONPATH=/path/to/project  # Linux
$env:PYTHONPATH="C:\path\to\project"  # Windows
```

### Module Not Found
```bash
# Ensure you're in project root
cd /path/to/local-computer-assistant

# Verify Python path
python -c "import sys; print(sys.path)"
```

## Related Documentation

- Main README: `/README.md`
- API Documentation: `/docs/api/`
- Architecture: `/docs/architecture/design.md`
- Configuration: `/config/README.md`


