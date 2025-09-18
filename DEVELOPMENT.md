# Development Guide for cohens-d-effect-size Package

## Package Successfully Published to PyPI! 🎉

**Package URL**: https://pypi.org/project/cohens-d-effect-size/  
**Installation**: `pip install cohens-d-effect-size`

## Development Setup

1. Clone the repository
2. Create virtual environment
3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests
```bash
cd cohens_d_package
pytest tests/
```

## Building Package
```bash
cd cohens_d_package
python -m build
```

## Publishing Updates
```bash
# Update version in cohens_d/__version__.py
# Run tests
# Build package
python -m twine upload dist/*
```

## Package Structure (Clean)
The package contains only essential files:
- `cohens_d/` - Main module
- `LICENSE` - License file
- `README.md` - Documentation
- Package metadata

Development files are kept in the repository but excluded from the package distribution.