"""
Development Information Provider
Provides system specs and development environment information
"""
from typing import Dict, Any
from src.core.logger import setup_logger
from src.core.platform import PlatformDetector
from src.checker.environment_checker import EnvironmentChecker

class DevelopmentInfoProvider:
    """Provides development-focused computer information"""
    
    def __init__(self, platform_info: Dict[str, Any], logger):
        self.platform_info = platform_info
        self.logger = logger
        self.checker = EnvironmentChecker(platform_info, logger)
    
    def get_development_info(self) -> Dict[str, Any]:
        """Get comprehensive development information"""
        
        # Get system information
        system_info = self.checker.check_system()
        resources = self.checker.check_resources()
        dev_tools = self.checker.check_development_tools()
        
        # Format for development use
        dev_info = {
            "system": {
                "os": system_info.get('os', 'unknown'),
                "os_version": system_info.get('version', 'unknown'),
                "os_release": system_info.get('release', 'unknown'),
                "architecture": system_info.get('architecture', 'unknown'),
                "hostname": system_info.get('hostname', 'unknown'),
                "processor": self.platform_info.get('processor', 'unknown'),
            },
            "specs": {
                "cpu": {
                    "cores": resources.get('cpu_count', 0),
                    "usage_percent": resources.get('cpu_percent', 0),
                    "processor": self.platform_info.get('processor', 'unknown'),
                },
                "memory": {
                    "total_gb": round(resources.get('memory_total_gb', 0), 2),
                    "available_gb": round(resources.get('memory_available_gb', 0), 2),
                    "used_percent": resources.get('memory_percent', 0),
                    "status": self._get_memory_status(resources.get('memory_percent', 0))
                },
                "disk": {
                    "total_gb": round(resources.get('disk_total_gb', 0), 2),
                    "free_gb": round(resources.get('disk_free_gb', 0), 2),
                    "used_percent": resources.get('disk_percent', 0),
                    "status": self._get_disk_status(resources.get('disk_percent', 0))
                }
            },
            "development_tools": self._format_dev_tools(dev_tools),
            "development_environment": {
                "python_version": dev_tools.get('python', {}).get('version', 'Not installed'),
                "docker_available": dev_tools.get('docker', {}).get('installed', False),
                "docker_running": dev_tools.get('docker', {}).get('daemon_running', False),
                "git_available": dev_tools.get('git', {}).get('installed', False),
                "node_available": dev_tools.get('node', {}).get('installed', False),
                "java_available": dev_tools.get('java', {}).get('installed', False),
            },
            "readiness": {
                "development_ready": self._assess_dev_readiness(dev_tools),
                "missing_tools": self._get_missing_tools(dev_tools),
                "recommendations": self._get_recommendations(dev_tools, resources)
            }
        }
        
        return dev_info
    
    def _format_dev_tools(self, dev_tools: Dict[str, Any]) -> Dict[str, Any]:
        """Format development tools information"""
        formatted = {}
        for tool, info in dev_tools.items():
            formatted[tool] = {
                "installed": info.get('installed', False),
                "version": info.get('version'),
                "status": "installed" if info.get('installed') else "not_installed"
            }
            if 'daemon_running' in info:
                formatted[tool]['daemon_running'] = info['daemon_running']
            if 'note' in info:
                formatted[tool]['note'] = info['note']
        return formatted
    
    def _get_memory_status(self, percent: float) -> str:
        """Get memory status"""
        if percent < 50:
            return "excellent"
        elif percent < 75:
            return "good"
        elif percent < 90:
            return "warning"
        else:
            return "critical"
    
    def _get_disk_status(self, percent: float) -> str:
        """Get disk status"""
        if percent < 50:
            return "excellent"
        elif percent < 80:
            return "good"
        elif percent < 90:
            return "warning"
        else:
            return "critical"
    
    def _assess_dev_readiness(self, dev_tools: Dict[str, Any]) -> bool:
        """Assess if system is ready for development"""
        # Consider development ready if Python is installed
        return dev_tools.get('python', {}).get('installed', False)
    
    def _get_missing_tools(self, dev_tools: Dict[str, Any]) -> list:
        """Get list of missing development tools"""
        essential_tools = ['python', 'git']
        missing = []
        for tool in essential_tools:
            if not dev_tools.get(tool, {}).get('installed', False):
                missing.append(tool)
        return missing
    
    def _get_recommendations(self, dev_tools: Dict[str, Any], resources: Dict[str, Any]) -> list:
        """Get development recommendations"""
        recommendations = []
        
        if not dev_tools.get('git', {}).get('installed', False):
            recommendations.append("Install Git for version control")
        
        if not dev_tools.get('docker', {}).get('installed', False):
            recommendations.append("Install Docker for containerization")
        elif dev_tools.get('docker', {}).get('installed') and not dev_tools.get('docker', {}).get('daemon_running', False):
            recommendations.append("Start Docker Desktop")
        
        if resources.get('memory_percent', 0) > 85:
            recommendations.append("Memory usage is high, consider closing unnecessary applications")
        
        if resources.get('disk_percent', 0) > 80:
            recommendations.append("Disk space is running low, consider cleanup")
        
        return recommendations

