# Contributing to Learn Python

Thank you for your interest in contributing to `learn-python`! This project serves as an authoritative enterprise architecture curriculum and interactive CPython platform.

## Development Setup

1. **Prerequisites**:
   - Python 3.11+ (Python 3.12 or 3.13 recommended)
   - Git 2.40+
   - Optional: Docker

2. **Clone & Environment Setup**:
   ```bash
   git clone https://github.com/manthanank/learn-python.git
   cd learn-python
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
   pip install -e ".[dev]"
   ```

3. **Running the Test Suite**:
   ```bash
   pytest
   ```

4. **Running the Web Engine & API Sandbox**:
   ```bash
   uvicorn src.api.app:app --reload --port 8000
   ```

## Commit Guidelines

We enforce the [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat:` New features or engine capabilities
- `fix:` Bug fixes or interpreter compat corrections
- `docs:` Documentation improvements or curriculum updates
- `test:` Additional test cases or test refactoring
- `refactor:` Code improvements that do not change behavior
- `perf:` Performance optimizations

## Pull Request Process

1. Fork the repository and create a descriptive branch name (`feat/gil-benchmarks`).
2. Add comprehensive unit tests in `tests/`.
3. Verify that all tests pass (`pytest`).
4. Ensure code adheres to PEP 8 standards (`ruff check .`).
5. Open a Pull Request referencing any relevant issues.
