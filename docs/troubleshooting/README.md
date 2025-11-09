# Troubleshooting Documentation

Issue-specific troubleshooting guides and solutions.

## Overview

This directory contains detailed troubleshooting guides for specific issues you might encounter when using CompAssist or managing your system.

## Available Guides

### [`windows-security-issues.md`](windows-security-issues.md)
**Windows Security and LSA Protection Issues**

Covers:
- LSA Protection blocking DLLs (e.g., EpePcNp64.dll)
- McAfee/Antivirus compatibility issues
- DLL signature verification
- Security policy troubleshooting
- When to disable vs update security software

**When to use**: When you encounter "This module is blocked from loading into the Local Security Authority" errors on Windows.

## Common Issues Quick Reference

| Issue | Guide | Platform |
|-------|-------|----------|
| LSA Protection blocking DLLs | [windows-security-issues.md](windows-security-issues.md) | Windows |
| Node.js not found after install | [../guides/nodejs-installation.md](../guides/nodejs-installation.md#troubleshooting) | All |
| Git not in PATH | [../guides/git-installation.md](../guides/git-installation.md) | All |
| Docker won't start | [../guides/docker-installation.md](../guides/docker-installation.md#troubleshooting) | Windows |
| Permission denied errors | [Installation Guide](../getting-started/installation.md#troubleshooting) | All |

## General Troubleshooting Steps

### 1. Check System Status

Use CompAssist to diagnose:

```bash
# Check environment
python src/main.py check

# Diagnose problems
python src/main.py diagnose

# Attempt automatic fixes
python src/main.py fix
```

### 2. Check Logs

```bash
# View recent logs
ls logs/

# Windows
Get-Content logs/latest.log -Tail 50

# Linux
tail -f logs/latest.log
```

### 3. Verify Installation

```bash
# Check specific tool
git --version
python --version
node --version
docker --version
```

### 4. Check PATH

**Windows:**
```powershell
$env:PATH -split ";"
```

**Linux/macOS:**
```bash
echo $PATH | tr ':' '\n'
```

## Troubleshooting by Category

### Installation Issues

**Symptoms:**
- Software won't install
- Installer fails
- Package not found

**Solutions:**
1. Check internet connection
2. Verify package manager is installed
3. Try different package manager
4. Use direct download method
5. Check logs for specific errors

**Relevant docs:**
- [Installation Guide](../getting-started/installation.md)
- [Configuration Guide](/config/README.md)

### PATH Issues

**Symptoms:**
- Command not found after installation
- Software installed but not accessible

**Solutions:**
1. Restart terminal/PowerShell
2. Check PATH includes installation directory
3. Run CompAssist environment setup
4. Manually add to PATH

**Tools:**
```bash
# Git PATH setup
python scripts/setup-git-env.py

# Check what CompAssist detects
python src/main.py check
```

### Permission Issues

**Symptoms:**
- Access denied
- Permission denied
- Need administrator rights

**Solutions:**

**Windows:**
- Run PowerShell as Administrator
- Check UAC settings
- Verify user has admin rights

**Linux:**
- Use `sudo` for system operations
- Check user is in correct groups
- Fix file permissions: `chmod`, `chown`

### Docker Issues

**Symptoms:**
- Docker command not found
- Docker Desktop won't start
- Container can't access host

**Solutions:**
1. Verify Docker Desktop is running (Windows)
2. Check Docker daemon status (Linux)
3. Use `host.docker.internal` for host access
4. Check firewall isn't blocking
5. Review [docker-setup.md](../getting-started/docker-setup.md)

### API Server Issues

**Symptoms:**
- Server won't start
- Connection refused
- API key errors

**Solutions:**
1. Check port is available
2. Verify PYTHONPATH is set
3. Set API_KEY environment variable
4. Check firewall rules
5. Review [API docs](../api/overview.md)

### Detection Issues

**Symptoms:**
- CompAssist doesn't detect installed software
- Wrong version reported
- Software shows as not installed

**Solutions:**
1. Restart terminal after installation
2. Verify software is in standard location
3. Check PATH includes software directory
4. Re-run check: `python src/main.py check`
5. Check logs for detection errors

## Platform-Specific Issues

### Windows

**Common issues:**
- UAC prompts
- PATH not updated
- PowerShell execution policy
- Windows Defender blocking downloads
- WSL2 issues with Docker

**Resources:**
- [Windows Security Issues](windows-security-issues.md)
- [Docker Installation](../guides/docker-installation.md)

### Linux

**Common issues:**
- Permission denied (need sudo)
- Package manager differences
- Missing dependencies
- SELinux blocking operations

**Resources:**
- [Installation Guide](../getting-started/installation.md)

### macOS

**Common issues:**
- Gatekeeper blocking apps
- Xcode Command Line Tools required
- Homebrew issues

**Resources:**
- Coming soon

## Getting Additional Help

### 1. Search Documentation

Use INDEX.md to find relevant docs:
```bash
# Open INDEX.md and use Ctrl+F to search
```

### 2. Check GitHub Issues

Search existing issues:
- [CompAssist Issues](https://github.com/Keven1894/CompAssist/issues)

### 3. Run Diagnostics

```bash
# Get detailed system info
python src/main.py check

# Diagnose specific problems
python src/main.py diagnose

# View logs
ls logs/
```

### 4. Enable Debug Logging

```bash
# Set log level to DEBUG
export LOG_LEVEL=DEBUG  # Linux/macOS
$env:LOG_LEVEL="DEBUG"  # Windows

# Run command
python src/main.py check
```

### 5. Create GitHub Issue

If you can't find a solution:
1. Search existing issues
2. Gather diagnostic information
3. Create detailed issue with:
   - OS and version
   - CompAssist version
   - Command you ran
   - Error message
   - Relevant logs

## Contributing Troubleshooting Guides

Found a solution to a common issue? Consider contributing:

### Guide Template

```markdown
# Issue Title

## Symptoms
- What the user experiences

## Cause
- Why this happens

## Solutions

### Solution 1: Primary Fix
Step-by-step instructions...

### Solution 2: Alternative
Alternative approach...

## Prevention
- How to avoid this issue

## Related Issues
- Links to similar problems
```

### How to Contribute

1. Create guide in `docs/troubleshooting/`
2. Update this README
3. Add to INDEX.md
4. Submit pull request

## Related Documentation

- **Installation**: [getting-started/installation.md](../getting-started/installation.md)
- **Configuration**: [/config/README.md](/config/README.md)
- **User Guides**: [guides/](../guides/README.md)
- **API Issues**: [api/overview.md](../api/overview.md)
- **Master Index**: [/INDEX.md](/INDEX.md)

---

**Last Updated**: November 9, 2024  
**Status**: Active - continuously updated with new issues and solutions


