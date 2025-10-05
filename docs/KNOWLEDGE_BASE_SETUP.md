# 🧠 Knowledge Base Setup for Cursor AI

## 🎯 **Overview**
This guide explains how to set up the knowledge base so Cursor AI can access all high-level project knowledge files.

## 📁 **Knowledge Base Location**
The knowledge base is located at `~/Desktop/workspace/projects/documents/` and contains:

- **Architecture guides** and implementation plans
- **Database setup** and configuration
- **Microservices analysis** and diagrams
- **Project status** and migration plans
- **Portal design** and backtrader service plans

## 🚀 **Setup Instructions**

### **Method 1: Automatic Setup (Recommended)**
Run the setup script:
```bash
./scripts/setup-knowledge-base.sh
```

### **Method 2: Manual Setup**
```bash
# Create knowledge-base directory
mkdir -p docs/knowledge-base

# Create symbolic link
ln -sf /Users/vision-mac-trader/Desktop/workspace/projects/documents docs/knowledge-base
```

## ✅ **Verification**
After setup, verify it works:
```bash
ls -la docs/knowledge-base/
```

You should see all the knowledge files from the documents directory.

## 🎯 **Usage with Cursor AI**

### **1. Reference Specific Files**
When asking questions, reference specific knowledge files:
```
"Based on MICROSERVICES_IMPLEMENTATION_PLAN.md, what's the next service to implement?"

"According to DATABASE_SETUP.md, how should I configure PostgreSQL for the Portfolio Service?"

"Using BACKTRADER_SERVICE_PLAN.md as reference, help me implement the strategy service API."
```

### **2. Context-Aware Questions**
Ask questions that leverage the comprehensive knowledge:
```
"What's the recommended tech stack for the Portfolio Service according to the architecture analysis?"

"How does the current web-portal implementation align with the portal design plan?"

"What are the database requirements for the Execution Service based on the architecture?"
```

### **3. Cross-Reference Information**
Ask for information that spans multiple documents:
```
"How does the database setup relate to the microservices architecture?"

"What's the implementation priority based on the project status analysis?"
```

## 📋 **Available Knowledge Files**

### **🏗️ Architecture & Design**
- `ARCHITECTURE_GUIDE.md` - Overall system architecture
- `MICROSERVICES_ARCHITECTURE_ANALYSIS.md` - Complete microservices analysis
- `MICROSERVICES_ARCHITECTURE_DIAGRAM.md` - Visual architecture diagrams
- `MICROSERVICES_IMPLEMENTATION_PLAN.md` - Step-by-step implementation guide

### **🗄️ Database & Infrastructure**
- `DATABASE_SETUP.md` - PostgreSQL setup and configuration
- `DATABASE_IMPLEMENTATION_COMPLETE.md` - Database implementation summary

### **🧠 Strategy & Backtesting**
- `BACKTRADER_SERVICE_PLAN.md` - Backtrader service implementation plan

### **🌐 Web Portal**
- `PORTAL_DESIGN_PLAN.md` - Web portal design and implementation

### **🔄 Migration & Refactoring**
- `MIGRATION_PLAN.md` - Migration from Smart Trader to Bifrost Trader
- `REFACTORING_PLAN.md` - Code refactoring strategy

### **📊 Project Status**
- `PROJECT_STATUS_ANALYSIS.md` - Current project status and analysis
- `AI_REFERENCE.md` - AI assistant reference information

## 🎯 **Best Practices**

### **1. Be Specific**
Instead of: "Help me with the project"
Use: "Based on MICROSERVICES_IMPLEMENTATION_PLAN.md, help me implement the Portfolio Service"

### **2. Reference Context**
Instead of: "What should I do next?"
Use: "According to PROJECT_STATUS_ANALYSIS.md, what's the next critical task?"

### **3. Cross-Reference**
Instead of: "How do I set up the database?"
Use: "Using DATABASE_SETUP.md and MICROSERVICES_ARCHITECTURE_ANALYSIS.md, help me configure the database for the Portfolio Service"

## 🎉 **Benefits**

- **Complete Context**: Cursor AI has access to all project knowledge
- **Consistent Guidance**: Follows established architectural patterns
- **Comprehensive Support**: Database, services, APIs, and deployment guidance
- **Real-time Updates**: Changes to source files are immediately available

## 🔧 **Troubleshooting**

### **Issue: Symlink not working**
```bash
# Check if target directory exists
ls -la /Users/vision-mac-trader/Desktop/workspace/projects/documents/

# Recreate symlink
rm docs/knowledge-base
ln -sf /Users/vision-mac-trader/Desktop/workspace/projects/documents docs/knowledge-base
```

### **Issue: Files not showing in IDE**
- Restart Cursor IDE
- Check if symlinks are supported in your IDE settings
- Verify the symlink is working: `ls -la docs/knowledge-base/`

---

**📝 Note**: The knowledge base is a symbolic link to `~/Desktop/workspace/projects/documents/`. Any changes made to files in the source directory will be immediately reflected in the project.
