# 🤖 AI Tools & Frameworks Reference

This document provides a comprehensive reference for all AI agent-related tools and frameworks utilized in the Bifrost Trader project.

## 📊 **Overview**

The Bifrost Trader project utilizes **8 major AI tools and frameworks** to create a comprehensive AI-assisted development ecosystem:

1. **Cursor AI Rules** - Project-specific AI behavior configuration
2. **AI Prompts Framework** - Structured prompt templates
3. **Code Templates** - Reusable code patterns
4. **MkDocs Documentation** - AI-accessible knowledge base
5. **AI Quality Check Script** - Code quality validation
6. **AI Collaboration Setup** - Automated framework setup
7. **GitHub Actions AI Workflow** - CI/CD integration
8. **AI Documentation** - Comprehensive collaboration guide

---

## 🎯 **1. Cursor AI Rules (`.cursorrules`)**

### **Purpose**
Defines behavior and constraints for Cursor AI to ensure consistent, project-specific responses.

### **Key Features**
- **Project Context**: Microservices architecture, FastAPI, PostgreSQL
- **Coding Standards**: Python/FastAPI best practices, type hints, async patterns
- **Knowledge Base Integration**: References to architecture and design guides
- **Quality Gates**: Error handling, testing, documentation requirements

### **How to Use**
```bash
# Automatic - Cursor AI reads this file automatically
# No manual action needed
# File location: .cursorrules (184 lines)
```

### **Benefits**
- **Consistent AI Behavior**: Ensures AI follows project standards
- **Context Awareness**: AI understands project architecture
- **Quality Standards**: Enforces coding best practices

---

## 🎯 **2. AI Prompts Framework (`ai-prompts/`)**

### **Purpose**
Provides structured prompt templates for consistent AI interactions and reproducible results.

### **Structure**
```
ai-prompts/
├── README.md                    # Framework overview
└── templates/
    ├── service-creation.md      # Microservice creation prompts
    └── api-endpoints.md         # API endpoint development prompts
```

### **Key Features**
- **Service Creation Prompts**: Templates for creating new microservices
- **API Endpoint Prompts**: Templates for API development
- **Database Operation Prompts**: Templates for database tasks
- **Test Generation Prompts**: Templates for test creation

### **How to Use**
```bash
# 1. Copy template from ai-prompts/templates/
cat ai-prompts/templates/service-creation.md

# 2. Customize with your specific requirements
# Example: Create a new portfolio service
# Replace [SERVICE_NAME] with "Portfolio"
# Replace [PORT_NUMBER] with "8002"
# Replace [SPECIFIC_FUNCTIONALITY] with "portfolio management"

# 3. Use with Cursor AI for consistent results
```

### **Example Usage**
```markdown
Based on ARCHITECTURE_GUIDE.md, create a new Portfolio microservice that:
1. Follows the microservices patterns defined in REFACTORING_GUIDE.md
2. Uses FastAPI framework with proper structure
3. Implements database models from DATABASE_REFERENCE.md
4. Includes proper error handling and logging
5. Has comprehensive tests
6. Follows the service boundaries defined in the architecture

Service should handle: portfolio management and tracking
Port: 8002
Database tables: portfolio, holding, transaction, cash_balance
```

---

## 🎯 **3. Code Templates (`code-templates/`)**

### **Purpose**
Provides reusable code templates for consistent development patterns and rapid prototyping.

### **Structure**
```
code-templates/
├── README.md                    # Template overview
├── microservice/               # Complete FastAPI service structure
├── api-endpoints/              # RESTful endpoint patterns
└── database-models/            # SQLAlchemy model patterns
```

### **Key Features**
- **Microservice Templates**: Complete FastAPI service structure
- **API Endpoint Templates**: RESTful endpoint patterns
- **Database Model Templates**: SQLAlchemy model patterns
- **Test Templates**: Comprehensive test structures

### **How to Use**
```bash
# 1. Copy template to create new service
cp -r code-templates/microservice/ services/new-service/

# 2. Customize the templates
# Replace placeholders with your specific requirements
# Update service names, ports, and functionality

# 3. Follow the patterns for consistent code structure
```

### **Template Structure**
```python
# Example: main.py template
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .api.dependencies import get_database
from .api.endpoints import [resource]
from .services.[service]_service import [Service]Service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting [Service Name] Service")
    yield
    # Shutdown
    logger.info("Shutting down [Service Name] Service")

app = FastAPI(
    title="[Service Name] Service",
    description="[Service description]",
    version="1.0.0",
    lifespan=lifespan
)
```

---

## 🎯 **4. MkDocs Documentation (`mkdocs.yml`)**

### **Purpose**
Provides AI-accessible documentation system with search functionality and live reload.

### **Status**
- **Running**: ✅ http://127.0.0.1:8001
- **Theme**: Material (modern, responsive)
- **Features**: Search, live reload, mobile responsive

### **Key Features**
- **Material Theme**: Modern, responsive design
- **Search Functionality**: Built-in search across all documentation
- **Live Reload**: Automatic updates on file changes
- **AI Reference**: Dedicated AI assistant documentation

### **How to Use**
```bash
# Start the documentation server
source venv/bin/activate && mkdocs serve --dev-addr=127.0.0.1:8001

# Access documentation
open http://127.0.0.1:8001

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### **Documentation Structure**
```
📚 Bifrost Trader Documentation
├── 🏠 Home: index.md
├── 🏁 Getting Started: installation, quick-start
├── 🏗️ Architecture: overview, database design
├── ⚙️ Services: web portal, service overviews
├── 💻 Development: migration, backtrader integration
├── 📖 Guides: AI collaboration framework
└── 📋 Reference: AI reference, configuration
```

---

## 🎯 **5. AI Quality Check Script (`scripts/ai-quality-check.py`)**

### **Purpose**
Validates AI-generated code against project standards and coding best practices.

### **Features**
- **Code Quality Validation**: Checks imports, functions, classes
- **Type Hint Verification**: Ensures proper type annotations
- **Docstring Validation**: Checks documentation completeness
- **Project Standards**: Enforces Bifrost Trader coding patterns

### **How to Use**
```bash
# Check a single file
python scripts/ai-quality-check.py path/to/file.py

# Check all Python files
python scripts/ai-quality-check.py $(find . -name "*.py" -not -path "./venv/*")

# Run as part of CI/CD
./scripts/ai-quality-check.py

# Check specific directory
python scripts/ai-quality-check.py services/web-portal/
```

### **Quality Checks**
- **Import Validation**: Ensures proper import statements
- **Function Analysis**: Checks function signatures and docstrings
- **Class Analysis**: Validates class structure and methods
- **Type Hints**: Verifies type annotations are present
- **Documentation**: Ensures docstrings are complete

---

## 🎯 **6. AI Collaboration Setup (`scripts/setup-ai-collaboration.sh`)**

### **Purpose**
Automated setup of the complete AI collaboration framework with all recommended tools.

### **Features**
- **Pre-commit Hooks**: Automated code quality checks
- **GitHub Actions**: CI/CD integration
- **Tool Installation**: Sets up recommended AI collaboration tools
- **Configuration**: Configures development environment

### **How to Use**
```bash
# Make script executable
chmod +x scripts/setup-ai-collaboration.sh

# Run the complete setup
./scripts/setup-ai-collaboration.sh

# This will set up:
# - Pre-commit hooks for code quality
# - GitHub Actions for CI/CD
# - Code quality tools (black, isort, flake8, mypy)
# - Development environment configuration
```

### **Setup Process**
1. **Install Dependencies**: Python packages and tools
2. **Configure Pre-commit**: Set up automated quality checks
3. **Setup GitHub Actions**: Configure CI/CD workflows
4. **Install Quality Tools**: black, isort, flake8, mypy
5. **Configure Environment**: Set up development environment

---

## 🎯 **7. GitHub Actions AI Workflow (`.github/workflows/ai-collaboration.yml`)**

### **Purpose**
Automated AI code quality checks integrated into CI/CD pipeline.

### **Triggers**
- **Pull Requests**: Runs on PR creation and updates
- **Main Branch**: Runs on pushes to main branch
- **Manual**: Can be triggered manually if needed

### **Features**
- **Automated Quality Checks**: Runs on every PR/push
- **Python Environment**: Sets up Python 3.9
- **Dependency Installation**: Installs quality tools
- **AI Quality Validation**: Runs the AI quality check script

### **How to Use**
```bash
# Automatically runs on:
# - Pull request creation/updates
# - Pushes to main branch

# Manual trigger (if needed)
gh workflow run ai-collaboration.yml

# View workflow runs
gh run list --workflow=ai-collaboration.yml
```

### **Workflow Steps**
1. **Checkout Code**: Get the latest code
2. **Setup Python**: Install Python 3.9
3. **Install Dependencies**: Install quality tools
4. **Run Quality Check**: Execute AI quality validation
5. **Report Results**: Provide feedback on code quality

---

## 🎯 **8. AI Documentation (`docs/guides/ai-collaboration.md`)**

### **Purpose**
Comprehensive guide for AI-human collaboration with best practices and implementation strategies.

### **Access**
- **MkDocs**: http://127.0.0.1:8001/guides/ai-collaboration/
- **File**: `docs/guides/ai-collaboration.md` (536 lines)

### **Key Features**
- **Collaboration Framework**: Complete AI-human workflow
- **Best Practices**: Proven patterns and techniques
- **Tool Recommendations**: Suggested tools and services
- **Implementation Guide**: Step-by-step setup instructions

### **How to Use**
```bash
# Access via MkDocs (recommended)
open http://127.0.0.1:8001/guides/ai-collaboration/

# Or read directly
cat docs/guides/ai-collaboration.md

# Search for specific topics
grep -i "quality gates" docs/guides/ai-collaboration.md
```

### **Content Sections**
- **Core Principles**: Knowledge-first development, quality gates
- **Recommended Tools**: Obsidian, Notion, GitHub Actions
- **Implementation Strategy**: Setup, configuration, best practices
- **Advanced Techniques**: Prompt engineering, knowledge graphs

---

## 🚀 **Complete Workflow: Using All AI Tools Together**

### **1. Initial Setup**
```bash
# Run the complete AI collaboration setup
./scripts/setup-ai-collaboration.sh

# Start documentation server
mkdocs serve --dev-addr=127.0.0.1:8001
```

### **2. Daily Development Workflow**
```bash
# 1. Use Cursor AI with .cursorrules for consistent behavior
# 2. Reference ai-prompts/ for structured prompts
# 3. Use code-templates/ for consistent code structure
# 4. Check quality with ai-quality-check.py
# 5. Access documentation via MkDocs
```

### **3. Creating New Services**
```bash
# 1. Use service creation prompt from ai-prompts/templates/
# 2. Copy microservice template from code-templates/
# 3. Customize for your specific service
# 4. Run quality check: python scripts/ai-quality-check.py
# 5. Commit changes (triggers GitHub Actions)
```

### **4. Quality Assurance**
```bash
# Pre-commit checks (automated)
git commit -m "your message"

# Manual quality check
python scripts/ai-quality-check.py your-file.py

# CI/CD checks (automated via GitHub Actions)
# Runs on every PR and push to main
```

---

## 🎯 **Benefits of This AI Tool Ecosystem**

### **✅ Consistency**
- **Standardized Patterns**: All tools follow the same patterns
- **Quality Gates**: Automated quality checks ensure standards
- **Documentation**: Comprehensive guides and references

### **✅ Efficiency**
- **Templates**: Reusable code and prompt templates
- **Automation**: Automated setup and quality checks
- **Integration**: Seamless integration between tools

### **✅ Quality**
- **Code Standards**: Enforced coding standards
- **Testing**: Comprehensive test templates
- **Documentation**: Always up-to-date documentation

### **✅ Collaboration**
- **AI-Human Workflow**: Structured collaboration patterns
- **Knowledge Sharing**: Centralized knowledge base
- **Best Practices**: Proven patterns and techniques

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **MkDocs Not Starting**
```bash
# Check if port is in use
lsof -i :8001

# Kill conflicting process
lsof -ti :8001 | xargs kill -9

# Restart MkDocs
mkdocs serve --dev-addr=127.0.0.1:8001
```

#### **Quality Check Failing**
```bash
# Check specific file
python scripts/ai-quality-check.py path/to/file.py

# Install missing dependencies
pip install black isort flake8 mypy

# Run with verbose output
python scripts/ai-quality-check.py --verbose
```

#### **GitHub Actions Not Running**
```bash
# Check workflow file
cat .github/workflows/ai-collaboration.yml

# Manual trigger
gh workflow run ai-collaboration.yml

# Check workflow status
gh run list --workflow=ai-collaboration.yml
```

---

## 📚 **Additional Resources**

### **Documentation Links**
- **AI Collaboration Guide**: http://127.0.0.1:8001/guides/ai-collaboration/
- **AI Reference**: http://127.0.0.1:8001/reference/ai-reference/
- **Architecture Overview**: http://127.0.0.1:8001/architecture/overview/
- **Development Guide**: http://127.0.0.1:8001/development/

### **File Locations**
- **Cursor Rules**: `.cursorrules`
- **AI Prompts**: `ai-prompts/`
- **Code Templates**: `code-templates/`
- **Quality Check**: `scripts/ai-quality-check.py`
- **Setup Script**: `scripts/setup-ai-collaboration.sh`
- **GitHub Actions**: `.github/workflows/ai-collaboration.yml`

### **Quick Commands**
```bash
# Start documentation
mkdocs serve --dev-addr=127.0.0.1:8001

# Run quality check
python scripts/ai-quality-check.py

# Setup AI collaboration
./scripts/setup-ai-collaboration.sh

# Build documentation
mkdocs build
```

---

**🎯 This comprehensive AI tool ecosystem provides a complete framework for AI-assisted development, ensuring consistency, quality, and efficiency in the Bifrost Trader project. Use this reference guide to maximize the benefits of AI collaboration in your development workflow.**
