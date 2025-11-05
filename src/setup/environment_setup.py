"""
Environment Setup Utilities
Handles setting up environment variables for installed software
"""
import os
import subprocess
from typing import Dict, Any
from pathlib import Path

class EnvironmentSetup:
    """Setup environment variables for installed software."""
    
    def __init__(self, platform_info: Dict[str, Any], logger):
        self.platform_info = platform_info
        self.logger = logger
        self.os = platform_info['os']
    
    def setup_git_path(self):
        """Add Git to PATH if not already present."""
        if self.os != 'windows':
            return
        
        self.logger.info("Checking Git installation and PATH...")
        
        # Common Git installation paths
        git_paths = [
            Path("C:/Program Files/Git/cmd"),
            Path("C:/Program Files (x86)/Git/cmd"),
            Path.home() / "AppData/Local/Programs/Git/cmd"
        ]
        
        git_path = None
        for path in git_paths:
            git_exe = path / "git.exe"
            if git_exe.exists():
                git_path = str(path)
                self.logger.info(f"Found Git at: {git_path}")
                break
        
        if not git_path:
            self.logger.warning("Git installation not found in common locations")
            return
        
        # Check if Git is in PATH
        current_path = os.environ.get('PATH', '')
        if git_path.lower() in current_path.lower():
            self.logger.info("Git is already in PATH")
            return
        
        # Add to PATH for current session
        new_path = f"{git_path};{current_path}"
        os.environ['PATH'] = new_path
        self.logger.info(f"Added Git to PATH for current session: {git_path}")
        
        # Add to system PATH permanently
        try:
            self._add_to_system_path(git_path)
            self.logger.info("Added Git to system PATH permanently")
        except Exception as e:
            self.logger.warning(f"Could not add to system PATH: {e}")
            self.logger.info("Please restart your terminal for PATH changes to take effect")
    
    def _add_to_system_path(self, path: str):
        """Add path to system PATH environment variable."""
        import winreg
        
        # Get current system PATH
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            0,
            winreg.KEY_ALL_ACCESS
        )
        
        try:
            current_path, _ = winreg.QueryValueEx(key, "Path")
            
            # Check if already in PATH
            if path.lower() in current_path.lower():
                return
            
            # Add to PATH
            new_path = f"{current_path};{path}"
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            
            # Broadcast environment change
            import ctypes
            ctypes.windll.user32.SendMessageW(
                0xFFFF,  # HWND_BROADCAST
                0x001A,  # WM_SETTINGCHANGE
                0,
                "Environment"
            )
        finally:
            winreg.CloseKey(key)
    
    def verify_git(self):
        """Verify Git installation and return version."""
        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                self.logger.info(f"Git verified: {version}")
                return version
        except Exception as e:
            self.logger.debug(f"Git verification failed: {e}")
        return None
    
    def configure_git(self, name: str = None, email: str = None):
        """Configure Git with user name and email."""
        if not name or not email:
            self.logger.info("Git configuration skipped (name/email not provided)")
            return
        
        try:
            # Configure name
            subprocess.run(
                ['git', 'config', '--global', 'user.name', name],
                check=True,
                capture_output=True
            )
            self.logger.info(f"Configured Git user.name: {name}")
            
            # Configure email
            subprocess.run(
                ['git', 'config', '--global', 'user.email', email],
                check=True,
                capture_output=True
            )
            self.logger.info(f"Configured Git user.email: {email}")
            
        except Exception as e:
            self.logger.warning(f"Failed to configure Git: {e}")



