#!/bin/bash

# Script dừng Forward API Gateway

echo "🛑 Stopping Forward API Gateway..."

# Dừng service
docker-compose down

echo "✅ Service stopped successfully!"
echo "📝 To start again: ./start.sh" 