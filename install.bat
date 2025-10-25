@echo off
REM Install required Python dependencies for BillionaireBot

echo Checking Python version...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Detected Python version: %PYTHON_VERSION%
echo %PYTHON_VERSION% | findstr /B /C:"3.13" > nul
if %errorlevel% == 0 (
    echo.
    echo ============================================================
    echo WARNING: Python 3.13 detected!
    echo ============================================================
    echo Python 3.13 on Windows lacks precompiled binary wheels for
    echo critical dependencies ^(msgpack, aiohttp, pydantic-core^).
    echo.
    echo This will cause installation failures unless you have:
    echo   - Visual Studio Build Tools with C++ support
    echo   - Rust toolchain ^(cargo/maturin^)
    echo.
    echo RECOMMENDED: Use Python 3.11 instead
    echo Download from: https://www.python.org/downloads/
    echo.
    echo Press Ctrl+C to cancel, or any key to continue anyway...
    pause > nul
)

echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

echo Installing dependencies from backend\requirements.txt...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo Installation failed!
    echo ============================================================
    echo If you see "cl.exe failed" or compilation errors:
    echo   1. Use Python 3.11 instead of 3.13
    echo   2. Or install Visual Studio Build Tools + Rust
    echo.
    echo For detailed instructions, see QUICKSTART.md
    echo ============================================================
    cd ..
    exit /b 1
)
cd ..

echo.
echo ============================================================
echo Installation complete!
echo ============================================================
echo To activate the environment: venv\Scripts\activate
echo To run the backend: cd backend ^&^& python main.py
echo ============================================================