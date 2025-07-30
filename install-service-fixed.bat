@echo off
echo Installing Forward API Gateway as Windows Service...
sc create "ForwardAPI" binPath="%~dp0forward-api-gateway.exe" start=auto
sc description "ForwardAPI" "Forward API Gateway Service"
echo Service installed. To start: sc start ForwardAPI
pause 