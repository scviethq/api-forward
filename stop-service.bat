@echo off
echo Stopping Forward API Gateway...
taskkill /F /IM forward-api-gateway.exe
echo Service stopped.
pause 