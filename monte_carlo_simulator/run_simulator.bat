@echo off
REM Startup script for DAS Monte Carlo Simulator (Windows)

echo.
echo DAS Maritime Surveillance - Monte Carlo Simulator
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Python found
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo Dependencies installed
echo.

REM Run the service
echo Starting web service...
echo Open your browser to: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python api_service.py

pause
