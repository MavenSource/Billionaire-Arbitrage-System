@echo off
REM Install required Python dependencies for BillionaireBot
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo Installation complete.