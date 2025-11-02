# Contributing to Azure DevOps Extended

Thank you for considering contributing! We welcome bug fixes, new features, documentation improvements, and test coverage expansion.

## Code of Conduct

- Be respectful and professional
- Focus on constructive feedback
- Welcome contributors of all backgrounds

## How to Contribute

### Reporting Bugs

Check existing [issues](https://github.com/ragingtortoise/azure_devops_mcp_extended/issues) first, then include:
- Clear title and steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, error messages)

### Suggesting Features

Check the [roadmap](docs/ROADMAP.md) first, then create an issue with:
- Use case description
- Expected behavior
- Examples

## Development Setup

**Prerequisites:** Python 3.8+, Git, Azure DevOps account with PAT token

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/azure_devops_mcp_extended.git
cd azure_devops_mcp_extended
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e .

# Configure credentials
cp .env.example .env
# Edit .env with your AZDO_ORGANIZATION, AZDO_PROJECT, AZDO_PAT

# Verify
python validate_setup.py
python integration_tests.py
```

## Pull Request Guidelines

1. Follow PEP 8 coding standards
2. Add tests for new functionality
3. Update documentation (README, docstrings)
4. Test with different process templates (Agile, Scrum)
5. Keep commits focused and descriptive

**PR Checklist:**
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Coding Standards

Follow PEP 8:
- 4 spaces indentation
- 100 character line length
- `snake_case` for functions/variables, `PascalCase` for classes
- Type hints for function parameters and returns
- Docstrings for all public functions/classes

**Example:**
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
    """
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")
    
    # Implementation...
```

## Testing

- Aim for 80%+ code coverage
- All new features must include tests
- Run `python integration_tests.py` before submitting

## Documentation

Update these files when adding features:
- `README.md` - Main documentation
- `QUICKSTART.md` - Getting started guide
- `.github/copilot-instructions.md` - AI assistant context
- Code docstrings - Inline documentation

## Questions?

Check the [documentation](README.md) or open an issue with the `question` label.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see [LICENSE](LICENSE)).
