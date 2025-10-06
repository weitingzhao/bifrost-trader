# 🤖 AI Prompts for Bifrost Trader

## 🎯 **Service Creation Prompts**

### **Create New Microservice**
```
Based on ARCHITECTURE_GUIDE.md, create a new [SERVICE_NAME] microservice that:

1. Follows the microservices patterns defined in REFACTORING_GUIDE.md
2. Uses FastAPI framework with proper structure
3. Implements database models from DATABASE_REFERENCE.md
4. Includes proper error handling and logging
5. Has comprehensive tests
6. Follows the service boundaries defined in the architecture

Service should handle: [SPECIFIC_FUNCTIONALITY]
Port: [PORT_NUMBER]
Database tables: [RELEVANT_TABLES]

Please create:
- Main FastAPI application
- Database models
- API endpoints
- Service logic
- Tests
- Documentation
```

### **Create API Endpoints**
```
Create API endpoints for [SERVICE_NAME] that:

1. Follow the patterns in ARCHITECTURE_GUIDE.md
2. Use database models from DATABASE_REFERENCE.md
3. Implement proper validation with Pydantic
4. Include error handling and logging
5. Follow RESTful conventions
6. Include comprehensive tests

Endpoints needed:
- [LIST_ENDPOINTS]

Reference the existing [SIMILAR_SERVICE] for patterns.
```

## 🗄️ **Database Operation Prompts**

### **Database Model Creation**
```
Create SQLAlchemy models for [TABLE_NAME] that:

1. Follow patterns in DATABASE_REFERENCE.md
2. Use proper TimescaleDB features if time-series data
3. Include appropriate indexes and constraints
4. Follow naming conventions
5. Include proper relationships
6. Have comprehensive tests

Table should handle: [SPECIFIC_FUNCTIONALITY]
Reference existing models in shared/models/ for patterns.
```

### **Database Query Operations**
```
Create database operations for [SERVICE_NAME] that:

1. Use models from DATABASE_REFERENCE.md
2. Follow connection patterns from shared/database/
3. Implement proper error handling
4. Use connection pooling
5. Include performance optimization
6. Have comprehensive tests

Operations needed:
- [LIST_OPERATIONS]

Follow the patterns in existing services.
```

## 🧪 **Testing Prompts**

### **Unit Tests**
```
Create comprehensive unit tests for [COMPONENT_NAME] that:

1. Test all public methods and functions
2. Include edge cases and error conditions
3. Use proper mocking for external dependencies
4. Follow testing patterns from existing tests
5. Include performance tests if applicable
6. Have good test coverage (>90%)

Component: [COMPONENT_DESCRIPTION]
Dependencies: [LIST_DEPENDENCIES]
```

### **Integration Tests**
```
Create integration tests for [SERVICE_NAME] that:

1. Test API endpoints with real database
2. Test service interactions
3. Include error scenarios
4. Use test database setup
5. Follow patterns from existing integration tests
6. Test performance and scalability

Service: [SERVICE_DESCRIPTION]
API endpoints: [LIST_ENDPOINTS]
Database operations: [LIST_OPERATIONS]
```

## 🔧 **Refactoring Prompts**

### **Code Refactoring**
```
Refactor [COMPONENT_NAME] to:

1. Follow patterns in ARCHITECTURE_GUIDE.md
2. Improve code organization and readability
3. Remove code duplication
4. Improve performance
5. Add proper error handling
6. Include comprehensive tests

Current issues:
- [LIST_ISSUES]

Reference REFACTORING_GUIDE.md for patterns.
```

### **Service Migration**
```
Migrate [COMPONENT_NAME] from Smart Trader to Bifrost Trader following:

1. Patterns in REFACTORING_GUIDE.md
2. Microservices architecture from ARCHITECTURE_GUIDE.md
3. Database patterns from DATABASE_REFERENCE.md
4. Maintain functionality while improving architecture
5. Add proper error handling and logging
6. Include comprehensive tests

Component: [COMPONENT_DESCRIPTION]
Current implementation: [CURRENT_LOCATION]
Target service: [TARGET_SERVICE]
```

## 📊 **Analysis Prompts**

### **Code Analysis**
```
Analyze [COMPONENT_NAME] and provide:

1. Code quality assessment
2. Performance analysis
3. Security review
4. Architecture compliance check
5. Suggestions for improvement
6. Refactoring recommendations

Component: [COMPONENT_DESCRIPTION]
Reference ARCHITECTURE_GUIDE.md for standards.
```

### **Architecture Review**
```
Review the architecture of [SERVICE_NAME] against:

1. ARCHITECTURE_GUIDE.md patterns
2. Microservices best practices
3. Database design from DATABASE_REFERENCE.md
4. Security requirements
5. Performance considerations
6. Scalability requirements

Provide recommendations for improvement.
```

## 🚀 **Deployment Prompts**

### **Docker Configuration**
```
Create Docker configuration for [SERVICE_NAME] that:

1. Follows patterns in ARCHITECTURE_GUIDE.md
2. Uses proper base images and security
3. Includes health checks and monitoring
4. Follows container best practices
5. Includes proper environment configuration
6. Has comprehensive documentation

Service: [SERVICE_DESCRIPTION]
Dependencies: [LIST_DEPENDENCIES]
Port: [PORT_NUMBER]
```

### **API Documentation**
```
Create comprehensive API documentation for [SERVICE_NAME] that:

1. Documents all endpoints clearly
2. Includes request/response examples
3. Documents error codes and handling
4. Includes authentication requirements
5. Follows OpenAPI standards
6. Is easy to understand and use

Service: [SERVICE_DESCRIPTION]
Endpoints: [LIST_ENDPOINTS]
```

## 🎯 **Best Practices**

### **Prompt Writing Guidelines**
1. **Be Specific**: Provide clear, detailed requirements
2. **Reference Context**: Always reference knowledge base files
3. **Provide Examples**: Show expected patterns and structures
4. **Include Constraints**: Specify limitations and requirements
5. **Ask for Clarification**: When requirements are ambiguous

### **Using Prompts Effectively**
1. **Start Simple**: Begin with basic prompts and refine
2. **Iterate**: Improve prompts based on results
3. **Context First**: Always provide project context
4. **Review Results**: Always review AI-generated code
5. **Update Knowledge**: Keep knowledge base current

---

**Remember**: These prompts are templates. Customize them for your specific needs and always reference the knowledge base for context.
