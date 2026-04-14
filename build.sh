#!/bin/bash
# Docker Build Verification Script

echo "🐳 Docker Build Verification"
echo "============================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    exit 1
fi

echo "✅ Docker installed: $(docker --version)"
echo ""

# Build the image
echo "🔨 Building Docker image..."
echo "Command: docker build -t emotion-detection:latest ."
echo ""

docker build -t emotion-detection:latest . 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📊 Image information:"
    docker images emotion-detection:latest
    echo ""
    
    # Get image size
    SIZE=$(docker images emotion-detection:latest --format "{{.Size}}")
    echo "📦 Image size: $SIZE"
    echo ""
    
    echo "🚀 Ready to deploy!"
    echo ""
    echo "Run commands:"
    echo "  docker run -p 8000:8000 emotion-detection:latest"
    echo "  docker-compose up -d"
else
    echo ""
    echo "❌ Build failed!"
    echo "Check the error messages above."
    exit 1
fi
