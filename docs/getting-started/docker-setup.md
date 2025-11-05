# Docker Setup Tools Documentation

## Overview

This document describes the tools and process for setting up Docker on your Windows machine (AMD64/x64).

## Prerequisites Check

Your system status:
- ✅ **Architecture**: AMD64/x64 (confirmed)
- ✅ **Processor**: Intel Core i9-14900K
- ✅ **OS**: Windows (x64-based PC)
- ⚠️ **Python**: Not currently installed/in PATH
- ⚠️ **Docker**: Not installed yet
- ⚠️ **winget**: Available but has permission issues
- ❌ **Chocolatey**: Not installed

## Step-by-Step Docker Setup

### Step 1: Install Python (Required for Assistant)

The assistant needs Python to run. Install Python first:

**Option A: Microsoft Store**
```powershell
# Open Microsoft Store and search for "Python 3.11" or "Python 3.12"
# Or use winget if permissions are fixed:
winget install Python.Python.3.12
```

**Option B: Direct Download**
1. Visit: https://www.python.org/downloads/
2. Download Python 3.11 or 3.12 (64-bit)
3. Run installer
4. ✅ **Important**: Check "Add Python to PATH" during installation

**Verify Python Installation:**
```powershell
python --version
pip --version
```

### Step 2: Install Docker Desktop

**Download Docker Desktop:**
1. Visit: https://www.docker.com/products/docker-desktop/
2. Click "Download for Windows"
3. Run `Docker Desktop Installer.exe`

**Installation Options:**
- ✅ Use WSL 2 instead of Hyper-V (recommended)
- ✅ Add shortcut to desktop
- ✅ Start Docker Desktop when Windows starts

**After Installation:**
- Restart Windows if prompted
- Launch Docker Desktop
- Wait for Docker to start (whale icon in system tray)

**Verify Docker:**
```powershell
docker --version
docker info
docker run hello-world
```

### Step 3: Setup WSL 2 (if needed)

If Docker Desktop prompts for WSL 2:

```powershell
# Check WSL status
wsl --status

# Install WSL 2 if needed
wsl --install

# Or manually enable features
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart, then set WSL 2 as default
wsl --set-default-version 2
```

## Assistant Setup

### Step 1: Install Assistant Dependencies

```bash
cd <project-root-directory>
# Example: cd C:\projects\local-computer-assistant
pip install -r requirements.txt
```

### Step 2: Test Assistant

```bash
# Check environment
python src/main.py check

# Should show:
# - System information
# - Docker status (should detect if installed)
# - Installed software
```

### Step 3: Build Docker Image

```bash
# Build the assistant Docker image
docker build -t local-computer-assistant .

# Verify image
docker images
```

### Step 4: Test Docker Container

```bash
# Run assistant in Docker
docker run -it --rm --privileged local-computer-assistant check

# Or use docker-compose
docker-compose up
```

## Installation Checklist

- [ ] Python installed and in PATH
- [ ] Assistant dependencies installed (`pip install -r requirements.txt`)
- [ ] Assistant works locally (`python src/main.py check`)
- [ ] WSL 2 installed (if needed)
- [ ] Docker Desktop installed
- [ ] Docker Desktop running (whale icon visible)
- [ ] Docker verified (`docker --version`, `docker info`)
- [ ] Assistant Docker image built (`docker build -t local-computer-assistant .`)
- [ ] Assistant runs in Docker (`docker run ...`)

## Common Issues

### Python Not Found
- **Solution**: Reinstall Python with "Add to PATH" checked
- Or manually add Python to PATH environment variable

### Docker Desktop Won't Start
- **Check**: WSL 2 is installed (`wsl --status`)
- **Check**: Virtualization enabled in BIOS
- **Check**: Windows features enabled

### Permission Issues with winget
- **Solution**: Run PowerShell as Administrator
- Or use direct downloads instead

## Next Steps

1. Install Python
2. Install Lightshot (testing first software)
3. Install Docker Desktop
4. Build and test Docker container
5. Document any issues encountered

## Quick Commands Reference

```powershell
# Check system
python src/main.py check

# Install Lightshot
python src/main.py setup --config config/user_example.yaml

# Build Docker
docker build -t local-computer-assistant .

# Run in Docker
docker run -it --rm --privileged local-computer-assistant check
```

