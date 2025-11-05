# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Docker Desktop (for Docker deployment) - Optional

## Installation

### Local Development

1. **Clone or navigate to the project directory:**
   ```bash
   cd local-computer-assistant
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Check Environment
```bash
python src/main.py check
```

### Setup System
```bash
python src/main.py setup --config config/default.yaml
```

### Check for Updates
```bash
python src/main.py update
```

### Diagnose Issues
```bash
python src/main.py diagnose
```

### Fix Issues
```bash
python src/main.py fix
```

### Verbose Output
Add `--verbose` or `-v` flag for detailed logging:
```bash
python src/main.py check --verbose
```

## Docker Deployment

### Build the Docker Image
```bash
docker build -t local-computer-assistant .
```

### Run with Docker
```bash
docker run -it --rm \
  --privileged \
  -v /:/host:ro \
  local-computer-assistant check
```

### Run with Docker Compose
```bash
docker-compose up
```

## Configuration

Edit `config/default.yaml` to customize:
- Software packages to install
- System settings
- Environment variables
- Problem detection thresholds

## Examples

### Development Environment Setup
```bash
# Check current environment
python src/main.py check

# Setup development tools
python src/main.py setup --config config/default.yaml

# Verify setup
python src/main.py check
```

### Troubleshooting
```bash
# Detect issues
python src/main.py diagnose

# Auto-fix issues
python src/main.py fix
```

## Platform Support

- ✅ **Windows**: Full support (PowerShell, winget, Chocolatey)
- 🔄 **Linux**: Basic support (apt, yum, dnf)
- 🔄 **macOS**: Planned

## Troubleshooting

### Import Errors
If you get import errors for Windows-specific modules (winreg, wmi):
- These are optional dependencies
- The assistant will work without them, but with reduced functionality
- Install them manually: `pip install pywin32 wmi`

### Permission Errors
Some operations require administrator/root privileges:
- Windows: Run PowerShell as Administrator
- Linux: Use `sudo` or run as root

### Docker Issues
- Ensure Docker Desktop is running (Windows)
- On Linux, ensure Docker daemon is running
- Some operations may require `--privileged` flag


