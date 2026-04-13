#!/bin/bash
# md-skill-craft automated setup script (macOS/Linux)

set -e

echo "╭─────────────────────────────────────╮"
echo "│   md-skill-craft Setup Script       │"
echo "╰─────────────────────────────────────╯"
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found"
    echo "Install: brew install python3  (macOS)"
    echo "       or apt-get install python3  (Linux)"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $PYTHON_VERSION found"

if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)'; then
    echo "ERROR: Python 3.12+ required"
    exit 1
fi
echo "✓ Python 3.12+ confirmed"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Install package
echo "Installing md-skill-craft..."
pip install -e . > /dev/null 2>&1
echo "✓ Installation complete"
echo ""

# Verify installation
echo "Verifying installation..."
if command -v md-skill-craft &> /dev/null; then
    echo "✓ md-skill-craft command ready"
else
    echo "! Command not found. Reactivate: source .venv/bin/activate"
fi
echo ""

echo "╭─────────────────────────────────────╮"
echo "│   ✓ Setup Complete!                │"
echo "╰─────────────────────────────────────╯"
echo ""
echo "Next steps:"
echo "  1. Activate environment:"
echo "     source .venv/bin/activate"
echo ""
echo "  2. Install your LLM provider:"
echo "     pip install -e '.[claude]'    (Claude)"
echo "     pip install -e '.[openai]'    (OpenAI)"
echo "     pip install -e '.[gemini]'    (Gemini)"
echo "     pip install -e '.[all]'       (All LLMs)"
echo ""
echo "  3. Run the application:"
echo "     md-skill-craft"
echo ""
