# Scripts Directory

Platform-specific scripts for system operations and automation.

## Overview

This directory contains PowerShell, Python, and shell scripts that support the Local Computer Assistant's operations.

## Scripts

### Windows PowerShell Scripts

#### `configure-git.ps1`
Configures Git with user information.

**Usage:**
```powershell
.\scripts\configure-git.ps1 -Name "Your Name" -Email "your.email@example.com"
```

**Features:**
- Sets Git user.name and user.email globally
- Configures default branch name
- Sets credential helper
- Configures line ending handling

#### `install-lightshot.ps1`
Opens the Lightshot download page for manual installation.

**Usage:**
```powershell
.\scripts\install-lightshot.ps1
```

**Features:**
- Opens browser to Lightshot download page
- Provides installation instructions

### Python Scripts

#### `setup-git-env.py`
Sets up Git environment variables and PATH configuration.

**Usage:**
```bash
python scripts/setup-git-env.py
```

**Features:**
- Detects Git installation location
- Adds Git to system PATH if needed
- Verifies Git accessibility
- Cross-platform support

## Adding New Scripts

When adding new scripts:

1. **Use descriptive names**: `action-target.extension`
2. **Add help/usage info**: Include usage instructions in script header
3. **Document here**: Add entry to this README
4. **Error handling**: Include proper error handling and exit codes
5. **Platform-specific**: Place in appropriate subdirectory if needed

## Script Conventions

### PowerShell Scripts (`.ps1`)
- Use approved verbs (Get-, Set-, New-, etc.)
- Include parameter documentation
- Use `CmdletBinding()` for advanced functions
- Include `-WhatIf` and `-Confirm` for destructive operations

### Python Scripts (`.py`)
- Include shebang: `#!/usr/bin/env python3`
- Use argparse for command-line arguments
- Include docstrings
- Follow PEP 8 style guide

### Shell Scripts (`.sh`)
- Include shebang: `#!/bin/bash` or `#!/bin/sh`
- Use getopts for argument parsing
- Include usage function
- Check for required commands before execution

## Security Considerations

- Never hardcode credentials or API keys
- Use environment variables for sensitive data
- Validate input parameters
- Use least privilege principle
- Document any elevated permissions required

## Testing

Test scripts on target platforms before committing:

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts/script-name.ps1

# Linux
bash scripts/script-name.sh

# Python
python scripts/script-name.py
```

## Related Documentation

- Main README: `/README.md`
- Setup Guide: `/docs/getting-started/installation.md`
- API Documentation: `/docs/api/overview.md`
