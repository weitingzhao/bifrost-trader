#!/bin/bash
# Setup script for Bifrost Trader Knowledge Base

echo "🧠 Setting up Bifrost Trader Knowledge Base for Cursor AI..."

# Create knowledge-base directory if it doesn't exist
mkdir -p docs/knowledge-base

# Remove existing symlink if it exists
if [ -L "docs/knowledge-base" ]; then
    echo "Removing existing symlink..."
    rm docs/knowledge-base
fi

# Create symbolic link to documents directory
echo "Creating symbolic link to ~/Desktop/workspace/projects/documents..."
ln -sf /Users/vision-mac-trader/Desktop/workspace/projects/documents docs/knowledge-base

# Verify the symlink works
if [ -d "docs/knowledge-base" ]; then
    echo "✅ Knowledge base symlink created successfully!"
    echo "📁 Available knowledge files:"
    ls -la docs/knowledge-base/ | grep -E "\.md$"
    
    echo ""
    echo "🎯 How to use with Cursor AI:"
    echo "1. Reference specific files: 'Based on MICROSERVICES_IMPLEMENTATION_PLAN.md...'"
    echo "2. Ask context-aware questions: 'What's the recommended tech stack according to the architecture analysis?'"
    echo "3. Cross-reference information: 'How does the database setup relate to the microservices architecture?'"
    
    echo ""
    echo "📚 Knowledge base is now accessible to Cursor AI!"
else
    echo "❌ Failed to create knowledge base symlink"
    exit 1
fi
