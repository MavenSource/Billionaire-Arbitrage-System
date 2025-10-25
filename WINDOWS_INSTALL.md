# Windows Installation Guide

This guide provides step-by-step instructions for setting up the Billionaire Arbitrage System on Windows, with special attention to Python version compatibility issues.

## ⚠️ Important: Python Version Compatibility

**RECOMMENDED:** Use **Python 3.11** on Windows for the best experience.

**Why not Python 3.13?**
- Python 3.13 is the newest release and many packages haven't published Windows binary wheels yet
- Dependencies like `msgpack`, `aiohttp`, and `pydantic-core` will try to compile from source
- Compilation requires Visual Studio Build Tools (MSVC) and Rust toolchain
- This adds significant complexity, installation time, and potential failure points

**Supported Python Versions:**
- ✅ **Python 3.11** - Recommended (best wheel availability)
- ✅ **Python 3.10** - Fully supported
- ✅ **Python 3.12** - Supported (most wheels available)
- ⚠️ **Python 3.13** - Not recommended on Windows (missing wheels)

## Prerequisites

- Windows 10 or Windows 11
- Python 3.11 (download from [python.org](https://www.python.org/downloads/))
- Node.js 18+ (download from [nodejs.org](https://nodejs.org/))
- Git (download from [git-scm.com](https://git-scm.com/))

## Step 1: Install Python 3.11

1. **Download Python 3.11:**
   - Visit https://www.python.org/downloads/
   - Click on "Download Python 3.11.x" (get the latest 3.11 version)
   - Choose the Windows installer (64-bit recommended)

2. **Run the installer:**
   - ✅ **IMPORTANT:** Check "Add Python 3.11 to PATH"
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify installation:**
   ```powershell
   python --version
   ```
   Should output: `Python 3.11.x`

## Step 2: Clone the Repository

Open PowerShell or Command Prompt:

```powershell
git clone https://github.com/MavenSource/Billionaire-Arbitrage-System.git
cd Billionaire-Arbitrage-System
```

## Step 3: Install Backend Dependencies

### Option A: Automated Install (Recommended)

```powershell
# Run the installation script
.\install.bat
```

The script will:
- Check your Python version and warn if using 3.13+
- Create a virtual environment
- Install all backend dependencies
- Handle errors gracefully

### Option B: Manual Install

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Upgrade pip and tools
python -m pip install --upgrade pip setuptools wheel

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

## Step 4: Configure Environment

```powershell
# Copy environment template
cd backend
copy .env.example .env

# Edit .env with your settings
notepad .env
```

Add your configuration:
```
RPC_URL=https://polygon-rpc.com
PRIVATE_KEY=your_private_key_here
MIN_PROFIT_USD=10
```

## Step 5: Install Frontend Dependencies (Optional)

```powershell
cd frontend
npm install
cd ..
```

## Step 6: Start the System

### Start Backend:
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\activate

# Start backend server
cd backend
python main.py
```

Backend will be available at: http://localhost:8000

### Start Frontend (in a new PowerShell window):
```powershell
cd Billionaire-Arbitrage-System\frontend
npm run dev
```

Frontend will be available at: http://localhost:3000

## Troubleshooting

### Issue: "cl.exe failed" or "error: Microsoft Visual C++ 14.0 or greater is required"

**Problem:** You're using Python 3.13 and pip is trying to compile packages from source.

**Solutions:**

1. **Recommended: Switch to Python 3.11**
   > **Note:** The path `C:\Python311\python.exe` assumes a default installation.  
   > If you installed Python elsewhere, adjust the path accordingly.  
   > To find your Python 3.11 executable, run one of the following in PowerShell:  
   > - `where python` (shows all python executables on your PATH)  
   > - `py -0p` (shows all installed Python versions and their paths)  
   ```powershell
   # Create new virtual environment with Python 3.11
   # Option 1: If you have multiple Python versions installed
   py -3.11 -m virtualenv .venv
   
   # Option 2: If Python 3.11 is installed in default location
   python -m virtualenv .venv -p C:\Python311\python.exe
   
   .venv\Scripts\activate
   cd backend
   pip install -r requirements.txt
   ```

2. **Alternative: Install Build Tools (NOT recommended)**
   - Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
   - Install "Desktop development with C++" workload
   - Install [Rust](https://rustup.rs/) for pydantic-core
   - Restart your terminal and try again

### Issue: "command not found: python"

Try using `py` instead:
```powershell
py --version
py -m venv venv
```

Or specify Python 3.11 explicitly:
```powershell
py -3.11 -m venv venv
```

### Issue: Multiple Python versions installed

**Check all installed versions:**
```powershell
py -0  # Lists all Python versions
```

**Use a specific version:**
```powershell
py -3.11 -m venv venv  # Create venv with Python 3.11
```

### Issue: ModuleNotFoundError after installation

Make sure your virtual environment is activated:
```powershell
.\venv\Scripts\activate
```

You should see `(venv)` in your prompt.

### Issue: Port already in use

If port 8000 or 3000 is already in use:

**Find and kill the process:**
```powershell
# For port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# For port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Issue: Permission errors

Run PowerShell as Administrator:
1. Right-click on PowerShell icon
2. Select "Run as Administrator"
3. Navigate to the project directory and try again

## Testing Your Installation

Once the backend is running, test it:

```powershell
# Test health endpoint
curl http://localhost:8000/api/health

# Or visit in browser
start http://localhost:8000/docs
```

## Quick Command Reference

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Deactivate virtual environment
deactivate

# Install WebSocket server dependencies
pip install websockets msgpack

# Run WebSocket server
python realtime\ws_server.py

# Check Python version
python --version

# Update pip
python -m pip install --upgrade pip

# List installed packages
pip list

# Run tests
python test_backend.py
```

## Production Deployment on Windows

For production use on Windows:

1. **Use Python 3.11** (avoid compatibility issues)
2. **Install as Windows Service** using [NSSM](https://nssm.cc/)
3. **Use IIS or nginx** as reverse proxy
4. **Configure Windows Firewall** appropriately
5. **Use PM2 or NSSM** for process management
6. **Set up SSL/TLS** for secure connections

## Additional Resources

- [Main README](README.md)
- [Quick Start Guide](QUICKSTART.md)
- [DEX Source Configuration](DEX_SOURCE_GUIDE.md)
- [Python Download](https://www.python.org/downloads/)
- [Node.js Download](https://nodejs.org/)
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)

## Support

If you encounter issues not covered in this guide:
1. Check the [QUICKSTART.md](QUICKSTART.md) troubleshooting section
2. Review the [complete_documentation.md](complete_documentation.md)
3. Open an issue on GitHub with:
   - Your Python version (`python --version`)
   - Your Windows version
   - Complete error messages
   - Steps to reproduce the issue

---

**Note:** This system is designed for DeFi trading and requires careful configuration. Always test with small amounts on testnets before using real funds on mainnet.
