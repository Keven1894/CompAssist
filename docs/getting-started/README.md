# Getting Started

Quick start guides and installation instructions for CompAssist.

## Overview

This directory contains everything you need to get CompAssist up and running on your machine.

## Documents in This Directory

### [`installation.md`](installation.md) ⭐ START HERE
**Complete Installation Guide**
- Prerequisites
- Installing Python and dependencies
- Installing CompAssist
- Environment setup
- First-time configuration
- Verification steps

**Best for:** New users, first-time setup

### [`quickstart.md`](quickstart.md)
**5-Minute Quick Start**
- Minimal installation
- Essential commands
- Basic usage examples
- Common tasks

**Best for:** Experienced users, quick reference

### [`docker-setup.md`](docker-setup.md)
**Docker Deployment Guide**
- Docker installation
- Building the image
- Running in containers
- Docker Compose setup
- Volume management
- Troubleshooting

**Best for:** Container-based deployment, portability

## Quick Navigation

### For Complete Beginners
1. Read [`installation.md`](installation.md)
2. Follow step-by-step instructions
3. Verify installation
4. Try [`quickstart.md`](quickstart.md) examples

### For Experienced Users
1. Skim [`quickstart.md`](quickstart.md)
2. Install dependencies
3. Start using immediately

### For Docker Users
1. Read [`docker-setup.md`](docker-setup.md)
2. Build or pull image
3. Run in container

## Installation Path Comparison

### Native Installation (Recommended)
**Pros:**
- Direct system access
- Full functionality
- Better performance
- Easier troubleshooting

**Cons:**
- Need to install Python
- Platform-specific setup
- Less portable

**Best for:**
- System administration tasks
- Regular local use
- Development

### Docker Installation
**Pros:**
- Portable across machines
- Isolated environment
- Consistent setup
- Easy to distribute

**Cons:**
- Limited host access (requires --privileged)
- Some operations need native execution
- Larger initial download

**Best for:**
- Testing on multiple machines
- Standardized environments
- Containerized workflows

## Prerequisites Summary

### All Installations
- **Operating System**: Windows 10+, Ubuntu 20.04+, or modern Linux
- **Disk Space**: 500MB minimum
- **Network**: Internet connection for downloads

### Native Installation
- **Python**: 3.8 or higher
- **pip**: Latest version
- **Administrator access**: For system operations

### Docker Installation
- **Docker**: Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- **Docker Compose**: 1.29+ (optional)

## Installation Time Estimates

| Method | Time Required |
|--------|---------------|
| Native (Python installed) | 5-10 minutes |
| Native (from scratch) | 15-20 minutes |
| Docker (image available) | 5 minutes |
| Docker (build from source) | 10-15 minutes |

## Common Installation Steps

### 1. Get the Code
```bash
# Clone repository
git clone https://github.com/Keven1894/CompAssist.git
cd CompAssist
```

### 2. Choose Installation Method

**Native:**
```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-api.txt

# Set environment
$env:PYTHONPATH="C:\projects\local-computer-assistant"

# Test installation
python src/main.py check
```

**Docker:**
```bash
# Build image
docker build -t compassist .

# Run container
docker run -it --rm compassist check
```

### 3. Verify Installation
```bash
# Check environment
python src/main.py check

# Expected output: System information and status
```

### 4. Configure (Optional)
```bash
# Copy example config
cp config/user_example.yaml config/user_yourname.yaml

# Edit configuration
notepad config/user_yourname.yaml  # Windows
nano config/user_yourname.yaml     # Linux
```

## First Commands to Try

### 1. Check Your System
```bash
python src/main.py check
```
Shows system information, installed software, and development tools.

### 2. Setup Software
```bash
python src/main.py setup --config config/user_yourname.yaml
```
Installs software defined in your configuration.

### 3. Diagnose Issues
```bash
python src/main.py diagnose
```
Checks for common problems like low disk space, high memory usage.

### 4. Start API Server
```bash
python src/api/server.py
```
Starts REST API server on http://localhost:8000

## Configuration Quick Start

### Minimal Configuration
```yaml
# config/user_yourname.yaml
platform:
  windows:
    enabled: true

packages:
  common:
    - git
    - python
```

### Usage
```bash
python src/main.py setup --config config/user_yourname.yaml
```

## Troubleshooting Common Issues

### Python Not Found
```bash
# Windows: Install from python.org
# Ubuntu: sudo apt install python3 python3-pip
# Verify: python --version
```

### Module Not Found
```bash
# Set PYTHONPATH
$env:PYTHONPATH="C:\path\to\CompAssist"  # Windows
export PYTHONPATH="/path/to/CompAssist"  # Linux
```

### Permission Denied
```bash
# Windows: Run PowerShell as Administrator
# Linux: Use sudo for system operations
```

### Docker Issues
```bash
# Check Docker is running
docker --version
docker ps

# Restart Docker Desktop (Windows/Mac)
```

## Environment Setup

### Windows PowerShell
```powershell
# Set Python path
$env:PYTHONPATH="C:\projects\local-computer-assistant"

# Set API key (optional)
$env:API_KEY="your-secret-key"

# Make permanent (optional)
[System.Environment]::SetEnvironmentVariable("PYTHONPATH", "C:\projects\local-computer-assistant", "User")
```

### Linux/Mac Bash
```bash
# Set Python path
export PYTHONPATH="/home/user/CompAssist"

# Set API key (optional)
export API_KEY="your-secret-key"

# Make permanent
echo 'export PYTHONPATH="/home/user/CompAssist"' >> ~/.bashrc
source ~/.bashrc
```

## Next Steps After Installation

### For System Administrators
1. **Configure packages**: Edit config file with your standard software
2. **Run setup**: Automate your machine setup
3. **Schedule checks**: Regular system health checks
4. **Document**: Create your workflow docs

### For Developers
1. **Check dev tools**: `python src/main.py check` to see installed tools
2. **Start API**: `python src/api/server.py` for programmatic access
3. **Explore API**: Visit http://localhost:8000/docs
4. **Integrate**: Use API in your workflows

### For AI Agent Developers
1. **Start MCP server**: `python src/api/mcp_server.py`
2. **Test endpoints**: Try MCP methods
3. **Review docs**: See `/docs/api/mcp-protocol.md`
4. **Integrate**: Connect your agents

## Learning Path

### Beginner
1. ✅ Install CompAssist
2. ✅ Run `check` command
3. ✅ Create basic config
4. ✅ Try `setup` command
5. ✅ Read user guides

### Intermediate
1. ✅ Customize configuration
2. ✅ Use all CLI commands
3. ✅ Start API server
4. ✅ Explore API docs
5. ✅ Try Docker deployment

### Advanced
1. ✅ Create custom configs
2. ✅ Integrate with CI/CD
3. ✅ Develop against API
4. ✅ Contribute to project
5. ✅ Extend functionality

## Additional Resources

### Documentation
- **Configuration**: `/config/README.md`
- **API Reference**: `/docs/api/`
- **Architecture**: `/docs/architecture/`
- **User Guides**: `/docs/guides/`

### User Guides
- **Docker Installation**: `/docs/guides/docker-installation.md`
- **Git Installation**: `/docs/guides/git-installation.md`
- **Lightshot Setup**: `/docs/guides/lightshot-installation.md`

### External Links
- [Python Download](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git Download](https://git-scm.com/downloads)
- [GitHub Repository](https://github.com/Keven1894/CompAssist)

## Getting Help

### Documentation
1. Check relevant docs in `/docs/`
2. Search for specific topics
3. Review examples in guides

### Issues
1. Check [GitHub Issues](https://github.com/Keven1894/CompAssist/issues)
2. Search for similar problems
3. Create new issue if needed

### Community
- **Repository**: https://github.com/Keven1894/CompAssist
- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas

## Success Checklist

After installation, you should be able to:

- [ ] Run `python src/main.py check` successfully
- [ ] See system information in the output
- [ ] Create a user configuration file
- [ ] Run `python src/main.py setup` (with your config)
- [ ] Start the API server
- [ ] Access Swagger UI at http://localhost:8000/docs
- [ ] Run `python src/main.py diagnose`

If you can do all of the above, you're ready to use CompAssist! 🎉

## What's Next?

Choose your path:

### 📚 Learn More
- Read `/docs/guides/` for specific tasks
- Explore `/docs/architecture/` for technical details
- Check `/docs/api/` for API integration

### 🛠️ Start Using
- Create your configuration
- Automate your setup
- Integrate with your workflow

### 🤝 Contribute
- Report issues
- Suggest features
- Submit pull requests

---

**Need Help?** Start with [`installation.md`](installation.md) for detailed instructions!


