#!/bin/bash

echo "=== RONGGO PROJECT SETUP START ==="

# 1. Install Dependencies
echo "[1/3] Installing Python Dependencies..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully."
else
    echo "Error installing dependencies!"
    exit 1
fi

# 2. Check GPU
echo "[2/3] Checking GPU Status..."
python3 -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}'); print(f'Device Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"

# 3. Environment Summary
echo "[3/3] Setup Complete."
echo "Current Directory: $(pwd)"
echo "You can now run experiments."
echo "=================================="
