#!/bin/bash

# 🚀 MkDocs Knowledge Base Server Script for Bifrost Trader
# This script builds and serves the MkDocs knowledge base

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "mkdocs.yml" ]; then
    print_error "Please run this script from the Bifrost Trader project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found. Please run ./scripts/setup-dev-environment.sh first"
    exit 1
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Check if MkDocs is installed
if ! command -v mkdocs &> /dev/null; then
    print_error "MkDocs not found. Please install it first:"
    echo "pip install mkdocs mkdocs-material mkdocs-mermaid2-plugin"
    exit 1
fi

print_success "MkDocs is available"

# Function to serve the site
serve_site() {
    print_status "Starting MkDocs development server..."
    print_status "The knowledge base will be available at: http://localhost:8000"
    print_status "Press Ctrl+C to stop the server"
    echo ""
    
    mkdocs serve --dev-addr=0.0.0.0:8000
}

# Function to build the site
build_site() {
    print_status "Building MkDocs site..."
    mkdocs build
    print_success "Site built successfully in 'site/' directory"
}

# Function to deploy to GitHub Pages
deploy_site() {
    print_status "Deploying to GitHub Pages..."
    mkdocs gh-deploy
    print_success "Site deployed to GitHub Pages"
}

# Function to show help
show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  serve    Start the development server (default)"
    echo "  build    Build the static site"
    echo "  deploy   Deploy to GitHub Pages"
    echo "  help     Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 serve    # Start development server"
    echo "  $0 build    # Build static site"
    echo "  $0 deploy   # Deploy to GitHub Pages"
}

# Main script logic
case "${1:-serve}" in
    "serve")
        serve_site
        ;;
    "build")
        build_site
        ;;
    "deploy")
        deploy_site
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
