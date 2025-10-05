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
