@echo off
REM Setup .env for BillionaireBot
echo Creating .env configuration file...
echo.
echo IMPORTANT: Please edit .env after creation and add your real values!
echo.

if not exist backend (
    echo ERROR: backend directory not found!
    echo Please run this script from the root of the Billionaire-Arbitrage-System directory
    pause
    exit /b 1
)

cd backend

(
echo # Blockchain Configuration
echo PRIVATE_KEY=your_private_key_here
echo POLYGON_RPC_URL=https://polygon-rpc.com
echo.
echo # Trade Execution Settings
echo FLASHLOAN_EXECUTOR_ADDRESS=0xBA12222222228d8Ba445958a75a0704d566BF2C8
echo MIN_PROFIT_USD=50
echo GAS_PRICE_GWEI=50
echo TAR_THRESHOLD=9.0
echo.
echo # System Configuration
echo MIN_PROFIT_PERCENTAGE=0.5
echo SCAN_INTERVAL=5
) > .env

echo .env template created successfully in backend directory.
echo.
echo ============================================================
echo NEXT STEPS:
echo ============================================================
echo 1. Edit backend\.env and replace placeholder values
echo 2. Run install.bat to install Python dependencies
echo 3. Make sure you're using Python 3.11 (recommended)
echo 4. See WINDOWS_INSTALL.md for detailed instructions
echo ============================================================
cd ..
pause