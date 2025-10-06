# Bifrost Trader - Cursor AI Configuration

## Project Overview
Microservices-based stock trading platform with comprehensive AI-assisted development framework.

## AI Tools Integration
- **Cursor AI Rules**: `.cursorrules` - Project-specific AI behavior
- **AI Prompts**: `ai-prompts/` - Structured prompt templates
- **Code Templates**: `code-templates/` - Reusable code patterns
- **MkDocs**: Documentation system with AI reference
- **Quality Checks**: Automated code quality validation
- **GitHub Actions**: CI/CD with AI collaboration

## Development Workflow
1. Use Cursor AI with project context from `.cursorrules`
2. Reference structured prompts from `ai-prompts/`
3. Apply code templates from `code-templates/`
4. Validate quality with `scripts/ai-quality-check.py`
5. Access documentation via MkDocs at http://127.0.0.1:8001

## Key Files
- `.cursorrules` - AI behavior configuration
- `ai-prompts/README.md` - Prompt framework guide
- `code-templates/README.md` - Code template guide
- `docs/guides/ai-tools-reference.md` - Complete AI tools reference
- `scripts/setup-ai-collaboration.sh` - Automated setup script

## Documentation
- **MkDocs**: http://127.0.0.1:8001
- **AI Tools Reference**: http://127.0.0.1:8001/guides/ai-tools-reference/
- **AI Collaboration**: http://127.0.0.1:8001/guides/ai-collaboration/
- **Architecture**: http://127.0.0.1:8001/architecture/overview/

## Quick Commands
```bash
# Start documentation
mkdocs serve --dev-addr=127.0.0.1:8001

# Run quality check
python scripts/ai-quality-check.py

# Setup AI collaboration
./scripts/setup-ai-collaboration.sh
```
