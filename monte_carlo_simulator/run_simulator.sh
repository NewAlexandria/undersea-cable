#!/bin/bash
# Startup script for DAS Monte Carlo Simulator

echo "🌊 DAS Maritime Surveillance - Monte Carlo Simulator"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Run the service
echo "🚀 Starting web service..."
echo "📍 Open your browser to: http://localhost:8000"
echo "⌨️  Press Ctrl+C to stop the server"
echo ""

python3 api_service.py
