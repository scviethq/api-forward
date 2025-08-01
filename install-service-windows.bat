@echo off
echo ========================================
echo Forward API Gateway - Service Installer
echo ========================================
echo.
echo IMPORTANT: This script requires Administrator privileges!
echo.
echo To run as Administrator:
echo 1. Right-click on this file
echo 2. Select "Run as administrator"
echo 3. Click "Yes" when prompted
echo.
echo Press any key to continue...
pause >nul

echo.
echo Installing Forward API Gateway as Windows Service...
sc create "ForwardAPI" binPath="%~dp0forward-api-gateway.exe" start=auto
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to create service!
    echo Make sure you are running as Administrator.
    echo.
    pause
    exit /b 1
)

sc description "ForwardAPI" "Forward API Gateway Service"
echo.
echo Service installed successfully!
echo.
echo To manage the service:
echo - Start:   sc start ForwardAPI
echo - Stop:    sc stop ForwardAPI
echo - Status:  sc query ForwardAPI
echo - Remove:  sc delete ForwardAPI
echo.
pause 