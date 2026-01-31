#!/bin/bash
# Immigration Guidance RAG System - Startup Script (Unix/Mac)
# This script activates the virtual environment and launches the Streamlit app

echo "================================================"
echo "Immigration Guidance RAG System"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv-1" ]; then
    echo "ERROR: Virtual environment not found at .venv-1"
    echo "Please create a virtual environment first:"
    echo "  python -m venv .venv-1"
    echo "  source .venv-1/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 1
fi

echo "[1/3] Activating virtual environment..."
source .venv-1/bin/activate

echo "[2/3] Checking for required packages..."
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

echo "[3/3] Launching Streamlit app..."
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""
streamlit run app.py
