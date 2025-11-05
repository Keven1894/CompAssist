import platform
import sys
from typing import Dict, Any

class PlatformDetector:
    """Detect and identify the current platform."""
    
    def detect(self) -> Dict[str, Any]:
        """Detect platform information."""
        system = platform.system().lower()
        
        info = {
            'os': system,
            'version': platform.version(),
            'release': platform.release(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'architecture': platform.architecture()[0],
            'python_version': sys.version,
        }
        
        if system == 'windows':
            info.update(self._detect_windows())
        elif system == 'linux':
            info.update(self._detect_linux())
        elif system == 'darwin':
            info.update(self._detect_macos())
        
        return info
    
    def _detect_windows(self) -> Dict[str, Any]:
        """Detect Windows-specific information."""
        info = {}
        
        try:
            if sys.platform == 'win32':
                import winreg
                # Get Windows version
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
                )
                try:
                    info['windows_version'] = winreg.QueryValueEx(key, "DisplayVersion")[0]
                except Exception:
                    pass
                try:
                    info['windows_build'] = winreg.QueryValueEx(key, "CurrentBuild")[0]
                except Exception:
                    pass
                winreg.CloseKey(key)
        except ImportError:
            pass
        except Exception:
            pass
        
        try:
            import wmi
            c = wmi.WMI()
            os_info = c.Win32_OperatingSystem()[0]
            info['windows_name'] = os_info.Caption
            info['total_memory_gb'] = int(os_info.TotalVisibleMemorySize) / 1024 / 1024
        except ImportError:
            pass
        except Exception:
            pass
        
        return info
    
    def _detect_linux(self) -> Dict[str, Any]:
        """Detect Linux-specific information."""
        info = {}
        
        try:
            import distro
            info['distribution'] = distro.name()
            info['distro_version'] = distro.version()
            info['distro_codename'] = distro.codename()
        except ImportError:
            # Fallback to /etc/os-release
            try:
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('NAME='):
                            info['distribution'] = line.split('=')[1].strip('"\n')
                        elif line.startswith('VERSION='):
                            info['distro_version'] = line.split('=')[1].strip('"\n')
            except Exception:
                pass
        
        return info
    
    def _detect_macos(self) -> Dict[str, Any]:
        """Detect macOS-specific information."""
        info = {}
        
        try:
            import subprocess
            result = subprocess.run(
                ['sw_vers'],
                capture_output=True,
                text=True
            )
            for line in result.stdout.split('\n'):
                if 'ProductVersion:' in line:
                    info['macos_version'] = line.split(':')[1].strip()
        except Exception:
            pass
        
        return info
    
    def is_windows(self) -> bool:
        """Check if running on Windows."""
        return platform.system().lower() == 'windows'
    
    def is_linux(self) -> bool:
        """Check if running on Linux."""
        return platform.system().lower() == 'linux'
    
    def is_macos(self) -> bool:
        """Check if running on macOS."""
        return platform.system().lower() == 'darwin'

