@echo off
REM Setup .env for BillionaireBot
echo PRIVATE_KEY=your_private_key_here>>.env
echo POLYGON_RPC_URL=https://polygon-rpc.com>>.env
echo FLASHLOAN_EXECUTOR_ADDRESS=0xBA12222222228d8Ba445958a75a0704d566BF2C8>>.env
echo MIN_PROFIT_USD=50>>.env
echo GAS_PRICE_GWEI=50>>.env
echo TAR_THRESHOLD=9.0>>.env
echo .env template created.