"""
Script to setup Git environment after installation
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.logger import setup_logger
from src.core.platform import PlatformDetector
from src.setup.environment_setup import EnvironmentSetup

def main():
    """Setup Git environment."""
    logger = setup_logger(verbose=True)
    detector = PlatformDetector()
    platform_info = detector.detect()
    
    logger.info("Setting up Git environment...")
    
    env_setup = EnvironmentSetup(platform_info, logger)
    
    # Setup Git PATH
    env_setup.setup_git_path()
    
    # Verify Git
    version = env_setup.verify_git()
    
    if version:
        logger.info(f"[OK] Git is working: {version}")
        logger.info("")
        logger.info("To configure Git with your identity, run:")
        logger.info('  git config --global user.name "Your Name"')
        logger.info('  git config --global user.email "your.email@example.com"')
        logger.info("")
        logger.info("[!] Note: You may need to restart your terminal for PATH changes to take full effect.")
    else:
        logger.warning("Git is not accessible. Please restart your terminal and try again.")
        logger.info("If Git is still not found, ensure it was installed correctly.")

if __name__ == '__main__':
    main()

