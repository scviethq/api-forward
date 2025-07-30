#!/bin/bash

echo "🔨 Building Forward API Gateway locally..."

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Kiểm tra dependencies
echo "📦 Checking dependencies..."
python3 -c "import fastapi, uvicorn, loguru, yaml, httpx, pydantic; print('✅ All dependencies OK')"

# Test import
echo "🧪 Testing imports..."
python3 -c "import app.main; print('✅ Main module OK')"
python3 -c "from app.config import config; print('✅ Config loaded, routes:', len(config.routes))"

# Cài PyInstaller nếu chưa có
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Build
echo "🔨 Building executable..."
pyinstaller --onefile --console app/main.py --name forward-api-gateway

# Kiểm tra kết quả
if [ -f "dist/forward-api-gateway" ]; then
    echo "✅ Build successful!"
    echo "📁 Executable: dist/forward-api-gateway"
    ls -la dist/forward-api-gateway
else
    echo "❌ Build failed!"
    exit 1
fi 