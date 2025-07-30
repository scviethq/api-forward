@echo off
echo ========================================
echo Forward API Gateway - Service Uninstaller
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
echo Stopping Forward API Gateway Service...
sc stop ForwardAPI
if %errorlevel% neq 0 (
    echo Service is not running or does not exist.
)

echo.
echo Removing Forward API Gateway Service...
sc delete ForwardAPI
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to remove service!
    echo Make sure you are running as Administrator.
    echo.
    pause
    exit /b 1
)

echo.
echo Service removed successfully!
echo.
pause 