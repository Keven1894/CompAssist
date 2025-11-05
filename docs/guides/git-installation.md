# Git Installation Guide

## Overview

Git is a distributed version control system essential for development work.

## Installation Methods

### Method 1: Direct Download (Recommended)

The assistant will automatically:
1. Detect that `git-scm.com/download/win` is a download page
2. Open your browser to the official Git download page
3. Prompt you to download and run the installer manually

**Steps:**
1. Run: `py src/main.py setup --config config/default.yaml`
2. The browser will open automatically
3. Download the Git installer (usually starts automatically)
4. Run the installer and follow the wizard
5. Verify installation: `git --version`

### Method 2: Using Package Manager (if available)

If you have winget or Chocolatey installed:

**Winget:**
```bash
winget install Git.Git
```

**Chocolatey:**
```bash
choco install git -y
```

## Verification

After installation, verify Git is working:

```bash
git --version
```

Expected output: `git version 2.x.x`

## Configuration

After installation, configure Git with your identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Configuration File

The Git installation is configured in `config/default.yaml`:

```yaml
software:
  packages:
    - name: Git
      type: direct_download
      url: https://git-scm.com/download/win
      installer: Git-installer.exe
      silent_install: false
      description: Git version control system
```

## Troubleshooting

### Git not found after installation

1. **Restart terminal/PowerShell** - PATH changes may require restart
2. **Check PATH**: Ensure Git is in your system PATH
3. **Manual PATH addition**: Add `C:\Program Files\Git\cmd` to PATH if needed

### Installer won't run

- Ensure you're running as Administrator
- Check Windows compatibility
- Try downloading from: https://git-scm.com/download/win

## Next Steps

After Git is installed:
1. Configure your Git identity (see above)
2. Set up SSH keys (optional): `ssh-keygen -t ed25519 -C "your.email@example.com"`
3. Verify installation: `git --version`



