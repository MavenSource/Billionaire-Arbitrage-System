# Billionaire Arbitrage System - Quick Start Guide

This guide will help you get the system up and running in minutes.

## Prerequisites

- **Python 3.11** (recommended for best compatibility)
  - Python 3.10 and 3.12 are also supported
  - **Windows users:** Python 3.13 is NOT recommended due to missing binary wheels
- Node.js 18 or higher
- Git

## Quick Installation

### 0. Check Your Python Version (Recommended)

Before starting, verify you have a compatible Python version:

```bash
python check_python_version.py
```

This script will:
- Verify your Python version
- Warn about potential compatibility issues
- Provide version-specific recommendations
- **Windows users with Python 3.13:** Will receive important warnings about missing binary wheels

### 1. Clone the Repository

```bash
git clone https://github.com/MavenSource/Billionaire-Arbitrage-System.git
cd Billionaire-Arbitrage-System
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your configuration (optional for testing)
# nano .env
```

### 3. Start the Backend

```bash
# Start the FastAPI server
python3 main.py
```

The backend API will be available at: http://localhost:8000

### 4. Test the Backend

In a new terminal:

```bash
# Test the system
python3 test_backend.py

# Or test API endpoints directly
curl http://localhost:8000/api/health
curl http://localhost:8000/api/pools
curl http://localhost:8000/api/stats
```

### 5. Frontend Setup (Optional)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at: http://localhost:3000

## Quick Test Without Installation

You can test the core functionality without any external dependencies:

```bash
# Test math engine and opportunity detector
python3 test_backend.py
```

## API Endpoints

Once the backend is running, you can access:

- **Health Check**: http://localhost:8000/api/health
- **Pool Data**: http://localhost:8000/api/pools
- **Opportunities**: http://localhost:8000/api/opportunities
- **Statistics**: http://localhost:8000/api/stats
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)

## Configuration

### Environment Variables (.env)

```bash
# Blockchain RPC
RPC_URL=https://polygon-rpc.com

# Private Key (for trade execution)
PRIVATE_KEY=your_private_key_here

# Trading Parameters
MIN_PROFIT_USD=10
MIN_PROFIT_PERCENTAGE=0.5
SCAN_INTERVAL=5
```

## Features Available

✅ **Working Features:**
- FastAPI backend with multiple endpoints
- Advanced arbitrage mathematics engine
- Web3 blockchain integration
- Opportunity detection and scoring
- Real-time pool monitoring
- Risk assessment
- WebSocket support for live data
- Next.js frontend with Material-UI dashboard

## Architecture

```
Billionaire-Arbitrage-System/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── modules/
│   │   ├── advanced_dex_mathematics.py
│   │   ├── web3_contract_integration.py
│   │   ├── flashloan_integration_flow.py
│   │   ├── advanced_opportunity_detection.py
│   │   └── ...
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   └── pages/
│   │       ├── index.js        # Dashboard
│   │       └── _app.js         # Theme config
│   ├── package.json
│   └── next.config.js
├── realtime/
│   └── ws_server.py            # WebSocket server
└── test_backend.py             # Test script
```

## Troubleshooting

### Backend won't start
- Ensure Python 3.11 is installed: `python3 --version`
- Install dependencies: `pip install -r backend/requirements.txt`

### Windows: pip build errors (cl.exe failed, msgpack/aiohttp/pydantic-core compilation errors)

**Problem:** On Windows with Python 3.13, you may see errors like:
```
error: command 'cl.exe' failed: None
ERROR: Failed building wheel for msgpack/aiohttp/pydantic-core
```

**Root Cause:** Python 3.13 lacks precompiled binary wheels for several dependencies on Windows. pip attempts to build from source but fails without MSVC or Rust toolchains.

**Solution (Recommended):** Use Python 3.11

1. **Download Python 3.11:**
   - Visit https://www.python.org/downloads/
   - Download Python 3.11.x (latest 3.11 version)
   - Run installer and check "Add Python to PATH"

2. **Create virtual environment with Python 3.11:**
   ```powershell
   # PowerShell
   python -m pip install --upgrade pip
   python -m pip install virtualenv
   python -m virtualenv .venv -p C:\Python311\python.exe
   .venv\Scripts\activate
   python -m pip install -U pip setuptools wheel
   cd backend
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```powershell
   python --version  # Should show Python 3.11.x
   pip list
   ```

**Alternative:** If you must use Python 3.13, install Visual Studio Build Tools and Rust, but this is NOT recommended:
- Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022) with "Desktop development with C++"
- Install [Rust](https://rustup.rs/) for pydantic-core
- This adds significant complexity and build time

### Frontend won't start
- Ensure Node.js 18+ is installed: `node --version`
- Install dependencies: `npm install` in frontend directory

### API returns errors
- Check if backend is running on port 8000
- Verify .env configuration
- Check logs for specific error messages

## Next Steps

1. **Configure RPC Endpoint**: Add your Polygon/Ethereum RPC URL to `.env`
2. **Add Private Key**: For trade execution (keep it secure!)
3. **Customize Parameters**: Adjust profit thresholds and scan intervals
4. **Explore API**: Visit http://localhost:8000/docs for interactive API documentation
5. **Monitor Dashboard**: Open http://localhost:3000 to see the live dashboard

## Security Notes

⚠️ **Important Security Practices:**
- Never commit your `.env` file with real credentials
- Use environment variables for sensitive data
- Test with testnets before using mainnet
- Keep your private keys secure
- Review all transactions before execution

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation in the repository
- Review the complete documentation: `complete_documentation.md`

---

**Ready to start?** Run `python3 backend/main.py` and visit http://localhost:8000/docs
