import psutil
import platform
import time
from typing import Dict, List, Any
from pathlib import Path

class EnvironmentChecker:
    """Check and analyze the computer environment."""
    
    def __init__(self, platform_info: Dict[str, Any], logger):
        self.platform_info = platform_info
        self.logger = logger
        self.os = platform_info['os']
    
    def check_all(self) -> Dict[str, Any]:
        """Perform all environment checks."""
        self.logger.info("Starting environment check...")
        
        results = {
            'system': self.check_system(),
            'resources': self.check_resources(),
            'software': self.check_installed_software(),
            'network': self.check_network(),
            'security': self.check_security(),
            'development': self.check_development_tools(),
        }
        
        self.logger.info("Environment check completed")
        return results
    
    def check_system(self) -> Dict[str, Any]:
        """Check system information."""
        self.logger.debug("Checking system information...")
        
        return {
            'os': self.platform_info.get('os', 'unknown'),
            'version': self.platform_info.get('version', 'unknown'),
            'release': self.platform_info.get('release', 'unknown'),
            'architecture': self.platform_info.get('architecture', 'unknown'),
            'hostname': platform.node(),
            'uptime_days': (time.time() - psutil.boot_time()) / 86400 if psutil.boot_time() else 0,
        }
    
    def check_resources(self) -> Dict[str, Any]:
        """Check system resources."""
        self.logger.debug("Checking system resources...")
        
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_total_gb': memory.total / (1024**3),
            'memory_available_gb': memory.available / (1024**3),
            'memory_percent': memory.percent,
            'disk_total_gb': disk.total / (1024**3),
            'disk_free_gb': disk.free / (1024**3),
            'disk_percent': disk.percent,
        }
    
    def check_installed_software(self) -> Dict[str, List[str]]:
        """Check installed software."""
        self.logger.debug("Checking installed software...")
        
        if self.os == 'windows':
            return self._check_windows_software()
        elif self.os == 'linux':
            return self._check_linux_software()
        else:
            return {'installed': [], 'error': 'Platform not supported'}
    
    def _check_windows_software(self) -> Dict[str, List[str]]:
        """Check installed software on Windows."""
        installed = []
        
        try:
            try:
                import winreg
            except ImportError:
                self.logger.debug("winreg not available, trying alternative method")
                # Fallback: Use PowerShell
                return self._check_windows_software_powershell()
            
            # Check 64-bit registry
            keys = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            ]
            
            for hkey, subkey in keys:
                try:
                    key = winreg.OpenKey(hkey, subkey)
                    for i in range(0, winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            subkey_path = f"{subkey}\\{subkey_name}"
                            subkey_handle = winreg.OpenKey(hkey, subkey_path)
                            
                            try:
                                display_name = winreg.QueryValueEx(subkey_handle, "DisplayName")[0]
                                if display_name:
                                    installed.append(display_name)
                            except FileNotFoundError:
                                pass
                            
                            winreg.CloseKey(subkey_handle)
                        except Exception:
                            continue
                    winreg.CloseKey(key)
                except Exception:
                    continue
        except Exception as e:
            self.logger.warning(f"Could not check Windows software via registry: {e}")
            return self._check_windows_software_powershell()
        
        return {'installed': list(set(installed))}
    
    def _check_windows_software_powershell(self) -> Dict[str, List[str]]:
        """Check installed software using PowerShell."""
        installed = []
        
        try:
            import subprocess
            ps_command = """
            Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | 
            Select-Object DisplayName | 
            Where-Object { $_.DisplayName } | 
            ForEach-Object { $_.DisplayName }
            """
            
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                installed = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        except Exception as e:
            self.logger.warning(f"Could not check Windows software via PowerShell: {e}")
        
        return {'installed': list(set(installed))}
    
    def _check_linux_software(self) -> Dict[str, List[str]]:
        """Check installed software on Linux."""
        installed = []
        
        try:
            import subprocess
            
            # Check dpkg (Debian/Ubuntu)
            result = subprocess.run(
                ['dpkg', '-l'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n')[5:]:  # Skip header
                    if line.startswith('ii'):
                        parts = line.split()
                        if len(parts) >= 2:
                            installed.append(parts[1])
            
            # Check rpm (RedHat/CentOS)
            result = subprocess.run(
                ['rpm', '-qa'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                installed.extend(result.stdout.strip().split('\n'))
                
        except Exception as e:
            self.logger.warning(f"Could not check Linux software: {e}")
        
        return {'installed': list(set(installed))}
    
    def check_network(self) -> Dict[str, Any]:
        """Check network configuration."""
        self.logger.debug("Checking network configuration...")
        
        interfaces = {}
        for interface, addrs in psutil.net_if_addrs().items():
            interfaces[interface] = [
                {'family': str(addr.family), 'address': addr.address}
                for addr in addrs
            ]
        
        return {
            'interfaces': interfaces,
            'connections': len(psutil.net_connections()),
        }
    
    def check_security(self) -> Dict[str, Any]:
        """Check security settings."""
        self.logger.debug("Checking security settings...")
        
        # Basic security checks
        checks = {
            'firewall_enabled': None,
            'antivirus_installed': False,
            'updates_pending': None,
        }
        
        if self.os == 'windows':
            checks.update(self._check_windows_security())
        elif self.os == 'linux':
            checks.update(self._check_linux_security())
        
        return checks
    
    def _check_windows_security(self) -> Dict[str, Any]:
        """Check Windows security settings."""
        checks = {}
        
        try:
            import subprocess
            # Check firewall status
            result = subprocess.run(
                ['netsh', 'advfirewall', 'show', 'allprofiles', 'state'],
                capture_output=True,
                text=True
            )
            checks['firewall_enabled'] = 'ON' in result.stdout.upper()
        except Exception:
            pass
        
        return checks
    
    def _check_linux_security(self) -> Dict[str, Any]:
        """Check Linux security settings."""
        checks = {}
        
        try:
            import subprocess
            # Check firewall (ufw/iptables)
            result = subprocess.run(
                ['ufw', 'status'],
                capture_output=True,
                text=True
            )
            checks['firewall_enabled'] = 'active' in result.stdout.lower()
        except Exception:
            pass
        
        return checks
    
    def check_development_tools(self) -> Dict[str, Any]:
        """Check development tools."""
        self.logger.debug("Checking development tools...")
        
        tools = {}
        
        # Check common development tools
        common_tools = {
            'git': 'git --version',
            'python': 'python --version',
            'node': 'node --version',
            'docker': 'docker --version',
            'java': 'java -version',
        }
        
        for tool, command in common_tools.items():
            try:
                import subprocess
                result = subprocess.run(
                    command.split(),
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                tools[tool] = {
                    'installed': result.returncode == 0,
                    'version': result.stdout.strip() if result.returncode == 0 else None
                }
                
                # Special handling for Docker - check if Docker Desktop is running (Windows)
                if tool == 'docker' and self.os == 'windows' and result.returncode == 0:
                    try:
                        # Check if Docker daemon is accessible
                        docker_info = subprocess.run(
                            ['docker', 'info'],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        tools[tool]['daemon_running'] = docker_info.returncode == 0
                        if docker_info.returncode != 0:
                            tools[tool]['note'] = 'Docker installed but daemon not running. Start Docker Desktop.'
                    except Exception:
                        tools[tool]['daemon_running'] = False
                        tools[tool]['note'] = 'Docker installed but daemon not accessible.'
                
            except Exception:
                tools[tool] = {'installed': False}
                if tool == 'docker':
                    tools[tool]['installation_guide'] = 'See DOCKER_INSTALLATION.md for installation instructions'
        
        return tools
    
    def print_report(self, results: Dict[str, Any]):
        """Print a formatted report of the check results."""
        from colorama import Fore, Style
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}ENVIRONMENT CHECK REPORT")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        # System
        print(f"{Fore.YELLOW}System Information:{Style.RESET_ALL}")
        sys_info = results['system']
        print(f"  OS: {sys_info['os']} {sys_info.get('release', '')}")
        print(f"  Architecture: {sys_info['architecture']}")
        print(f"  Hostname: {sys_info['hostname']}")
        
        # Resources
        print(f"\n{Fore.YELLOW}System Resources:{Style.RESET_ALL}")
        res = results['resources']
        print(f"  CPU: {res['cpu_count']} cores, {res['cpu_percent']:.1f}% usage")
        print(f"  Memory: {res['memory_available_gb']:.1f} GB / {res['memory_total_gb']:.1f} GB ({res['memory_percent']:.1f}% used)")
        print(f"  Disk: {res['disk_free_gb']:.1f} GB / {res['disk_total_gb']:.1f} GB ({res['disk_percent']:.1f}% used)")
        
        # Development Tools
        print(f"\n{Fore.YELLOW}Development Tools:{Style.RESET_ALL}")
        dev_tools = results['development']
        for tool, info in dev_tools.items():
            # Use ASCII-friendly characters for Windows compatibility
            status = f"{Fore.GREEN}[OK]{Style.RESET_ALL}" if info.get('installed') else f"{Fore.RED}[X]{Style.RESET_ALL}"
            version = f" ({info.get('version', '')})" if info.get('version') else ""
            
            # Special handling for Docker
            if tool == 'docker' and info.get('installed'):
                if not info.get('daemon_running', True):
                    status = f"{Fore.YELLOW}[!]{Style.RESET_ALL}"
                    version += f" {Fore.YELLOW}(Docker Desktop not running){Style.RESET_ALL}"
            
            print(f"  {status} {tool}{version}")
            
            # Show notes if any
            if 'note' in info:
                print(f"    {Fore.YELLOW}Note: {info['note']}{Style.RESET_ALL}")
            if 'installation_guide' in info:
                print(f"    {Fore.CYAN}Tip: {info['installation_guide']}{Style.RESET_ALL}")
        
        # Installed Software
        print(f"\n{Fore.YELLOW}Installed Software:{Style.RESET_ALL}")
        software = results['software'].get('installed', [])
        print(f"  Found {len(software)} installed applications")
        if software:
            print(f"  Sample: {', '.join(software[:10])}")
            if len(software) > 10:
                print(f"  ... and {len(software) - 10} more")
        
        print()

