#!/bin/bash

# Script build Windows executable từ macOS

echo "🍎 Building Windows executable from macOS..."

# Kiểm tra Wine
if ! command -v wine &> /dev/null; then
    echo "❌ Wine not found. Installing..."
    brew install wine
fi

# Kiểm tra PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Tạo thư mục build
mkdir -p build/windows

echo "🔨 Building with PyInstaller..."

# Build với spec file
pyinstaller build-windows.spec --distpath build/windows

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    # Copy config và docs
    cp config.yaml build/windows/
    cp README.md build/windows/
    
    # Tạo script start cho Windows
    cat > build/windows/start.bat << 'EOF'
@echo off
echo Starting Forward API Gateway...
forward-api-gateway.exe
pause
EOF
    
    # Tạo script install service
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
    echo "🚀 To deploy on Windows Server 2012 R2:"
    echo "1. Copy build/windows/ folder to Windows server"
    echo "2. Edit config.yaml if needed"
    echo "3. Run start.bat or install as service"
    
else
    echo "❌ Build failed!"
    exit 1
fi 