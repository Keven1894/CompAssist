# Quick PowerShell script to open Lightshot download page
Write-Host "Opening Lightshot download page..."
Start-Process "https://app.prntscr.com/download.html"

Write-Host ""
Write-Host "Instructions:"
Write-Host "1. Click 'Download for Windows' on the webpage"
Write-Host "2. Run the installer when download completes"
Write-Host "3. Follow the installation wizard"
Write-Host ""
Write-Host "After installation, verify with:"
Write-Host "  python src/main.py check"
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

