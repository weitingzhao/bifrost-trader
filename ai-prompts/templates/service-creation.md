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
