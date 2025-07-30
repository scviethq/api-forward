#!/bin/bash

# Script để build và push Docker image lên Docker Hub

# Configuration
DOCKER_USERNAME="your-username"
IMAGE_NAME="forward-api"
VERSION=${1:-latest}

echo "🐳 Building Docker image..."

# Build image
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$VERSION .

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    # Tag as latest if not already
    if [ "$VERSION" != "latest" ]; then
        docker tag $DOCKER_USERNAME/$IMAGE_NAME:$VERSION $DOCKER_USERNAME/$IMAGE_NAME:latest
    fi
    
    echo "📤 Pushing to Docker Hub..."
    
    # Push to Docker Hub
    docker push $DOCKER_USERNAME/$IMAGE_NAME:$VERSION
    
    if [ [ "$VERSION" != "latest" ]; then
        docker push $DOCKER_USERNAME/$IMAGE_NAME:latest
    fi
    
    echo "🎉 Successfully pushed $DOCKER_USERNAME/$IMAGE_NAME:$VERSION to Docker Hub!"
    echo "📋 Usage:"
    echo "  docker pull $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
    echo "  docker run -p 8000:8000 $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
    
else
    echo "❌ Build failed!"
    exit 1
fi 