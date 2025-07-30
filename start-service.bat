@echo off
echo Starting Forward API Gateway as Background Service...
echo Service will run in background. Check logs for status.
echo.
start /B forward-api-gateway.exe
echo Service started in background.
echo To stop: taskkill /F /IM forward-api-gateway.exe
pause 