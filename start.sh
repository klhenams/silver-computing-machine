#!/bin/bash

# Support System Quick Start Script
echo "🚀 Starting Support System..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration (especially HUGGINGFACE_API_KEY for LLM features)"
fi

# Start the services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if API is responding
echo "🔍 Checking API health..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Support System is running successfully!"
    echo ""
    echo "🌐 Available endpoints:"
    echo "  - API Documentation: http://localhost/docs"
    echo "  - Health Check: http://localhost/health"
    echo "  - API Base URL: http://localhost/api/v1"
    echo ""
    echo "📚 Example API calls:"
    echo "  curl http://localhost/health"
    echo "  curl -X POST http://localhost/api/v1/documents/ -H 'Content-Type: application/json' -d '{\"title\":\"Test\",\"content\":\"Content\",\"category\":\"test\",\"tags\":[]}'"
    echo ""
    echo "🔧 To stop: docker-compose down"
    echo "📖 For more info, see README.md"
else
    echo "❌ API is not responding. Check logs with: docker-compose logs"
    exit 1
fi