@echo off
REM Immigration Guidance RAG System - Startup Script
REM This script activates the virtual environment and launches the Streamlit app

echo ================================================
echo Immigration Guidance RAG System
echo ================================================
echo.

REM Check if virtual environment exists
if not exist ".venv-1\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found at .venv-1
    echo Please create a virtual environment first:
    echo   python -m venv .venv-1
    echo   .venv-1\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [1/3] Activating virtual environment...
call .venv-1\Scripts\activate.bat

echo [2/3] Checking for required packages...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo WARNING: Streamlit not found. Installing dependencies...
    pip install -r requirements.txt
)

echo [3/3] Launching Streamlit app...
echo.
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
streamlit run app.py

pause
