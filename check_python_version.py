#!/usr/bin/env python3
"""
Python Version Checker for Billionaire Arbitrage System

This script checks your Python version and provides recommendations
for the best installation experience, especially on Windows.
"""

import sys
import platform

def check_python_version():
    """Check Python version and provide recommendations."""
    version_info = sys.version_info
    major = version_info.major
    minor = version_info.minor
    patch = version_info.micro
    
    version_str = f"{major}.{minor}.{patch}"
    os_name = platform.system()
    
    print("=" * 70)
    print("Python Version Check - Billionaire Arbitrage System")
    print("=" * 70)
    print(f"Python Version: {version_str}")
    print(f"Operating System: {os_name}")
    print(f"Platform: {platform.platform()}")
    print("=" * 70)
    print()
    
    # Check if Python 3
    if major < 3:
        print("❌ ERROR: Python 3 is required!")
        print(f"   You are using Python {version_str}")
        print("   Please install Python 3.11 from https://www.python.org/downloads/")
        return False
    
    # Check minimum version (3.9+)
    if minor < 9:
        print(f"❌ ERROR: Python 3.9+ is required!")
        print(f"   You are using Python {version_str}")
        print("   Please upgrade to Python 3.11 (recommended)")
        return False
    
    # Check for Python 3.13 on Windows
    if minor == 13 and os_name == "Windows":
        print("⚠️  WARNING: Python 3.13 on Windows is NOT RECOMMENDED!")
        print()
        print("   Why?")
        print("   - Many packages lack precompiled binary wheels for Python 3.13")
        print("   - Dependencies will try to compile from source")
        print("   - This requires Visual Studio Build Tools and Rust")
        print("   - Installation will likely FAIL without these tools")
        print()
        print("   📥 RECOMMENDED ACTION:")
        print("   - Install Python 3.11 from https://www.python.org/downloads/")
        print("   - See WINDOWS_INSTALL.md for detailed instructions")
        print()
        print("   Alternative (not recommended):")
        print("   - Install Visual Studio Build Tools with C++ support")
        print("   - Install Rust toolchain from https://rustup.rs/")
        print("   - Expect longer installation times and potential issues")
        print()
        return None  # Warning, not error
    
    # Check for Python 3.13 on other platforms
    if minor == 13:
        print("⚠️  WARNING: Python 3.13 is very new")
        print("   Some packages may not have binary wheels yet")
        print("   Python 3.11 is recommended for best compatibility")
        print()
        return None
    
    # Optimal versions
    if minor == 11:
        print("✅ EXCELLENT: Python 3.11 detected!")
        print("   This is the recommended version with best package compatibility")
        print()
        return True
    
    # Good versions
    if minor in [10, 12]:
        print("✅ GOOD: Python 3.{} is fully supported".format(minor))
        print("   All dependencies should install smoothly")
        print()
        return True
    
    # Python 3.9
    if minor == 9:
        print("⚠️  Python 3.9 is supported but older")
        print("   Consider upgrading to Python 3.11 for best experience")
        print()
        return True
    
    # Future versions
    if minor > 13:
        print("⚠️  WARNING: Very new Python version detected")
        print(f"   Python {version_str} may not have full package support")
        print("   Python 3.11 is recommended")
        print()
        return None
    
    return True

def print_next_steps():
    """Print next steps after version check."""
    os_name = platform.system()
    
    print("=" * 70)
    print("Next Steps:")
    print("=" * 70)
    
    if os_name == "Windows":
        print("1. See WINDOWS_INSTALL.md for detailed installation instructions")
        print("2. Run setup_env.bat to create .env configuration")
        print("3. Run install.bat to install dependencies")
        print("4. Start backend: cd backend && python main.py")
    else:
        print("1. Install dependencies: cd backend && pip install -r requirements.txt")
        print("2. Configure environment: cp backend/.env.example backend/.env")
        print("3. Edit backend/.env with your settings")
        print("4. Start backend: cd backend && python main.py")
    
    print()
    print("For more information:")
    print("- README.md - Complete system overview")
    print("- QUICKSTART.md - Quick start guide with troubleshooting")
    if os_name == "Windows":
        print("- WINDOWS_INSTALL.md - Windows-specific installation guide")
    print("=" * 70)

def main():
    """Main function."""
    result = check_python_version()
    
    if result is False:
        print("❌ Python version check FAILED")
        print("   Please install a compatible Python version")
        sys.exit(1)
    elif result is None:
        print("⚠️  Python version check completed with WARNINGS")
        print("   Installation may encounter issues")
        print()
        user_input = input("Continue anyway? (y/N): ").strip().lower()
        if user_input != 'y':
            print("Installation cancelled. Please install Python 3.11")
            sys.exit(1)
    else:
        print("✅ Python version check PASSED")
    
    print()
    print_next_steps()

if __name__ == "__main__":
    main()
