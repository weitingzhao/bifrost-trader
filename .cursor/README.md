# 🤖 Bifrost Trader - Cursor AI Configuration

## 📁 **Folder Structure**

```
.cursor/
├── README.md                    # This file - overview and usage
├── project.json                 # Project metadata and service status
├── ai-config.json              # AI assistant configuration
├── workspace.json              # Workspace settings and file watching
├── settings.json               # Cursor-specific settings
├── prompts/                    # AI prompt templates
│   ├── README.md              # Prompt framework guide
│   └── templates/             # Structured prompt templates
│       ├── service-creation.md
│       └── api-endpoints.md
├── templates/                  # Code templates
│   ├── README.md              # Code template guide
│   ├── microservice/          # Complete FastAPI service structure
│   ├── api-endpoints/         # RESTful endpoint patterns
│   └── database-models/       # SQLAlchemy model patterns
└── scripts/                   # AI collaboration scripts
    ├── ai-quality-check.py    # Code quality validation
    └── setup-ai-collaboration.sh # Automated setup script
```

## 🎯 **Purpose**

This folder contains all AI-related configuration, templates, and tools for the Bifrost Trader project. It provides a centralized location for Cursor AI to understand the project structure, access templates, and maintain quality standards.

## 🛠️ **Components**

### **Configuration Files**
- **`project.json`**: Project metadata, services, AI tools integration
- **`ai-config.json`**: AI assistant role, workflow, and quality gates
- **`workspace.json`**: Workspace settings, file watching, development environment
- **`settings.json`**: Cursor-specific configuration and preferences

### **AI Prompts (`prompts/`)**
- **Structured Templates**: Consistent prompt patterns for AI interactions
- **Service Creation**: Templates for creating new microservices
- **API Development**: Templates for API endpoint development
- **Database Operations**: Templates for database tasks

### **Code Templates (`templates/`)**
- **Microservice Structure**: Complete FastAPI service templates
- **API Endpoints**: RESTful endpoint patterns
- **Database Models**: SQLAlchemy model templates
- **Test Structures**: Comprehensive test templates

### **Scripts (`scripts/`)**
- **Quality Check**: Validates AI-generated code against project standards
- **Setup Script**: Automated setup of AI collaboration framework

## 🚀 **How to Use**

### **For Cursor AI**
The `.cursorrules` file (in project root) references this folder and its contents. Cursor AI automatically uses:
- Configuration files for project context
- Prompt templates for consistent interactions
- Code templates for development patterns
- Quality scripts for code validation

### **For Developers**
```bash
# Use prompt templates
cat .cursor/prompts/templates/service-creation.md

# Copy code templates
cp -r .cursor/templates/microservice/ services/new-service/

# Run quality checks
python .cursor/scripts/ai-quality-check.py

# Setup AI collaboration
./.cursor/scripts/setup-ai-collaboration.sh
```

### **For Documentation**
- **MkDocs**: http://127.0.0.1:8001
- **AI Tools Reference**: http://127.0.0.1:8001/guides/ai-tools-reference/
- **AI Collaboration**: http://127.0.0.1:8001/guides/ai-collaboration/

## 🔧 **Development Workflow**

### **1. Creating New Services**
```bash
# Use service creation prompt
# Reference: .cursor/prompts/templates/service-creation.md

# Copy microservice template
cp -r .cursor/templates/microservice/ services/new-service/

# Customize for your specific service
# Run quality check
python .cursor/scripts/ai-quality-check.py services/new-service/
```

### **2. Daily Development**
```bash
# Cursor AI uses .cursorrules and this folder automatically
# Reference prompts from .cursor/prompts/
# Apply templates from .cursor/templates/
# Validate quality with .cursor/scripts/ai-quality-check.py
```

### **3. Quality Assurance**
```bash
# Pre-commit checks (automated)
git commit -m "your message"

# Manual quality check
python .cursor/scripts/ai-quality-check.py your-file.py

# CI/CD checks (automated via GitHub Actions)
```

## 📚 **Related Files**

### **Project Root**
- **`.cursorrules`**: Cursor AI behavior configuration (kept in root for Cursor to find)
- **`mkdocs.yml`**: Documentation configuration
- **`.pre-commit-config.yaml`**: Pre-commit hooks configuration
- **`.github/workflows/ai-collaboration.yml`**: CI/CD workflow

### **Documentation**
- **`docs/guides/ai-tools-reference.md`**: Complete AI tools reference
- **`docs/guides/ai-collaboration.md`**: AI collaboration framework
- **`docs/architecture/overview.md`**: System architecture
- **`docs/development/migration-guide.md`**: Migration guide

## 🎯 **Benefits**

### **✅ Centralized Organization**
- **Single Location**: All AI-related files in one place
- **Easy Maintenance**: Update templates and configs in one location
- **Clear Structure**: Logical organization of AI tools and resources

### **✅ Enhanced Cursor AI**
- **Complete Context**: Cursor AI has access to all project information
- **Consistent Patterns**: Standardized templates and prompts
- **Quality Standards**: Automated quality checks and validation

### **✅ Team Collaboration**
- **Shared Resources**: Common templates and configurations
- **Consistent Development**: Standardized patterns across the team
- **Easy Onboarding**: New developers can understand the AI setup quickly

## 🔍 **Quick Reference**

### **Essential Commands**
```bash
# Start documentation
mkdocs serve --dev-addr=127.0.0.1:8001

# Run quality check
python .cursor/scripts/ai-quality-check.py

# Setup AI collaboration
./.cursor/scripts/setup-ai-collaboration.sh

# Access documentation
open http://127.0.0.1:8001/guides/ai-tools-reference/
```

### **Key URLs**
- **Documentation**: http://127.0.0.1:8001
- **AI Tools Reference**: http://127.0.0.1:8001/guides/ai-tools-reference/
- **AI Collaboration**: http://127.0.0.1:8001/guides/ai-collaboration/
- **Architecture**: http://127.0.0.1:8001/architecture/overview/

---

**🎯 This consolidated `.cursor` folder provides a complete AI collaboration framework for the Bifrost Trader project, ensuring consistent development patterns, quality standards, and enhanced AI-assisted development.**