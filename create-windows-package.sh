#!/bin/bash

echo "📦 Creating Windows deployment package..."

# Tạo thư mục package
mkdir -p windows-package

# Copy files cần thiết
cp config.yaml windows-package/
cp README.md windows-package/

# Tạo start script cho Windows
cat > windows-package/start.bat << 'EOF'
@echo off
echo Starting Forward API Gateway...
python app/main.py
pause
EOF

# Tạo install script
cat > windows-package/install.bat << 'EOF'
@echo off
echo Installing Python dependencies...
pip install fastapi uvicorn loguru pyyaml httpx pydantic
echo Installation completed!
pause
EOF

# Tạo service install script
cat > windows-package/install-service.bat << 'EOF'
@echo off
echo Installing Forward API Gateway as Windows Service...
sc create "ForwardAPI" binPath="%~dp0python.exe %~dp0app\main.py" start=auto
sc description "ForwardAPI" "Forward API Gateway Service"
echo Service installed. To start: sc start ForwardAPI
pause
EOF

# Copy app directory
cp -r app windows-package/

echo "✅ Windows package created in windows-package/"
echo "📁 Contents:"
ls -la windows-package/

echo ""
echo "🚀 To deploy on Windows:"
echo "1. Copy windows-package/ to Windows server"
echo "2. Install Python 3.11+ on Windows"
echo "3. Run install.bat to install dependencies"
echo "4. Run start.bat to start the service"
echo "5. Or run install-service.bat to install as Windows service" 