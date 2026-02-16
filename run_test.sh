#!/bin/bash
# Quick test runner for FixBrain Phase 1

set -e

echo "🤖 FixBrain Phase 1 - Quick Test Runner"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Must run from fixbrain directory"
    exit 1
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found"
    echo "   Please create one with: OPENAI_API_KEY=your-key-here"
    echo "   Or export it: export OPENAI_API_KEY=your-key"
    echo ""
    read -p "   Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run the test
echo ""
echo "🧪 Running Phase 1 test suite..."
echo "========================================"
python tests/test_real.py

echo ""
echo "✅ Test complete!"
