# Contributing to Azure DevOps Extended

Thank you for considering contributing to Azure DevOps Extended! This document provides guidelines and instructions for contributing to the project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

---

## Code of Conduct

This project follows the standard open-source code of conduct:

- **Be respectful** - Treat everyone with respect and kindness
- **Be collaborative** - Work together and help each other
- **Be professional** - Focus on constructive feedback
- **Be inclusive** - Welcome contributors of all backgrounds and skill levels

---

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report:
1. Check existing [issues](https://github.com/ragingtortoise/azure_devops_mcp_extended/issues) to avoid duplicates
2. Verify the bug with the latest version
3. Collect relevant information (Python version, OS, error messages)

When creating a bug report, include:
- **Clear title** - Descriptive summary of the issue
- **Steps to reproduce** - Exact steps to trigger the bug
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Environment details** - Python version, OS, Azure DevOps version
- **Error messages** - Full stack traces if applicable

### Suggesting Features

Before suggesting a feature:
1. Check the [roadmap](docs/ROADMAP.md) to see if it's already planned
2. Search existing feature requests
3. Consider if it aligns with the project's goals

When suggesting a feature:
- Use the `feature-request` label
- Describe the use case clearly
- Explain expected behavior
- Provide examples if possible

### Contributing Code

Areas where we welcome contributions:
- Bug fixes
- New MCP tools for Azure DevOps operations
- Documentation improvements
- Test coverage expansion
- Performance optimizations
- CLI enhancements
- Features from the [roadmap](docs/ROADMAP.md)

---

## Development Setup

### Prerequisites

- **Python 3.8+** (3.13+ recommended)
- **Git**
- **Azure DevOps account** with PAT token
- **pip** package manager

### Local Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/azure_devops_mcp_extended.git
   cd azure_devops_mcp_extended
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install in development mode**:
   ```bash
   pip install -e .
   ```

4. **Configure environment variables**:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your Azure DevOps credentials
   # AZDO_ORGANIZATION=your-org
   # AZDO_PROJECT=your-project
   # AZDO_PAT=your-personal-access-token
   ```

5. **Verify setup**:
   ```bash
   python validate_setup.py
   ```

### Running Tests

```bash
# Run integration tests (requires configured .env)
python integration_tests.py

# Test CLI commands
devops-extended --help
devops-extended get <work-item-id>

# Test MCP server
python -m devops_extended.mcp
```

---

## Pull Request Process

### Before Submitting

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes**:
   - Follow [coding standards](#coding-standards)
   - Add tests for new functionality
   - Update documentation as needed
   - Keep commits focused and atomic

3. **Test thoroughly**:
   - Run integration tests
   - Test with different process templates (Agile, Scrum, etc.)
   - Verify backward compatibility

4. **Update documentation**:
   - Update README.md if adding features
   - Update QUICKSTART.md if changing usage
   - Add docstrings to new functions/classes
   - Update examples if needed

### Submitting the PR

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create pull request** with:
   - Clear title describing the change
   - Reference to related issue (if applicable)
   - Description of changes made
   - Screenshots/examples (if UI changes)
   - Testing performed

3. **PR checklist**:
   - [ ] Code follows project style guidelines
   - [ ] Tests added/updated and passing
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented if necessary)
   - [ ] Commit messages are clear and descriptive

### Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, maintainers will merge

---

## Coding Standards

### Python Style

Follow **PEP 8** with these specifics:

- **Indentation**: 4 spaces (no tabs)
- **Line length**: 100 characters max (120 for comments)
- **Naming conventions**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### Code Quality Principles

- **DRY** (Don't Repeat Yourself) - Extract common logic
- **SOLID** principles - Single responsibility, clean abstractions
- **Semantic naming** - Self-documenting variable/function names
- **Guard clauses** - Early returns for validation
- **Error handling** - Explicit error handling with context

### Example Code Pattern

```python
def create_work_item(title: str, work_item_type: str, description: str = None) -> dict:
    """
    Create a work item in Azure DevOps.
    
    Args:
        title: Work item title (required)
        work_item_type: Type (Bug, Task, etc.)
        description: Optional description
        
    Returns:
        dict: Created work item details with ID
        
    Raises:
        ValueError: If title is empty or work_item_type is invalid
        AzureDevOpsError: If API call fails
    """
    # Guard clauses
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")
    
    if not work_item_type:
        raise ValueError("Work item type is required")
    
    # Main logic
    payload = [
        {"op": "add", "path": "/fields/System.Title", "value": title}
    ]
    
    if description:
        payload.append({
            "op": "add",
            "path": "/fields/System.Description",
            "value": description
        })
    
    return self._client.create_work_item(work_item_type, payload)
```

---

## Testing Guidelines

### Test Coverage

- Aim for **80%+ code coverage**
- All new features must include tests
- Bug fixes should include regression tests

### Test Types

1. **Unit tests** - Test individual functions in isolation
2. **Integration tests** - Test Azure DevOps API interactions
3. **MCP tests** - Test MCP server tools end-to-end

### Writing Tests

```python
def test_create_pbi_success():
    """Test successful PBI creation with required fields."""
    # Arrange
    title = "Test PBI"
    description = "Test description"
    
    # Act
    result = create_pbi(title, description=description)
    
    # Assert
    assert result["id"] is not None
    assert result["fields"]["System.Title"] == title
    assert result["fields"]["System.WorkItemType"] == "Product Backlog Item"
```

### Running Tests

```bash
# Run all tests
python integration_tests.py

# Validate environment setup
python validate_setup.py

# Test specific functionality manually
devops-extended create-pbi "Test" --description "Test"
```

---

## Documentation

### What to Document

- **New features** - Update README.md and QUICKSTART.md
- **MCP tools** - Add to tool list in documentation
- **Breaking changes** - Clearly document in PR and CHANGELOG
- **Configuration** - Update .env.example if new vars added
- **Examples** - Add to examples/ directory if helpful

### Documentation Style

- Use **Markdown** for all documentation
- Include **code examples** with syntax highlighting
- Add **screenshots** for UI changes (if applicable)
- Keep explanations **concise but complete**
- Use **tables** for structured data
- Include **links** to related documentation

### Files to Update

- `README.md` - Main project documentation
- `QUICKSTART.md` - Getting started guide
- `.github/copilot-instructions.md` - AI assistant context
- `docs/ROADMAP.md` - Feature planning (if adding planned features)
- Code docstrings - Inline documentation

---

## Questions?

If you have questions about contributing:

1. Check existing [documentation](README.md)
2. Search [GitHub issues](https://github.com/ragingtortoise/azure_devops_mcp_extended/issues)
3. Open a new issue with the `question` label
4. Reach out to maintainers

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see [LICENSE](LICENSE)).
