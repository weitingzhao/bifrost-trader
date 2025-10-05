#!/bin/bash

# Development Environment Setup for Bifrost Trader
# Sets up the complete development environment for AI collaboration

set -e

echo "🚀 Setting up Bifrost Trader Development Environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
if [[ $(echo "$python_version < 3.9" | bc -l) -eq 1 ]]; then
    echo "❌ Python 3.9+ required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install development dependencies
echo "📦 Installing development dependencies..."
pip install black isort flake8 mypy pytest pre-commit

# Setup pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
pre-commit install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp env.example .env
    echo "⚠️  Please update .env file with your configuration"
fi

# Setup database
echo "🗄️ Setting up database..."
if command -v docker &> /dev/null; then
    echo "🐳 Starting database services..."
    docker-compose -f docker-compose-db.yml up -d
    echo "⏳ Waiting for database to be ready..."
    sleep 10
else
    echo "⚠️  Docker not found. Please install Docker to run database services"
fi

# Run knowledge sync
echo "🔄 Syncing knowledge base..."
python scripts/knowledge-sync.py

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Update .env file with your configuration"
echo "2. Run 'source venv/bin/activate' to activate virtual environment"
echo "3. Start developing with AI collaboration tools!"
