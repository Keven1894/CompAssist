# Docker Installation Guide for Windows

## ✅ Yes, Docker Desktop Must Be Installed Manually

Docker Desktop for Windows is not included with Windows and requires manual installation.

## Installation Steps

### Prerequisites

1. **Windows 10/11** (64-bit)
   - Windows 10 version 2004 or higher (Build 19041 or higher)
   - Windows 11 (any version)

2. **WSL 2 Backend** (Required for Docker Desktop)
   - WSL 2 is the recommended backend for Docker Desktop
   - Can be enabled during Docker Desktop installation

3. **Hardware Requirements**
   - 64-bit processor with Second Level Address Translation (SLAT)
   - 4GB system RAM minimum (8GB+ recommended)
   - Virtualization enabled in BIOS

### Installation Methods

#### Method 1: Download from Docker Website (Recommended)

1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop/
   - Click "Download for Windows"
   - Run the installer: `Docker Desktop Installer.exe`

2. **Installation Options**
   - ✅ Use WSL 2 instead of Hyper-V (recommended)
   - ✅ Add shortcut to desktop
   - ✅ Start Docker Desktop when Windows starts

3. **Complete Installation**
   - Restart Windows when prompted
   - Launch Docker Desktop
   - Accept the license agreement
   - Wait for Docker to start (whale icon in system tray)

#### Method 2: Using winget (Windows Package Manager)

If you have Windows 10/11 with winget:

```powershell
winget install Docker.DockerDesktop
```

#### Method 3: Using Chocolatey

If you have Chocolatey installed:

```powershell
choco install docker-desktop
```

### Verify Installation

After installation, verify Docker is working:

```powershell
# Check Docker version
docker --version

# Check Docker Desktop is running
docker info

# Test with a simple container
docker run hello-world
```

### Troubleshooting

#### Docker Desktop Won't Start

1. **Check WSL 2 is installed:**
   ```powershell
   wsl --status
   ```

2. **If WSL 2 is not installed:**
   ```powershell
   # Enable WSL
   wsl --install
   
   # Or manually enable features
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   
   # Restart and set WSL 2 as default
   wsl --set-default-version 2
   ```

3. **Check Virtualization is Enabled:**
   - Restart computer
   - Enter BIOS/UEFI settings
   - Enable "Virtualization Technology" or "Intel VT-x" / "AMD-V"

#### Common Issues

- **"Docker Desktop requires Windows 10 Pro"** - Install WSL 2 backend instead
- **"Hardware assisted virtualization not enabled"** - Enable in BIOS
- **"WSL 2 installation is incomplete"** - Run `wsl --update` and restart

### Using Our Assistant to Check Docker

After installation, you can verify Docker is detected:

```bash
python src/main.py check
```

The assistant will show Docker installation status in the "Development Tools" section.

## Alternative: Use Assistant Without Docker

**Good news!** You don't need Docker to use the assistant locally. The assistant works perfectly fine running directly on Windows:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run directly (no Docker needed)
python src/main.py check
python src/main.py setup
python src/main.py diagnose
```

Docker is only needed if you want to:
- Containerize the assistant for portability
- Run it on multiple machines without installing Python
- Deploy it in a standardized environment

## Next Steps

1. **For Local Use**: Install Python and run directly (no Docker needed)
2. **For Docker Deployment**: Install Docker Desktop, then build and run containers
3. **Check Status**: Use `python src/main.py check` to verify Docker is detected


