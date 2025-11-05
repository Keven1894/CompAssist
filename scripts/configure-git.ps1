# Git Configuration Script
# This script configures Git user settings

Write-Host "Configuring Git..." -ForegroundColor Cyan

$gitPath = "C:\Program Files\Git\cmd\git.exe"

if (Test-Path $gitPath) {
    Write-Host "Found Git at: $gitPath" -ForegroundColor Green
    
    # Get current user info
    $currentName = & $gitPath config --global user.name 2>&1
    $currentEmail = & $gitPath config --global user.email 2>&1
    
    Write-Host "`nCurrent Git Configuration:" -ForegroundColor Yellow
    Write-Host "  Name: $currentName"
    Write-Host "  Email: $currentEmail"
    
    # Prompt for user info if not set
    if (-not $currentName -or $currentName -match "error") {
        Write-Host "`nGit user name is not configured." -ForegroundColor Yellow
        $userName = Read-Host "Enter your name for Git commits"
        if ($userName) {
            & $gitPath config --global user.name $userName
            Write-Host "Set Git user.name to: $userName" -ForegroundColor Green
        }
    }
    
    if (-not $currentEmail -or $currentEmail -match "error") {
        Write-Host "`nGit user email is not configured." -ForegroundColor Yellow
        $userEmail = Read-Host "Enter your email for Git commits"
        if ($userEmail) {
            & $gitPath config --global user.email $userEmail
            Write-Host "Set Git user.email to: $userEmail" -ForegroundColor Green
        }
    }
    
    # Show final configuration
    Write-Host "`nFinal Git Configuration:" -ForegroundColor Green
    & $gitPath config --global --list | Select-String -Pattern "user\."
    
    Write-Host "`nGit is configured!" -ForegroundColor Green
} else {
    Write-Host "Git not found at expected location." -ForegroundColor Red
}

