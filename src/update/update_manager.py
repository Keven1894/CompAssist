import subprocess
from typing import Dict, Any, List
from pathlib import Path

class UpdateManager:
    """Manage system and software updates."""
    
    def __init__(self, platform_info: Dict[str, Any], logger):
        self.platform_info = platform_info
        self.logger = logger
        self.os = platform_info['os']
    
    def check_and_update(self):
        """Check for and apply updates."""
        self.logger.info("Checking for updates...")
        
        if self.os == 'windows':
            self._check_windows_updates()
        elif self.os == 'linux':
            self._check_linux_updates()
    
    def _check_windows_updates(self):
        """Check for Windows updates."""
        self.logger.info("Checking Windows updates...")
        
        try:
            # Use PowerShell to check for updates
            ps_command = """
            $UpdateSession = New-Object -ComObject Microsoft.Update.Session
            $UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
            $SearchResult = $UpdateSearcher.Search("IsInstalled=0")
            $Updates = $SearchResult.Updates
            
            if ($Updates.Count -gt 0) {
                Write-Host "Found $($Updates.Count) updates available"
                foreach ($Update in $Updates) {
                    Write-Host "$($Update.Title)"
                }
            } else {
                Write-Host "No updates available"
            }
            """
            
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True
            )
            
            self.logger.info(result.stdout)
            
        except Exception as e:
            self.logger.error(f"Failed to check Windows updates: {e}")
    
    def _check_linux_updates(self):
        """Check for Linux updates."""
        self.logger.info("Checking Linux updates...")
        
        # Try apt (Debian/Ubuntu)
        try:
            result = subprocess.run(
                ['apt', 'list', '--upgradable'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                updates = [line for line in result.stdout.split('\n') if '/' in line]
                if updates:
                    self.logger.info(f"Found {len(updates)} packages with updates available")
                else:
                    self.logger.info("System is up to date")
                return
        except Exception:
            pass
        
        # Try yum/dnf (RedHat/CentOS)
        try:
            result = subprocess.run(
                ['yum', 'check-update'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 or result.returncode == 100:
                self.logger.info("Update check completed")
            return
        except Exception:
            pass
        
        self.logger.warning("Could not determine update status")


