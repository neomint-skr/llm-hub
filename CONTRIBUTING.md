# Contributing to LLM Hub

Thank you for your interest in contributing to LLM Hub! This document provides guidelines and information for contributors.

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Issues

Before creating an issue, please:
1. Check existing issues to avoid duplicates
2. Use the appropriate issue template
3. Provide clear, detailed information
4. Include steps to reproduce for bugs

### Suggesting Features

Feature requests are welcome! Please:
1. Use the feature request template
2. Explain the use case and benefits
3. Consider implementation complexity
4. Discuss with maintainers before large changes

### Contributing Code

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/llm-hub.git
   cd llm-hub
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   # Run validation
   ops/scripts/rule0-check.sh
   ops/scripts/mcp-compliance-test.sh
   ops/scripts/run-all-tests.sh
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request using the PR template.

## Development Setup

### Prerequisites
- Windows 10/11 with WSL2 or Linux
- Docker Desktop
- Python 3.11+
- Git

### Local Development
```bash
# Clone and setup
git clone https://github.com/your-org/llm-hub.git
cd llm-hub

# Copy environment template
cp ops/compose/.env.example ops/compose/.env

# Edit for development (set AUTH_ENABLED=false, LOG_LEVEL=DEBUG)
# Start services
start.bat

# Run tests
cd ops/scripts
bash run-all-tests.sh
```

## Coding Standards

### Python Code Style
- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 88 characters
- Use meaningful variable and function names
- Add docstrings for all public functions

### Example Code Structure
```python
"""Module description."""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ServiceManager:
    """Manages service operations."""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize service manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
    
    async def process_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming request.
        
        Args:
            data: Request data
            
        Returns:
            Processed response
            
        Raises:
            ValueError: If data is invalid
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        return {"status": "success", "data": data}
```

### Commit Message Format
Use conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

Examples:
```
feat: add streaming support to inference endpoint
fix: resolve authentication timeout issue
docs: update API documentation for new endpoints
test: add integration tests for gateway routing
```

### Architecture Guidelines

Follow the **dedardf** principles:
- **Decoupled** - Units operate independently
- **Declarative** - Configuration over code
- **Atomic** - Single responsibility per unit
- **Resilient** - Graceful failure handling
- **Discoverable** - Self-describing services
- **Federated** - Distributed architecture

### Adding New Units

1. **Create Unit Structure**
   ```bash
   mkdir units/my-new-unit
   cd units/my-new-unit
   touch unit.yml mcp-validation.yml Dockerfile start.sh
   mkdir api config logic
   ```

2. **Define Unit Contract**
   Create `unit.yml` with proper metadata and dependencies.

3. **Implement MCP Compliance**
   Ensure full MCP 2025-06-18 specification compliance.

4. **Add Tests**
   Include unit tests and integration tests.

5. **Update Documentation**
   Add to relevant documentation files.

## Testing Requirements

### Required Tests
- Unit tests for all new functions
- Integration tests for new endpoints
- MCP compliance validation
- Performance tests for critical paths

### Test Commands
```bash
# Unit tests
cd units/your-unit
python -m pytest tests/

# Integration tests
cd ops/scripts
bash run-all-tests.sh

# MCP compliance
bash mcp-compliance-test.sh

# Performance tests
python3 inference-test.py
```

### Test Coverage
- Aim for >80% code coverage
- Test both success and error paths
- Include edge cases and boundary conditions

## Documentation Requirements

### Required Documentation
- Update README.md if adding major features
- Add/update API documentation for new endpoints
- Create/update configuration documentation
- Add Architecture Decision Record (ADR) for significant changes

### Documentation Style
- Use clear, concise language
- Include code examples
- Provide step-by-step instructions
- Keep documentation up-to-date with code changes

## Pull Request Guidelines

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] MCP compliance maintained
- [ ] No breaking changes (or properly documented)
- [ ] Commit messages follow convention
- [ ] PR description is clear and complete

### PR Review Process
1. Automated checks must pass
2. At least one maintainer review required
3. All feedback addressed
4. Final approval from maintainer
5. Squash and merge (preferred)

### PR Size Guidelines
- Keep PRs focused and reasonably sized
- Large changes should be discussed first
- Consider breaking large features into smaller PRs

## Release Process

### Version Numbering
- Follow Semantic Versioning (semver.org)
- Major: Breaking changes
- Minor: New features, backward compatible
- Patch: Bug fixes, backward compatible

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers bumped
- [ ] Release notes prepared
- [ ] Security review completed

## Getting Help

### Communication Channels
- GitHub Issues for bugs and features
- GitHub Discussions for questions
- Pull Request comments for code review

### Maintainer Response Time
- Issues: Within 48 hours
- Pull Requests: Within 72 hours
- Security issues: Within 24 hours

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- README.md contributors section
- Release notes for major features

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing:
1. Check existing documentation
2. Search closed issues
3. Create a new issue with the "question" label
4. Be specific about what you're trying to achieve

Thank you for contributing to LLM Hub!
