#!/bin/bash

# Script khởi động Forward API Gateway

echo "🚀 Starting Forward API Gateway..."

# Kiểm tra Docker có chạy không
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Kiểm tra file config
if [ ! -f "config.yaml" ]; then
    echo "❌ config.yaml not found. Please create config.yaml first."
    exit 1
fi

# Pull image mới nhất (optional)
echo "📥 Pulling latest image..."
docker pull buzzhoang/forward-api:latest

# Tạo thư mục logs nếu chưa có
mkdir -p logs

# Khởi động service
echo "🔄 Starting service..."
docker-compose up -d

# Kiểm tra status
echo "⏳ Waiting for service to start..."
sleep 5

# Health check
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Service started successfully!"
    echo "📊 Health check: http://localhost:8000/health"
    echo "📋 API docs: http://localhost:8000/docs"
    echo "📝 Logs: docker-compose logs -f forward-api"
else
    echo "❌ Service failed to start. Check logs:"
    docker-compose logs forward-api
    exit 1
fi 