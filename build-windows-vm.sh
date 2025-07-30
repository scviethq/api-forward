#!/bin/bash

# Script để build Windows executable trên Windows VM
# Chạy script này trên Windows machine

echo "🪟 Building Windows executable on Windows VM..."

# Kiểm tra Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

# Kiểm tra PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Installing PyInstaller..."
    pip install pyinstaller
fi

# Tạo thư mục build
mkdir -p build/windows

echo "🔨 Building with PyInstaller..."

# Build executable
pyinstaller --onefile --console --name forward-api-gateway app/main.py --add-data "config.yaml;." --add-data "app;app"

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    # Copy files
    cp dist/forward-api-gateway.exe build/windows/
    cp config.yaml build/windows/
    cp README.md build/windows/
    
    # Tạo start script
    cat > build/windows/start.bat << 'EOF'
@echo off
echo Starting Forward API Gateway...
forward-api-gateway.exe
pause
EOF
    
    # Tạo service installer
    cat > build/windows/install-service.bat << 'EOF'
@echo off
echo Installing Forward API Gateway as Windows Service...
sc create "ForwardAPI" binPath="%~dp0forward-api-gateway.exe" start=auto
sc description "ForwardAPI" "Forward API Gateway Service"
echo Service installed. To start: sc start ForwardAPI
pause
EOF
    
    echo "📦 Windows package created in build/windows/"
    echo "📁 Contents:"
    ls -la build/windows/
    
    echo ""
    echo "🚀 Ready for deployment on Windows Server 2012 R2!"
    
else
    echo "❌ Build failed!"
    exit 1
fi 