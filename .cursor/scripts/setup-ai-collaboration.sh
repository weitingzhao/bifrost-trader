#!/bin/bash

# 🛠️ AI-Human Collaboration Setup Script for Bifrost Trader
# This script sets up the recommended tools and frameworks for effective AI collaboration

set -e

echo "🚀 Setting up AI-Human Collaboration Framework for Bifrost Trader..."

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
if [ ! -f "docs/knowledge-base/ARCHITECTURE_GUIDE.md" ]; then
    print_error "Please run this script from the Bifrost Trader project root directory"
    exit 1
fi

print_status "Setting up AI-Human Collaboration Framework..."

# 1. Setup Pre-commit Hooks
print_status "Setting up pre-commit hooks for code quality..."
if command -v pre-commit &> /dev/null; then
    print_success "Pre-commit is already installed"
else
    print_status "Installing pre-commit..."
    pip install pre-commit
fi

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3
        args: [--line-length=88]
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        args: [--profile=black]
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
  - repo: local
    hooks:
      - id: ai-code-quality
        name: AI Code Quality Check
        entry: python scripts/ai-quality-check.py
        language: system
        files: \.(py)$
        pass_filenames: true
EOF

print_success "Created .pre-commit-config.yaml"

# Install pre-commit hooks
pre-commit install
print_success "Installed pre-commit hooks"

# 2. Create AI Quality Check Script
print_status "Creating AI quality check script..."
mkdir -p scripts

cat > scripts/ai-quality-check.py << 'EOF'
#!/usr/bin/env python3
"""
AI Code Quality Check Script
Validates AI-generated code against project standards
"""

import sys
import ast
import re
from pathlib import Path
from typing import List, Dict, Any

class AICodeQualityChecker:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def check_file(self, file_path: str) -> bool:
        """Check a single Python file for quality issues"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Run checks
            self._check_imports(tree)
            self._check_functions(tree)
            self._check_classes(tree)
            self._check_docstrings(tree)
            self._check_type_hints(tree)
            
            return len(self.errors) == 0
            
        except SyntaxError as e:
            self.errors.append(f"Syntax error in {file_path}: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error checking {file_path}: {e}")
            return False
    
    def _check_imports(self, tree: ast.AST):
        """Check import statements"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith('shared.'):
                        continue  # Allow shared imports
                    if not self._is_standard_import(alias.name):
                        self.warnings.append(f"Non-standard import: {alias.name}")
    
    def _check_functions(self, tree: ast.AST):
        """Check function definitions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for type hints
                if not node.returns and node.name != '__init__':
                    self.warnings.append(f"Function {node.name} missing return type hint")
                
                # Check for docstrings
                if not ast.get_docstring(node):
                    self.warnings.append(f"Function {node.name} missing docstring")
    
    def _check_classes(self, tree: ast.AST):
        """Check class definitions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check for docstrings
                if not ast.get_docstring(node):
                    self.warnings.append(f"Class {node.name} missing docstring")
    
    def _check_docstrings(self, tree: ast.AST):
        """Check docstring quality"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                if docstring and len(docstring) < 10:
                    self.warnings.append(f"{type(node).__name__} {node.name} has short docstring")
    
    def _check_type_hints(self, tree: ast.AST):
        """Check type hint usage"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    if arg.annotation is None and arg.arg != 'self':
                        self.warnings.append(f"Function {node.name} argument {arg.arg} missing type hint")
    
    def _is_standard_import(self, module_name: str) -> bool:
        """Check if import is from standard library or common packages"""
        standard_modules = {
            'typing', 'collections', 'datetime', 'json', 'os', 'sys',
            'pathlib', 'logging', 'asyncio', 'contextlib', 'functools',
            'fastapi', 'pydantic', 'sqlalchemy', 'pytest'
        }
        return module_name.split('.')[0] in standard_modules
    
    def print_results(self):
        """Print check results"""
        if self.errors:
            print("❌ Errors found:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("⚠️  Warnings found:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            print("✅ No quality issues found")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python ai-quality-check.py <file1> [file2] ...")
        sys.exit(1)
    
    checker = AICodeQualityChecker()
    all_passed = True
    
    for file_path in sys.argv[1:]:
        print(f"Checking {file_path}...")
        if not checker.check_file(file_path):
            all_passed = False
    
    checker.print_results()
    
    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

chmod +x scripts/ai-quality-check.py
print_success "Created AI quality check script"

# 3. Create Knowledge Sync Script
print_status "Creating knowledge sync script..."

cat > scripts/knowledge-sync.py << 'EOF'
#!/usr/bin/env python3
"""
Knowledge Base Synchronization Script
Keeps knowledge base files in sync and validates consistency
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set
from datetime import datetime

class KnowledgeSync:
    def __init__(self):
        self.knowledge_base_path = Path("docs/knowledge-base")
        self.source_path = Path("/Users/vision-mac-trader/Desktop/workspace/projects/documents")
        self.issues: List[str] = []
    
    def sync_knowledge_base(self):
        """Sync knowledge base files"""
        print("🔄 Syncing knowledge base...")
        
        # Check if source directory exists
        if not self.source_path.exists():
            print(f"⚠️  Source directory {self.source_path} does not exist")
            return
        
        # List files in source directory
        source_files = list(self.source_path.glob("*.md"))
        knowledge_files = list(self.knowledge_base_path.glob("*.md"))
        
        print(f"📁 Found {len(source_files)} files in source directory")
        print(f"📁 Found {len(knowledge_files)} files in knowledge base")
        
        # Check for missing files
        self._check_missing_files(source_files, knowledge_files)
        
        # Check for consistency
        self._check_consistency()
        
        # Generate report
        self._generate_report()
    
    def _check_missing_files(self, source_files: List[Path], knowledge_files: List[Path]):
        """Check for missing files"""
        source_names = {f.name for f in source_files}
        knowledge_names = {f.name for f in knowledge_files}
        
        missing_in_kb = source_names - knowledge_names
        if missing_in_kb:
            self.issues.append(f"Missing files in knowledge base: {missing_in_kb}")
        
        extra_in_kb = knowledge_names - source_names
        if extra_in_kb:
            self.issues.append(f"Extra files in knowledge base: {extra_in_kb}")
    
    def _check_consistency(self):
        """Check consistency of knowledge base files"""
        readme_path = self.knowledge_base_path / "README.md"
        if not readme_path.exists():
            self.issues.append("README.md missing in knowledge base")
            return
        
        # Read README content
        with open(readme_path, 'r') as f:
            readme_content = f.read()
        
        # Check for references to all knowledge files
        knowledge_files = list(self.knowledge_base_path.glob("*.md"))
        for file_path in knowledge_files:
            if file_path.name == "README.md":
                continue
            
            file_name = file_path.name
            if file_name not in readme_content:
                self.issues.append(f"README.md missing reference to {file_name}")
    
    def _generate_report(self):
        """Generate sync report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n📊 Knowledge Base Sync Report - {timestamp}")
        print("=" * 50)
        
        if self.issues:
            print("❌ Issues found:")
            for issue in self.issues:
                print(f"  - {issue}")
        else:
            print("✅ Knowledge base is in sync")
        
        print("=" * 50)

def main():
    """Main function"""
    sync = KnowledgeSync()
    sync.sync_knowledge_base()

if __name__ == "__main__":
    main()
EOF

chmod +x scripts/knowledge-sync.py
print_success "Created knowledge sync script"

# 4. Create GitHub Actions Workflow
print_status "Creating GitHub Actions workflow for AI collaboration..."

mkdir -p .github/workflows

cat > .github/workflows/ai-collaboration.yml << 'EOF'
name: AI Collaboration Quality Check

on:
  pull_request:
    types: [opened, synchronize]
  push:
    branches: [main]

jobs:
  ai-quality-check:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install black isort flake8 mypy
      
      - name: Run AI Quality Check
        run: |
          python scripts/ai-quality-check.py $(find . -name "*.py" -not -path "./venv/*" -not -path "./.git/*")
      
      - name: Run Knowledge Sync Check
        run: |
          python scripts/knowledge-sync.py
      
      - name: Check Code Formatting
        run: |
          black --check .
          isort --check-only .
      
      - name: Run Linting
        run: |
          flake8 .
      
      - name: Run Type Checking
        run: |
          mypy . --ignore-missing-imports

  knowledge-base-check:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Check Knowledge Base Consistency
        run: |
          python scripts/knowledge-sync.py
      
      - name: Validate Documentation
        run: |
          # Check if all knowledge base files exist
          test -f docs/knowledge-base/ARCHITECTURE_GUIDE.md
          test -f docs/knowledge-base/REFACTORING_GUIDE.md
          test -f docs/knowledge-base/DATABASE_REFERENCE.md
          test -f docs/knowledge-base/BACKTRADER_SERVICE_PLAN.md
          test -f docs/knowledge-base/PORTAL_DESIGN_PLAN.md
          test -f docs/knowledge-base/README.md
EOF

print_success "Created GitHub Actions workflow"

# 5. Create Development Environment Setup
print_status "Creating development environment setup..."

cat > scripts/setup-dev-environment.sh << 'EOF'
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
EOF

chmod +x scripts/setup-dev-environment.sh
print_success "Created development environment setup script"

# 6. Create AI Prompt Templates
print_status "Creating AI prompt templates..."

mkdir -p ai-prompts/templates

cat > ai-prompts/templates/service-creation.md << 'EOF'
# Service Creation Prompt Template

## Context
Based on ARCHITECTURE_GUIDE.md, create a new [SERVICE_NAME] microservice that:

## Requirements
1. Follows the microservices patterns defined in REFACTORING_GUIDE.md
2. Uses FastAPI framework with proper structure
3. Implements database models from DATABASE_REFERENCE.md
4. Includes proper error handling and logging
5. Has comprehensive tests (>90% coverage)
6. Follows the service boundaries defined in the architecture

## Service Details
- **Service Name**: [SERVICE_NAME]
- **Port**: [PORT_NUMBER]
- **Functionality**: [SPECIFIC_FUNCTIONALITY]
- **Database Tables**: [RELEVANT_TABLES]
- **Dependencies**: [OTHER_SERVICES]

## Deliverables
Please create:
- Main FastAPI application with lifespan context manager
- Database models using SQLAlchemy
- API endpoints with proper validation
- Service logic with business rules
- Comprehensive tests (unit and integration)
- Documentation and README

## Quality Requirements
- Follows .cursorrules coding standards
- Uses proper type hints and Pydantic models
- Implements async patterns for I/O operations
- Includes proper error handling and logging
- Maintains service boundaries and contracts
EOF

cat > ai-prompts/templates/api-endpoints.md << 'EOF'
# API Endpoints Creation Prompt Template

## Context
Create API endpoints for [SERVICE_NAME] that follow project standards and patterns.

## Requirements
1. Follow the patterns in ARCHITECTURE_GUIDE.md
2. Use database models from DATABASE_REFERENCE.md
3. Implement proper validation with Pydantic v2
4. Include comprehensive error handling and logging
5. Follow RESTful conventions
6. Include comprehensive tests

## Endpoint Specifications
- **Service**: [SERVICE_NAME]
- **Endpoints**: [LIST_ENDPOINTS]
- **Database Operations**: [LIST_OPERATIONS]
- **Authentication**: [AUTH_REQUIREMENTS]
- **Rate Limiting**: [RATE_LIMITING]

## Code Requirements
- Use FastAPI with proper dependency injection
- Implement proper HTTP status codes
- Include comprehensive docstrings
- Use async patterns for database operations
- Follow error handling patterns from existing services
- Include input validation and sanitization

## Reference Implementation
Reference the existing [SIMILAR_SERVICE] for patterns and structure.
EOF

print_success "Created AI prompt templates"

# 7. Create Monitoring Setup
print_status "Creating monitoring setup..."

cat > docker-compose-monitoring.yml << 'EOF'
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: bifrost-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: bifrost-grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    networks:
      - monitoring

  redis-exporter:
    image: oliver006/redis_exporter:latest
    container_name: bifrost-redis-exporter
    ports:
      - "9121:9121"
    environment:
      - REDIS_ADDR=redis://redis:6379
    networks:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:

networks:
  monitoring:
    driver: bridge
EOF

mkdir -p monitoring/grafana/dashboards monitoring/grafana/provisioning

cat > monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'bifrost-services'
    static_configs:
      - targets: 
        - 'api-gateway:8000'
        - 'data-service:8001'
        - 'portfolio-service:8002'
        - 'strategy-service:8003'
        - 'execution-service:8004'
        - 'risk-service:8005'
        - 'web-portal:8006'
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
EOF

print_success "Created monitoring setup"

# 8. Create Final Summary
print_status "Creating setup summary..."

cat > docs/AI_COLLABORATION_SETUP_COMPLETE.md << 'EOF'
# 🎉 AI Collaboration Setup Complete!

## ✅ **What Was Installed**

### **Code Quality Tools**
- **Pre-commit Hooks**: Automated code formatting and linting
- **AI Quality Check Script**: Validates AI-generated code
- **GitHub Actions**: Automated quality checks on PR/push

### **Knowledge Management**
- **Knowledge Sync Script**: Keeps knowledge base synchronized
- **AI Prompt Templates**: Reusable prompts for common tasks
- **Development Environment Setup**: Complete dev environment

### **Monitoring & Analytics**
- **Prometheus + Grafana**: Application monitoring
- **Redis Exporter**: Redis monitoring
- **Custom Dashboards**: Service-specific monitoring

## 🚀 **How to Use**

### **Daily Development Workflow**
1. **Morning**: Run `python scripts/knowledge-sync.py` to sync knowledge
2. **Development**: Use AI prompts from `ai-prompts/templates/`
3. **Code Review**: Pre-commit hooks run automatically
4. **Evening**: Update knowledge base with new patterns

### **AI Collaboration Best Practices**
1. **Context-Aware Prompts**: Always reference knowledge base files
2. **Quality Gates**: All AI code must pass quality checks
3. **Knowledge Updates**: Keep documentation current
4. **Pattern Recognition**: Document recurring patterns

### **Monitoring & Analytics**
1. **Start Monitoring**: `docker-compose -f docker-compose-monitoring.yml up -d`
2. **View Metrics**: http://localhost:9090 (Prometheus)
3. **View Dashboards**: http://localhost:3000 (Grafana)
4. **Monitor Services**: Check service health and performance

## 🎯 **Success Metrics**

### **Code Quality**
- ✅ Automated code formatting and linting
- ✅ AI-generated code validation
- ✅ Comprehensive test coverage
- ✅ Type checking and validation

### **Knowledge Management**
- ✅ Synchronized knowledge base
- ✅ Consistent documentation
- ✅ Reusable prompt templates
- ✅ Pattern documentation

### **Team Collaboration**
- ✅ Clear AI interaction guidelines
- ✅ Quality gates and reviews
- ✅ Automated monitoring
- ✅ Continuous improvement

## 🔄 **Next Steps**

1. **Start Development**: Use the enhanced AI collaboration framework
2. **Monitor Quality**: Track code quality metrics
3. **Update Knowledge**: Keep knowledge base current
4. **Improve Prompts**: Refine AI prompts based on results
5. **Scale Framework**: Extend tools as project grows

---

**🎯 Your AI collaboration framework is now complete and ready for productive development!**
EOF

print_success "Created setup summary"

# Final summary
print_success "🎉 AI-Human Collaboration Framework Setup Complete!"
echo ""
echo "📋 What was installed:"
echo "  ✅ Pre-commit hooks for code quality"
echo "  ✅ AI quality check script"
echo "  ✅ Knowledge sync script"
echo "  ✅ GitHub Actions workflow"
echo "  ✅ Development environment setup"
echo "  ✅ AI prompt templates"
echo "  ✅ Monitoring and analytics setup"
echo ""
echo "🚀 Next steps:"
echo "  1. Run: python scripts/knowledge-sync.py"
echo "  2. Run: ./scripts/setup-dev-environment.sh"
echo "  3. Start developing with enhanced AI collaboration!"
echo ""
echo "📚 Documentation:"
echo "  - docs/AI_COLLABORATION_FRAMEWORK.md"
echo "  - docs/AI_COLLABORATION_TOOLS.md"
echo "  - docs/AI_COLLABORATION_SETUP_COMPLETE.md"
echo ""
print_success "Setup complete! Happy coding with AI! 🤖✨"
