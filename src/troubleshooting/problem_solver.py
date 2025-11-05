from typing import Dict, Any, List
from colorama import Fore, Style

class ProblemSolver:
    """Detect and fix common computer problems."""
    
    def __init__(self, platform_info: Dict[str, Any], logger):
        self.platform_info = platform_info
        self.logger = logger
        self.os = platform_info['os']
    
    def detect_issues(self) -> List[Dict[str, Any]]:
        """Detect common issues."""
        self.logger.info("Detecting issues...")
        
        issues = []
        
        # Check disk space
        issues.extend(self._check_disk_space())
        
        # Check memory
        issues.extend(self._check_memory())
        
        # Check network connectivity
        issues.extend(self._check_network_connectivity())
        
        # Check security
        issues.extend(self._check_security_issues())
        
        return issues
    
    def _check_disk_space(self) -> List[Dict[str, Any]]:
        """Check disk space issues."""
        issues = []
        
        try:
            import psutil
            import os
            disk = psutil.disk_usage(os.path.expanduser('~'))
            percent_used = disk.percent
            
            if percent_used > 90:
                issues.append({
                    'severity': 'high',
                    'category': 'disk',
                    'issue': f'Disk space critically low ({percent_used:.1f}% used)',
                    'fix': 'cleanup_disk',
                })
            elif percent_used > 80:
                issues.append({
                    'severity': 'medium',
                    'category': 'disk',
                    'issue': f'Disk space running low ({percent_used:.1f}% used)',
                    'fix': 'cleanup_disk',
                })
        except Exception as e:
            self.logger.warning(f"Could not check disk space: {e}")
        
        return issues
    
    def _check_memory(self) -> List[Dict[str, Any]]:
        """Check memory issues."""
        issues = []
        
        try:
            import psutil
            memory = psutil.virtual_memory()
            
            if memory.percent > 90:
                issues.append({
                    'severity': 'high',
                    'category': 'memory',
                    'issue': f'Memory usage critically high ({memory.percent:.1f}%)',
                    'fix': 'free_memory',
                })
        except Exception as e:
            self.logger.warning(f"Could not check memory: {e}")
        
        return issues
    
    def _check_network_connectivity(self) -> List[Dict[str, Any]]:
        """Check network connectivity."""
        issues = []
        
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
        except OSError:
            issues.append({
                'severity': 'high',
                'category': 'network',
                'issue': 'No internet connectivity detected',
                'fix': 'check_network',
            })
        
        return issues
    
    def _check_security_issues(self) -> List[Dict[str, Any]]:
        """Check security issues."""
        issues = []
        
        # Check if firewall is enabled (platform-specific)
        if self.os == 'windows':
            try:
                import subprocess
                result = subprocess.run(
                    ['netsh', 'advfirewall', 'show', 'allprofiles', 'state'],
                    capture_output=True,
                    text=True
                )
                if 'OFF' in result.stdout.upper():
                    issues.append({
                        'severity': 'medium',
                        'category': 'security',
                        'issue': 'Windows Firewall is disabled',
                        'fix': 'enable_firewall',
                    })
            except Exception:
                pass
        
        return issues
    
    def print_issues(self, issues: List[Dict[str, Any]]):
        """Print detected issues."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}ISSUE DETECTION REPORT")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        if not issues:
            print(f"{Fore.GREEN}✓ No issues detected!{Style.RESET_ALL}\n")
            return
        
        severity_colors = {
            'high': Fore.RED,
            'medium': Fore.YELLOW,
            'low': Fore.CYAN,
        }
        
        for issue in issues:
            severity = issue['severity']
            color = severity_colors.get(severity, '')
            print(f"{color}[{severity.upper()}]{Style.RESET_ALL} {issue['category'].upper()}: {issue['issue']}")
        
        print()
    
    def fix_issues(self, issues: List[Dict[str, Any]]):
        """Fix detected issues."""
        self.logger.info(f"Attempting to fix {len(issues)} issues...")
        
        for issue in issues:
            fix_method = issue.get('fix')
            if fix_method:
                self._apply_fix(fix_method, issue)
    
    def _apply_fix(self, fix_method: str, issue: Dict[str, Any]):
        """Apply a fix method."""
        self.logger.info(f"Applying fix: {fix_method}")
        
        fixes = {
            'cleanup_disk': self._fix_disk_space,
            'free_memory': self._fix_memory,
            'check_network': self._fix_network,
            'enable_firewall': self._fix_firewall,
        }
        
        fix_func = fixes.get(fix_method)
        if fix_func:
            fix_func(issue)
        else:
            self.logger.warning(f"Unknown fix method: {fix_method}")
    
    def _fix_disk_space(self, issue: Dict[str, Any]):
        """Fix disk space issues."""
        self.logger.info("Running disk cleanup...")
        
        if self.os == 'windows':
            try:
                import subprocess
                # Run Windows disk cleanup
                subprocess.run(['cleanmgr', '/d', 'C:'], check=False)
                self.logger.info("Disk cleanup initiated")
            except Exception as e:
                self.logger.error(f"Failed to run disk cleanup: {e}")
        else:
            self.logger.info("Manual disk cleanup recommended")
    
    def _fix_memory(self, issue: Dict[str, Any]):
        """Fix memory issues."""
        self.logger.info("Memory cleanup suggestions:")
        self.logger.info("  - Close unnecessary applications")
        self.logger.info("  - Restart the system if needed")
        self.logger.info("  - Check for memory leaks in running processes")
    
    def _fix_network(self, issue: Dict[str, Any]):
        """Fix network issues."""
        self.logger.info("Network troubleshooting:")
        self.logger.info("  - Check physical connections")
        self.logger.info("  - Restart network adapter")
        self.logger.info("  - Check DNS settings")
        self.logger.info("  - Contact ISP if problem persists")
    
    def _fix_firewall(self, issue: Dict[str, Any]):
        """Fix firewall issues."""
        if self.os == 'windows':
            self.logger.info("Enabling Windows Firewall...")
            try:
                import subprocess
                subprocess.run(
                    ['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'on'],
                    check=True
                )
                self.logger.info("Windows Firewall enabled")
            except Exception as e:
                self.logger.error(f"Failed to enable firewall: {e}")

