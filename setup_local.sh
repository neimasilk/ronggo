#!/bin/bash

echo "=== RONGGO PROJECT: LOCAL SETUP ==="

# 1. Create Virtual Environment if not exists
if [ ! -d ".venv" ]; then
    echo "[1/3] Creating Virtual Environment (.venv)..."
    python3 -m venv .venv
else
    echo "[1/3] Virtual Environment already exists."
fi

# 2. Install Dependencies
echo "[2/3] Installing Dependencies..."
# We use the python binary inside the venv directly to avoid activation issues in script
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

# 3. Create .env template if not exists
if [ ! -f ".env" ]; then
    echo "GEMINI_API_KEY=your_key_here" > .env
    echo "DEEPSEEK_API_KEY=your_key_here" >> .env
    echo "[INFO] Created template .env file. Please edit it with your keys."
fi

echo "[3/3] Setup Complete!"
echo "To start working, run:"
echo "  source .venv/bin/activate"
