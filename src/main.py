import sys
import platform
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.logger import setup_logger
from src.core.platform import PlatformDetector
from src.checker.environment_checker import EnvironmentChecker
from src.setup.setup_manager import SetupManager
from src.update.update_manager import UpdateManager
from src.troubleshooting.problem_solver import ProblemSolver

def main():
    """Main entry point for the Local Computer Assistant."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Local Computer Assistant - Standardize and manage your computer environment'
    )
    parser.add_argument(
        'command',
        choices=['check', 'setup', 'update', 'diagnose', 'fix'],
        help='Command to execute'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--config', '-c',
        type=str,
        default='config/default.yaml',
        help='Configuration file path'
    )
    
    args = parser.parse_args()
    
    # Setup logger
    logger = setup_logger(verbose=args.verbose)
    
    # Detect platform
    detector = PlatformDetector()
    platform_info = detector.detect()
    
    logger.info(f"Detected platform: {platform_info['os']} {platform_info['version']}")
    
    try:
        if args.command == 'check':
            checker = EnvironmentChecker(platform_info, logger)
            results = checker.check_all()
            checker.print_report(results)
            
        elif args.command == 'setup':
            manager = SetupManager(platform_info, logger)
            manager.setup_from_config(args.config)
            
        elif args.command == 'update':
            update_manager = UpdateManager(platform_info, logger)
            update_manager.check_and_update()
            
        elif args.command == 'diagnose':
            solver = ProblemSolver(platform_info, logger)
            issues = solver.detect_issues()
            solver.print_issues(issues)
            
        elif args.command == 'fix':
            solver = ProblemSolver(platform_info, logger)
            issues = solver.detect_issues()
            solver.fix_issues(issues)
            
    except Exception as e:
        logger.error(f"Error executing command '{args.command}': {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()


