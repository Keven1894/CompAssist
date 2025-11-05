# Lightshot Installation Guide

## About Lightshot

Lightshot is a free, user-friendly screen capture tool that allows you to:
- Quickly capture any area of your screen
- Edit screenshots immediately after capturing
- Upload and share screenshots via short links
- Search for similar images online

## Installation Methods

### Method 1: Using the Assistant (Recommended)

The assistant can help you install Lightshot. Run:

```bash
python src/main.py setup --config config/user_example.yaml
```

### Method 2: Manual Installation

1. **Download Lightshot:**
   - Visit: https://app.prntscr.com/download.html
   - Click "Download for Windows"
   - The installer will be saved to your Downloads folder

2. **Run the Installer:**
   - Navigate to Downloads folder
   - Double-click `setup-lightshot.exe`
   - Follow the installation wizard
   - Accept the license terms if prompted

3. **Verify Installation:**
   - Look for the Lightshot feather icon in your system tray
   - Press `Print Screen` key to test the capture tool

## Quick Installation Script

You can also use this PowerShell script:

```powershell
# Download Lightshot
$url = "https://app.prntscr.com/download.html"
$output = "$env:USERPROFILE\Downloads\setup-lightshot.exe"

# Open download page in browser
Start-Process $url

Write-Host "Please download Lightshot from the browser window that opened."
Write-Host "Save it to: $output"
Write-Host "Then run: Start-Process $output"
```

## Post-Installation

After installation:
1. Lightshot will appear in your system tray (feather icon)
2. Press `Print Screen` to capture screenshots
3. Right-click the tray icon to access settings

## Integration with Assistant

The assistant can:
- ✅ Detect if Lightshot is installed
- ✅ Help with installation via direct download
- ✅ Document your setup preferences

## Troubleshooting

- **Icon not appearing**: Check system tray (click the ^ arrow)
- **Print Screen not working**: Check Lightshot settings for hotkey configuration
- **Installation fails**: Try running installer as Administrator

