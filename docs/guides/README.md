# User Guides

Step-by-step guides for specific tasks and software installations.

## Overview

This directory contains detailed how-to guides for installing specific software and accomplishing common tasks with CompAssist.

## Documents in This Directory

### [`docker-installation.md`](docker-installation.md)
**Docker Desktop Installation Guide**
- Installing Docker Desktop on Windows
- System requirements
- Installation steps with screenshots
- Verification
- Common issues and solutions

**Best for:** Users who need Docker for containerization

### [`git-installation.md`](git-installation.md)
**Git Version Control Installation**
- Installing Git on Windows
- Installation wizard walkthrough
- Configuration steps
- PATH setup
- Verification

**Best for:** Setting up version control

### [`lightshot-installation.md`](lightshot-installation.md)
**Lightshot Screen Capture Tool**
- Installing Lightshot on Windows
- Download and setup
- Configuration
- Usage tips

**Best for:** Setting up screen capture capabilities

## Installation Guides Index

### Development Tools

| Tool | Guide | Platform | Auto-Install Support |
|------|-------|----------|---------------------|
| Git | [`git-installation.md`](git-installation.md) | Windows | ✅ Yes (CompAssist) |
| Docker | [`docker-installation.md`](docker-installation.md) | Windows | ⚠️ Manual required |
| Node.js | [`nodejs-installation.md`](nodejs-installation.md) | Windows/Linux | ✅ Yes (CompAssist) |
| Python | Coming soon | Windows/Linux | ✅ Yes (CompAssist) |

### Productivity Tools

| Tool | Guide | Platform | Auto-Install Support |
|------|-------|----------|---------------------|
| Lightshot | [`lightshot-installation.md`](lightshot-installation.md) | Windows | ⚠️ Browser opens |
| VS Code | Coming soon | Windows/Linux | ✅ Yes (CompAssist) |

## Using These Guides

### Manual Installation
Each guide provides step-by-step instructions for manual installation if you prefer or need to install software manually.

### Automated Installation
Many tools can be installed automatically using CompAssist:

```bash
# Add to your config file
packages:
  development:
    - git
    - docker
    - nodejs
    
# Run setup
python src/main.py setup --config config/user_yourname.yaml
```

## Guide Format

Each guide follows a consistent structure:

1. **Overview**: What the tool is and why you need it
2. **Prerequisites**: What you need before starting
3. **Installation Steps**: Detailed walkthrough with commands/screenshots
4. **Configuration**: Post-installation setup
5. **Verification**: How to verify it works
6. **Troubleshooting**: Common issues and solutions
7. **Next Steps**: What to do after installation

## When to Use Manual vs Automated Installation

### Use Manual Installation When:
- First time installing on a machine
- Need to understand the process
- Want custom installation options
- Troubleshooting installation issues
- Learning about the tool

### Use Automated Installation When:
- Setting up multiple machines
- Standardizing environments
- Repeating installations
- Batch installing multiple tools
- Time is limited

## Platform-Specific Guides

### Windows
Most current guides are Windows-focused:
- Docker Desktop for Windows
- Git for Windows
- Lightshot for Windows

### Linux
Coming soon:
- Docker Engine installation
- Git via package managers
- Development tool setup

### macOS
Planned:
- Homebrew setup
- Development environment
- Common tools

## Creating Configuration from Guides

After following a guide manually, you can add tools to your configuration for automated installation on other machines:

```yaml
# config/user_yourname.yaml

packages:
  # Tools from guides
  development:
    - name: git
      manager: winget  # Or direct_download
      
  productivity:
    - name: lightshot
      manager: direct_download
      url: https://app.prntscr.com/en/download.html
```

## Verification Commands

After following any guide, verify installation:

```bash
# Check with CompAssist
python src/main.py check

# Or check directly
git --version
docker --version
node --version
```

## Troubleshooting

### Common Issues Across All Installations

#### PATH Not Updated
**Problem:** Command not found after installation

**Solution:**
```bash
# Restart terminal/PowerShell
# Or run CompAssist environment setup
python scripts/setup-git-env.py  # For Git specifically
```

#### Permission Denied
**Problem:** Insufficient permissions

**Solution:**
- Windows: Run as Administrator
- Linux: Use `sudo` or check user groups

#### Installation Failed
**Problem:** Download failed or installer error

**Solution:**
1. Check internet connection
2. Verify system requirements
3. Try direct download from official site
4. Check antivirus isn't blocking

#### Already Installed But Not Detected
**Problem:** Software installed but CompAssist doesn't detect it

**Solution:**
1. Verify PATH includes installation directory
2. Restart terminal
3. Check installation location is standard
4. Run `python src/main.py check` again

## Contributing Guides

Want to add a new guide? Follow this template:

### Guide Template

```markdown
# Tool Name Installation

Brief description of the tool.

## Prerequisites
- Requirement 1
- Requirement 2

## Installation Steps

### Step 1: Download
Instructions...

### Step 2: Install
Instructions...

### Step 3: Configure
Instructions...

## Verification
How to verify installation...

## Troubleshooting
Common issues and solutions...

## Next Steps
What to do next...
```

### Guidelines for New Guides
1. **Be specific**: Include exact steps
2. **Use screenshots**: Visual aids help
3. **Test thoroughly**: Follow your own guide
4. **Include troubleshooting**: Anticipate issues
5. **Link to official docs**: For detailed info
6. **Keep updated**: Review periodically

## Advanced Installation Topics

### Custom Installation Locations
Some guides cover non-standard installation paths and how to configure CompAssist to find them.

### Multi-Version Management
For tools like Python or Node.js, guides can cover version managers (pyenv, nvm).

### Enterprise Deployments
Special considerations for corporate environments with proxies, restricted access, etc.

## Integration with CompAssist

### After Manual Installation
1. **Verify**: Run `python src/main.py check`
2. **Configure**: Add to your config if needed
3. **Document**: Note any custom steps
4. **Automate**: Use config for future installs

### Creating Automated Installers
If you frequently install a tool, consider:
1. Adding it to `config/default.yaml`
2. Testing automated installation
3. Documenting special requirements
4. Contributing back to project

## Quick Reference Commands

### Check What's Installed
```bash
python src/main.py check
```

### Install from Config
```bash
python src/main.py setup --config config/user_yourname.yaml
```

### Diagnose Issues
```bash
python src/main.py diagnose
```

### Fix Common Problems
```bash
python src/main.py fix
```

## Related Documentation

### Setup and Configuration
- **Getting Started**: `/docs/getting-started/`
- **Configuration**: `/config/README.md`
- **Installation Guide**: `/docs/getting-started/installation.md`

### Technical Details
- **Architecture**: `/docs/architecture/`
- **API Documentation**: `/docs/api/`
- **Source Code**: `/src/README.md`

## External Resources

### Official Download Sites
- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/)
- [Python](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/)

### Package Managers
- [Winget](https://learn.microsoft.com/en-us/windows/package-manager/)
- [Chocolatey](https://chocolatey.org/)
- [Homebrew](https://brew.sh/) (macOS/Linux)

### Documentation
- [Docker Docs](https://docs.docker.com/)
- [Git Documentation](https://git-scm.com/doc)
- [Node.js Docs](https://nodejs.org/docs/)

## Feedback

Have suggestions for new guides or improvements?
- Open an issue on [GitHub](https://github.com/Keven1894/CompAssist/issues)
- Include "Guide Request" in the title
- Describe what guide would be helpful

## Upcoming Guides

Planned guides in development:
- [x] Node.js Installation ✅ [`nodejs-installation.md`](nodejs-installation.md)
- [ ] Python Installation and Setup
- [ ] VS Code Setup and Extensions
- [ ] PowerShell Configuration
- [ ] WSL2 Setup
- [ ] Development Environment Templates

---

**Need help?** Choose the guide that matches your needs and follow the step-by-step instructions!

