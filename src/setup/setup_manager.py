import yaml
import subprocess
import requests
import os
from typing import Dict, Any, List
from pathlib import Path
from urllib.parse import urlparse

from src.setup.environment_setup import EnvironmentSetup

class SetupManager:
    """Manage software setup and configuration."""
    
    def __init__(self, platform_info: Dict[str, Any], logger):
        self.platform_info = platform_info
        self.logger = logger
        self.os = platform_info['os']
    
    def setup_from_config(self, config_path: str):
        """Setup system from configuration file."""
        config_file = Path(config_path)
        
        if not config_file.exists():
            self.logger.error(f"Configuration file not found: {config_path}")
            return
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        self.logger.info(f"Loading setup configuration from {config_path}")
        
        # Install software
        if 'software' in config:
            packages = config['software'].get('packages', [])
            
            # Handle new format with package dictionaries
            for package in packages:
                if isinstance(package, dict):
                    # New format with detailed info
                    self._install_package(package)
                else:
                    # Simple string format - use existing method
                    if self.os == 'windows':
                        self._install_windows_software({'packages': [package]})
                    elif self.os == 'linux':
                        self._install_linux_software({'packages': [package]})
        
        # Configure settings
        if 'settings' in config:
            self._configure_settings(config['settings'])
        
        # Setup environment
        if 'environment' in config:
            self._setup_environment(config['environment'])
    
    def _install_software(self, software_config: Dict[str, Any]):
        """Install software packages."""
        self.logger.info("Installing software packages...")
        
        packages = software_config.get('packages', [])
        
        if self.os == 'windows':
            self._install_windows_software(software_config)
        elif self.os == 'linux':
            self._install_linux_software(software_config)
    
    def _install_package(self, package: Any):
        """Install a single package (handles dict or string format)."""
        if isinstance(package, dict):
            # New format with detailed info
            package_name = package.get('name', '')
            package_type = package.get('type', 'standard')
            
            if package_type == 'direct_download':
                self._install_direct_download(package)
            else:
                # Standard package manager installation
                self._install_windows_software({'packages': [package_name]})
        else:
            # Simple string format
            if self.os == 'windows':
                self._install_windows_software({'packages': [package]})
            elif self.os == 'linux':
                self._install_linux_software({'packages': [package]})
    
    def _install_direct_download(self, package_info: Dict[str, Any]):
        """Install software via direct download."""
        package_name = package_info.get('name', 'Unknown')
        url = package_info.get('url')
        installer_name = package_info.get('installer', 'setup.exe')
        silent = package_info.get('silent_install', False)
        
        if not url:
            self.logger.error(f"No URL provided for {package_name}")
            return
        
        self.logger.info(f"Installing {package_name} via direct download...")
        
        try:
            # Download the installer
            downloads_dir = Path.home() / 'Downloads'
            downloads_dir.mkdir(exist_ok=True)
            
            installer_path = downloads_dir / installer_name
            
            self.logger.info(f"Downloading from {url}...")
            
            # For Lightshot, we need to handle the download page
            # Let's try to download directly
            response = requests.get(url, allow_redirects=True, timeout=30)
            
            # If it's HTML, try to extract download link
            if 'html' in response.headers.get('content-type', '').lower():
                self.logger.warning(f"Got HTML page instead of installer. Opening browser for manual download.")
                self.logger.info(f"Please download {package_name} from: {url}")
                
                # Try to open browser
                try:
                    import webbrowser
                    webbrowser.open(url)
                    self.logger.info(f"Browser opened. Please download and run the installer manually.")
                except Exception:
                    pass
                return
            
            # Save the installer
            with open(installer_path, 'wb') as f:
                f.write(response.content)
            
            self.logger.info(f"Downloaded to {installer_path}")
            
            # Run installer
            self.logger.info(f"Running installer...")
            
            # For Windows, try to open the installer (will open GUI installer)
            if self.os == 'windows':
                try:
                    # Use Start-Process to open installer (allows GUI interaction)
                    import subprocess
                    if silent:
                        # Silent install attempt
                        result = subprocess.run(
                            [str(installer_path), '/VERYSILENT', '/NORESTART'],
                            check=False,
                            timeout=300  # 5 minute timeout
                        )
                    else:
                        # Open installer in GUI mode (user can interact)
                        self.logger.info(f"Opening installer GUI for {package_name}...")
                        self.logger.info(f"Please complete the installation wizard.")
                        # Use start command to open GUI installer
                        subprocess.Popen([str(installer_path)], shell=True)
                        self.logger.info(f"Installer opened. Please complete the installation manually.")
                        return  # Return early - user will complete installation
                except subprocess.TimeoutExpired:
                    self.logger.warning(f"Installer timed out")
                except Exception as e:
                    self.logger.error(f"Error running installer: {e}")
                    # Fallback: try to open it
                    try:
                        os.startfile(str(installer_path))
                        self.logger.info(f"Opened installer. Please complete installation manually.")
                        return
                    except Exception:
                        pass
            else:
                # Linux/Mac
                if silent:
                    cmd = [str(installer_path), '/S']  # Silent install
                else:
                    cmd = [str(installer_path)]
                
                result = subprocess.run(cmd, check=False, timeout=300)
                
                if result.returncode == 0:
                    self.logger.info(f"Successfully installed {package_name}")
                else:
                    self.logger.warning(f"Installer returned code {result.returncode}. May need manual installation.")
                
        except Exception as e:
            self.logger.error(f"Failed to install {package_name}: {e}")
            self.logger.info(f"Please download manually from: {url}")
    
    def _install_windows_software(self, software_config: Dict[str, Any]):
        """Install software on Windows."""
        # Check for winget, chocolatey, or manual installation
        import subprocess
        
        # Try winget first (Windows 10/11)
        try:
            result = subprocess.run(['winget', '--version'], capture_output=True)
            if result.returncode == 0:
                self.logger.info("Using winget for installation")
                for package in software_config.get('packages', []):
                    self._install_with_winget(package)
                return
        except Exception:
            pass
        
        # Try chocolatey
        try:
            result = subprocess.run(['choco', '--version'], capture_output=True)
            if result.returncode == 0:
                self.logger.info("Using Chocolatey for installation")
                for package in software_config.get('packages', []):
                    self._install_with_chocolatey(package)
                return
        except Exception:
            pass
        
        self.logger.warning("No package manager found. Manual installation required.")
    
    def _install_with_winget(self, package: str):
        """Install package using winget."""
        import subprocess
        self.logger.info(f"Installing {package} with winget...")
        try:
            subprocess.run(['winget', 'install', package, '--accept-package-agreements', '--accept-source-agreements'], check=True)
            self.logger.info(f"Successfully installed {package}")
        except Exception as e:
            self.logger.error(f"Failed to install {package}: {e}")
    
    def _install_with_chocolatey(self, package: str):
        """Install package using Chocolatey."""
        import subprocess
        self.logger.info(f"Installing {package} with Chocolatey...")
        try:
            subprocess.run(['choco', 'install', package, '-y'], check=True)
            self.logger.info(f"Successfully installed {package}")
        except Exception as e:
            self.logger.error(f"Failed to install {package}: {e}")
    
    def _install_linux_software(self, software_config: Dict[str, Any]):
        """Install software on Linux."""
        import subprocess
        
        # Detect package manager
        package_manager = None
        try:
            subprocess.run(['apt', '--version'], capture_output=True, check=True)
            package_manager = 'apt'
        except Exception:
            try:
                subprocess.run(['yum', '--version'], capture_output=True, check=True)
                package_manager = 'yum'
            except Exception:
                try:
                    subprocess.run(['dnf', '--version'], capture_output=True, check=True)
                    package_manager = 'dnf'
                except Exception:
                    pass
        
        if not package_manager:
            self.logger.error("No supported package manager found")
            return
        
        self.logger.info(f"Using {package_manager} for installation")
        
        for package in software_config.get('packages', []):
            self._install_with_package_manager(package_manager, package)
    
    def _install_with_package_manager(self, manager: str, package: str):
        """Install package using system package manager."""
        import subprocess
        self.logger.info(f"Installing {package} with {manager}...")
        
        commands = {
            'apt': ['apt-get', 'install', '-y', package],
            'yum': ['yum', 'install', '-y', package],
            'dnf': ['dnf', 'install', '-y', package],
        }
        
        try:
            subprocess.run(commands[manager], check=True)
            self.logger.info(f"Successfully installed {package}")
        except Exception as e:
            self.logger.error(f"Failed to install {package}: {e}")
    
    def _configure_settings(self, settings_config: Dict[str, Any]):
        """Configure system settings."""
        self.logger.info("Configuring system settings...")
        
        if self.os == 'windows':
            self._configure_windows_settings(settings_config)
        elif self.os == 'linux':
            self._configure_linux_settings(settings_config)
    
    def _configure_windows_settings(self, settings_config: Dict[str, Any]):
        """Configure Windows settings."""
        # Placeholder for Windows configuration
        self.logger.info("Windows settings configuration not yet implemented")
    
    def _configure_linux_settings(self, settings_config: Dict[str, Any]):
        """Configure Linux settings."""
        # Placeholder for Linux configuration
        self.logger.info("Linux settings configuration not yet implemented")
    
    def _setup_environment(self, env_config: Dict[str, Any]):
        """Setup environment variables."""
        self.logger.info("Setting up environment variables...")
        
        # Setup Git PATH if needed
        env_setup = EnvironmentSetup(self.platform_info, self.logger)
        env_setup.setup_git_path()
        
        if self.os == 'windows':
            self._setup_windows_environment(env_config)
        elif self.os == 'linux':
            self._setup_linux_environment(env_config)
    
    def _setup_windows_environment(self, env_config: Dict[str, Any]):
        """Setup Windows environment variables."""
        import winreg
        
        variables = env_config.get('variables', {})
        
        # Check and add Git to PATH if installed but not in PATH
        self._ensure_git_in_path()
        
        # Set user environment variables
        for key, value in variables.items():
            try:
                # Set user environment variable
                key_path = r"Environment"
                reg_key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    key_path,
                    0,
                    winreg.KEY_ALL_ACCESS
                )
                
                try:
                    # Get current value
                    current_value, _ = winreg.QueryValueEx(reg_key, key)
                    if current_value != value:
                        winreg.SetValueEx(reg_key, key, 0, winreg.REG_EXPAND_SZ, value)
                        self.logger.info(f"Updated environment variable: {key}={value}")
                    else:
                        self.logger.debug(f"Environment variable {key} already set correctly")
                except FileNotFoundError:
                    # Variable doesn't exist, create it
                    winreg.SetValueEx(reg_key, key, 0, winreg.REG_EXPAND_SZ, value)
                    self.logger.info(f"Created environment variable: {key}={value}")
                
                winreg.CloseKey(reg_key)
                
            except Exception as e:
                self.logger.error(f"Failed to set environment variable {key}: {e}")
        
        if variables:
            self.logger.info("Environment variables updated. Please restart your terminal for changes to take effect.")
    
    def _setup_linux_environment(self, env_config: Dict[str, Any]):
        """Setup Linux environment variables."""
        variables = env_config.get('variables', {})
        
        # Add to ~/.bashrc or ~/.profile
        home = Path.home()
        bashrc = home / '.bashrc'
        
        for key, value in variables.items():
            export_line = f'export {key}="{value}"\n'
            
            # Check if already exists
            if bashrc.exists():
                with open(bashrc, 'r') as f:
                    if export_line.strip() in f.read():
                        continue
            
            # Append to bashrc
            with open(bashrc, 'a') as f:
                f.write(export_line)
            
            self.logger.info(f"Added {key} to ~/.bashrc")
        
        if variables:
            self.logger.info("Environment variables added to ~/.bashrc. Please run 'source ~/.bashrc' or restart terminal.")
    
    def _ensure_git_in_path(self):
        """Ensure Git is in PATH if installed."""
        import winreg
        
        # Check common Git installation paths
        git_paths = [
            r"C:\Program Files\Git\cmd",
            r"C:\Program Files\Git\bin",
            r"C:\Program Files (x86)\Git\cmd",
            r"C:\Program Files (x86)\Git\bin",
        ]
        
        git_found = None
        for git_path in git_paths:
            if Path(git_path).exists() and Path(git_path).joinpath("git.exe").exists():
                git_found = git_path
                self.logger.info(f"Found Git at: {git_path}")
                break
        
        if not git_found:
            self.logger.warning("Git installation not found in common locations")
            return
        
        # Check current PATH
        try:
            key_path = r"Environment"
            reg_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0,
                winreg.KEY_ALL_ACCESS
            )
            
            try:
                path_value, _ = winreg.QueryValueEx(reg_key, "Path")
                path_list = path_value.split(';')
                
                # Check if Git path is already in PATH
                if git_found in path_list:
                    self.logger.info(f"Git is already in PATH: {git_found}")
                    winreg.CloseKey(reg_key)
                    return
                
                # Add Git to PATH
                new_path = path_value + ';' + git_found if path_value else git_found
                winreg.SetValueEx(reg_key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                winreg.CloseKey(reg_key)
                
                self.logger.info(f"Added Git to PATH: {git_found}")
                self.logger.info("Please restart your terminal for PATH changes to take effect.")
                
            except FileNotFoundError:
                # PATH doesn't exist (unlikely), create it
                winreg.SetValueEx(reg_key, "Path", 0, winreg.REG_EXPAND_SZ, git_found)
                winreg.CloseKey(reg_key)
                self.logger.info(f"Created PATH with Git: {git_found}")
                
        except Exception as e:
            self.logger.error(f"Failed to update PATH: {e}")


